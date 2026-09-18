# Causal Estimators — Worked Calls, Diagnostics, Refutations

Loaded on demand from the causal-inference SKILL.md. Every call is verified against the library's
current docs (versions pinned in the SKILL frontmatter). No flag here is invented; if your
installed version differs, confirm against `--help`/docs rather than guessing.

## Difference-in-differences (parallel trends)

Two-period 2×2 with clustered SEs (statsmodels):

```python
import statsmodels.formula.api as smf
m = smf.ols("y ~ treat*post", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["unit"]})
```

Staggered adoption is biased under two-way fixed effects with heterogeneous effects; use a
modern estimator (pyfixest v0.60):

```python
import pyfixest as pf
# Sun & Abraham interaction-weighted event study inside a feols formula:
m = pf.feols("y ~ sunab(cohort_year, year) | unit + year", data=df)
m.iplot()                      # event-study coefficients
# or Gardner (2021) two-stage:
es = pf.did2s(df, yname="y", first_stage="~ 0 | unit + year",
              second_stage="~ i(rel_year)", treatment="treated", cluster="unit")
```

Diagnostic: inspect **pre-treatment** event-study coefficients (should be ~0). Refutation:
placebo timing; drop the largest cohort.

## Panel fixed effects (no time-varying confounders)

```python
from linearmodels.panel import PanelOLS
panel = df.set_index(["unit", "year"])
res = PanelOLS.from_formula("y ~ 1 + x + EntityEffects + TimeEffects", panel).fit(
    cov_type="clustered", cluster_entity=True)
```

Fixed effects remove *time-invariant* confounders only; a shock correlated with treatment timing
still biases. Add unit-specific trends as a robustness check.

## Instrumental variables (exclusion restriction)

```python
from linearmodels.iv import IV2SLS
res = IV2SLS.from_formula("y ~ 1 + exog + [treat ~ z1 + z2]", df).fit()
print(res.first_stage)         # first-stage F: weak-instrument diagnostic (F > ~10)
```

The exclusion restriction is a **substantive** argument, not a test — the instrument must affect
Y *only* through the treatment. Report the reduced form and defend exclusion in prose.

## Regression discontinuity (continuity at the cutoff)

```python
from rdrobust import rdrobust, rdbwselect, rdplot
out = rdrobust(y, x, c=cutoff)         # local-polynomial, robust bias-corrected CIs
rdplot(y, x, c=cutoff)                  # visualize the discontinuity
```

Diagnostic: McCrary/density test for manipulation of the running variable; covariate continuity
at the cutoff. The estimate is **local** to the cutoff — external validity is limited. Refutation:
bandwidth sensitivity, placebo cutoffs, donut RD.

## Selection-on-observables (conditional ignorability)

```python
from dowhy import CausalModel
model = CausalModel(data=df, treatment="treat", outcome="y", graph=dag_string)
est_and = model.identify_effect()
est = model.estimate_effect(est_and, method_name="backdoor.propensity_score_matching")
ref = model.refute_estimate(est_and, est, method_name="random_common_cause")
```

Conditional ignorability (no unmeasured confounding) is the strongest, least testable assumption —
say so. Diagnostic: overlap/common support and post-matching covariate balance. Refutation:
`random_common_cause`, `placebo_treatment_refuter`, `data_subset_refuter`; quantify robustness to
unmeasured confounding with an E-value.

## Heterogeneous treatment effects / CATE

```python
from econml.dml import LinearDML, CausalForestDML
est = CausalForestDML()
est.fit(Y, T, X=X, W=W)        # X = effect-modifiers, W = controls
tau = est.effect(X_test)        # CATE per unit
```

DML cross-fits nuisance models to debias (Chernozhukov et al. 2017). Requires overlap across the
covariate space. Report the average and the distribution of CATE, not a single number.

## Choosing an SE structure

- Panel/DiD: cluster on the treatment-assignment level (usually the unit), not the observation.
- Few clusters (< ~40): use wild-cluster bootstrap rather than asymptotic clustered SEs.

## References

- Angrist & Pischke (2009), *Mostly Harmless Econometrics.*
- Cunningham (2021), *Causal Inference: The Mixtape.*
- Chernozhukov et al. (2018), Double/debiased machine learning.
- Callaway & Sant'Anna (2021); Sun & Abraham (2021); Goodman-Bacon (2021) — staggered DiD.
- Calonico, Cattaneo & Titiunik (2014) — robust RD inference (`rdrobust`).
