---
name: alterlab-missing-data
description: "Handles missing data with principled methods — forces an explicit MCAR / MAR / MNAR mechanism statement, then applies multiple imputation by chained equations (MICE) with Rubin's-rules pooling of estimates and standard errors, or full-information maximum likelihood (FIML) where a likelihood/SEM model applies. Uses statsmodels MICE / MICEData in Python or the field-standard R mice via Rscript, and warns that single (mean/regression) imputation and scikit-learn's IterativeImputer return one completed dataset without Rubin's-rules pooling, so they understate standard errors if used as multiple imputation. Use when a dataset has missing values, when choosing an imputation strategy, or when reporting how missingness was handled. For general modeling on complete data prefer alterlab-statistical-analysis; for latent-variable models with FIML prefer alterlab-sem-psychometrics. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires (declare in-session, no runtime install on Anthropic API): Python statsmodels>=0.14 (statsmodels.imputation.mice), pandas; scikit-learn IterativeImputer only for single imputation (NOT Rubin pooling) — OR the field-standard R mice>=3.19 via Rscript (mice/with/pool). Runs locally via `uv run python` / `Rscript`; no API key."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-statistical-analysis (complete-data modeling), alterlab-sem-psychometrics (FIML for latent models); audited by alterlab-ssci-inference-gate"
---

# Missing Data — Name the Mechanism, Impute Multiply, Pool by Rubin's Rules

**Skill type: ANALYSIS MODULE.** Missing data is not a nuisance to delete or fill with a mean.
The discipline: state the **missingness mechanism**, then use a method whose uncertainty is honest —
multiple imputation with **Rubin's-rules pooling**, or FIML. The dangerous shortcut is single
imputation, which treats guessed values as observed and understates standard errors.

## Core Mission

```
STATE THE MECHANISM (MCAR / MAR / MNAR). MULTIPLY IMPUTE AND POOL BY RUBIN'S RULES —
SINGLE IMPUTATION FAKES CERTAINTY IT DOESN'T HAVE.
```

## When to Use This Skill

- "My dataset has missing values — how should I handle them?"
- "Should I use multiple imputation? How many imputations?"
- "How do I pool results across imputed datasets?"
- "Is mean imputation / listwise deletion okay here?"

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Modeling on already-complete data | `alterlab-statistical-analysis` / `alterlab-statsmodels` | No missingness to handle. |
| FIML inside an SEM / latent-variable model | `alterlab-sem-psychometrics` | That skill fits the latent model with FIML. |
| Survey weights / design (a different kind of "adjustment") | `alterlab-survey-analysis` | Design-based inference, not imputation. |
| Whether the study design is sound | `alterlab-ssci-design-gate` | Design routing. |

## Step 1 — state the mechanism (Rubin)

| Mechanism | Meaning | Consequence |
|-----------|---------|-------------|
| **MCAR** | missingness independent of everything | listwise deletion is unbiased (but wasteful) |
| **MAR** | missingness depends on *observed* data | MI / FIML are valid (the workhorse assumption) |
| **MNAR** | missingness depends on the *unobserved* value itself | needs a selection / pattern-mixture model + sensitivity analysis |

The mechanism is an **assumption**, largely untestable (MAR vs MNAR especially) — state it and
justify it; inspect the missingness pattern (`mice::md.pattern`) and test MCAR (Little's test) as
supporting evidence, not proof.

## Step 2 — multiple imputation with Rubin's-rules pooling

Create m completed datasets (each imputes with added noise reflecting uncertainty), analyze each,
then **pool**: the point estimate is the mean across imputations; the SE combines *within*-imputation
and *between*-imputation variance (Rubin's rules), so it honestly reflects imputation uncertainty.

**Python — statsmodels MICE:**
```python
from statsmodels.imputation import mice
imp = mice.MICEData(df)                                  # chained-equations imputer over the frame
fit = mice.MICE("y ~ x1 + x2", sm.OLS, imp).fit(n_burnin=10, n_imputations=20)
fit.summary()                                            # pooled estimates + SEs (Rubin's rules)
```

**R — mice (field standard):**
```r
library(mice)
md.pattern(data)                                         # inspect the missingness pattern
imp  <- mice(data, m = 20, method = "pmm")               # m completed datasets
fit  <- with(imp, lm(y ~ x1 + x2))
summary(pool(fit))                                       # Rubin's-rules pooling (fmi, lambda, df)
```

**FIML** — for likelihood/SEM models under MAR, full-information ML uses all available data without
explicit imputation; route to `alterlab-sem-psychometrics` when the model is latent-variable.

## The single-imputation trap (verified caveat)

- **Mean / regression / single imputation** treats imputed values as if observed → **biased,
  understated SEs**. Not acceptable as a final analysis.
- **scikit-learn `IterativeImputer`** returns a **single** completed dataset and does **not** pool by
  Rubin's rules — the sklearn docs say so explicitly. It is fine for a prediction pipeline, but using
  it as "multiple imputation" for inference understates uncertainty. If you must, run it repeatedly
  with `sample_posterior=True` and different seeds and pool manually — but `mice`/statsmodels MICE do
  this correctly out of the box.

## How many imputations (m)

Rule of thumb: m at least the **percentage of incomplete cases** (higher fraction of missing
information → larger m); modern guidance often uses m ≈ 20–50. Report m and the fraction of missing
information (FMI).

## Reporting checklist

```
MECHANISM:   MCAR / MAR / MNAR — stated and justified; pattern inspected (md.pattern)
METHOD:      MICE (m, imputation model) with Rubin's-rules pooling | FIML | (deletion only if MCAR)
POOLING:     estimates + SEs pooled by Rubin's rules; report FMI
SENSITIVITY: for MNAR, a sensitivity analysis (selection / pattern-mixture)
```

## References

- `references/mechanisms_and_pooling.md` — MCAR/MAR/MNAR detail, Rubin's-rules math, FIML vs MI, m guidance, the sklearn caveat.

Part of the AlterLab Academic Skills suite.
