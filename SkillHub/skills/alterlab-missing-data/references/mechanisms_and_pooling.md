# Missingness Mechanisms and Rubin's-Rules Pooling

Loaded on demand from the missing-data SKILL.md. APIs verified 2026 against statsmodels, scikit-learn,
and R mice docs.

## The mechanisms (Rubin's taxonomy)

- **MCAR** (missing completely at random): P(missing) does not depend on observed or unobserved
  data. Listwise deletion is unbiased (just inefficient). Testable-ish via **Little's MCAR test**.
- **MAR** (missing at random): P(missing) depends only on **observed** variables. This is the
  assumption under which MICE and FIML are valid. It is **not** directly testable against MNAR.
- **MNAR** (missing not at random): P(missing) depends on the **unobserved** value itself (e.g. high
  earners omit income). Requires a **selection model** or **pattern-mixture model**, plus a
  sensitivity analysis over the untestable assumption.

Inspect the pattern first: `mice::md.pattern(data)` (R) or a missingness heatmap. State the assumed
mechanism explicitly — it is the load-bearing assumption of everything downstream.

## Why single imputation is wrong

Filling each hole with one value (the mean, or one regression prediction) and then analyzing the
"completed" data treats imputed values as if they were observed. The analysis therefore acts as if
the sample were larger and more certain than it is → **standard errors are too small, CIs too
narrow, tests anti-conservative**. This includes mean imputation, LOCF, and a single regression
imputation.

## Multiple imputation + Rubin's rules

1. **Impute** m times, each draw adding noise that reflects both the residual and the parameter
   uncertainty (so the m datasets differ).
2. **Analyze** each completed dataset with the intended model → m sets of estimates and SEs.
3. **Pool** (Rubin 1987):
   - Pooled estimate: Q̄ = (1/m) Σ Q̂ⱼ.
   - Within-imputation variance: Ū = (1/m) Σ Uⱼ.
   - Between-imputation variance: B = (1/(m−1)) Σ (Q̂ⱼ − Q̄)².
   - Total variance: T = Ū + (1 + 1/m) B → SE = √T.
   - Degrees of freedom via Barnard-Rubin; **FMI** = fraction of missing information ≈ (1+1/m)B / T.

R `mice`: `pool(with(imp, lm(...)))` does this and reports fmi/lambda/df. statsmodels `MICE(...).fit()`
pools internally.

## The scikit-learn caveat (verified)

`from sklearn.experimental import enable_iterative_imputer` then `from sklearn.impute import
IterativeImputer`. The docs state IterativeImputer "differs from [R MICE] by returning a **single
imputation instead of multiple imputations**." It does not implement Rubin's-rules pooling, so used
naively as MI it understates SEs. It is appropriate inside a **prediction** pipeline (where you want
one completed matrix), not for **inferential** SEs. To approximate MI you must loop it with
`sample_posterior=True` and distinct seeds and pool manually — but `mice`/statsmodels MICE are the
correct tools for inference.

## FIML

Full-information maximum likelihood uses all observed data directly in the likelihood (no explicit
imputation), valid under MAR, and is the natural choice inside SEM/latent-variable models. Route to
`alterlab-sem-psychometrics` when the model is latent. FIML and MI give similar results under MAR;
FIML is model-specific, MI is model-agnostic (impute once, analyze many ways).

## How many imputations (m)

- Old rule: m = 3–5 suffices for point estimates.
- Modern guidance: m ≥ the **percentage of incomplete cases** (White, Royston & Wood 2011); van Buuren
  suggests m ≈ 50 for stable SE/FMI estimates. Larger m costs little compute and stabilizes inference.
Report m and the FMI.

## References

- Rubin, D. B. (1987). *Multiple Imputation for Nonresponse in Surveys.*
- van Buuren, S. (2018). *Flexible Imputation of Missing Data* (2nd ed.) — the `mice` reference.
- White, Royston & Wood (2011). Multiple imputation using chained equations.
- Enders, C. K. (2010). *Applied Missing Data Analysis* (FIML vs MI).
