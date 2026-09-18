# Intercoder Reliability — Coefficients, APIs, and Reporting

Loaded on demand from the qualitative-analysis SKILL.md. APIs verified 2026 against PyPI/CRAN.

## Krippendorff's alpha (primary)

Chance-corrected agreement that handles ≥2 coders, any measurement level, and missing data. Based
on the coincidence matrix of observed vs expected disagreement: `alpha = 1 - Do/De`.

```python
import numpy as np, krippendorff        # krippendorff >= 0.8.2
# reliability_data shape = coders (rows) x units (columns); missing = np.nan
data = [[1, 1, np.nan, 2, 1],
        [1, 2, 3,      2, 1]]
krippendorff.alpha(reliability_data=data, level_of_measurement="nominal")   # point estimate ONLY
```

The package default `level_of_measurement` is `"interval"` — **always pass it explicitly**
(`"nominal"`/`"ordinal"`/`"interval"`/`"ratio"`). It returns a single number with **no CI**, so:

- **Bundled stdlib** `scripts/icr.py` — nominal α + a nonparametric **bootstrap 95% CI over units**
  + Cohen's κ, no dependencies.
- **R for all levels + CIs**: `irrCAC::krippen.alpha.raw(ratings, weights="unweighted",
  conflev=0.95)` (returns `coeff.se`, `conf.int`) or `icr::krippalpha(data, metric="nominal",
  bootstrap=TRUE, nboot=20000)`.

## Kappa family (fixed rater count)

```python
from statsmodels.stats.inter_rater import aggregate_raters, fleiss_kappa, cohens_kappa
table, cats = aggregate_raters(codes_subjects_by_raters)   # -> N subjects x k categories counts
fleiss_kappa(table, method="fleiss")                        # >2 raters
cohens_kappa(agreement_table)                               # 2 raters, square agreement matrix
# cross-check:
from sklearn.metrics import cohen_kappa_score
cohen_kappa_score(coder_a, coder_b, weights=None)           # weights: None | "linear" | "quadratic"
```

## NOT valid ICR measures

- **Chi-square** — tests association, not agreement.
- **Cronbach's alpha** — internal consistency of a scale, not chance-corrected inter-rater agreement.
- **Pearson's r** — linear covariation; two coders can correlate perfectly while never agreeing.

Refuse these if offered as "reliability."

## Interpretation thresholds (Krippendorff)

| α | Verdict |
|---|---------|
| ≥ .800 | reliable |
| .667 – .799 | draw **tentative** conclusions only |
| < .667 | unreliable — revise codebook / retrain coders |

Report α **with a 95% CI**. A high point estimate on few units can have a CI that crosses the
threshold — the CI is the honest signal.

## LLM-assisted coding (current practice)

Benchmark an LLM coder against a human gold standard with the same machinery: Krippendorff's α
between each LLM and the human coding, with CIs used to judge statistical indistinguishability.
Report the model, the coding prompt, the % double-coded, and the α+CI. The LLM is a coder to be
validated, not a shortcut around reliability.

## Reporting standard (Lombard et al.; O'Connor & Joffe)

State: the ICR measure used, the number of coders, the % of data double-coded, and the
disagreement-resolution process — plus α + CI + threshold verdict, and the branch (content-analytic
vs reflexive TA).

## References

- Krippendorff, K. Computing Krippendorff's Alpha-Reliability (method paper).
- Lombard, Snyder-Duch & Bracken (2002). Content analysis in mass communication: ICR.
- O'Connor & Joffe (2020). Intercoder reliability in qualitative research.
- Marzi et al. (2024). K-Alpha Calculator.
