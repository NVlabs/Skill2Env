# Multiplicity — The Escalation Gate

```
Ran 3+ tests on the SAME hypothesis searching for significance? STOP.
```

Running many tests and reporting the one that crossed .05 is the textbook definition of
multiple comparisons abuse. With a per-test alpha of .05, the probability of at least one
false positive across `k` independent tests is `1 - (1 - 0.05)^k` — roughly 14% at k=3,
23% at k=5, 40% at k=10. The reported p-value of the "winner" no longer means what it says.

## The family

The correction is applied across the **family** of tests *actually run* on a hypothesis —
including the ones that did not "work." Selectively forgetting the non-significant attempts
is the abuse the correction exists to prevent. Define the family honestly before
correcting.

## Two honest options (never a fourth test)

### 1. Correct for all of them

- **Bonferroni** — compare each p-value against `alpha / k`, where `k` is the number of
  tests in the family. Simple, conservative; controls the family-wise error rate.
- **Benjamini-Hochberg (FDR)** — less conservative; controls the *false discovery rate*.
  Sort the `k` p-values ascending; the largest `i` for which `p(i) <= (i / k) * alpha` and
  all smaller ranks are declared significant. Preferred when `k` is large and some false
  positives are tolerable.

Use Bonferroni when false positives are costly and `k` is small; use Benjamini-Hochberg
when screening many hypotheses.

### 2. Declare the analysis exploratory

Label it exploratory, report **every** test run (not just the significant one), and drop
the confirmatory p-value language. Exploratory findings generate hypotheses for a future
confirmatory study; they are not themselves confirmatory evidence.

## What this gate forbids

Running test #4 (or #5, #6) on the same hypothesis to find p < .05 without correcting the
whole family or relabeling the work as exploratory. The number 3 is the prompt to stop and
choose — not a budget of free tests.

For computing the corrections in code, hand off to `alterlab-statistical-analysis` /
`alterlab-statsmodels` (`statsmodels.stats.multitest.multipletests` implements both
methods). For disclosing all tests run in the write-up, hand off to
`alterlab-results-transparency`.
