# Multilevel Model Reporting — The Standard, in Detail

Loaded on demand from the multilevel-models SKILL.md. APIs verified 2026. The reporting items below
are those a 400-article review (Meteyard & Davies, 2020) and follow-ups found persistently
under-reported; enforcing them is the skill's value-add.

## Full model specification

Report both parts explicitly:
- **Fixed effects** — every predictor and interaction.
- **Random effects** — which intercepts and *slopes* vary by which grouping factor, and their
  correlation. `y ~ x + (1 + x | group)` = random intercept + random slope of x across groups,
  correlated. `(1 | group) + (0 + x | group)` = uncorrelated. `(1 | g1) + (1 | g2)` = crossed random
  effects. Do not report only "a mixed model was fit."

## Centering (a real decision, often omitted)

- **Grand-mean centering** — changes the intercept's meaning; leaves slopes/variances essentially
  unchanged; aids interpretation.
- **Group-mean (within-cluster) centering** — separates within-cluster from between-cluster effects
  (the "contextual"/Mundlak distinction). Choose deliberately when level-1 and level-2 effects
  differ; report the choice and why.

## Estimation: ML vs REML

- **REML** — less biased variance-component estimates; use for the *final* model and for comparing
  models that differ only in random effects.
- **ML** — required to compare models differing in **fixed** effects (likelihood-ratio test).
Report which you used. lme4 defaults to REML for `lmer`.

## ICC and R²

Variance-partition **ICC** = between-cluster variance / total variance = τ₀₀ / (τ₀₀ + σ²) for a
random-intercept model. In R: `performance::icc(m)` (adjusted = random effects only; conditional =
incl. fixed). In Python, statsmodels gives no ICC helper — compute from `res.cov_re` (τ) and
`res.scale` (σ²): `icc = cov_re.iloc[0,0] / (cov_re.iloc[0,0] + res.scale)`. Do **not** use
`pingouin.intraclass_corr` for this — that is a rater-reliability ICC, a different quantity.

**Effect size / R²**: Nakagawa's marginal R² (fixed effects) and conditional R² (fixed + random) —
`performance::r2(m)`. Report standardized fixed effects too.

## Assumptions and diagnostics

- Normality of level-1 residuals and of random effects.
- Homoscedasticity across clusters; linearity.
- Influential clusters (a school with 3 pupils can swing a variance component).
- **Convergence & singularity**: report warnings. A `boundary (singular) fit` means a variance
  component is estimated at zero — simplify the random structure rather than ignore it.

## Model comparison

Nested models: likelihood-ratio test (ML-fitted) for fixed effects; AIC/BIC for non-nested. Build
up from an intercept-only (null) model — its ICC tells you whether multilevel structure is even
warranted (ICC ≈ 0 → clustering may be a nuisance, not a question; consider cluster-robust SEs).

## Power

LMM power is not a closed form — use **Monte Carlo simulation** (e.g. R `simr`) over the fixed
effect of interest, given the variance components. Report the assumed effect and variance structure.

## Structure vs question (restate)

A multilevel data structure alone does not mandate a mixed model. If the question is at one level
and clustering is a nuisance, cluster-robust/sandwich SEs are simpler and sufficient. Use a mixed
model when between-cluster variation or a random-slope (effect-varies-by-group) question is
substantive.

## References

- Meteyard, L., & Davies, R. A. I. (2020). Best practice guidance for linear mixed-effects models. *J. Memory & Language.*
- Nakagawa, S., & Schielzeth, H. (2013). A general and simple method for obtaining R² from GLMMs.
- Barr, D. J., et al. (2013). Random effects structure for confirmatory hypothesis testing: keep it maximal.
- Bates, D., et al. (2015). Fitting linear mixed-effects models using lme4.
