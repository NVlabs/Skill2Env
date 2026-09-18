# Rationalizations — Excuse vs. Reality (extended)

Every row is a real thought that precedes a p-value-driven test switch or a researcher
degree of freedom. When one appears — from you or the user — name it, quote the Reality
column, and stop. This extends the short table in `SKILL.md`.

| Excuse | Reality |
|---|---|
| "The t-test wasn't significant, let me try Mann-Whitney." | You are choosing the test by its result — test-shopping. The non-parametric test is valid only if the *assumption check* (not the p-value) sent you there. |
| "The data suggested a better test after I looked." | You are fitting noise / HARKing. Re-run the pre-specified test; report anything else as exploratory. |
| "I'll just drop these 3 outliers and re-run." | Outlier rules must be pre-specified or reported as a sensitivity analysis — not invented to cross .05. |
| "Adding this covariate obviously improves the model." | Obvious *post hoc* = a researcher degree of freedom. Pre-specify it or label the result exploratory. |
| "Non-parametric is more conservative, so switching is safe." | Switching *because the first test failed* still conditions the choice on the outcome; the inflation is real in either direction. |
| "It's only exploratory anyway." | Then say so explicitly, drop confirmatory p-value language, and do not report it as a test of the hypothesis. |
| "Everyone reports the test that worked." | Selective reporting of the significant test among several is p-hacking; report all tests run or correct for them. |
| "The omnibus ANOVA was n.s. but this one pair looks significant." | Pairwise fishing after a non-significant omnibus is multiplicity abuse. See `multiplicity.md`. |
| "Let me re-categorize the outcome and re-test." | Re-binning the outcome to chase significance is a researcher degree of freedom; the cutpoints must be pre-specified. |
| "I'll one-tail it now that I see the direction." | A one-tailed test must be pre-registered with its direction *before* the data; switching tails after seeing the effect halves the real p-value dishonestly. |
| "We can stop collecting — it's already significant." | Optional stopping inflates Type I error; report the sequential design (and its correction) or stop peeking. |
| "Let me run a couple more tests, one will hit." | That is the escalation gate's exact trigger — 3+ tests on one hypothesis. Correct or declare exploratory; do not run test #4. |

## The forcing line

For all of these:

> **STOP. You are exploiting researcher degrees of freedom. Return to the pre-specified
> test, or label the analysis exploratory and drop the confirmatory claim.**

The only legitimate reason to change the test is a **pre-specified assumption-check
verdict** or a documented, pre-result correction to the design or question — never the
p-value of a test you already ran.
