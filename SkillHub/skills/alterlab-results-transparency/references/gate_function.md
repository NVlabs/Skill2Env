# The Gate Function — Full Walkthrough

This is the long-form companion to the Gate Function in `SKILL.md`. It explains
each step, defines the claim-manifest the `scripts/reporting_gate.py` helper
reads, and works one passing and one failing example.

The pattern is adapted from `verification-before-completion` (obra/superpowers):
*evidence before assertions, always*. There the gate stands between "I think the
code works" and "the code works"; here it stands between "the analysis came out
this way" and a sentence in the Results section.

---

## Step 1 — IDENTIFY the claim

Write the exact sentence you intend to publish. Vague intent hides the
violation; the concrete sentence exposes it. Example:

> "Mindfulness training significantly reduced exam anxiety (p < .05)."

The moment it is written out, steps 4 and 6 already have something to bite on:
there is no effect size, no CI, no df, no exact p.

## Step 2 — LIST every test actually run

Enumerate every test executed against *this* hypothesis, regardless of outcome.
This includes:

- Tests that returned p > .05.
- Model specifications you ran and then abandoned.
- Alternative outlier-exclusion rules you tried.
- A non-parametric test you ran "to check" after a parametric one.

If this list is longer than what the draft reports, the gap **is** the selective
reporting. The fix is to report all of them (a supplementary "all analyses run"
table is standard) or to justify, in the frozen plan, why only a subset is
confirmatory.

## Step 3 — CHECK assumptions were reported

Statistical claims rest on assumptions. The assumption results produced by
`alterlab-statistical-analysis/scripts/assumption_checks.py`
(normality: Shapiro-Wilk + Q-Q; homogeneity: Levene; linearity; outliers:
IQR + z-score) — must appear in the write-up. If an assumption was violated, the
remediation taken (Welch's correction, a non-parametric test chosen *a priori*, a
transformation) must be stated. "Assumptions were met" with no numbers does not
clear the gate.

## Step 4 — CHECK effect size + 95% CI present

A bare p-value is not interpretable: it conflates magnitude with sample size and
says nothing about practical importance. Every claim must carry an effect size
*with a 95% confidence interval*. Use the effect sizes and benchmarks owned by
`alterlab-statistical-analysis` (e.g. Cohen's d, η²_p, Pearson r, R², Cramér's V)
— this skill does not compute them, it requires their presence.

## Step 5 — CHECK pre-registration deviations disclosed

Compare the analysis as run to the frozen plan owned by
`alterlab-preregistration-discipline`. Any difference — a changed primary
outcome, an added covariate, a different exclusion rule, a switched test — must be
named and labelled. Confirmatory claims must match the plan; everything else is
exploratory and must say so.

## Step 6 — ONLY THEN write the sentence

A sentence that clears the gate looks like:

> "As pre-registered, mindfulness training reduced exam anxiety relative to
> control, t(58) = 2.71, p = .009, d = 0.70, 95% CI [0.18, 1.22]; normality
> (Shapiro-Wilk) and homogeneity (Levene) assumptions held. Two further
> exploratory models (adding sleep hours; excluding 3 high-leverage cases) are
> reported in the supplement and did not change the direction of the effect."

---

## Claim manifest (input to `scripts/reporting_gate.py`)

The helper reads a small JSON object describing one claim and what was run. It is
a transparency linter — it checks completeness and disclosure, never recomputes
statistics.

```json
{
  "claim": "Mindfulness training reduced exam anxiety relative to control.",
  "preregistered": true,
  "tests_run": [
    {
      "name": "independent t-test",
      "reported": true,
      "confirmatory": true,
      "statistic": "t(58) = 2.71",
      "p_value": "0.009",
      "effect_size": "d = 0.70",
      "ci_95": "[0.18, 1.22]",
      "assumptions_reported": true
    },
    {
      "name": "ANCOVA adding sleep hours",
      "reported": true,
      "confirmatory": false,
      "assumptions_reported": true
    }
  ],
  "deviations": [
    {"description": "added sleep-hours covariate", "labelled_exploratory": true}
  ]
}
```

Field rules the script enforces:

- Every `tests_run` entry with `reported: false` is a transparency failure
  (an analysis was run but not reported).
- Every `reported` entry that is `confirmatory: true` must have a non-empty
  `effect_size` **and** `ci_95`, and `assumptions_reported: true`.
- Every `deviations` entry must have `labelled_exploratory: true`.
- If `tests_run` has 3+ entries on the same claim, the script warns about
  multiple comparisons (correct for all, or declare exploratory).

A clean manifest exits 0. Any failure exits non-zero and prints the specific
gate step that was not cleared.

---

## Worked example — FAIL

Manifest with two tests run but only the significant one `reported: true`, and
that claim carrying a p-value but no `effect_size`/`ci_95`:

- Step 2 LIST fails: a test was run (`reported: false`) and omitted.
- Step 4 fails: confirmatory claim has no effect size + CI.

Exit non-zero; the draft sentence may not be written until both are fixed.

## Worked example — PASS

The manifest above (one confirmatory test fully reported with d + CI + assumptions,
one exploratory model labelled, the deviation labelled exploratory) exits 0. The
sentence in Step 6 is now defensible.
