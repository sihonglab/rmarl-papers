# Citation Analysis of the Robust-MARL Paper Set

Analyses the **reference lists** of the 133 processed robust-MARL papers
(`../processed-papers/text/`) to support writing the survey. It answers:

1. **Coverage gaps** — robust-MARL works cited by our papers but *missing* from
   the set → strong candidates to add.
2. **Most-cited background** — the works our papers cite most, grouped by topic,
   for the introduction / related-work.
3. **Internal structure** — the directed citation graph *among* the 133 papers.

## Layout

```
citation-analysis/
├── README.md
├── scripts/            # the reproducible pipeline (run_all.sh)
│   ├── common.py               # shared parsing / normalisation / classify
│   ├── 01_extract_references.py
│   ├── 02_internal_graph.py
│   ├── 03_cluster_external.py
│   ├── 04_missing_candidates.py
│   └── 05_write_reports.py
├── data/               # intermediate + machine-readable artifacts
│   ├── references.json         # parsed reference entries per paper
│   ├── internal_*.json/.csv    # citation graph among our papers
│   ├── internal_graph.graphml  # open in Gephi / Cytoscape
│   ├── clusters.json/.csv      # deduplicated unique cited works + counts
│   └── missing_candidates.json/.csv
└── reports/            # human-readable English findings
    ├── 00_overview.md
    ├── 01_internal_citation_graph.md
    ├── 02_most_cited_references.md
    ├── 03_missing_robust_marl_candidates.md
    ├── 04_missing_vs_master_list.md    # ← candidates cross-checked vs robust-marl-papers.xlsx
    └── internal_citation_graph.html   # ← interactive graph (open in a browser)
```

## Interactive graph

`reports/internal_citation_graph.html` is a **self-contained** (D3 inlined, no
internet/server needed) force-directed view of the 133-paper citation network.
Just double-click it. Node size = times cited within the set; color = topic;
arrows point from citing → cited. Hover for details, click a node to highlight
its citation neighbourhood, search by id/title, filter by category, slide the
min-in-degree control, or hide the 36 isolated nodes.

## Reproduce

```bash
cd scripts
pip install rapidfuzz numpy        # pandas not required
bash run_all.sh
```

## Updating the master spreadsheet

`08_prepare_xlsx_rows.py` cleans the genuine-gap candidates (dedupes variants,
re-derives venue/year/authors/arXiv, maps to the spreadsheet's category
taxonomy) into `data/xlsx_new_rows.json`. `09_append_to_xlsx.py` then inserts
them into `../robust-marl-papers.xlsx` (tagged `Source = cite-analysis`,
auto-backup first, idempotent), and `10_append_to_md.py` inserts a marked
supplement section into `../robust-marl-MASTER.md` in that file's own style.
Steps 09/10 are **not** part of `run_all.sh` — run them manually.

- xlsx: 52 gaps → **47** unique rows, added as No. 147–193.
- master md: **45** added as No. 147–191 (2 fewer — the ACM CSUR'25 survey is
  already in §10, and one comm paper is already corpus #65).

## Headline numbers

- 132 / 133 papers parsed → **5,767** reference entries → **3,405** unique works.
- **318** internal citation links; most-cited anchor = Robust-MADDPG (minimax DDPG).
- **55** robust-MARL works cited by our papers are missing from the set
  (top: *ROMAX*, cited 10×).

## Caveats

Heuristic pipeline over PyMuPDF-extracted text. Reference **counts and the
identity of top works are reliable**; secondary fields (per-entry `year`,
`arXiv` id) are occasionally wrong due to reference-boundary bleed in the raw
text. Topical buckets are keyword-based. Verify individual candidates before
acting on them.
