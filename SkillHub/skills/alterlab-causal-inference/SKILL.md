---
name: alterlab-causal-inference
description: "Estimates causal effects from observational and quasi-experimental data — difference-in-differences, instrumental variables, regression discontinuity, panel fixed effects, propensity-score / doubly-robust methods, and heterogeneous treatment effects (CATE) — using the verified Python stack: statsmodels and linearmodels (PanelOLS, IV2SLS), pyfixest (feols, event studies, Sun-Abraham, did2s), DoWhy (identify -> estimate -> refute), EconML (LinearDML, CausalForestDML, DRLearner), and rdrobust for RD. It names the identifying assumption before estimating and runs a refutation/robustness check after. Use when the request mentions difference-in-differences, instrumental variables, regression discontinuity, fixed effects / panel causal estimation, propensity scores, or treatment-effect estimation from non-randomized data. For choosing the design first prefer alterlab-ssci-design-gate; for plain regression or descriptive stats prefer alterlab-statistical-analysis. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires (declare in-session, no runtime install on Anthropic API): statsmodels, linearmodels>=6, pyfixest>=0.25, dowhy>=0.12, econml>=0.15, rdrobust>=1.3 (pip). Runs locally via `uv run python`; no API key."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-ssci-design-gate (design + assumption), alterlab-statsmodels, alterlab-statistical-analysis; audited by alterlab-ssci-inference-gate"
---

# Causal Inference — Name the Assumption, Estimate, Then Try to Break It

**Skill type: ANALYSIS MODULE.** Estimates a causal effect from data that was not fully
randomized. The discipline is not the estimator — it is the **identifying assumption** the
estimator relies on, stated before the fit and stress-tested after. If the design is not yet
fixed, that belongs upstream in `alterlab-ssci-design-gate`.

## Core Mission

```
EVERY CAUSAL ESTIMATE INHERITS AN ASSUMPTION. STATE IT, ESTIMATE UNDER IT, THEN REFUTE IT.
```

## When to Use This Skill

- "Estimate the effect with difference-in-differences / an event study."
- "I have an instrument for the treatment — run instrumental variables / 2SLS."
- "There's a cutoff score — run a regression discontinuity."
- "Panel data with unit and time fixed effects — estimate the treatment effect."
- "Give me the heterogeneous treatment effect / CATE across subgroups."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Choosing the design & its identifying assumption | `alterlab-ssci-design-gate` | Design routing precedes estimation. |
| Plain OLS / descriptive or inferential stats (no causal identification) | `alterlab-statistical-analysis` / `alterlab-statsmodels` | No treatment-effect identification problem. |
| Latent-variable / SEM / factor structure | `alterlab-sem-psychometrics` | Measurement model, not treatment effect. |
| Auditing whether the final claim is licensed | `alterlab-ssci-inference-gate` | Claim audit, downstream. |

## Estimator map (verified libraries, pinned)

| Design | Identifying assumption | Estimator (verified API) |
|--------|------------------------|--------------------------|
| **DiD / event study** | parallel trends | `pyfixest` (v0.60): `pf.feols("y ~ i(time, treat, ref) | unit + time", df)`, `pf.event_study(...)`, `pf.did2s(...)`; or `statsmodels` `smf.ols("y ~ treat*post").fit(cov_type='cluster', cov_kwds={'groups': df.unit})`. Staggered adoption → Sun-Abraham `sunab()` or `did2s`. |
| **Panel fixed effects** | no time-varying confounders | `linearmodels` (v7): `PanelOLS.from_formula("y ~ 1 + x + EntityEffects + TimeEffects", panel).fit(cov_type='clustered', cluster_entity=True)`. |
| **Instrumental variables** | exclusion restriction + relevance | `linearmodels` `IV2SLS.from_formula("y ~ 1 + exog + [treat ~ z1 + z2]", df).fit()`; check first-stage F (weak instrument). |
| **Regression discontinuity** | continuity at the cutoff (no sorting) | `rdrobust` (v2): `rdrobust(y, x, c=cutoff)`, `rdbwselect`, `rdplot`; McCrary/density check for manipulation. |
| **Selection-on-observables** | conditional ignorability | `DoWhy` (v0.14): `CausalModel(df, treatment, outcome, graph).identify_effect()` → `estimate_effect(method_name="backdoor.propensity_score_matching")` → `refute_estimate(..., method_name="random_common_cause")`. |
| **Heterogeneous effects (CATE)** | (as above) + overlap | `EconML` (v0.16): `LinearDML()` / `CausalForestDML()` `.fit(Y, T, X=X, W=W)` then `.effect(X)`. |

A stdlib router that maps the design to the estimator + its assumption + the verified call:
`scripts/estimator_router.py`. Fuller worked patterns and diagnostics:
`references/estimators.md`.

## The mandatory two steps around every estimate

1. **Before**: write the identifying assumption in one sentence and how you will defend it
   (pre-trend plot for DiD, first-stage F and an exclusion argument for IV, density/McCrary test
   for RDD, overlap/common-support for PSM). No assumption, no causal estimate.
2. **After**: run a refutation/robustness check — `DoWhy.refute_estimate` (random common cause,
   placebo treatment, data subset), a pre-trend/event-study plot, a bandwidth-sensitivity for RDD,
   or an E-value / sensitivity analysis for unmeasured confounding. Report it next to the estimate.

## Output Template

```
DESIGN + ASSUMPTION: <e.g. DiD; parallel trends, defended by the pre-2019 event-study plot>
ESTIMATOR:           <library.call(...), pinned version>
ESTIMATE:            <point estimate, 95% CI, clustered SE — never a bare p-value>
DIAGNOSTIC:          <first-stage F / density test / pre-trends / overlap>
REFUTATION:          <placebo / random-common-cause / bandwidth sensitivity result>
CLAIM SCOPE:         causal IFF the assumption + diagnostics hold; else associational
```

## Quality Standards

- Report effect sizes with confidence intervals and the SE structure (clustered where relevant).
- Never present a causal estimate without its diagnostic and at least one refutation.
- Hand the final estimate + assumption to `alterlab-ssci-inference-gate` for the claim audit.
- No fabricated flags: every call above is verified against the library's current docs; if a
  flag is unverified in your installed version, check `--help`/docs, do not guess.

## References

- `references/estimators.md` — per-design worked calls, diagnostics, and refutation menu.
- `scripts/estimator_router.py` — stdlib design→estimator+assumption router.

Part of the AlterLab Academic Skills suite.
