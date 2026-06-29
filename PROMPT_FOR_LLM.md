# Prompt — Generate English Robust-MARL paper notes (for a file-capable LLM/agent)

> Hand this whole file to the other LLM. It assumes the agent can read and write files in the repo.

---

You are an expert research assistant building a literature corpus for a survey on **Robust Multi-Agent Reinforcement Learning (Robust MARL)**. Your job is to turn extracted paper texts into standardized **English** notes.

## Repo paths
- **Source texts** (read): `processed-papers/text/<name>.txt`
- **Output notes** (write here): `processed-papers/notes-en/<name>.md` — same base name as the `.txt`, with `.md` extension.
- **Template to follow exactly** (read first): `processed-papers/NOTE_TEMPLATE_EN.md`
- **Finished exemplar to imitate** (read first — copy its style, depth, and especially its Related Work + Cited-references handling): `processed-papers/notes-en/1_Robust MARL with Model Uncertainty.md`

## Before you start
1. Read `processed-papers/NOTE_TEMPLATE_EN.md` (the required structure).
2. Read the exemplar `processed-papers/notes-en/1_Robust MARL with Model Uncertainty.md` once, so your output matches its format precisely.

## Procedure for EACH assigned paper
1. Read the FULL `.txt` (OCR/PDF-extracted — tolerate broken line breaks, hyphenation like "rein-\nforcement", and math artifacts).
2. Write `processed-papers/notes-en/<same name>.md` in **English**, using every heading from the template, in this order:
   `# <id>. <Title>` → `## Metadata` → `## Taxonomy` → `## TL;DR` → `## Problem & Motivation` → `## Robustness Setting` → `## Method` → `## Theoretical Contributions` → `## Experiments` → `## Key Results` → `## Limitations & Future Work` → `## Relevance to Survey` → `## Related Work (verbatim excerpts from the paper)`.
3. `<id>` = the leading number in the filename. Keep technical terms in English.

## Hard rules
- English only. Concise and faithful; respect the per-section bullet guidance in the template.
- **Never fabricate.** If a field is not determinable from the text, write `Not specified`. Do not invent authors, venue, numbers, or results.
- Do not modify any other files. Do not touch the Chinese notes in `processed-papers/notes/` or the `.txt` files.

## CRITICAL — the "Related Work" section must be VERBATIM
- Copy the **original, exact text** from the paper. Do NOT paraphrase, translate, or summarize in this section.
- Prioritize passages on **robust MARL, robust RL / robust MDP, adversarial RL, distributionally robust RL/MARL**, and closely related themes (adversarial attacks, communication robustness, safety, fault tolerance).
- Preserve in-text citation markers exactly: `[12]`, `[18, 19, 20]`, `(Zhang et al., 2020)`.
- Source: if there is a dedicated "Related Work" / "Background and Related Work" / "Literature Review" section, quote its relevant paragraphs; otherwise quote the verbatim paragraph(s) from the Introduction (or elsewhere) discussing prior work. Keep the paper's thematic sub-groupings if any.
- Prefix each quoted block with its location: `> _[Section 2, Related Work]_` or `> _[Introduction]_`.
- Only fix obvious OCR artifacts inside quotes (rejoin split words). Do not change wording, citations, or meaning.
- If the paper truly has no related-work discussion, write exactly: `No related-work discussion found in the text.`

## CRITICAL — resolve the citations
After the verbatim quotes, add a subsection:
`### Cited references (resolved from the paper's bibliography)`
Resolve EVERY citation marker that appears in your quotes to the actual paper, by looking it up in the References/Bibliography at the END of the text file. Format each as:
- **[n]** Author(s) (abbreviated, et al. ok). *Title.* Venue Year.

List ONLY the markers that appear in your quotes (not the whole bibliography). If the extracted text has no usable bibliography, write: `Bibliography not available in the extracted text.` See the exemplar for the exact format.

## Assigned files
Process **every `.txt` in `processed-papers/text/` that does NOT already have a corresponding `.md` in `processed-papers/notes-en/`** (same base name). Currently only paper 1 is done; the other 159 remain. This rule lets you skip finished notes and safely resume if you stop partway.

Tip: process them one at a time (read → write → next). Long context tends to corrupt verbatim quotes, so finish and write each note before moving on. If your context/output is limited, do ~8 files per run and repeat.

## When done
Report, per file: the output path written, and whether a dedicated related-work section existed or excerpts were pulled from the Introduction.
