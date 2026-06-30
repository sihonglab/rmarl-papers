# Paper skeleton — Robust MARL Survey (CSUR)

LaTeX skeleton built 2026-06-17. Target venue: **ACM Computing Surveys** (`acmart`/`acmsmall`).
Corpus: `../robust-marl-MASTER.md` (146 works). Collaboration plan: `../CONTRIBUTING.md`.

## Structure (modular — one file per owner)

```
paper/
├── main.tex                 # preamble, title, abstract, \input glue, PAGE BUDGET
├── refs.bib                 # stub — populate from de-duped raw-data bib (see file header)
├── fig/taxonomy.tex         # signature taxonomy tree (forest), built around the thesis
└── sections/
    ├── 01-introduction.tex  # Lead
    ├── 02-background.tex     # Lead (+ Theory owner for prelims/notation)
    ├── 03-model-uncertainty.tex  # §1 MASTER #1-27   — Theory lead (Profile A)
    ├── 04-state-observation.tex  # §2 MASTER #28-42  — Methods lead (Profile B)
    ├── 05-adversarial.tex        # §3 MASTER #43-59  — Methods lead (Profile B)
    ├── 06-communication.tex      # §4 MASTER #60-72  — Systems lead (Profile C)
    ├── 07-byzantine.tex          # §5 MASTER #73-86  — Systems lead (Profile C)
    ├── 08-llm-mas.tex            # §6 MASTER #87-91  — Systems/frontier or Lead
    ├── 09-offline.tex            # §7 MASTER #92-93  — Systems lead (Profile C)
    ├── 10-benchmarks.tex         # §8 MASTER #94-105 — Systems / entry (Profile D)
    ├── 11-applications.tex       # §9 MASTER #106-146 — Lead + entry (Profile D)
    ├── 12-challenges.tex         # Lead (synthesize)
    └── 13-conclusion.tex         # Lead
```

## Page budget (~36 pp body) — see top of `main.tex` for the per-section split.

## Writing rules (enforced in every section file header)
- **Synthesize, don't enumerate.** Each subsection makes a claim/comparison; papers are evidence.
- **Every content section closes with two questions:** (Q1) why is this harder / new in MARL vs single-agent? (Q2) what is the open gap?
- Use the shared notation/terminology fixed in `02-background.tex`.
- Cross-category papers: cite in the primary section, x-ref the secondary (see `｜跨 §X` tags in MASTER).
- Four-段式 per representative paper: setting → method → result → limitation+classification.

## Compile
```
latexmk -pdf main.tex      # needs a TeX dist with acmart + forest
```
`refs.bib` is a stub; citations won't resolve until it is populated (see `refs.bib` header).
The `\documentclass[...,review,anonymous]{acmart}` options give line numbers / hide authors
for submission — remove for camera-ready.

## Next steps
1. Lead: fill `01`, `02` (freeze thesis/taxonomy/notation) — week 1–2.
2. Populate `refs.bib` (de-dupe raw bib).
3. Hand `03`–`11` to section owners with the one-page task brief (CONTRIBUTING §12 / §11.x).
