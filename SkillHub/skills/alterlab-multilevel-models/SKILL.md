---
name: alterlab-multilevel-models
description: "Fits and reports mixed-effects / multilevel / hierarchical models for clustered, nested, longitudinal, and repeated-measures data — random intercepts and slopes, variance components and the ICC, cross-level interactions, and GLMMs (logistic/Poisson) — using statsmodels MixedLM and bambi (Bayesian on PyMC) in Python, or the field-standard R lme4 / glmmTMB / brms via Rscript. It enforces the reporting items reviews find under-reported: full fixed + random specification, centering, variance components + ICC, estimation method, assumption checks, model comparisons, and effect sizes. Use when data are grouped/nested (students in schools, repeated measures, panel/longitudinal) and the question concerns within- vs between-cluster variation. For general single-level regression prefer alterlab-statsmodels; for panel fixed effects used for causal identification prefer alterlab-causal-inference. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires (declare in-session, no runtime install on Anthropic API): Python statsmodels>=0.14 (MixedLM), optionally bambi>=0.18 (Bayesian, on PyMC) — OR the field-standard R lme4>=2.0 (+ lmerTest for p-values), glmmTMB, brms, and performance (icc/r2) via Rscript. Runs locally via `uv run python` / `Rscript`; no API key."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-statsmodels (single-level regression), alterlab-statistical-analysis, alterlab-causal-inference (panel FE for causal ID); audited by alterlab-ssci-inference-gate"
---

# Multilevel Models — Fit the Nesting, Report the Whole Model

**Skill type: ANALYSIS MODULE.** Correlated data (pupils in schools, repeated measures within
people, panel waves) violate independence; a mixed-effects model partitions variance into levels.
The value here is **discipline, not a `fit()` call**: methods reviews document a reporting crisis
— models specified and reported inconsistently — so this skill enforces the reporting standard.

## Core Mission

```
FITTING THE MODEL IS EASY; REPORTING IT COMPLETELY IS THE JOB.
STATE THE FULL FIXED + RANDOM STRUCTURE, THE ICC, THE ESTIMATION, THE CHECKS.
```

## When to Use This Skill

- "I have students nested in schools / repeated measures / panel data — fit a multilevel model."
- "Random intercepts and slopes for [group]; what's the ICC?"
- "Multilevel logistic / Poisson (GLMM)."
- "How much variance is between groups vs within?"

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Single-level / ordinary regression, no grouping | `alterlab-statsmodels` / `alterlab-statistical-analysis` | No random-effects structure needed. |
| Panel fixed effects for **causal** identification (DiD/within) | `alterlab-causal-inference` | FE-for-identification, not variance partitioning. |
| Latent variables / SEM / factor structure | `alterlab-sem-psychometrics` | Measurement model. |
| Whether the design/question even needs multilevel | `alterlab-ssci-design-gate` | Design routing. |

## Structure ≠ question

Having a multilevel **data structure** is not the same as having a **question** that requires
multilevel analysis. If inference is at one level and clustering is only a nuisance, cluster-robust
(sandwich) SEs may suffice; reach for a mixed model when the question concerns **between-cluster
variation** (e.g. how much of the outcome varies across schools, or whether an effect varies by
group). State which case you are in.

## Verified calls (pinned)

**Python — statsmodels MixedLM:**
```python
import statsmodels.formula.api as smf
m = smf.mixedlm("y ~ x", data, groups=data["group"], re_formula="~x")   # random intercept + slope
res = m.fit(reml=True)                    # REML for final variance estimates
res.summary(); res.cov_re                 # fixed effects + random-effect covariance
```
`vc_formula=` adds named variance components. **Bambi** (Bayesian, on PyMC): `import bambi as bmb;
bmb.Model("y ~ x + (1 + x | group)", data).fit()` — lme4-style `(1|group)` / `(x|group)` syntax.

**R — lme4 / glmmTMB / brms (field standard):**
```r
library(lme4); library(lmerTest)          # lmerTest adds Satterthwaite dof + p-values (lme4 omits them)
m <- lmer(y ~ x + (1 + x | group), data)
glmer(y01 ~ x + (1 | group), family = binomial, data = data)     # GLMM
performance::icc(m); performance::r2(m)    # variance-partition ICC + Nakagawa marginal/conditional R2
```
`glmmTMB` (zero-inflation, faster) and `brms` (Bayesian via Stan) share the `(1|group)` syntax.

Note: statsmodels has no built-in variance-partition ICC — compute it from `cov_re` and the
residual scale (see the reference). `pingouin.intraclass_corr` computes a *reliability* ICC
(Shrout & Fleiss), which is a different quantity — do not confuse them.

## The reporting checklist (the reason this skill exists)

```
SPECIFICATION:  full fixed-effects + full random-effects structure (which slopes vary by which group)
CENTERING:      predictor centering decision (grand-mean / group-mean / none) + rationale
VARIANCE:       variance components + ICC (proportion of variance between clusters)
ESTIMATION:     ML vs REML (REML for final variance estimates; ML to compare fixed effects)
ASSUMPTIONS:    residual + random-effect normality, homoscedasticity, influential clusters
COMPARISON:     nested-model comparisons (LRT / AIC / BIC), and convergence/singularity checks
EFFECT SIZE:    standardized fixed effects and/or Nakagawa marginal & conditional R2
```

These are exactly the items methods reviews find under-reported. There is no single correct LMM —
surface the modeling decisions as a justified path, don't hardcode one recipe.

## References

- `references/mlm_reporting.md` — the full reporting standard, ICC/R² computation, centering, convergence, power.

Part of the AlterLab Academic Skills suite.
