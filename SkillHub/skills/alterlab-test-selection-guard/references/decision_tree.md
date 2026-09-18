# Decision Tree — Full Branch Logic

This expands the digraph in `SKILL.md`. Every fork is decided by the research question
and the data's structure, **before** any p-value is visible. It mirrors and stays
consistent with the Test Selection Guide in `alterlab-statistical-analysis`
(`references/test_selection_guide.md`); this file adds the timing discipline.

## 1. Outcome type — the first fork

| Outcome | Goes to |
|---|---|
| Continuous or ordinal, compared across groups | Group-comparison branch (§2/§3) |
| Categorical counts (frequencies in cells) | Categorical branch (§4) |
| Relationship between two variables | Association branch (§5) |

## 2. Two groups, continuous/ordinal outcome

- **Independent + normal** → independent-samples t-test. If the variances are unequal
  (Levene significant), use **Welch's** t-test rather than the pooled-variance form.
- **Independent + non-normal** → Mann-Whitney U.
- **Paired + normal differences** → paired-samples t-test (normality applies to the
  *difference* scores, not the raw groups).
- **Paired + non-normal differences** → Wilcoxon signed-rank.

The parametric branch is the default pre-specification; the non-parametric branch is taken
**only when the assumption-check gate (`references/assumption_gate.md`) sends you there** —
never because the t-test returned a non-significant p-value.

## 3. Three or more groups, continuous/ordinal outcome

- **Independent + normal** → one-way ANOVA. Plan post-hoc comparisons (e.g. Tukey HSD) in
  advance; do not pick the post-hoc by which pair is significant.
- **Independent + non-normal** → Kruskal-Wallis.
- **Repeated/within-subject + normal** → repeated-measures ANOVA (check sphericity;
  Greenhouse-Geisser correction if violated).
- **Repeated + non-normal** → Friedman.

A non-significant omnibus test does **not** license fishing through pairwise tests; that is
the multiplicity trap (`references/multiplicity.md`).

## 4. Categorical outcome (counts)

- **Expected cell count >= 5 in (nearly) all cells** → chi-square test of independence.
- **Small expected counts / 2x2 with sparse cells** → Fisher's exact test.

The choice here is driven by the *expected* cell counts, computed before testing — not by
which test yields significance.

## 5. Association between two variables

- **Both continuous, linear + bivariate-normal** → Pearson r.
- **Both continuous, monotonic but non-normal / non-linear** → Spearman rho.
- **Continuous outcome + one or more predictors** → linear regression (check
  linearity, residual normality, homoscedasticity).
- **Binary outcome + predictors** → logistic regression.

## Bayesian alternatives

Bayesian counterparts exist for all of the above and can support the null directly (Bayes
factors). They are chosen the same way — by structure, in advance. See
`alterlab-statistical-analysis` (`references/bayesian_statistics.md`).

## What does NOT change the branch

- The p-value of a previously run test.
- A desire to "get under .05."
- Eyeballing descriptives split by the outcome.

What legitimately moves you between branches: the **pre-specified** assumption-check
verdict, a corrected design fact (e.g. realizing the data are actually paired), or a
correction to the research question made and documented *before* the result is seen.
