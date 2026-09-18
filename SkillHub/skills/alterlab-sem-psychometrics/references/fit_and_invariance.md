# Fit, Reliability, and Invariance — Full Reference

Loaded on demand from the sem-psychometrics SKILL.md. Verified against semopy / factor_analyzer /
pingouin current docs (versions pinned in the SKILL frontmatter).

## Omega vs alpha (why the bundled script exists)

Cronbach's alpha assumes tau-equivalence (equal loadings) and is a lower bound. McDonald's omega
uses the actual standardized loadings and is the honest congeneric-model reliability. Neither
semopy nor pingouin returns omega directly (pingouin exposes only `cronbach_alpha`; semopy's
`calc_stats` returns fit indices, not reliability), so compute it from the standardized loadings
you get from `Model.inspect(std_est=True)`:

```
omega_total = (Σ λ_i)² / [ (Σ λ_i)² + Σ (1 − λ_i²) ]
```

`scripts/omega.py` does this and also reports coefficient H (maximal reliability). Report alpha and
omega together; the gap is usually small for well-constructed unidimensional scales but you should
show it rather than assume it.

## Fit indices (semopy `calc_stats`)

`calc_stats(model)` returns a DataFrame including `chi2`, `chi2 p-value`, `CFI`, `TLI`, `RMSEA`,
`AIC`, `BIC`, `LogLik` (and GFI/AGFI/NFI). It does **not** return SRMR — compute SRMR separately
(from the residual correlation matrix) if a reviewer requires it.

Hu & Bentler (1999) guideline cutoffs, used as a two-index combination, not hard gates:

| Index | Good fit | Note |
|-------|----------|------|
| CFI, TLI | ≥ .95 | incremental fit vs the null model |
| RMSEA | ≤ .06 | report its 90% CI; ≤ .08 is "acceptable" |
| SRMR | ≤ .08 | standardized residual; compute separately |
| χ² / df | small, but χ² is sample-size sensitive | never decisive on its own |

## semopy objective functions

`Model.fit(data, obj=...)`: `MLW` (default maximum likelihood Wishart), `FIML` for missing data,
`ULS`/`GLS`/`WLS`/`DWLS` for non-normal/ordinal indicators (DWLS with a polychoric matrix is the
usual choice for ordinal Likert items).

## EFA workflow (factor_analyzer)

1. Adequacy: `calculate_kmo(X)` (overall KMO > .60) and `calculate_bartlett_sphericity(X)` (p < .05).
2. Retention: parallel analysis or scree; eigenvalues > 1 is a weak default.
3. Rotation: `promax` (oblique — factors correlated) or `varimax` (orthogonal).
4. `FactorAnalyzer(n_factors=k, rotation="promax").fit(X)`; inspect `.loadings_` and
   `.get_factor_variance()`.

Then confirm the structure on fresh data with a CFA (semopy) — do not report EFA on the same
sample as if it were confirmatory.

## Measurement invariance (multi-group CFA)

Fit nested models across groups and stop at the first that fails (ΔCFI ≤ .01, ΔRMSEA ≤ .015):

| Level | Equal across groups | Licenses |
|-------|---------------------|----------|
| configural | same pattern | same construct exists |
| metric (weak) | + loadings | comparing slopes / relationships |
| scalar (strong) | + intercepts | comparing **latent means** |
| strict | + residual variances | comparing observed composites |

If scalar fails, partial invariance (freeing a minority of intercepts) can still license latent-mean
comparison; report which parameters were freed and why.

## IRT notes

`girth`: `twopl_mml(data)` → `{'Discrimination', 'Difficulty'}`; `rasch_mml(data)` for the 1PL.
`py-irt`: Bayesian, scalable, Pyro-based. For graded-response / partial-credit / multidimensional
models with full fit output, R `mirt` remains the practical standard — document the R dependency
rather than shipping a thin or fabricated Python path.

## References

- McNeish (2018), Thanks coefficient alpha, we'll take it from here. *Psychological Methods.*
- Hu & Bentler (1999), Cutoff criteria for fit indexes.
- Putnick & Bornstein (2016), Measurement invariance conventions.
- Igolkina & Meshcheryakov (2020), semopy; semopy 2 (arXiv 2106.01140).
