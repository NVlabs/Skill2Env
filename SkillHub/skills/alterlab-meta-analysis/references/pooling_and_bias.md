# Pooling, Heterogeneity, and Publication Bias

Loaded on demand from the meta-analysis SKILL.md. APIs verified 2026 against statsmodels + R
metafor docs.

## Effect sizes and their variances

| Outcome | Effect size | statsmodels | metafor `escalc(measure=)` |
|---------|-------------|-------------|-----------------------------|
| Continuous, 2 groups | Hedges' g (bias-corrected SMD) | `effectsize_smd(m1,sd1,n1,m2,sd2,n2)` | `"SMD"` |
| Binary, 2 groups | log odds ratio | `effectsize_2proportions(c1,n1,c2,n2, statistic="odds-ratio")` | `"OR"` |
| Binary, 2 groups | log risk ratio | `effectsize_2proportions(..., statistic="risk-ratio")` | `"RR"` |
| Correlations | Fisher's z | (transform manually) | `"ZCOR"` |

Always pool on the analysis scale (log for OR/RR, Fisher's z for r) and back-transform for display.
Each effect size carries a variance used as the inverse-variance weight.

## Pooling models

- **Fixed-effect** (common-effect): weight = 1/vᵢ. Assumes a single true effect.
- **Random-effects**: weight = 1/(vᵢ + τ²). τ² estimated by DerSimonian-Laird (`method_re="dl"` /
  metafor `method="DL"`), REML (`"REML"`, metafor default and generally preferred), or Paule-Mandel
  (`"pm"`). Report the estimator.

The random-effects mean is an estimate of the *mean of a distribution* of effects; pair it with a
**prediction interval** (the interval a new study's true effect would fall in), which is wider than
the CI of the mean and is the honest summary under heterogeneity.

## Heterogeneity statistics

- **Q** (Cochran): Σ wᵢ(θᵢ − θ̄)²; tests homogeneity. Underpowered with few studies, over-powered
  with many — do not rely on its p-value alone.
- **I²** = max(0, (Q − df)/Q): the % of total variation attributable to heterogeneity. Rough bands:
  ~25% low, ~50% moderate, ~75% high (context-dependent, not thresholds).
- **τ²**: absolute between-study variance on the effect scale — the input to the prediction interval.

High heterogeneity is a finding, not a nuisance: investigate with **meta-regression** (`rma(yi, vi,
mods = ~moderator)`) or subgroup analysis before interpreting the pooled mean.

## Publication-bias diagnostics

- **Funnel plot**: effect size vs precision (1/SE). Symmetric ≈ no small-study effect; asymmetry
  suggests missing small null/negative studies.
- **Egger's regression** (`regtest(res)`): regress the standardized effect on precision; a non-zero
  intercept flags asymmetry.
- **Trim-and-fill** (`trimfill`): imputes studies to restore symmetry and re-pools — a *sensitivity*
  analysis, not a correction to report as the primary estimate.
- Alternatives: PET-PEESE, selection models, p-curve. All are diagnostics; none proves bias is
  absent (few studies → low power to detect asymmetry).

## PRISMA 2020 reporting

A meta-analysis is the quantitative core of a systematic review. Report: the search and screening
flow (PRISMA flow diagram — hand discovery to `alterlab-deep-research`), eligibility criteria,
extracted effect sizes and study characteristics, the synthesis model, heterogeneity (I²/τ²/Q),
publication-bias diagnostics, and per-study risk-of-bias (e.g. RoB 2 / ROBINS-I).

## References

- Borenstein, Hedges, Higgins & Rothstein (2009). *Introduction to Meta-Analysis.*
- Viechtbauer, W. (2010). Conducting meta-analyses in R with the metafor package.
- Cochrane Handbook, ch. 10 (heterogeneity, bias).
- Page et al. (2021). PRISMA 2020 statement.
