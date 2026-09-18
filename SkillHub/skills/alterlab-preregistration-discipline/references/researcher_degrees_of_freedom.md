# Researcher Degrees of Freedom — The Failure Modes This Skill Catches

Pre-registration discipline exists to neutralize *researcher degrees of freedom*: the
many undisclosed analytic choices that, made after seeing the data, can manufacture an
apparently significant result. This file documents each failure mode and the verified
source behind it, so the Iron Law, the Excuse-vs-Reality table, and the Red-Flags list
in SKILL.md are grounded rather than asserted.

## The core mechanism

Simmons, Nelson & Simonsohn (2011) showed that flexibility in data collection, analysis,
and reporting — choosing when to stop collecting, which conditions to report, which
covariates to include — *"dramatically increases actual false-positive rates,"* to the
point that one can present almost anything as statistically significant. The fix they
propose is disclosure and pre-specification: the same commitment a pre-registration
makes binding. This is the empirical foundation for freezing the plan before data are
visible.

> Source: Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-Positive
> Psychology: Undisclosed Flexibility in Data Collection and Analysis Allows Presenting
> Anything as Significant. *Psychological Science, 22*(11), 1359–1366.

## The named failure modes

| Failure mode | What it is | Where it shows up in the workflow |
|---|---|---|
| **HARKing** | Hypothesizing After the Results are Known — presenting a post-hoc hypothesis as if it were predicted a priori. | Switching/inventing the hypothesis after CONFIRM; demote to EXPLORE. |
| **Optional stopping** | Peeking at accruing data and stopping when p < .05; inflates the Type I error rate. | Violates the COLLECT stopping-rule gate. |
| **p-hacking** | Trying analytic variants (transforms, exclusions, covariates) until something crosses significance. | Violates the CONFIRM "traces to the plan" gate; fires the 3+-tests escalation gate. |
| **Outcome switching** | Reporting a secondary outcome as primary because it came out significant. | Primary outcome must be ranked and frozen in PLAN. |
| **Test-shopping** | Choosing the statistical test by which gives the smaller p-value. | Test decision must be frozen in PLAN; unplanned swap → EXPLORE. |
| **Garden of forking paths** | Even with *no* deliberate fishing, a single dataset implies many analyses that *would have been* run under different data — so a single comparison is effectively multiple. | Why covariates/transforms/exclusions must all be pre-specified, not just the headline test. |

### HARKing

Kerr (1998) coined HARKing and catalogued its costs: it dresses an exploratory,
data-driven hypothesis in confirmatory clothing, destroying the diagnostic meaning of
the test. Pre-registration is the direct antidote — the hypothesis is on the record
before the result exists.

> Source: Kerr, N. L. (1998). HARKing: Hypothesizing After the Results are Known.
> *Personality and Social Psychology Review, 2*(3), 196–217.
> https://doi.org/10.1207/s15327957pspr0203_4

### Garden of forking paths

Gelman & Loken (2014) make the subtle point that the multiple-comparisons problem does
not require conscious p-hacking. If the specific analysis is *contingent on the data*
(you would have analyzed a different subgroup, or coded the variable differently, had the
numbers come out otherwise), then a single reported comparison is statistically equivalent
to having run many — and its p-value is not interpretable at face value. This is why PLAN
must freeze covariates, transformations, exclusions, and missing-data handling, not just
the primary test. Only a plan fixed before the data can close every fork.

> Source: Gelman, A., & Loken, E. (2014). The Statistical Crisis in Science. *American
> Scientist, 102*(6), 460. https://doi.org/10.1511/2014.111.460

## What this skill does NOT do with these

It does not *correct* p-hacked statistics, choose tests, or compute FDR/Bonferroni
corrections — that is `alterlab-statistical-analysis`. It does not grade the resulting
evidence quality (GRADE / risk of bias) — that is `alterlab-scientific-thinking`. It does
not produce the registration document — that is `alterlab-open-science`. Its sole job is
to enforce the boundary: *no confirmatory claim without a plan that predates the data,
and every unplanned analysis labeled exploratory.*
