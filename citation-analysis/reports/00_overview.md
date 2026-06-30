# Robust-MARL Citation Analysis — Overview

This folder analyses the reference lists of the **133 processed
robust-MARL papers** in `processed-papers/text/`. Three questions are answered:

1. **Coverage gaps** — robust-MARL works cited by our papers but missing from
   the 133-paper set (→ `03_missing_robust_marl_candidates.md`).
2. **Most-cited background** — the works most frequently cited across the set,
   useful for the survey introduction / related-work (→ `02_most_cited_references.md`).
3. **Internal structure** — how the 133 papers cite each other
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

- **132 / 133** papers yielded a parseable
  reference list; **5,767** reference entries total
  (≈ 44 per paper).
- Splitter usage: {'bracket': 74, 'apa': 6, 'authoryear': 41, 'fallback': 2, 'alpha-bracket': 3, 'numbered': 6, 'NONE': 1}.
- **1** paper had no extractable bibliography (scanned/preprint
  layout): #115. Papers #22 and #138 are short extended-abstract /
  book-chapter formats with very few references.
- **3,405** unique cited works after dedup; **587** are cited
  by ≥ 2 of our papers.

## Headline findings

- **318** internal citation links exist among the 133
  papers; the most internally-cited work is Robust-MADDPG (minimax DDPG).
- **19**
  robust-MARL works cited by ≥ 2 of our papers are **missing** from the set —
  topped by *ROMAX* (certifiably robust MARL, cited 10×).

> ⚠️ Heuristic pipeline over noisy PDF text. Treat counts as well-supported
> estimates (±1–2), and verify individual candidates before acting.
