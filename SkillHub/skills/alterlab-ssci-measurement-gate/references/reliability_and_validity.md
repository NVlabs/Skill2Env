# Reliability and Validity — Full Reference

Loaded on demand from the measurement-gate SKILL.md. Covers the alpha-vs-omega math, the four
validities, the measurement-invariance sequence, and reporting templates.

## Reliability: why alpha is a lower bound

Cronbach's alpha estimates internal consistency under the **tau-equivalent** measurement model:
every item loads equally on a single common factor and differs only in error variance. Two things
follow.

1. When loadings are **unequal** (the congeneric case that real scales almost always show), alpha
   *underestimates* reliability — it is a lower bound.
2. When errors are **correlated** (shared method, adjacent-item wording, reverse-coded clusters),
   alpha can *overestimate* reliability — the "lower bound" guarantee breaks.

So alpha is neither a floor you can always trust nor an unbiased estimate. It is a single number
resting on an assumption you have usually not checked.

### McDonald's omega

Omega is computed from a fitted factor model rather than assuming equal loadings:

```
        (Σ λ_i)²
ω = ─────────────────────
    (Σ λ_i)² + Σ ψ_i
```

where `λ_i` are the standardized factor loadings and `ψ_i` the item error variances. Because it
weights items by their actual loadings, omega is the reliability of the total score under the
**congeneric** model — the honest general-case estimate. Report `omega_total` for the composite;
`omega_hierarchical` isolates the variance due to a general factor when the scale is
multidimensional with a bifactor structure.

**Recommended practice** (McNeish, 2018, *Psychological Methods*, "Thanks coefficient alpha, we'll
take it from here"): report omega as the default; if you also report alpha, state the
tau-equivalence assumption it rests on. Empirically the two often land close for well-constructed
unidimensional scales — Warne (2025) finds a median underestimate on the order of ~4.5% — so the
point is not that alpha is always badly wrong, but that you should not *assume* the gap is small
without evidence.

### The reliability checklist

- [ ] Dimensionality established (EFA/CFA) **before** any single reliability coefficient is trusted.
- [ ] `omega_total` reported for each composite; alpha optional and caveated.
- [ ] Item-total correlations reported; flagged items pre-specified, not fished.
- [ ] For 2-item or split forms, Spearman-Brown rather than alpha.
- [ ] Reliability of *difference* or *change* scores treated separately (they are typically lower).

## Validity: four kinds, none optional

Reliability is necessary but not sufficient. A perfectly consistent thermometer that reads 10° too
high is reliable and invalid. The four validity questions:

| Validity | Question it answers | Typical evidence |
|----------|---------------------|------------------|
| **Content** | Do the items span the construct's definitional domain? | expert judges, content-validity index, a blueprint mapping items to sub-domains |
| **Criterion** | Does the score track an external gold standard? | concurrent correlation (same time), predictive correlation (future outcome) |
| **Convergent** | Does it correlate with measures it *should*? | average variance extracted (AVE ≥ .50), correlations with kindred scales |
| **Discriminant** | Is it separable from constructs it *should not* equal? | heterotrait-monotrait ratio (HTMT < .85), √AVE > inter-construct correlations, no cross-loadings |

Construct validity is not one test but a **nomological** argument: the measure behaves, across many
relationships, the way theory says the construct should. A confirmatory factor analysis is the
usual quantitative core — fit indices against Hu & Bentler (1999) cutoffs (CFI/TLI ≥ .95,
RMSEA ≤ .06, SRMR ≤ .08, treated as guidelines not hard gates). Route the CFA to
`alterlab-sem-psychometrics`.

## Measurement invariance before any group comparison

A latent-mean or latent-relationship comparison across groups (countries, waves, arms) is
interpretable only if the instrument measures the same construct on the same scale in every group.
Test a **multi-group CFA** hierarchy and stop at the first level that fails:

| Level | What is constrained equal across groups | What it licenses |
|-------|------------------------------------------|------------------|
| **Configural** | same factor *structure* (which items load on which factor) | the same construct exists in each group |
| **Metric (weak)** | + factor **loadings** | comparing *relationships* / regression slopes across groups |
| **Scalar (strong)** | + item **intercepts** | comparing **latent means** across groups |
| **Strict** | + item **residual variances** | comparing observed composites directly |

Judge each step by change in fit (ΔCFI ≤ .01, ΔRMSEA ≤ .015 as common rules of thumb), not only a
chi-square difference test, which is sample-size sensitive. If scalar invariance fails, partial
invariance (freeing a minority of intercepts) may rescue latent-mean comparison — but a raw
group-mean difference on the composite, reported without any invariance evidence, may be a pure
measurement artifact. Route the invariance run to `alterlab-sem-psychometrics`.

## Reporting template (paste into the Design Passport)

```yaml
constructs:
  - name: <construct>
    definition: <one sentence, the conceptual definition items must span>
    items: <k>
    dimensionality: <unidimensional | k-factor; CFA fit: CFI= RMSEA= SRMR=>
    reliability:
      omega_total: <value>
      alpha: <value, with "assumes tau-equivalence" caveat if reported>
      item_total_range: <min–max>
    validity_evidence:
      content: <expert review / CVI / blueprint — or "not established">
      criterion: <concurrent / predictive r with what — or "not established">
      convergent: <AVE, correlations — or "not established">
      discriminant: <HTMT / √AVE comparison — or "not established">
    invariance: <none | configural | metric | scalar | strict>  # required before group comparison
```

## Common failures this gate catches

- Reporting alpha as *the* reliability and stopping there.
- Treating a high alpha as evidence the scale is *valid* (it is not evidence of validity at all).
- Computing one alpha across a set that is actually multidimensional.
- Comparing group means on a latent construct with **zero** invariance testing.
- Dropping items post hoc to inflate alpha, then reporting the inflated value without disclosure.

## References

- McNeish, D. (2018). Thanks coefficient alpha, we'll take it from here. *Psychological Methods*.
- Hu, L., & Bentler, P. M. (1999). Cutoff criteria for fit indexes in covariance structure analysis.
- Warne, R. T. (2025). On the empirical gap between coefficient alpha and omega.
- Putnick, D. L., & Bornstein, M. H. (2016). Measurement invariance conventions and reporting.
