# Standardized Paper Note Template (Robust MARL Survey) — English

> One note file per paper. Filename matches the text file (`<id>_<title>.md`), stored in `processed-papers/notes-en/`.
> Fill every field strictly following the structure below. If a field cannot be determined from the full text, write `Not specified` — do not fabricate. Keep technical terms in their original English form.
> The **Related Work** section is special: it must contain the **verbatim original text** copied from the paper (see instructions in that section).

---

```markdown
# <id>. <Paper Title>

## Metadata
- **Title**:
- **Authors**: (first few + et al.)
- **Affiliation**:
- **Venue**: <venue> <year> (write `Not specified` if undeterminable)
- **Link/arXiv**: (fill if present in text, otherwise `Not specified`)

## Taxonomy
- **Robustness / perturbation type targeted**: (e.g., environment/model uncertainty, state/observation perturbation, action perturbation, adversarial agents, communication attacks, Byzantine/fault tolerance, reward poisoning, agent failure, safety constraints, etc.)
- **Method paradigm**: (e.g., DRMG theory, adversarial training, minimax, value decomposition, certified robustness, risk-sensitive, curriculum learning, game-theoretic equilibrium, etc.)
- **Keywords**: 3–6 terms

## TL;DR
(One sentence summarizing what the paper does and its single most important contribution.)

## Problem & Motivation
(What problem it solves, why it matters, and the gaps in prior work.)

## Robustness Setting
- **Threat model / uncertainty set**: (where the perturbation acts, the attacker's capability, how uncertainty is modeled)
- **Setting**: cooperative / competitive / mixed; CTDE / decentralized / centralized; online / offline

## Method
(Core idea and algorithmic steps, 2–5 bullet points. Describe key formulas/losses/constraints in words.)

## Theoretical Contributions
(Convergence, sample complexity, equilibrium existence, certified radius, etc.; write `None / mostly empirical` if absent.)

## Experiments
- **Environment/Benchmark**:
- **Baselines**:
- **Evaluation metrics**:

## Key Results
(Quantitative conclusions and most important findings, 2–4 bullet points.)

## Limitations & Future Work

## Relevance to Survey
(Where this paper sits in the robust MARL landscape; which themes/method lines it connects to.)

## Related Work (verbatim excerpts from the paper)
> Copy the **original, verbatim text** of the paper's discussion of related work — prioritize passages on **robust MARL, robust RL/robust MDP, adversarial RL, distributionally robust RL**, and closely related topics. Preserve in-text citation markers (e.g., [12], (Zhang et al., 2020)) exactly as they appear.
> - If the paper has a dedicated "Related Work" / "Background and Related Work" / "Literature Review" section, quote the relevant paragraphs from it.
> - If there is no dedicated section, extract the verbatim paragraphs from the Introduction (or elsewhere) where prior work is discussed.
> - Group quotes under sub-headings when the paper organizes related work by theme (e.g., "Robust RL", "MARL", "Adversarial attacks").
> - Indicate the source location for each block, e.g. `> _[Section 2, Related Work]_` or `> _[Introduction]_`.
> - Do NOT paraphrase or summarize here — this section is for reusable verbatim source material. If the paper truly contains no related-work discussion, write `No related-work discussion found in the text.`
>
> After the verbatim quotes, add a `### Cited references (resolved from the paper's bibliography)` subsection that resolves EVERY citation marker appearing in the quotes above to its actual reference. Look the markers up in the paper's References/Bibliography section at the end of the text and list them as:
> `- **[n]** Author(s) (abbreviated, et al. ok). *Title.* Venue Year.`
> Only list the markers that actually appear in your quoted excerpts. If the text has no usable bibliography to resolve them, write `Bibliography not available in the extracted text.`
```
