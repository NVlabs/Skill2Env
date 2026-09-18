---
name: alterlab-meta-analysis
description: "Runs quantitative meta-analysis — computes effect sizes (Hedges' g / standardized mean difference, log odds/risk ratios) with their variances, pools them under fixed-effect and random-effects models, quantifies heterogeneity (I-squared, tau-squared, Cochran's Q), draws forest and funnel plots, and tests publication bias (Egger's regression, trim-and-fill) — using statsmodels.stats.meta_analysis in Python or the field-standard R metafor via Rscript. It enforces PRISMA reporting and the random- vs fixed-effect decision. Use when pooling effect sizes across studies, running a systematic review's quantitative synthesis, or assessing heterogeneity and publication bias. For finding and screening the literature prefer alterlab-deep-research; for a single study's statistics prefer alterlab-statistical-analysis. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires (declare in-session, no runtime install on Anthropic API): Python statsmodels>=0.14 (statsmodels.stats.meta_analysis) — OR the field-standard R metafor>=5.0 via Rscript (escalc/rma/forest/funnel/regtest/trimfill). Note: the PyPI PythonMeta package is stale/unmaintained — prefer statsmodels or metafor. Runs locally via `uv run python` / `Rscript`; no API key."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-deep-research (literature search/screening), alterlab-statistical-analysis; audited by alterlab-ssci-inference-gate"
---

# Meta-Analysis — Pool Honestly, Then Interrogate Heterogeneity and Bias

**Skill type: ANALYSIS MODULE.** Synthesizes effect sizes across studies. The discipline is not the
pooled point estimate — it is the **model choice** (fixed vs random effects), the **heterogeneity**
you must characterize, and the **publication-bias** diagnostics that decide whether the pooled
estimate is trustworthy at all.

## Core Mission

```
THE POOLED EFFECT IS ONLY AS GOOD AS ITS HETEROGENEITY STORY AND ITS PUBLICATION-BIAS CHECK.
```

## When to Use This Skill

- "Pool these effect sizes / run a meta-analysis across N studies."
- "Compute I² / τ² — how heterogeneous are my studies?"
- "Is there publication bias? Draw a funnel plot / run Egger's test."
- "Convert these means and SDs (or 2×2 tables) into effect sizes and combine them."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Finding / screening the literature (search, PRISMA flow) | `alterlab-deep-research` | Discovery & screening, upstream of pooling. |
| A single study's descriptive/inferential statistics | `alterlab-statistical-analysis` | One dataset, not cross-study synthesis. |
| Fitting one regression / GLM | `alterlab-statsmodels` | Not effect-size pooling. |
| Whether the review question/design is sound | `alterlab-ssci-design-gate` | Design routing. |

## Fixed-effect vs random-effects (the first decision)

- **Fixed-effect** — assumes one true effect; studies differ only by sampling error. Rarely
  defensible across heterogeneous social-science studies.
- **Random-effects** — assumes a *distribution* of true effects (between-study variance τ²); the
  default when studies vary in population, measure, or design. Report the model and why.

## Verified calls (pinned)

**Python — statsmodels:**
```python
from statsmodels.stats.meta_analysis import effectsize_smd, combine_effects
eff, var = effectsize_smd(m1, sd1, n1, m2, sd2, n2)          # Hedges' g + variance
res = combine_effects(eff, var, method_re="dl")              # DerSimonian-Laird random effects
res.summary_frame()                                          # fixed + random rows, CIs, weights
res.tau2, res.i2, res.q                                      # heterogeneity
res.plot_forest()
# binary outcomes: effectsize_2proportions(c1, n1, c2, n2, statistic="odds-ratio")  # log OR + var
```

**R — metafor (field standard):**
```r
library(metafor)
dat <- escalc(measure = "SMD", m1i=, sd1i=, n1i=, m2i=, sd2i=, n2i=, data = studies)  # or "OR"/"RR"
res <- rma(yi, vi, data = dat, method = "REML")              # random-effects
summary(res)                                                 # I2, tau2, Q
forest(res); funnel(res)
regtest(res)                                                 # Egger's test for funnel asymmetry
trimfill(res)                                                # trim-and-fill sensitivity
```

## Heterogeneity — characterize, don't hide

- **Cochran's Q** (test of homogeneity; low power with few studies),
- **I²** (% of variation due to heterogeneity, not chance),
- **τ²** (between-study variance, on the effect-size scale).
High I²/τ² means the pooled mean summarizes a *distribution* — report a prediction interval, and
explore moderators (meta-regression / subgroups) rather than over-interpreting the point estimate.

## Publication bias

- **Funnel plot** — asymmetry suggests small-study effects / missing null results.
- **Egger's regression test** (`regtest`) — a formal asymmetry test.
- **Trim-and-fill** (`trimfill`) — imputes "missing" studies as a sensitivity analysis.
No single test is definitive; report the funnel plot plus at least one test, and treat them as
sensitivity analyses, not proof.

## Reporting standard (PRISMA)

Report per PRISMA 2020: the search/screening flow (hand off discovery to `alterlab-deep-research`),
inclusion criteria, per-study effect sizes and weights, the pooling model, I²/τ²/Q, the
publication-bias diagnostics, and risk-of-bias assessment.

## References

- `references/pooling_and_bias.md` — effect-size formulas, RE estimators, heterogeneity, bias diagnostics, PRISMA.

Part of the AlterLab Academic Skills suite.
