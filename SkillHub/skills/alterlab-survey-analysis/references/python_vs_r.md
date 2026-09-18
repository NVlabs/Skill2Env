# Python vs R for Complex-Survey Analysis

Loaded on demand from the survey-analysis SKILL.md. Verified 2026 against PyPI/CRAN. **The R
`survey` + `srvyr` stack is the field standard and the most complete**; the Python path is viable
but younger. Since this repo already shells to R (QCA), the R path is fully legitimate here.

## Python

### samplics (stable — use this as the Python default)
- PyPI `samplics>=0.6`. Import: `from samplics.estimation import TaylorEstimator`;
  `from samplics.utils.types import PopParam`.
- `TaylorEstimator(PopParam.mean)` (also `.total`, `.proportion`, `.ratio`); `.estimate(y=,
  samp_weight=, stratum=, psu=, ssu=, fpc=, domain=, deff=True, remove_nan=True)`.
- Also provides sample selection, weighting/adjustment, and calibration modules.
- **Caveat**: confirm the replicate-weight estimator class name/signature against the installed
  version before relying on it (the Taylor path is the well-documented one). Mark `TODO(verify)` if
  unsure rather than guessing.

### svy (samplics' successor — forward-looking)
- PyPI `svy>=0.18` by the same author; `samplics` is now archived in its favor. API:
  `svy.Design(stratum=, psu=, wgt=, rep_weights=)`, `svy.Sample(data=, design=)`,
  `sample.estimation.mean(y=)/.total()/.proportion()/.ratio()/.median()`, `sample.glm.fit()`.
- **Caveat**: the package README still warns examples "cannot yet be run" even though PyPI has real
  artifacts — treat the API as unstable, pin the version, and re-verify against the installed
  package before shipping analysis on it. Prefer samplics or R until it stabilizes.

## R (field standard — fully verified)

### survey (Lumley) — `survey>=4.5`, `library(survey)`
```r
des <- svydesign(ids = ~psu, strata = ~strata, weights = ~wt, fpc = ~fpc, data = dat, nest = TRUE)
svymean(~y, des, deff = TRUE); svytotal(~y, des); svyquantile(~y, des, quantiles = 0.5)
svyciprop(~I(y == 1), des, method = "logit")           # proportion CI on the right scale
svyby(~y, ~group, des, svymean)                          # domain estimation
svyglm(y ~ x1 + x2, design = des, family = quasibinomial())   # design-adjusted logistic
```
Replicate designs: `svrepdesign(weights=, repweights=, type="BRR"|"JKn"|"bootstrap", data=)` or
`as.svrepdesign(des, type=...)`.
Calibration: `postStratify(des, ~cell, pop.cell)`, `rake(des, sample.margins, population.margins)`,
`calibrate(des, formula, population)`.

### srvyr — `srvyr>=1.3`, `library(srvyr)` (dplyr-style wrapper over survey)
```r
dat %>% as_survey_design(ids = psu, strata = strata, weights = wt, fpc = fpc, nest = TRUE) %>%
  group_by(group) %>%
  summarise(p = survey_mean(y, vartype = c("se", "ci"), deff = TRUE))
```

### Bayesian: csSampling + brms
`cs_sampling()` (GitHub `RyanHornby/csSampling`) wraps a `brms` model with a `survey` design and a
sandwich covariance correction. Install via `remotes::install_github` (not on CRAN).

## Choosing a path

| Situation | Use |
|-----------|-----|
| Provider ships replicate weights; complex calibration; the authoritative answer | R `survey`/`srvyr` |
| Pure-Python pipeline, Taylor SEs, straightforward design | `samplics` |
| Bayesian design-based model | R `csSampling` + `brms` |
| Bleeding edge / future-proofing | `svy` (pin + re-verify) |
