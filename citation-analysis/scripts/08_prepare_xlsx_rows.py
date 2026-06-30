"""Step 8a: prepare clean spreadsheet rows for the genuinely-absent robust-MARL
gaps. Dedupes the candidates among themselves, cleans titles, re-derives
metadata (venue / year / authors / arXiv) from the reference entry that
actually contains the title, classifies into the spreadsheet's category
taxonomy, and writes data/xlsx_new_rows.json for review + insertion (step 09).
"""
import os
import re
import csv
from rapidfuzz import fuzz
import common as C

# spreadsheet category taxonomy (exact strings used in robust-marl-papers.xlsx)
CATS = {
    "fault": "Teammates/Byzantine/Fault Tolerance",
    "comm": "Communication Robustness",
    "attack": "Adversarial Attacks & Training",
    "state": "State/Observation Perturbation",
    "bench": "Benchmarks & Evaluation",
    "theory": "Model/Environment Uncertainty (DRMG/Theory)",
    "app": "Applications & Safe-Robust",
    "offline": "Offline / Distribution Shift",
}

VENUES = [
    (r"advances in neural information processing|neurips|\bnips\b", "NeurIPS"),
    (r"international conference on machine learning|\bicml\b", "ICML"),
    (r"international conference on learning representations|\biclr\b", "ICLR"),
    (r"aaai conference|advancement of artificial intelligence|\baaai\b", "AAAI"),
    (r"\bijcai\b|international joint conference on artificial", "IJCAI"),
    (r"\bcvpr\b|computer vision and pattern recognition", "CVPR"),
    (r"international conference on computer vision|\biccv\b", "ICCV"),
    (r"international conference on robotics and automation|\bicra\b", "ICRA"),
    (r"intelligent robots and systems|\biros\b", "IROS"),
    (r"conference on decision and control|\bcdc\b", "CDC"),
    (r"american control conference|\bacc\b", "ACC"),
    (r"artificial intelligence and statistics|aistats", "AISTATS"),
    (r"conference on robot learning|\bcorl\b", "CoRL"),
    (r"autonomous agents and multiagent|\baamas\b", "AAMAS"),
    (r"learning theory|\bcolt\b", "COLT"),
    (r"journal of machine learning research|\bjmlr\b", "JMLR"),
    (r"acm computing surveys|comput\.? surv", "ACM Computing Surveys"),
    (r"transactions on neural networks", "IEEE TNNLS"),
    (r"transactions on dependable", "IEEE TDSC"),
    (r"transactions on automatic control", "IEEE TAC"),
    (r"transactions on cybernetics", "IEEE Trans. Cybernetics"),
    (r"transactions on control of network", "IEEE TCNS"),
    (r"internet of things", "IEEE IoT-J"),
    (r"transactions on intelligent transportation", "IEEE T-ITS"),
    (r"science china", "Science China"),
    (r"annual review", "Annual Reviews in Control"),
    (r"transportation research", "Transportation Research"),
    (r"frontiers of computer science", "Frontiers of Computer Science"),
    (r"applied energy", "Applied Energy"),
    (r"ieee transactions", "IEEE Transactions"),
    (r"\barxiv\b", "arXiv"),
]


def dehy(s):
    """Fix ligatures and join line-break hyphenation ('multi- agent')."""
    return re.sub(r"(\w)-\s+(\w)", r"\1\2", C.fix_ligatures(s))


def sig(s):
    return re.sub(r"[^a-z0-9]", "", dehy(s).lower())


def detect_venue(raw):
    low = dehy(raw).lower()
    for pat, name in VENUES:
        if re.search(pat, low):
            return name
    m = re.search(r"\bIn ([A-Z][^.,]{6,45})", dehy(raw))
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def classify_cat(title):
    t = re.sub(r"-\s*", "", title.lower())
    if re.search(r"byzantine|resilien|fault[ ]?toleran|consensus|"
                 r"distributed optimization|redundancy|fault tolerant", t):
        return CATS["fault"]
    if re.search(r"communicat", t):
        return CATS["comm"]
    if re.search(r"offline", t):
        return CATS["offline"]
    if re.search(r"benchmark|evaluat|testing|\bgnas\b", t):
        return CATS["bench"]
    if re.search(r"attack|poison|backdoor|adversarial minority|defence|"
                 r"defense|security", t):
        return CATS["attack"]
    if re.search(r"state perturb|observation|partially observable|"
                 r"state uncertainty", t):
        return CATS["state"]
    if re.search(r"markov game|model uncertainty|distributionally|"
                 r"regulariz|function approximation|policy gradient|"
                 r"nash equilibr|fundamental limits|opponents", t):
        return CATS["theory"]
    if re.search(r"vehicle|lane|robot|uav|wireless|iot|cyber.?physical|"
                 r"traffic|microgrid|energy|portfolio|logistics|patrol|water|"
                 r"tracking control|leader.following|control of|federated", t):
        return CATS["app"]
    return CATS["attack"]


def clean_title(t):
    t = dehy(t)
    for a, b in [("Multiagent", "Multi-Agent"), ("multiagent", "multi-agent"),
                 ("Multirobot", "Multi-Robot"), ("multirobot", "multi-robot"),
                 ("modelbased", "model-based"), ("modelfree", "model-free"),
                 ("zerosum", "zero-sum"), ("meanfield", "mean-field"),
                 ("actorcritic", "actor-critic"), ("rewardfree", "reward-free"),
                 ("faulttolerant", "fault-tolerant"), ("realtime", "real-time"),
                 ("Byzantineresilient", "Byzantine-resilient"),
                 ("byzantineresilient", "Byzantine-resilient")]:
        t = t.replace(a, b)
    t = re.sub(r"\bmarl\b", "MARL", t, flags=re.I)
    t = re.sub(r"\bsok\b", "SoK", t, flags=re.I)
    t = re.sub(r"\biot\b", "IoT", t, flags=re.I)
    t = re.sub(r"\buav\b", "UAV", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" .,:;\"'")
    return t[:1].upper() + t[1:] if t else t


GARBLED = re.compile(r"^\s*(?:[A-Z]\.,|[A-Z][a-zA-Z]+,\s+[A-Z]\.|and\s+[A-Z]|"
                     r"[A-Z]\.\s|[a-z])")
# leading run of author tokens to strip from a garbled title
AUTHOR_PREFIX = re.compile(r"^(?:[A-Z]\.,?\s+|[A-Z][a-zà-ÿ'’\-]+,\s+|"
                           r"and\s+|&\s+|[A-Z]\.\s+)+")


def strip_author_prefix(t):
    return AUTHOR_PREFIX.sub("", dehy(t)).strip()


def find_title_span(raw, title):
    """Locate the title inside a (de-hyphenated) reference entry so venue / year
    can be read from the text right after it rather than from a bled-in
    neighbouring reference."""
    draw = dehy(raw)
    words = re.findall(r"[A-Za-z]{2,}", title)[:4]
    if len(words) < 2:
        return None
    pat = r"\W+".join(re.escape(w) for w in words)
    m = re.search(pat, draw, re.I)
    return (draw, m.start(), m.end()) if m else None


def make_bibkey(author, year, title):
    sur = re.sub(r"[^a-z]", "", (author or "anon").split()[-1].lower()) or "anon"
    skip = {"robust", "multi", "agent", "deep", "learning", "against", "multiagent",
            "reinforcement", "via", "with", "based", "using", "toward", "towards"}
    w = next((x for x in re.sub(r"[^a-z0-9 ]", " ", title.lower()).split()
              if len(x) > 3 and x not in skip), "x")
    return f"{sur}{year or ''}{w}"


def main():
    refs = {int(k): v for k, v in C.load_json("references.json").items()}
    entries = [r for rs in refs.values() for r in rs]
    entry_sig = [sig(r["raw"]) for r in entries]

    rows = list(csv.DictReader(
        open(os.path.join(C.DATA_DIR, "missing_vs_xlsx.csv"), encoding="utf-8")))
    absent = [r for r in rows if r["in_xlsx"] == "no"]
    mc = {(c["title"] or c["rep_raw"]): c
          for c in C.load_json("missing_candidates.json")}

    cands = []
    for r in absent:
        c = mc.get(r["candidate_title"], {})
        cands.append({
            "title": r["candidate_title"],
            "year": int(r["year"]) if r["year"] not in ("", "?", "None") else None,
            "arxiv": r["arxiv"] or (c.get("arxiv") or ""),
            "citing": [int(x) for x in r["citing_papers"].split()]
                      if r["citing_papers"] else c.get("citing_papers", []),
        })

    # 1) dedupe candidates among themselves (de-hyphenated, fuzzy + arXiv)
    cands.sort(key=lambda c: -len(c["citing"]))
    merged = []
    for c in cands:
        q = C.normalize_title(dehy(c["title"]))
        hit = None
        for m in merged:
            same_ax = c["arxiv"] and c["arxiv"] == m["arxiv"]
            if same_ax or fuzz.token_sort_ratio(q, m["_norm"]) >= 86:
                hit = m
                break
        if hit:
            hit["citing"] = sorted(set(hit["citing"]) | set(c["citing"]))
            if not hit["arxiv"] and c["arxiv"]:
                hit["arxiv"] = c["arxiv"]
        else:
            c["_norm"] = q
            merged.append(c)

    # 2) clean title + derive metadata from the entry that contains the title
    out = []
    for c in merged:
        raw_title = strip_author_prefix(c["title"]) if GARBLED.match(c["title"]) \
            else c["title"]
        title = clean_title(raw_title)

        # metadata entry = longest reference entry whose signature contains title
        ts = sig(title)
        meta_idx = [i for i, es in enumerate(entry_sig)
                    if len(ts) >= 18 and ts in es]
        author = year = arxiv = venue = None
        if meta_idx:
            i = max(meta_idx, key=lambda i: len(entry_sig[i]))
            raw = entries[i]["raw"]
            span = find_title_span(raw, title)
            if span:
                draw, s, e = span
                after, before = draw[e:e + 260], draw[:s]
                venue = detect_venue(after) or detect_venue(draw)
                year = C.extract_year(after) or entries[i].get("year")
                arxiv = C.extract_arxiv(after) or entries[i].get("arxiv")
                author = C.first_author_surname(before) or entries[i].get("author")
            else:
                venue = detect_venue(raw)
                year = entries[i].get("year")
                arxiv = entries[i].get("arxiv")
                author = entries[i].get("author")
        year = c["year"] or year
        arxiv = c["arxiv"] or arxiv or ""
        vy = " ".join(x for x in [venue or "", str(year) if year else ""] if x)
        if author:
            vy = (vy + ", " if vy else "") + author.title() + " et al."
        out.append({
            "title": title,
            "category": classify_cat(title),
            "venue_authors": vy,
            "year": year,
            "bibkey": make_bibkey(author, year, title),
            "link": f"https://arxiv.org/abs/{arxiv}" if arxiv else "",
            "citing": c["citing"],
            "count": len(c["citing"]),
        })

    out.sort(key=lambda r: -r["count"])
    C.dump_json(out, "xlsx_new_rows.json")
    print(f"{len(absent)} absent candidates -> {len(out)} unique rows after dedup\n")
    for i, r in enumerate(out, 1):
        print(f"{i:2d}. [{r['count']}x] {r['category'][:26]:26s} | {r['title'][:58]}")
        print(f"      {r['venue_authors']}  | {r['link']}")


if __name__ == "__main__":
    main()
