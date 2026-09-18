---
name: alterlab-qualitative-analysis
description: "Analyzes qualitative data as a dispatched pipeline module — codebook development, thematic / framework / content analysis, and inter-coder reliability computed correctly (Krippendorff's alpha as primary via the krippendorff package or a bundled stdlib nominal calculator with bootstrap CIs; Cohen's / Fleiss' kappa via statsmodels) with 95% CIs and thresholds (alpha >= .80 reliable, .667-.80 tentative). It BRANCHES by design: coefficient-based ICR for codebook / content-analytic coding, versus consensus-and-reflexivity for reflexive thematic analysis where a statistic is not the right criterion. Supports human-vs-LLM double-coding with an alpha check against a human gold standard. Use when coding interviews or open-ended text, building a codebook, or reporting intercoder reliability. For topic modeling / embeddings / supervised text classification prefer alterlab-text-as-data; for the reflexivity gate prefer alterlab-ssci-reflexivity-gate. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires (declare in-session, no runtime install on Anthropic API): Python krippendorff>=0.8, statsmodels>=0.14 (Fleiss/Cohen kappa via statsmodels.stats.inter_rater), pandas. For alpha with CIs use R irrCAC / icr, or the bundled stdlib nominal calculator. Optional LLM-assisted coding uses the platform's model. Runs locally via `uv run python`; no extra API key."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-qualitative-methods (methodology reference), alterlab-text-as-data (computational text), alterlab-ssci-reflexivity-gate (trustworthiness)"
---

# Qualitative Analysis — Reliability When It Fits, Consensus When It Doesn't

**Skill type: ANALYSIS MODULE.** Codes qualitative data and reports agreement *correctly*. The
central discipline is a branch: a reliability **coefficient** is right for codebook/content-analytic
work, but for reflexive thematic analysis the criterion is **consensus and reflexivity**, not a
statistic. The skill does not oversell the number.

## Core Mission

```
KRIPPENDORFF'S ALPHA IS THE PRIMARY COEFFICIENT — BUT A COEFFICIENT IS THE WRONG TOOL FOR REFLEXIVE TA.
BRANCH BY DESIGN.
```

## When to Use This Skill

- "Two RAs coded my interviews with a codebook — compute intercoder reliability."
- "Build/refine a codebook and report agreement."
- "I used an LLM to code open-ended responses — does it agree with my human coding?"
- "Which reliability statistics do I report for a content analysis?"

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Topic modeling / embeddings / supervised text classification | `alterlab-text-as-data` | Computational text, not human-coding reliability. |
| Whether the study is trustworthy (positionality, Lincoln & Guba) | `alterlab-ssci-reflexivity-gate` | Trustworthiness gate, not the coding itself. |
| Choosing the qualitative method (grounded theory, phenomenology) | `alterlab-qualitative-methods` | Methodology selection, upstream. |
| Whether a scale is reliable/valid (quantitative) | `alterlab-ssci-measurement-gate` | Psychometrics, different problem. |

## The branch (this is the core discipline)

| Design | Reliability criterion |
|--------|-----------------------|
| **Codebook / content-analytic** coding (fixed categories, replicable) | compute an **ICR coefficient** (Krippendorff's α) with a CI and threshold |
| **Reflexive thematic analysis** (interpretive, researcher-as-instrument) | **consensus + reflexivity** — collaborative discussion to understand differences; a coefficient misrepresents the epistemology and is NOT required. Route trustworthiness to `alterlab-ssci-reflexivity-gate`. |

Do not force α onto reflexive TA, and do not skip α on content-analytic coding.

## Correct coefficient choice (verified)

- **Krippendorff's α — primary.** Handles ≥2 coders, any measurement level (nominal/ordinal/
  interval/ratio), and missing data. Python `krippendorff.alpha(reliability_data=<coders × units>,
  level_of_measurement="nominal")` returns a **point estimate only** — pair it with a bootstrap CI
  (the bundled `scripts/icr.py` does nominal α + a bootstrap CI + Cohen's κ in pure stdlib; R
  `irrCAC::krippen.alpha.raw` or `icr::krippalpha(..., bootstrap=TRUE)` give CIs for all levels).
- **Cohen's κ** (2 coders) / **Fleiss' κ** (>2, fixed number): `statsmodels.stats.inter_rater`
  `cohens_kappa`, `fleiss_kappa` (build the count table with `aggregate_raters`); sklearn
  `cohen_kappa_score` as a cross-check.
- **NOT valid ICR measures:** chi-square, Cronbach's alpha, and Pearson's r — they measure
  covariation/internal consistency, not chance-corrected agreement. Refuse these.

Thresholds (Krippendorff): **α ≥ .80 reliable**; **.667 ≤ α < .80 tentative conclusions only**;
α < .667 unreliable. Report α **with a 95% CI**, never the bare point estimate.

## LLM-assisted coding (supported, never free)

Treat an LLM as another coder: human↔LLM **double-coding**, compute Krippendorff's α between each
LLM and a **human gold standard**, and use the CI to judge whether the LLM is statistically
indistinguishable from human coders. Disclose the model, the prompt, and the agreement — never
present LLM coding as uncontrolled or cost-free.

## Reporting checklist (put in every ICR report)

```
BRANCH:        content-analytic (coefficient) | reflexive TA (consensus+reflexivity)
ICR MEASURE:   Krippendorff alpha (level) | Cohen/Fleiss kappa — and why
CODERS:        number of coders; human / LLM
DOUBLE-CODED:  % of the data double-coded
ALPHA:         point estimate + 95% CI + threshold verdict (.80 / .667)
RESOLUTION:    how disagreements were resolved (adjudication / consensus)
```

## References

- `references/icr_and_reporting.md` — coefficient math, verified APIs, LLM-benchmarking, the reporting standard.
- `references/reflexive_vs_codebook.md` — when a statistic applies vs. when it does not.
- `scripts/icr.py` — stdlib nominal Krippendorff's α + bootstrap CI + Cohen's κ (no numpy / no deps).

Part of the AlterLab Academic Skills suite.
