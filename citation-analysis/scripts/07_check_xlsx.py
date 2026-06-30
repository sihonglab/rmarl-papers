"""Step 7: cross-check the candidate "missing" robust-MARL papers against the
master list in robust-marl-papers.xlsx (146 entries, 13 of which are not yet
in the 133 processed set). Decides, per candidate, whether it is ALREADY in the
spreadsheet or genuinely absent.

Outputs:
  data/missing_vs_xlsx.csv
  reports/04_missing_vs_master_list.md
"""
import os
import csv
import pandas as pd
from rapidfuzz import fuzz, process
import common as C

XLSX = os.path.join(C.PROJECT_DIR, "robust-marl-papers.xlsx")


def load_xlsx():
    df = pd.read_excel(XLSX, sheet_name="Robust MARL Papers")
    rows = []
    for _, r in df.iterrows():
        if pd.isna(r["Title"]) or pd.isna(r["No"]):
            continue
        rows.append({
            "no": int(r["No"]),
            "title": str(r["Title"]),
            "year": r.get("Year"),
            "venue": r.get("Venue/Authors"),
        })
    return rows


def decide(set_score, sort_score):
    """Returns 'yes' (already in list), 'verify' (likely same line of work but
    titles/venues differ enough to check by hand), or 'no' (genuinely absent).
    token_set >= 93 is near-identical even when leftover author fragments
    depress the ordered score; the 88-93 band with decent ordering is a
    journal/conference-variant grey zone."""
    if set_score >= 93:
        return "yes"
    if set_score >= 88 and sort_score >= 68:
        return "verify"
    return "no"


def main():
    xls = load_xlsx()
    xls_norm = [C.normalize_title(x["title"]) for x in xls]
    papers = C.load_json("papers.json")
    proc = set(int(k) for k in papers)

    cand = [c for c in C.load_json("missing_candidates.json")
            if not c["probable_duplicate"]]

    results = []
    for c in cand:
        q = C.normalize_title(c["title"] or c["rep_raw"])
        i = process.extractOne(q, xls_norm, scorer=fuzz.token_set_ratio)
        j = process.extractOne(q, xls_norm, scorer=fuzz.token_sort_ratio)
        m = xls[i[2]]
        in_xlsx = decide(i[1], j[1])
        results.append({
            "count": c["count"],
            "title": c["title"] or c["rep_raw"],
            "year": c["year"],
            "arxiv": c["arxiv"],
            "citing_papers": c["citing_papers"],
            "in_xlsx": in_xlsx,
            "xlsx_no": m["no"],
            "xlsx_title": m["title"],
            "xlsx_processed": m["no"] in proc,
            "set_score": round(i[1], 1),
            "sort_score": round(j[1], 1),
        })

    order = {"yes": 0, "verify": 1, "no": 2}
    results.sort(key=lambda r: (order[r["in_xlsx"]], -r["count"]))

    # CSV
    with open(os.path.join(C.DATA_DIR, "missing_vs_xlsx.csv"), "w",
              newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["count", "candidate_title", "year", "arxiv", "in_xlsx",
                     "xlsx_no", "xlsx_title", "xlsx_processed", "set_score",
                     "sort_score", "citing_papers"])
        for r in results:
            wr.writerow([r["count"], r["title"], r["year"], r["arxiv"],
                         r["in_xlsx"], r["xlsx_no"], r["xlsx_title"],
                         r["xlsx_processed"], r["set_score"], r["sort_score"],
                         " ".join(map(str, r["citing_papers"]))])

    already = [r for r in results if r["in_xlsx"] == "yes"]
    verify = [r for r in results if r["in_xlsx"] == "verify"]
    absent = [r for r in results if r["in_xlsx"] == "no"]

    # Markdown report
    L = ["# Missing Candidates vs. Master List (`robust-marl-papers.xlsx`)\n"]
    L.append("Checks whether the robust-MARL papers flagged as *missing from the "
             "133 processed set* are nonetheless **already tracked in the 146-row "
             "master spreadsheet**. (The spreadsheet has 13 entries not yet "
             "processed into `processed-papers/`.)\n")
    L.append(f"- Candidates checked: **{len(results)}**")
    L.append(f"- Already in the spreadsheet: **{len(already)}**")
    L.append(f"- Possibly already in (conference/journal variant — verify): "
             f"**{len(verify)}**")
    L.append(f"- Genuinely absent (true gaps): **{len(absent)}**\n")
    L.append("Full table: `data/missing_vs_xlsx.csv`. Match = token-set / "
             "token-sort fuzzy similarity on normalised titles; borderline rows "
             "were verified by hand.\n")

    L.append("## ✅ Already in the master list (no action needed)\n")
    L.append("| Cites | Candidate (from references) | → Master row | "
             "Processed? | sim (set/sort) |")
    L.append("|------:|------------------------------|--------------|"
             "-----------|----------------|")
    for r in already:
        proc_s = "yes" if r["xlsx_processed"] else "**not yet**"
        L.append(f"| {r['count']} | {r['title'][:60]} | "
                 f"No.{r['xlsx_no']} — {r['xlsx_title'][:42]} | {proc_s} | "
                 f"{r['set_score']}/{r['sort_score']} |")

    if verify:
        L.append("\n## ⚠️ Possibly already in — verify (likely conference vs. "
                 "journal version of a listed paper)\n")
        L.append("| Cites | Candidate (from references) | Closest master row | "
                 "Processed? | sim (set/sort) |")
        L.append("|------:|------------------------------|--------------------|"
                 "-----------|----------------|")
        for r in verify:
            proc_s = "yes" if r["xlsx_processed"] else "**not yet**"
            L.append(f"| {r['count']} | {r['title'][:60]} | "
                     f"No.{r['xlsx_no']} — {r['xlsx_title'][:40]} | {proc_s} | "
                     f"{r['set_score']}/{r['sort_score']} |")

    L.append("\n## ❌ Genuinely absent — true coverage gaps "
             f"({len(absent)} works)\n")
    L.append("Not in the processed set **and** not in the spreadsheet. Ranked by "
             "how many of our papers cite them.\n")
    L.append("| Cites | Candidate work | Year | Cited by | Closest master row "
             "(sim) |")
    L.append("|------:|----------------|------|----------|----------------------|")
    for r in absent:
        cb = ", ".join(f"#{p}" for p in r["citing_papers"])
        ax = f" · arXiv:{r['arxiv']}" if r["arxiv"] else ""
        L.append(f"| {r['count']} | {r['title']}{ax} | {r['year'] or '?'} | "
                 f"{cb} | No.{r['xlsx_no']} ({r['set_score']}/{r['sort_score']}) |")

    with open(os.path.join(C.REPORTS_DIR, "04_missing_vs_master_list.md"),
              "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"checked {len(results)} candidates")
    print(f"  already in xlsx : {len(already)}")
    for r in already:
        print(f"     [{r['count']}x] {r['title'][:50]}  -> No.{r['xlsx_no']} "
              f"({'processed' if r['xlsx_processed'] else 'NOT processed'}) "
              f"set{r['set_score']}/sort{r['sort_score']}")
    print(f"  genuinely absent: {len(absent)}")


if __name__ == "__main__":
    main()
