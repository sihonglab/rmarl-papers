"""Step 2: build the internal citation graph among the 133 papers.

For every ordered pair (A, B) we decide whether paper A cites paper B by
searching B's canonical title inside A's reference list. Matching is done on a
separator-free signature (so 'multi- agent', 'multi-agent' and 'multiagent' all
match), with a fuzzy fall-back for slight title variants.

Outputs:
  data/internal_edges.json   - list of {src, dst, how}
  data/internal_stats.json   - per-paper in/out degree + ranking
"""
import re
from rapidfuzz import fuzz
import common as C


def sig(s):
    """Separator-free lowercase signature."""
    return re.sub(r"[^a-z0-9]", "", C.fix_ligatures(s).lower())


def main():
    papers = C.load_json("papers.json")
    refs = C.load_json("references.json")
    papers = {int(k): v for k, v in papers.items()}
    refs = {int(k): v for k, v in refs.items()}
    ids = sorted(papers)

    # signatures
    title_sig = {pid: sig(papers[pid]["canonical_title"]) for pid in ids}
    # per-paper concatenated reference signature + list of per-entry sigs
    ref_blob = {}
    ref_entry_sigs = {}
    for pid in ids:
        entries = refs.get(pid, [])
        ref_entry_sigs[pid] = [sig(e["raw"]) for e in entries]
        ref_blob[pid] = " ".join(C.fix_ligatures(e["raw"]).lower()
                                 for e in entries)
    ref_blob_sig = {pid: sig(ref_blob[pid]) for pid in ids}

    edges = []
    for a in ids:
        if not refs.get(a):
            continue
        for b in ids:
            if a == b:
                continue
            tsig = title_sig[b]
            if len(tsig) < 20:
                continue  # too short to match safely
            how = None
            if tsig in ref_blob_sig[a]:
                how = "exact"
            else:
                # fuzzy: best partial match against individual ref entries
                best = 0
                for es in ref_entry_sigs[a]:
                    if abs(len(es) - len(tsig)) > 0.6 * len(tsig) + 40:
                        # cheap length gate before fuzzy
                        pass
                    r = fuzz.partial_ratio(tsig, es)
                    if r > best:
                        best = r
                    if best >= 94:
                        break
                if best >= 94:
                    how = "fuzzy"
            if how:
                edges.append({"src": a, "dst": b, "how": how})

    # degrees
    outdeg = {pid: 0 for pid in ids}
    indeg = {pid: 0 for pid in ids}
    cited_by = {pid: [] for pid in ids}
    cites = {pid: [] for pid in ids}
    for e in edges:
        outdeg[e["src"]] += 1
        indeg[e["dst"]] += 1
        cited_by[e["dst"]].append(e["src"])
        cites[e["src"]].append(e["dst"])

    stats = {
        "n_papers": len(ids),
        "n_edges": len(edges),
        "n_exact": sum(1 for e in edges if e["how"] == "exact"),
        "n_fuzzy": sum(1 for e in edges if e["how"] == "fuzzy"),
        "per_paper": {
            str(pid): {
                "title": papers[pid]["canonical_title"],
                "in": indeg[pid],
                "out": outdeg[pid],
                "cited_by": sorted(cited_by[pid]),
                "cites": sorted(cites[pid]),
            } for pid in ids
        },
    }

    C.dump_json(edges, "internal_edges.json")
    C.dump_json(stats, "internal_stats.json")

    print(f"internal edges: {len(edges)} "
          f"(exact={stats['n_exact']}, fuzzy={stats['n_fuzzy']})")
    n_iso = sum(1 for pid in ids if indeg[pid] == 0 and outdeg[pid] == 0)
    print(f"papers with no internal links at all: {n_iso}")
    top_cited = sorted(ids, key=lambda p: indeg[p], reverse=True)[:15]
    print("\nTop internally-cited papers (most cited BY the other 132):")
    for p in top_cited:
        print(f"  [{indeg[p]:2d} cites] #{p}: {papers[p]['canonical_title'][:70]}")
    top_citing = sorted(ids, key=lambda p: outdeg[p], reverse=True)[:8]
    print("\nPapers citing the most others in the set:")
    for p in top_citing:
        print(f"  [{outdeg[p]:2d} out] #{p}: {papers[p]['canonical_title'][:60]}")


if __name__ == "__main__":
    main()
