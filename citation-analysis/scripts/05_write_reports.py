"""Step 5: turn the analysis JSON into human-readable English reports plus
spreadsheet/graph artifacts.

Outputs (in reports/ and data/):
  reports/00_overview.md
  reports/01_internal_citation_graph.md
  reports/02_most_cited_references.md
  reports/03_missing_robust_marl_candidates.md
  data/internal_edges.csv
  data/internal_nodes.csv
  data/internal_graph.graphml
  data/clusters.csv
  data/missing_candidates.csv
"""
import os
import csv
import html
import common as C

CAT_LABEL = {
    "robust_marl": "Robust MARL",
    "marl": "MARL (non-robust)",
    "robust_rl": "Robust RL (single-agent)",
    "rl": "RL / Deep RL",
    "game_theory": "Game theory / equilibria",
    "other": "Other",
}


def load():
    papers = {int(k): v for k, v in C.load_json("papers.json").items()}
    stats = C.load_json("internal_stats.json")
    edges = C.load_json("internal_edges.json")
    clusters = C.load_json("clusters.json")
    extract = C.load_json("extract_stats.json")
    missing = C.load_json("missing_candidates.json")
    return papers, stats, edges, clusters, extract, missing


def w(path, text):
    with open(os.path.join(C.REPORTS_DIR, path), "w", encoding="utf-8") as f:
        f.write(text)


def short(papers, pid):
    return papers[pid]["short_title"]


# --------------------------------------------------------------------------
# CSV / GraphML artifacts
# --------------------------------------------------------------------------
def write_artifacts(papers, stats, edges, clusters, missing):
    pp = stats["per_paper"]
    # internal nodes
    with open(os.path.join(C.DATA_DIR, "internal_nodes.csv"), "w",
              newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["id", "title", "category", "in_degree", "out_degree"])
        for pid in sorted(papers):
            d = pp[str(pid)]
            wr.writerow([pid, papers[pid]["canonical_title"],
                         C.classify(papers[pid]["canonical_title"]),
                         d["in"], d["out"]])
    # internal edges
    with open(os.path.join(C.DATA_DIR, "internal_edges.csv"), "w",
              newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["src", "dst", "src_title", "dst_title", "how"])
        for e in edges:
            wr.writerow([e["src"], e["dst"],
                         papers[e["src"]]["short_title"],
                         papers[e["dst"]]["short_title"], e["how"]])
    # GraphML (directed: src cites dst)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
             '<key id="title" for="node" attr.name="title" attr.type="string"/>',
             '<key id="cat" for="node" attr.name="category" attr.type="string"/>',
             '<key id="indeg" for="node" attr.name="indegree" attr.type="int"/>',
             '<graph edgedefault="directed">']
    for pid in sorted(papers):
        d = pp[str(pid)]
        t = html.escape(papers[pid]["canonical_title"])
        cat = C.classify(papers[pid]["canonical_title"])
        lines.append(f'<node id="n{pid}"><data key="title">{t}</data>'
                     f'<data key="cat">{cat}</data>'
                     f'<data key="indeg">{d["in"]}</data></node>')
    for i, e in enumerate(edges):
        lines.append(f'<edge id="e{i}" source="n{e["src"]}" '
                     f'target="n{e["dst"]}"/>')
    lines += ["</graph>", "</graphml>"]
    with open(os.path.join(C.DATA_DIR, "internal_graph.graphml"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(lines))
    # clusters
    with open(os.path.join(C.DATA_DIR, "clusters.csv"), "w",
              newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["count", "category", "title", "year", "arxiv",
                     "in_set_id", "n_variants", "citing_papers", "rep_raw"])
        for c in clusters:
            wr.writerow([c["count"], c["category"], c["title"], c["year"],
                         c["arxiv"], c["in_set_id"], c["n_variants"],
                         " ".join(map(str, c["citing_papers"])), c["rep_raw"]])
    # missing
    with open(os.path.join(C.DATA_DIR, "missing_candidates.csv"), "w",
              newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["count", "title", "year", "arxiv", "probable_duplicate",
                     "nearest_set_id", "nearest_score", "citing_papers",
                     "rep_raw"])
        for c in missing:
            wr.writerow([c["count"], c["title"], c["year"], c["arxiv"],
                         c["probable_duplicate"], c["nearest_set_id"],
                         c["nearest_score"],
                         " ".join(map(str, c["citing_papers"])), c["rep_raw"]])


# --------------------------------------------------------------------------
# Reports
# --------------------------------------------------------------------------
def report_overview(papers, stats, edges, clusters, extract, missing):
    n_norefs = [s["id"] for s in extract if s["method"] == "NONE"]
    total_refs = sum(s["n"] for s in extract)
    from collections import Counter
    methods = Counter(s["method"] for s in extract)
    n_multi = len([c for c in clusters if c["count"] >= 2])
    md = f"""# Robust-MARL Citation Analysis — Overview

This folder analyses the reference lists of the **{len(papers)} processed
robust-MARL papers** in `processed-papers/text/`. Three questions are answered:

1. **Coverage gaps** — robust-MARL works cited by our papers but missing from
   the {len(papers)}-paper set (→ `03_missing_robust_marl_candidates.md`).
2. **Most-cited background** — the works most frequently cited across the set,
   useful for the survey introduction / related-work (→ `02_most_cited_references.md`).
3. **Internal structure** — how the {len(papers)} papers cite each other
   (→ `01_internal_citation_graph.md`).

## Pipeline (reproducible)

| Step | Script | Output |
|------|--------|--------|
| 1 | `01_extract_references.py` | `data/references.json` — reference entries per paper |
| 2 | `02_internal_graph.py` | `data/internal_*.json` — citation graph among our papers |
| 3 | `03_cluster_external.py` | `data/clusters.json` — deduplicated unique cited works |
| 4 | `04_missing_candidates.py` | `data/missing_candidates.json` — robust-MARL gaps |
| 5 | `05_write_reports.py` | these reports + CSV / GraphML artifacts |
| 6 | `06_build_html.py` | `reports/internal_citation_graph.html` — interactive graph |

Run `bash run_all.sh` from `scripts/` to regenerate everything.

> 📊 **Interactive graph:** open `reports/internal_citation_graph.html` in any
> browser (self-contained, no server needed) to explore the citation network —
> node size = times cited, color = topic, arrows point citing → cited.

## Method notes

- **Reference extraction.** Text is PyMuPDF-extracted, so reference lists appear
  in many styles. The parser auto-detects and handles numeric `[n]`, alphabetic
  `[Author, year]`, numbered `1.`, APA `Author (year). Title.`, and natbib
  author–year lists, picking whichever splitter yields the most entries.
- **Deduplication.** The same work cited by different papers is merged via arXiv
  id plus year-blocked fuzzy matching (`token_set_ratio ≥ 88`) on normalised
  entries, robust to author-format and hyphenation differences.
- **In-set / missing detection.** A cited work is "in-set" when an existing
  paper's title is found (separator-free) inside one of its citation strings;
  near-identical title variants are caught with `token_sort_ratio ≥ 93`.
- **Topical buckets** (`robust_marl`, `marl`, `robust_rl`, `rl`, `game_theory`,
  `other`) are keyword-based and approximate — a coarse filter, not ground truth.

## Data quality

- **{len(papers) - len(n_norefs)} / {len(papers)}** papers yielded a parseable
  reference list; **{total_refs:,}** reference entries total
  (≈ {total_refs / max(1, len(papers) - len(n_norefs)):.0f} per paper).
- Splitter usage: {dict(methods)}.
- **{len(n_norefs)}** paper had no extractable bibliography (scanned/preprint
  layout): {', '.join('#'+str(i) for i in n_norefs)}. Papers #22 and #138 are short extended-abstract /
  book-chapter formats with very few references.
- **{len(clusters):,}** unique cited works after dedup; **{n_multi}** are cited
  by ≥ 2 of our papers.

## Headline findings

- **{stats['n_edges']}** internal citation links exist among the {len(papers)}
  papers; the most internally-cited work is Robust-MADDPG (minimax DDPG).
- **{len([c for c in missing if not c['probable_duplicate'] and c['count']>=2])}**
  robust-MARL works cited by ≥ 2 of our papers are **missing** from the set —
  topped by *ROMAX* (certifiably robust MARL, cited 10×).

> ⚠️ Heuristic pipeline over noisy PDF text. Treat counts as well-supported
> estimates (±1–2), and verify individual candidates before acting.
"""
    w("00_overview.md", md)


def report_internal(papers, stats, edges):
    pp = stats["per_paper"]
    ids = sorted(papers)
    indeg = {p: pp[str(p)]["in"] for p in ids}
    outdeg = {p: pp[str(p)]["out"] for p in ids}

    def trow(p):
        return (f"| {indeg[p]} | {outdeg[p]} | #{p} | "
                f"{papers[p]['canonical_title']} |")

    top_cited = sorted(ids, key=lambda p: indeg[p], reverse=True)[:25]
    top_citing = sorted(ids, key=lambda p: outdeg[p], reverse=True)[:15]
    backbone = sorted([p for p in ids if indeg[p] >= 1 and outdeg[p] >= 1],
                      key=lambda p: indeg[p] + outdeg[p], reverse=True)
    iso = sorted([p for p in ids if indeg[p] == 0 and outdeg[p] == 0])

    lines = []
    lines.append("# Internal Citation Graph (how the 133 papers cite each other)\n")
    lines.append(f"- Nodes: **{len(ids)}** papers · Directed edges "
                 f"(A cites B): **{stats['n_edges']}** "
                 f"(exact title match {stats['n_exact']}, "
                 f"fuzzy {stats['n_fuzzy']}).")
    lines.append(f"- Edge density {stats['n_edges'] / (len(ids)*(len(ids)-1)):.3%}; "
                 f"**{len(iso)}** papers have no internal links (peripheral / "
                 f"application or very recent works).")
    lines.append("- Machine-readable: `data/internal_edges.csv`, "
                 "`data/internal_nodes.csv`, `data/internal_graph.graphml` "
                 "(open in Gephi/Cytoscape).\n")

    lines.append("## Most internally-cited papers (the field's anchors)\n")
    lines.append("These are cited most often *by the other papers in the set* — "
                 "the foundational references a survey must foreground.\n")
    lines.append("| In | Out | # | Title |")
    lines.append("|----|-----|---|-------|")
    lines += [trow(p) for p in top_cited]

    lines.append("\n## Papers that cite the most others in the set\n")
    lines.append("High out-degree ≈ well-grounded in robust-MARL prior work "
                 "(often the most survey-like / recent papers).\n")
    lines.append("| In | Out | # | Title |")
    lines.append("|----|-----|---|-------|")
    lines += [trow(p) for p in top_citing]

    lines.append("\n## Connected backbone (both cited and citing)\n")
    lines.append(f"{len(backbone)} papers participate in the citation network on "
                 "both sides — the densely-linked core of the robust-MARL "
                 "literature.\n")
    lines.append("| In | Out | # | Title |")
    lines.append("|----|-----|---|-------|")
    lines += [trow(p) for p in backbone[:30]]

    lines.append("\n## Notable citation chains\n")
    # show, for each top-cited paper, who cites it
    for p in top_cited[:6]:
        citers = ", ".join(f"#{c}" for c in pp[str(p)]["cited_by"])
        lines.append(f"- **#{p} {papers[p]['canonical_title'][:60]}** "
                     f"← cited by {indeg[p]} papers: {citers}")

    lines.append("\n## Isolated papers (no internal citation link)\n")
    lines.append("Neither cite nor are cited by any other paper in the set. "
                 "Usually adjacent-domain (energy, UAV, routing, LLM-agent) or "
                 "very recent. Worth checking they belong in the survey scope.\n")
    for p in iso:
        lines.append(f"- #{p} — {papers[p]['canonical_title']}")

    w("01_internal_citation_graph.md", "\n".join(lines))


def report_most_cited(papers, clusters):
    def fmt(c, show_cat=True):
        tag = (f" · **[in set #{c['in_set_id']}]**" if c["in_set_id"] else "")
        yr = f" ({c['year']})" if c["year"] else ""
        title = c["title"] or c["rep_raw"]
        ax = f" · arXiv:{c['arxiv']}" if c["arxiv"] else ""
        work = f"{title}{yr}{ax}{tag}"
        if show_cat:
            return f"| {c['count']} | `{c['category']}` | {work} |"
        return f"| {c['count']} | {work} |"

    lines = ["# Most-Cited References (background for the survey intro)\n"]
    lines.append("Works ranked by **how many of our 133 papers cite them**. "
                 "`[in set #id]` marks works already in the collection. Use the "
                 "non-in-set rows as the canonical background citations for the "
                 "introduction / related-work.\n")
    lines.append("Full table: `data/clusters.csv`.\n")

    top = [c for c in clusters if c["count"] >= 5]
    lines.append(f"## Overall top works (cited by ≥ 5 papers, "
                 f"{len(top)} works)\n")
    lines.append("| Cites | Category | Work |")
    lines.append("|------:|----------|------|")
    lines += [fmt(c) for c in top]

    for cat in ["robust_marl", "robust_rl", "marl", "rl", "game_theory"]:
        sub = [c for c in clusters if c["category"] == cat and c["count"] >= 3]
        if not sub:
            continue
        lines.append(f"\n## {CAT_LABEL[cat]} — cited by ≥ 3 papers "
                     f"({len(sub)} works)\n")
        lines.append("| Cites | Work |")
        lines.append("|------:|------|")
        lines += [fmt(c, show_cat=False) for c in sub]

    w("02_most_cited_references.md", "\n".join(lines))


def report_missing(papers, missing):
    genuine = [c for c in missing if not c["probable_duplicate"]]
    dup = [c for c in missing if c["probable_duplicate"]]

    lines = ["# Candidate Missing Robust-MARL Papers\n"]
    lines.append("Robust-MARL works **cited by our papers but not in the "
                 "133-paper set** — ranked by number of citing papers. Each is "
                 "checked against every in-set title; the *nearest in-set* "
                 "column (token-sort similarity) confirms it is a distinct work. "
                 "Strong candidates for inclusion in the survey.\n")
    lines.append("Full table: `data/missing_candidates.csv`.\n")

    def block(items, minc):
        out = ["| Cites | Candidate work | Year | Cited by | Nearest in-set "
               "(sim) |", "|------:|----------------|------|----------|"
               "------------------|"]
        for c in items:
            if c["count"] < minc:
                continue
            cb = ", ".join(f"#{p}" for p in c["citing_papers"])
            t = c["title"] or c["rep_raw"]
            ax = f" · arXiv:{c['arxiv']}" if c["arxiv"] else ""
            near = f"#{c['nearest_set_id']} ({c['nearest_score']})"
            out.append(f"| {c['count']} | {t}{ax} | {c['year'] or '?'} | "
                       f"{cb} | {near} |")
        return out

    lines.append("## Top candidates (cited by ≥ 2 papers)\n")
    lines += block(genuine, 2)

    singles = [c for c in genuine if c["count"] == 1]
    lines.append(f"\n## Long tail (cited by exactly 1 paper, "
                 f"{len(singles)} works)\n")
    lines.append("Lower priority, but may still fill niche subtopics "
                 "(application robust-MARL, attacks, safety).\n")
    lines.append("| Candidate work | Year | Cited by |")
    lines.append("|----------------|------|----------|")
    for c in singles:
        t = c["title"] or c["rep_raw"]
        cb = ", ".join(f"#{p}" for p in c["citing_papers"])
        lines.append(f"| {t} | {c['year'] or '?'} | {cb} |")

    if dup:
        lines.append("\n## Flagged as already-in-set variants (excluded)\n")
        for c in dup:
            lines.append(f"- {c['title']} — matches in-set "
                         f"#{c['nearest_set_id']} ({c['nearest_score']})")

    w("03_missing_robust_marl_candidates.md", "\n".join(lines))


def main():
    papers, stats, edges, clusters, extract, missing = load()
    write_artifacts(papers, stats, edges, clusters, missing)
    report_overview(papers, stats, edges, clusters, extract, missing)
    report_internal(papers, stats, edges)
    report_most_cited(papers, clusters)
    report_missing(papers, missing)
    print("Reports written to reports/ ; artifacts to data/")
    for fn in sorted(os.listdir(C.REPORTS_DIR)):
        print("  reports/" + fn)


if __name__ == "__main__":
    main()
