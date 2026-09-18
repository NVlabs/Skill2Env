# Inference Audit — Full Reference

Loaded on demand from the inference-gate SKILL.md. Works the three-ceiling audit (design, sample,
uncertainty) through in detail, with the p-value/CI corrections and multiplicity handling.

## Ceiling 1 — Design: when is causal language licensed?

A claim's *verb* encodes its inferential ambition. Map it to the Passport's `design_type` and
whether `identifying_assumption` is **defended**, not merely named:

| Design | Causal claim licensed? | Condition |
|--------|------------------------|-----------|
| True experiment (RCT) | yes | randomization intact (check compliance, attrition, spillover) |
| Difference-in-differences | yes | parallel-trends defended (pre-trends inspected) |
| Instrumental variables | yes | exclusion restriction defended substantively + instrument relevant |
| Regression discontinuity | yes (local) | continuity/no-sorting defended; claim is local to the cutoff |
| Interrupted time series | yes | modeled counterfactual defended; no co-occurring shock |
| Fixed effects / panel | qualified | only if no time-varying confounders — usually a weak defense |
| Observational / selection-on-observables | **no**, unless | conditional ignorability is argued *and* sensitivity-analysed (E-value) |

If the condition is not met, rewrite the verb: *causes → is associated with*; *increases →
predicts / is higher among*; *the effect of → the relationship between*. A statistically
significant regression coefficient is **not** a license to upgrade the verb.

## Ceiling 2 — Sample: statistical vs analytical generalization

- **Statistical generalization** (the sample estimate speaks for the population within sampling
  error) requires a probability sample and a frame that covers the target population. Only then may
  standard errors / CIs be read as population statements.
- **Analytical (theoretical) generalization** (the case informs a theory or a similar setting) is
  the ceiling for non-probability samples — convenience, quota, snowball, purposive. Scope the
  claim to the studied cases and argue transferability; do not attach a population margin of error.
- Flag universal quantifiers ("adults", "consumers", "people") on a narrow frame.

## Ceiling 3 — Uncertainty

### p-values (ASA 2016 statement)

1. A p-value is `P(data at least this extreme | null and all model assumptions)`. It is **not**
   `P(null is true)`, not the probability the results are due to chance, and not `1 − P(replication)`.
2. **p > 0.05 does not establish "no effect."** It is a failure to reject; the CI shows the range
   of effects still compatible with the data. A wide CI spanning zero is *inconclusive*. Only an
   equivalence test (e.g. TOST against a pre-set bound) can support "no meaningful effect."
3. Significance thresholds are conventions, not laws of nature; p = 0.049 and p = 0.051 are nearly
   identical evidence. Avoid "trending toward significance."
4. A p-value says nothing about effect **size** or **importance**.

### Confidence intervals

A 95% CI is a realization of a procedure that captures the fixed true parameter 95% of the time in
the long run. It is **not** "a 95% probability the parameter is in this interval" (that is a
credible-interval / Bayesian statement, which requires a prior). Report and interpret the CI's
*width* as the study's precision, and its position relative to values that would matter.

### Effect sizes ("New Statistics")

Report a standardized or raw effect size with its interval as the primary result; the p-value is
secondary. Statistical significance is not practical significance: a trivial effect can be
significant at large N, and an important effect can be non-significant at small N. Judge the effect
against a smallest-effect-of-interest, not against zero alone.

### Multiplicity and researcher degrees of freedom

- **Multiple comparisons**: testing many hypotheses inflates the family-wise false-positive rate.
  Pre-specify the primary test(s); for the rest, control the family-wise error (Bonferroni/Holm) or
  the false discovery rate (Benjamini-Hochberg), and disclose the full family — including tests
  that were run and not reported.
- **Optional stopping**: peeking and stopping when p < 0.05 inflates Type I error; use a
  pre-registered N or a sequential design with corrected boundaries (see `alterlab-ssci-sampling-gate`).
- **HARKing** (hypothesizing after results are known): relabeling an exploratory finding as an
  a-priori prediction. Keep confirmatory and exploratory claims explicitly separate.

## The audit, worked

Passport: `design_type: observational`, `identifying_assumption` not defended,
`claim_type: associational`, `sampling_method: convenience`, `generalization: analytical`.

Draft claim: *"Remote work increases job satisfaction among adults (p = 0.02)."*

- Ceiling 1 (design): "increases" is causal; observational with no defended assumption → downgrade
  to "is associated with higher".
- Ceiling 2 (sample): "among adults" over-generalizes a convenience sample → scope to "among the
  surveyed employees".
- Ceiling 3 (uncertainty): "p = 0.02" alone → add the effect size and its CI; do not imply the
  result proves the relationship.

Audited claim: *"Among the surveyed employees, remote work was associated with higher job
satisfaction (β = …, 95% CI […, …]); the design does not support a causal interpretation."*

## References

- Wasserstein, R. L., & Lazar, N. A. (2016). The ASA statement on p-values. *The American Statistician.*
- Cumming, G. (2014). The new statistics: why and how. *Psychological Science.*
- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate.
- Kerr, N. L. (1998). HARKing: Hypothesizing After the Results are Known.
- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology.
