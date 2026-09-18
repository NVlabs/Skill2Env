# Design Decision Tree — Full Logic

Loaded on demand from the design-gate SKILL.md. The routing question is always the same:
**what makes the causal effect identified?** Design families differ only in the assumption
they lean on.

## True experiment

Researcher randomly assigns the cause. Randomization makes assignment independent of potential
outcomes (ignorability), so a simple difference in means is unbiased for the average treatment
effect. Threats: non-compliance, attrition, contamination/spillover, failure of randomization.
When assignment is random but uptake is not, you are back to an IV problem (assignment
instruments for uptake).

## The five quasi-experimental designs

A quasi-experiment is observational data plus an identifying assumption. Each buys credibility
by burning information (bookdown.org/mike/data_analysis).

| Design | Exploits | Identifying assumption | Key threat / check |
|--------|----------|------------------------|--------------------|
| **Difference-in-differences (DiD)** | a treatment turned on for some units at some time | **parallel trends**: treated and control would have moved together absent treatment | inspect pre-trends; beware staggered adoption & heterogeneous effects |
| **Instrumental variables (IV)** | an as-good-as-random shifter of treatment | **exclusion restriction** + relevance: instrument affects Y only via the treatment | weak-instrument diagnostics; defend exclusion substantively (not statistically) |
| **Regression discontinuity (RDD)** | treatment assigned by a threshold on a running variable | **continuity** of potential outcomes at the cutoff; no manipulation of the score | McCrary/density test for sorting; local to the cutoff (limited external validity) |
| **Interrupted time series (ITS)** | one series observed over many periods around an intervention | the modeled pre-trend counterfactual would have continued | autocorrelation; co-occurring shocks at the interruption |
| **Fixed effects / panel** | repeated observations of the same units | no **time-varying** confounders (unit/time confounders differenced out) | still biased by shocks correlated with treatment timing |

## Observational / selection-on-observables

Adjust for measured confounders (regression, matching, weighting). Rests on **conditional
ignorability** — no unmeasured confounding — the strongest and least testable assumption. Say
so explicitly; sensitivity analysis (e.g. E-value) quantifies how strong an unmeasured
confounder would have to be to overturn the result.

## Qualitative

Interpretive/theory-building aims (grounded theory, phenomenology, case study, ethnography).
Route to `alterlab-qualitative-methods`. Sample size is governed by **saturation / information
power**, not a power calculation — see `alterlab-ssci-sampling-gate`. External validity is
**transferability**, scoped to the case, not statistical generalization.

## Mixed methods

Combine strands with an explicit design (convergent, explanatory-sequential,
exploratory-sequential, embedded) and a joint-display integration plan. Route to
`alterlab-mixed-methods`.

## Worked routing examples

- *"Minimum-wage rose in one state in 2019; did employment fall?"* → DiD; assumption = parallel
  employment trends between the treated state and comparison states pre-2019.
- *"Does military service affect later earnings?"* → IV (draft lottery); assumption = the
  lottery number affects earnings only through service.
- *"Does a scholarship (given above a test cutoff) raise graduation?"* → RDD; assumption =
  continuity at the cutoff, no score manipulation.
- *"We surveyed employees once; is remote work causing higher satisfaction?"* →
  observational/selection-on-observables at best; downgrade to associational unless a QED and
  its assumption are supplied.
