"""Step 3: deduplicate all reference entries across the 133 papers into unique
cited works, count how many of our papers cite each, classify each by topic,
and flag whether it already belongs to our 133-paper set.

Outputs:
  data/clusters.json  - list of unique cited works with counts/metadata
"""
import re
import numpy as np
from rapidfuzz import process, fuzz
import common as C

CUTOFF = 88  # token_set_ratio threshold for "same work"


def clu_norm(entry):
    """Normalised text used for fuzzy clustering (title + authors dominate)."""
    e = C.fix_ligatures(entry).lower()
    e = re.sub(r"^\s*\[\d+\]\s*", "", e)
    e = re.sub(r"arxiv[:\s].*$", " ", e)
    e = re.sub(r"https?://\S+", " ", e)
    e = re.sub(r"doi[:\s]\S+", " ", e)
    e = re.sub(r"[^a-z0-9 ]+", " ", e)
    toks = [t for t in e.split() if not t.isdigit() and len(t) > 1]
    return " ".join(toks)


def sig(s):
    return re.sub(r"[^a-z0-9]", "", C.fix_ligatures(s).lower())


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


_AUTHORY_START = re.compile(
    r"^(?:[A-Z]\.[,)]?\s|[A-Z][a-zà-ÿ]+,\s+[A-Z]\.|[A-Z]\.,|et al)")


def title_score(t):
    """Higher = looks more like a real paper title (not an author list)."""
    if not t:
        return -1e9
    toks = t.split()
    if not toks:
        return -1e9
    lower = sum(1 for w in toks if w[:1].islower())
    score = lower * 3                     # titles have many lowercase words
    if _AUTHORY_START.match(t):           # starts like an author list
        score -= 12
    if 25 <= len(t) <= 160:
        score += 4
    if len(t) < 12:
        score -= 8
    # commas early suggest an author list
    score -= t[:40].count(",") * 2
    return score


classify = C.classify


def main():
    papers = {int(k): v for k, v in C.load_json("papers.json").items()}
    refs = {int(k): v for k, v in C.load_json("references.json").items()}

    # flatten
    items = []  # (src_pid, ref_dict, norm)
    for pid, rs in refs.items():
        for r in rs:
            n = clu_norm(r["raw"])
            if len(n) < 12:
                continue
            items.append((pid, r, n))
    norms = [n for _, _, n in items]
    N = len(items)
    print(f"clustering {N} reference entries ...")

    uf = UF(N)
    # 1) hard-merge by arxiv id
    by_arxiv = {}
    for i, (_, r, _) in enumerate(items):
        if r.get("arxiv"):
            by_arxiv.setdefault(r["arxiv"], []).append(i)
    for ids in by_arxiv.values():
        for j in ids[1:]:
            uf.union(ids[0], j)

    # 2) fuzzy merge via blockwise cdist (token_set_ratio, score_cutoff)
    #    block by year to keep matrices small; compare each year with itself
    #    and the two neighbouring years (handles arXiv vs published year drift).
    year_of = []
    for _, r, _ in items:
        year_of.append(r.get("year") or 0)
    from collections import defaultdict
    blocks = defaultdict(list)
    for i, y in enumerate(year_of):
        blocks[y].append(i)

    years = sorted(blocks)
    for y in years:
        group = list(blocks[y]) + list(blocks.get(y + 1, []))  # y vs y and y+1
        if len(group) < 2:
            continue
        sub = [norms[i] for i in group]
        sim = process.cdist(sub, sub, scorer=fuzz.token_set_ratio,
                            score_cutoff=CUTOFF, dtype=np.uint8, workers=-1)
        rows, cols = np.where(sim >= CUTOFF)
        for a, b in zip(rows, cols):
            if a < b:
                uf.union(group[a], group[b])

    # gather clusters
    clusters = {}
    for i, (pid, r, n) in enumerate(items):
        root = uf.find(i)
        clusters.setdefault(root, []).append(i)

    # build our-set title signatures for in-set detection
    set_sigs = {pid: sig(papers[pid]["canonical_title"]) for pid in papers}
    set_sig_list = [(pid, s) for pid, s in set_sigs.items() if len(s) >= 20]

    out = []
    for root, idxs in clusters.items():
        members = [items[i] for i in idxs]
        srcs = sorted({m[0] for m in members})
        # representative title = member whose title_guess looks most title-like
        rep = max(members, key=lambda m: title_score(m[1]["title_guess"]))
        rep_title = rep[1]["title_guess"]
        # longest raw entry = most complete record for in-set matching / display
        rep_raw = max(members, key=lambda m: len(m[1]["raw"]))[1]["raw"]
        years = [m[1]["year"] for m in members if m[1]["year"]]
        arxiv = next((m[1]["arxiv"] for m in members if m[1].get("arxiv")), None)
        # in-set? match any member's signature against our canonical titles
        in_set = None
        member_sig = " ".join(sig(m[1]["raw"]) for m in members)
        for pid, s in set_sig_list:
            if s in member_sig:
                in_set = pid
                break
        if in_set is not None:
            rep_title = papers[in_set]["canonical_title"]
        out.append({
            "count": len(srcs),
            "citing_papers": srcs,
            "title": rep_title,
            "rep_raw": rep_raw[:300],
            "year": max(set(years), key=years.count) if years else None,
            "arxiv": arxiv,
            "category": classify(rep_title if len(rep_title or "") >= 12
                                 else rep_raw),
            "in_set_id": in_set,
            "n_variants": len(members),
        })

    # Consolidate clusters that resolve to the SAME in-set paper. Such splits
    # come from year-block boundaries / mis-parsed years; an in-set work is a
    # known single paper, so we union the citing papers.
    merged = {}
    final = []
    for c in out:
        pid = c["in_set_id"]
        if pid is None:
            final.append(c)
            continue
        if pid not in merged:
            merged[pid] = c
            c["citing_papers"] = set(c["citing_papers"])
            final.append(c)
        else:
            m = merged[pid]
            m["citing_papers"] |= set(c["citing_papers"])
            m["n_variants"] += c["n_variants"]
            if not m["arxiv"] and c["arxiv"]:
                m["arxiv"] = c["arxiv"]
    for c in final:
        c["citing_papers"] = sorted(c["citing_papers"])
        c["count"] = len(c["citing_papers"])
    final.sort(key=lambda d: d["count"], reverse=True)
    out = final
    C.dump_json(out, "clusters.json")

    from collections import Counter
    print(f"unique cited works: {len(out)}")
    print("category distribution:",
          dict(Counter(c["category"] for c in out)))
    multi = [c for c in out if c["count"] >= 2]
    print(f"works cited by >=2 of our papers: {len(multi)}")
    print(f"works cited by >=5: {len([c for c in out if c['count']>=5])}")
    print("\nTOP 25 most-cited works overall:")
    for c in out[:25]:
        tag = f"[in-set #{c['in_set_id']}]" if c["in_set_id"] else ""
        print(f"  {c['count']:3d} | {c['category']:11s} | "
              f"{(c['title'] or c['rep_raw'])[:62]} {tag}")


if __name__ == "__main__":
    main()
