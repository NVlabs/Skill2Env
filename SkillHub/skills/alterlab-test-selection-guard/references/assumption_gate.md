# The Assumption-Check Gate

Assumption checks are **inputs** to the decision tree, not post-hoc justifications. They
run and are reported **before** the test result is interpreted. This is the analog of
"verify the test is RED before you trust GREEN": the p-value is uninterpretable until the
assumptions behind it are shown.

## Fixed order

1. **Pre-specify** the test the data structure points to (parametric branch by default —
   see `references/decision_tree.md`).
2. **Run the checks.** Use `alterlab-statistical-analysis`'s
   `scripts/assumption_checks.py` (`comprehensive_assumption_check()` and the targeted
   functions). It performs:
   - **Normality** — Shapiro-Wilk + Q-Q plot.
   - **Homogeneity of variance** — Levene's test + box plots.
   - **Outliers** — IQR and z-score screens (report; do not silently delete).
   - **Linearity / homoscedasticity** (regression) — residual diagnostics.
3. **Report the check results** alongside the test.
4. **Then** take the pre-specified parametric or non-parametric branch the *checks*
   dictate.

## Handling violations (pre-specified responses)

These responses are decided in advance, by the assumption verdict — not by the p-value.

| Violation | Pre-specified response |
|---|---|
| Normality, mild + n > 30/group | Proceed (parametric tests are robust at that n). |
| Normality, moderate | Move to the pre-specified non-parametric fallback. |
| Normality, severe | Transform, or use the non-parametric fallback. |
| Homogeneity (t-test) | Use Welch's t-test. |
| Homogeneity (ANOVA) | Welch's ANOVA or Brown-Forsythe. |
| Linearity (regression) | Polynomial terms, transform, or GAM. |

(These mirror the violation table in `alterlab-statistical-analysis`.)

## The trap this gate closes

The illegitimate move is: run the t-test, see p = .07, *then* "discover" non-normality and
switch to Mann-Whitney. The switch is conditioned on the result. The gate forbids it: the
normality check is run and reported **before** the p-value is read, so the branch is fixed
by the data, not by the outcome. A switch is only valid if the assumption check — run
first — sent you there.
