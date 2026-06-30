# Robust MARL — Author × Paper Analysis Outputs

Generated from parsing the `Metadata` / `Taxonomy` fields of all 160 notes in `notes-en/`.

- **160** papers, **550** distinct authors, **87** authors appearing in ≥2 papers.
- Co-authorship graph (recurring authors only): **84 nodes**, **199 edges**, **18 connected teams**.

## Files

| File | What it is |
|---|---|
| `papers_metadata.csv` | One row per paper: id, year, venue, #authors, full author list, affiliation, robustness type, method paradigm. |
| `author_paper_long.csv` | Tidy long format — one row per (author, paper). 1,000+ rows; ideal for pivot tables / pandas `groupby`. |
| `author_x_paper_matrix.csv` | **The author × paper matrix.** Rows = the 87 recurring authors (sorted by paper count); columns = the 80 papers that involve a recurring author; cell = `1` if authored. |
| `coauthorship_edges.csv` | Edge list among recurring authors: author_a, author_b, #shared papers, paper_ids. Sorted by tie strength. |
| `teams_summary.csv` | The 18 collaboration clusters (connected components), with members, their paper counts, and all paper ids. |
| `collaboration_graph.mmd` | Mermaid diagram of the clusters — paste into any Mermaid renderer / GitHub markdown. |
| `collaboration_graph.gexf` | Same graph for **Gephi / Cytoscape** (nodes carry `team` + `papers` attributes). |

## Notes / caveats
- Author names parsed from the `Authors` field (often "first few + et al."), so **junior co-authors past the et-al. cutoff are missing**; counts are lower bounds.
- 5 papers are double-blind (`Anonymous authors`) and cannot be attributed.
- Clusters are *connected components* — two distinct research lines get merged if even one author bridges them (e.g., Maryland's Yanchao Sun co-authoring with UConn's Fei Miao on #106). Treat the bridge as a real collaboration, not an error.
