---
name: alterlab-survey-analysis
description: "Analyzes complex-sample survey data with design-based inference — declares a survey design (weights, strata, PSUs/clusters, FPC) before estimating means, totals, proportions, ratios, and quantiles, computes design-adjusted standard errors via Taylor linearization or replicate weights (BRR, Jackknife, Bootstrap), calibrates with post-stratification / raking / GREG, and fits design-adjusted GLMs (linear, logistic, Poisson). Uses samplics (stable Python), the emerging svy successor, or the field-standard R survey + srvyr via Rscript. Use when analyzing GSS/ANES/ESS/DHS/Eurobarometer or any weighted/stratified/clustered survey, when a dataset ships survey weights, or when someone quotes unweighted percentages from a complex survey. For questionnaire and sampling-plan DESIGN prefer alterlab-survey-design; for the sampling-adequacy gate prefer alterlab-ssci-sampling-gate; for causal identification prefer alterlab-causal-inference. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires (declare in-session, no runtime install on Anthropic API): Python samplics>=0.6 (stable; TaylorEstimator) — or svy>=0.18 (samplics' successor; API still maturing, pin + re-verify) — OR the field-standard R survey>=4.5 + srvyr>=1.3 via Rscript (csSampling+brms for Bayesian design-based models). Runs locally via `uv run python` / `Rscript`; no API key."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-survey-design (item/sample design), alterlab-ssci-sampling-gate (frame/size gate), alterlab-statistical-analysis; audited by alterlab-ssci-inference-gate"
---

# Survey Analysis — Declare the Design Before You Estimate Anything

**Skill type: ANALYSIS MODULE.** Complex-sample surveys (GSS, ANES, ESS, DHS, Eurobarometer) are
drawn with stratification, clustering, and unequal probabilities. Analyzing them as if they were a
simple random sample **underestimates standard errors** and yields falsely narrow CIs and wrong
tests. The discipline is design-based inference: a declared design object comes first, every
estimate flows through it.

## Core Mission

```
YOU MUST WEIGHT (AND DECLARE STRATA + PSUs) BEFORE QUOTING ANY NUMBER FROM A COMPLEX SURVEY.
```

## When to Use This Skill

- "Give me the weighted % who [X] from ANES/GSS/DHS, with correct standard errors."
- "Why are my survey confidence intervals so narrow?" (← design ignored)
- "Post-stratify / rake my sample to census margins."
- "Fit a logistic regression on this weighted, clustered survey."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Writing questionnaire items / choosing a sampling frame | `alterlab-survey-design` | Instrument & sampling *design*, not weighted analysis. |
| Whether the sample size / frame is adequate | `alterlab-ssci-sampling-gate` | Sampling-adequacy gate, upstream. |
| Causal identification (DiD/IV/RDD) | `alterlab-causal-inference` | Design-based *survey* SEs ≠ causal identification. |
| Plain unweighted descriptive/inferential stats | `alterlab-statistical-analysis` | No survey design to honor. |

## The design-object-first rule

Declare **weights + strata + PSU/cluster + FPC** before any estimate:

- **weights** — the inverse-inclusion-probability weight; scales the sample to the population.
- **strata** — variances are computed *within* each stratum and pooled. Dropping strata leaves
  point estimates unchanged but **inflates** SEs (you lose the variance reduction).
- **PSU / cluster** — the **unit of randomization**. If whole districts were sampled, the district
  is the PSU; lower units are **not** independent. Declaring the PSU is what corrects the SE upward
  for the clustering.
- **FPC** — finite-population correction when the sampling fraction is non-trivial.

**Domain (subpopulation) estimation:** subset the **design object**, never filter the data frame
first — filtering discards the strata/PSU structure needed for correct domain SEs.

## Weight-type discipline

Distinguish **design weights** (selection probability only) from **post-stratification / calibration
weights** (also correct for sampling error and non-response). One or the other must always be used;
report which. "Weight before quoting any percentage."

## Variance estimation — support both families

- **Taylor linearization** — the default analytic method.
- **Replicate weights** — BRR, Jackknife (JKn), Bootstrap. Use these when the data provider *ships*
  replicate weights (many public files do); do not re-derive a design they already replicated.

## Verified calls (pinned)

**Python — samplics (stable):**
```python
from samplics.estimation import TaylorEstimator
from samplics.utils.types import PopParam
est = TaylorEstimator(PopParam.mean)
est.estimate(y=df["trust"], samp_weight=df["wt"], stratum=df["strata"], psu=df["psu"],
             fpc=df.get("fpc", 1.0), domain=df.get("region"), deff=True, remove_nan=True)
```
`svy` (samplics' successor, `import svy`) mirrors this with `svy.Design(...)` / `svy.Sample(...)`;
its API is still maturing — pin `svy>=0.18` and re-verify against the installed package.

**R — survey / srvyr (field standard, fully verified):**
```r
library(survey)
des <- svydesign(ids = ~psu, strata = ~strata, weights = ~wt, fpc = ~fpc,
                 data = dat, nest = TRUE)
svymean(~trust, des, deff = TRUE)
svyby(~trust, ~region, des, svymean)                 # domain estimation (keeps structure)
svyglm(trust01 ~ age + educ, design = des, family = quasibinomial())
# replicate weights when provided:
rep <- svrepdesign(weights = ~wt, repweights = "wtrep[0-9]+", type = "JKn", data = dat)
# calibration:
des2 <- rake(des, sample.margins = list(~agecat, ~sex),
             population.margins = list(pop.agecat, pop.sex))
```

Full Taylor-vs-replicate math, calibration (post-stratification / raking / GREG), and the Python
caveats vs the canonical R recipes: `references/design_and_variance.md`, `references/python_vs_r.md`.

## Reporting checklist (put in every survey result)

```
DESIGN:     weights (type: design | post-strat/calibrated) + strata + PSU + FPC declared
VARIANCE:   Taylor linearization | replicate weights (BRR/JKn/Bootstrap)
N:          unweighted N  vs  weighted population estimate
DEFF:       design effect per key estimate (how much the design inflates variance)
DOMAINS:    subset of the DESIGN object, not a filtered data frame
```

## References

- `references/design_and_variance.md` — Taylor vs replicate variance, calibration math, DEFF, domain estimation.
- `references/python_vs_r.md` — samplics/svy caveats and the canonical R survey/srvyr recipes.

Part of the AlterLab Academic Skills suite.
