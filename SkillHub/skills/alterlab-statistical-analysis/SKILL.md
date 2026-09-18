---
name: alterlab-statistical-analysis
description: Guided statistical analysis with hypothesis-test selection, assumption checking, power analysis, and APA-formatted reporting. Use when choosing the appropriate statistical test for data, verifying test assumptions, computing power/sample size, or producing APA-style results for academic research. For implementing specific models programmatically prefer statsmodels. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: No API key required. Runs locally via `uv run python`. Core deps are scipy, statsmodels, and pingouin>=0.6 (0.6 renamed output columns, e.g. p-val to p_val, CI95% to CI95, cohen-d to cohen_d); Bayesian examples additionally need pymc and arviz.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Statistical Analysis

## Overview

A systematic process for testing hypotheses and quantifying relationships. Conduct
hypothesis tests (t-test, ANOVA, chi-square), regression, correlation, and Bayesian
analyses with assumption checks and APA reporting. For academic research.

## When to Use This Skill

Use when:
- Conducting hypothesis tests (t-tests, ANOVA, chi-square)
- Performing regression or correlation analyses
- Running Bayesian statistical analyses
- Checking statistical assumptions and diagnostics
- Calculating effect sizes and conducting power analyses
- Reporting statistical results in APA format

## Core Capabilities

1. **Test selection & planning** — choose tests by research question and data type;
   a priori power analysis; multiple-comparison strategy.
2. **Assumption checking** — verify normality, homogeneity, linearity; diagnostic plots;
   remediation when violated.
3. **Statistical testing** — parametric and non-parametric tests; regression; correlation;
   Bayesian alternatives with Bayes Factors.
4. **Effect sizes & interpretation** — appropriate effect sizes with CIs; statistical vs.
   practical significance.
5. **Professional reporting** — APA-style reports, publication-ready figures and tables.

## Workflow

```
SELECT a test?      → Test Selection Guide
CHECK assumptions?  → Assumption Checking
RUN analysis?       → Running Statistical Tests + references/code_examples.md
REPORT results?     → Reporting Results + references/apa_report_templates.md
```

Worked code for every step is in `references/code_examples.md`.

## Test Selection Guide

Quick reference (full decision tree: `references/test_selection_guide.md`):

**Two groups** — independent + normal → independent t-test; independent + non-normal →
Mann-Whitney U; paired + normal → paired t-test; paired + non-normal → Wilcoxon
signed-rank; binary outcome → chi-square or Fisher's exact.

**3+ groups** — independent + normal → one-way ANOVA; independent + non-normal →
Kruskal-Wallis; paired + normal → repeated-measures ANOVA; paired + non-normal → Friedman.

**Relationships** — two continuous → Pearson (normal) or Spearman (non-normal); continuous
outcome + predictors → linear regression; binary outcome + predictors → logistic regression.

**Bayesian alternatives** exist for all of the above, giving direct probability statements,
Bayes Factors, and the ability to support the null. See `references/bayesian_statistics.md`.

## Assumption Checking

**ALWAYS check assumptions before interpreting results.** Use the bundled
`scripts/assumption_checks.py` (`comprehensive_assumption_check()` and targeted functions —
code in `references/code_examples.md`). It performs outlier detection (IQR + z-score),
normality testing (Shapiro-Wilk + Q-Q), homogeneity of variance (Levene + box plots), and
interpretation.

**When violated:**
- *Normality* — mild + n>30/group → proceed (robust); moderate → non-parametric;
  severe → transform or non-parametric.
- *Homogeneity* — t-test → Welch's; ANOVA → Welch's or Brown-Forsythe; regression →
  robust SE or WLS.
- *Linearity (regression)* — polynomial terms, transform variables, or GAM.

Detail: `references/assumptions_and_diagnostics.md`.

## Running Statistical Tests

Primary libraries: `scipy.stats` (core tests), `statsmodels` (regression/diagnostics),
`pingouin` (tests + effect sizes), `pymc` + `arviz` (Bayesian).

Copy-paste examples for t-test, ANOVA + post-hoc, linear regression with full
diagnostics, and a Bayesian t-test: `references/code_examples.md`.

## Effect Sizes

**Effect sizes quantify magnitude; p-values only indicate existence.** Always report
them, with CIs. Benchmarks (guidelines only — context matters):

| Test | Effect Size | Small | Medium | Large |
|------|-------------|-------|--------|-------|
| T-test | Cohen's d | 0.20 | 0.50 | 0.80 |
| ANOVA | η²_p | 0.01 | 0.06 | 0.14 |
| Correlation | r | 0.10 | 0.30 | 0.50 |
| Regression | R² | 0.02 | 0.13 | 0.26 |
| Chi-square | Cramér's V | 0.07 | 0.21 | 0.35 |

Calculation code and CI computation: `references/code_examples.md`. Full guidance:
`references/effect_sizes_and_power.md`.

## Power Analysis

Run **a priori** power analysis to size a study before collecting data, and **sensitivity
analysis** afterward to report the smallest detectable effect. Avoid post-hoc power.
Code: `references/code_examples.md`. Guidance: `references/effect_sizes_and_power.md`.

## Reporting Results

Follow APA style (`references/reporting_standards.md`). Report descriptive statistics
(M, SD, n), test statistics (name, statistic, df, exact p), effect sizes with CIs,
assumption checks, and all planned analyses.

Ready-to-adapt report paragraphs for t-test, ANOVA, multiple regression, and Bayesian
analysis: `references/apa_report_templates.md`.

## Bayesian Statistics

Consider Bayesian methods when you have prior information, want direct probability
statements, have small samples or sequential data, need to quantify evidence for the
null, or have a complex (hierarchical, missing-data) model. Key advantages: intuitive
interpretation, evidence for the null, flexibility, full uncertainty quantification.
Comprehensive guide (priors, Bayes Factors, credible intervals, convergence checks):
`references/bayesian_statistics.md`.

## Best Practices

Pre-register analyses; always check assumptions; report effect sizes with CIs; report all
planned analyses including non-significant ones; distinguish statistical from practical
significance; visualize before and after; check regression/ANOVA diagnostics; run
sensitivity analyses; share data and code; be transparent about violations and decisions.

## Common Pitfalls

P-hacking; HARKing; ignoring assumptions; confusing significance with importance; not
reporting effect sizes; cherry-picking results; misinterpreting p-values; uncorrected
multiple comparisons; ignoring missing-data mechanism (MCAR/MAR/MNAR); overinterpreting
non-significant results.

## Getting Started Checklist

- [ ] Define research question and hypotheses
- [ ] Determine the test (`references/test_selection_guide.md`)
- [ ] Power analysis for sample size
- [ ] Load and inspect data; check missing data and outliers
- [ ] Verify assumptions (`scripts/assumption_checks.py`)
- [ ] Run primary analysis; compute effect sizes with CIs
- [ ] Post-hoc tests if needed (with corrections)
- [ ] Create visualizations
- [ ] Write results (`references/reporting_standards.md`)
- [ ] Sensitivity analyses; share data and code

## Index of Bundled Resources

### References (`references/`)
- `test_selection_guide.md` — decision tree for choosing a test
- `assumptions_and_diagnostics.md` — checking and handling violations
- `effect_sizes_and_power.md` — effect sizes and power analysis
- `bayesian_statistics.md` — complete Bayesian guide
- `reporting_standards.md` — APA reporting rules
- `code_examples.md` — worked Python for tests, diagnostics, Bayesian, power, effect sizes
- `apa_report_templates.md` — ready-to-adapt APA results paragraphs

### Scripts (`scripts/`)
- `assumption_checks.py` — automated assumption checking with visualizations
  (`comprehensive_assumption_check`, `check_normality`, `check_homogeneity_of_variance`,
  `check_linearity`, `detect_outliers`)

## Further Reading

Key textbooks: Cohen (1988), Field (2013), Gelman & Hill (2006), Kruschke (2014).
Online: APA Style Guide (https://apastyle.apa.org/), Cross Validated
(stats.stackexchange.com).
