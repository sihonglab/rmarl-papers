"""Step 4: from the clustered references, surface robust-MARL works that are
cited by our papers but are NOT in the 133-paper set -> candidates that may be
missing from the survey. Each candidate is checked against every in-set title
with fuzzy matching to avoid recommending a paper that is already included
under a slightly different title.

Outputs:
  data/missing_candidates.json
"""
import re
from rapidfuzz import fuzz, process
import common as C


def robusty(text):
    t = re.sub(r"-\s+", "", (text or "").lower())
    ma = re.search(r"multi[ -]?agent|multiagent|\bmarl\b|markov game|"
                   r"mean[ -]field|multi[ -]robot", t)
    rob = re.search(r"robust|resilien|adversar|byzantine|fault[- ]toleran|"
                    r"perturb|\battack|poison|certif|distributionally", t)
    return bool(ma and rob)


def main():
    papers = {int(k): v for k, v in C.load_json("papers.json").items()}
    clusters = C.load_json("clusters.json")

    set_titles = [(pid, papers[pid]["canonical_title"]) for pid in papers]
    set_norm = [C.normalize_title(t) for _, t in set_titles]

    candidates = []
    for c in clusters:
        if c["in_set_id"]:
            continue
        text = c["title"] or c["rep_raw"]
        if not robusty(text):
            continue
        # nearest in-set title (guard against variants already included).
        # token_sort_ratio is order/length sensitive, so it does NOT inflate on
        # short generic in-set titles the way token_set_ratio does.
        q = C.normalize_title(text)
        best = process.extractOne(q, set_norm, scorer=fuzz.token_sort_ratio)
        nearest_pid, nearest_title, nearest_score = None, None, 0
        if best:
            nearest_title = set_titles[best[2]][1]
            nearest_pid = set_titles[best[2]][0]
            nearest_score = round(best[1], 1)
        candidates.append({
            "count": c["count"],
            "title": c["title"],
            "rep_raw": c["rep_raw"],
            "year": c["year"],
            "arxiv": c["arxiv"],
            "category": c["category"],
            "citing_papers": c["citing_papers"],
            "nearest_set_id": nearest_pid,
            "nearest_set_title": nearest_title,
            "nearest_score": nearest_score,
        })

    # likely already-in-set only if the title is near-identical (variant)
    for c in candidates:
        c["probable_duplicate"] = c["nearest_score"] >= 93

    candidates.sort(key=lambda d: (d["count"], d["nearest_score"]), reverse=True)
    C.dump_json(candidates, "missing_candidates.json")

    genuine = [c for c in candidates if not c["probable_duplicate"]]
    print(f"robust-MARL candidates not in set: {len(candidates)}")
    print(f"  flagged probable-duplicate (>=90 fuzzy): "
          f"{len(candidates)-len(genuine)}")
    print(f"  genuine missing candidates: {len(genuine)}")
    print(f"  genuine cited by >=3: {len([c for c in genuine if c['count']>=3])}")
    print("\nTop genuine missing candidates (cited by >=2 papers):")
    for c in genuine:
        if c["count"] < 2:
            break
        print(f"  {c['count']:2d}x | {(c['title'] or c['rep_raw'])[:66]}")
        print(f"        nearest in-set ({c['nearest_score']}): "
              f"{(c['nearest_set_title'] or '')[:60]}")

    print("\n--- probable-duplicate flags (verify these are really in set) ---")
    for c in candidates:
        if c["probable_duplicate"]:
            print(f"  {c['count']:2d}x | {(c['title'] or c['rep_raw'])[:55]}  "
                  f"~#{c['nearest_set_id']} ({c['nearest_score']})")


if __name__ == "__main__":
    main()
