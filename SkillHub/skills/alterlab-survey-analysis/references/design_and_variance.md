# Design-Based Variance and Calibration

Loaded on demand from the survey-analysis SKILL.md. Verified against the R `survey` (Lumley) and
`samplics` docs.

## Why ignoring the design biases inference

Design-based inference accounts for how the sample was drawn — stratification, clustering, unequal
probabilities — when computing standard errors. Ignoring the design typically **underestimates**
SEs, producing falsely narrow CIs and anti-conservative tests. The three design features act as:

- **Stratification** reduces variance (estimates pooled within strata) → ignoring strata *inflates*
  the reported SE relative to the correct design-based SE, but more importantly you cannot claim the
  precision the stratified design bought.
- **Clustering** increases variance (units within a PSU are correlated) → ignoring the PSU
  *understates* the SE. This is the dangerous direction and the common error.
- **Unequal weights** change point estimates *and* variance.

The net effect is summarized by the **design effect** (DEFF = design-based variance ÷ SRS variance).
Report DEFF per key estimate; DEFF > 1 means clustering/weighting dominates the (variance-reducing)
stratification.

## Taylor linearization vs replicate weights

- **Taylor (linearization)** — approximates the variance of a nonlinear statistic (ratio, mean of a
  weighted total) by a first-order Taylor expansion, using the stratum/PSU structure. The analytic
  default; needs the design variables (strata, PSU).
- **Replicate weights** — the provider ships K sets of weights; the estimator is recomputed on each
  replicate and the spread gives the variance. Families:
  - **BRR** (Balanced Repeated Replication) — for two-PSU-per-stratum designs.
  - **Jackknife (JK1 / JKn)** — delete-one(-cluster) reweighting.
  - **Bootstrap** — resample PSUs within strata.
  Use replicate weights when provided (they encode the provider's exact design, including
  confidentiality perturbations); otherwise use Taylor with the design variables.

## Calibration (weight adjustment to known totals)

- **Post-stratification** — scale weights so sample cell counts match known population cell counts
  for a single cross-classification.
- **Raking (iterative proportional fitting)** — match several marginal distributions simultaneously
  when the full cross-classification is unknown. R: `rake(design, sample.margins, population.margins)`.
- **GREG (generalized regression)** — calibrate to auxiliary totals via a regression model. R:
  `calibrate(design, formula, population)`.

Calibration reduces variance and corrects non-response/coverage bias when the auxiliary variables
predict both response and the outcome.

## Domain (subpopulation) estimation — do it right

To estimate within a subgroup, **subset the design object** (`subset(design, region=="north")` in R;
the `domain=` argument in samplics), never `df[df.region=="north"]`. Filtering the data frame
discards the strata/PSU membership of the excluded units, so the domain variance is computed as if
the subgroup were its own SRS — wrong. `subset.survey.design` deliberately retains the original
count of clusters and strata so the domain SE is correct.

## Bayesian design-based models

`csSampling` (R, GitHub) bridges a `brms`/`rstan` weighted model with a `survey` design object and
applies a design-effect (sandwich) covariance correction, so posterior uncertainty reflects the
sampling design rather than treating weighted observations as iid.

## References

- Lumley, T. (2010). *Complex Surveys: A Guide to Analysis Using R.*
- Heeringa, West & Berglund (2017). *Applied Survey Data Analysis.*
- Valliant, Dever & Kreuter (2018). *Practical Tools for Designing and Weighting Survey Samples.*
