---
name: alterlab-ssci-design-gate
description: "Routes a social-science study to its research design — true experiment, quasi-experiment (difference-in-differences, instrumental variables, regression discontinuity, interrupted time series, fixed effects), observational/correlational, qualitative, or mixed — by walking the random-selection and random-assignment decisions, then PINS the identifying assumption the causal claim will rest on (parallel trends, exclusion restriction, continuity at the cutoff, selection-on-observables, or qualitative saturation logic) before any analysis begins. Use when choosing a study design, asking what design to use, framing a causal question from observational data, or deciding experiment vs quasi-experiment vs observational. For executing the analysis prefer alterlab-statistical-analysis; for qualitative design depth prefer alterlab-qualitative-methods; for choosing the statistical test downstream prefer alterlab-test-selection-guard. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: No API key required. A discipline-enforcing design-routing skill; the optional decision-tree helper runs locally via `uv run python` (standard library only).
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-qualitative-methods, alterlab-mixed-methods, alterlab-statistical-analysis, alterlab-test-selection-guard; hands the pinned assumption to alterlab-ssci-inference-gate"
---

# Design Gate — Pin the Identifying Assumption Before Anything Else

**Skill type: DISCIPLINE-ENFORCING.** This is the entry point of the social-science methods
spine, not an analysis engine. It routes a study to the right *design family* and forces the
one decision every downstream gate depends on: **what identifying assumption licenses the
causal claim?** It does not run models — for execution it hands off to the analysis skills.

## The Core Rule

```
A CAUSAL CLAIM IS ONLY AS GOOD AS ITS IDENTIFYING ASSUMPTION — NAME IT FIRST.
```

Design is chosen by the **question and the data-generating process** — who was selected, who
was assigned, what varies and when — not by which method is fashionable or convenient. A
quasi-experiment is an observational design that *earns* a causal interpretation only by
committing, up front, to an assumption that makes the effect identified. State that assumption
before touching an estimator; if you cannot defend one, the claim is associational, not causal.

## When to Use This Skill

Trigger the design gate whenever a design is being **chosen, defended, or implied by a claim**:

- "What research design should I use for this question?"
- "I have observational survey data and want to claim X improves Y." (← pin the assumption)
- "Should this be an experiment or a quasi-experiment?"
- "Can a difference-in-differences / IV / regression-discontinuity design answer this?"
- "Is my before/after comparison enough to claim the program worked?"

### Does NOT Trigger

Route these adjacent requests to the real sibling skill. This gate picks the *design* and pins
the *assumption*; it does not execute, choose the test, or write.

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Running the analysis / a specific model once the design is fixed | `alterlab-statistical-analysis` / `alterlab-statsmodels` | Execution, not design choice. |
| Which statistical *test* to use (t-test vs Mann-Whitney, etc.) | `alterlab-test-selection-guard` | Test choice is downstream of design. |
| Deep qualitative design (grounded theory, phenomenology, coding) | `alterlab-qualitative-methods` | This gate only routes *to* qual; that skill does it. |
| Integrating qual + quant strands, joint displays | `alterlab-mixed-methods` | Mixed-methods design mechanics. |
| Grading evidence quality, confounders, bias upstream | `alterlab-scientific-thinking` | Study-validity judgment, not design routing. |
| Designing the instrument/questionnaire itself | `alterlab-survey-design` | Measurement instrument, not design family. |

## The Design Decision Tree

Walk top-down. **Each branch is decided by the data-generating process, not the desired claim.**

```
1. Is the CAUSE randomly ASSIGNED by the researcher?
   ├─ YES → TRUE EXPERIMENT (RCT / lab / field experiment)
   │         identifying assumption: randomization → ignorability (assignment ⊥ potential outcomes)
   └─ NO  → 2. Is there exogenous variation you can exploit?
            ├─ a policy/treatment turned on for some units at some time → DIFFERENCE-IN-DIFFERENCES
            │     assumption: PARALLEL TRENDS (treated & control would have moved together absent treatment)
            ├─ an "as-good-as-random" nudge affecting treatment but not the outcome directly → INSTRUMENTAL VARIABLES
            │     assumption: EXCLUSION RESTRICTION + relevance (instrument affects Y only through the treatment)
            ├─ treatment assigned by a threshold on a running variable → REGRESSION DISCONTINUITY
            │     assumption: CONTINUITY of potential outcomes at the cutoff (no manipulation of the score)
            ├─ one unit observed before/after an intervention over many periods → INTERRUPTED TIME SERIES
            │     assumption: the pre-trend + modeled counterfactual would have continued absent the intervention
            ├─ repeated observations, unit/time confounders → FIXED EFFECTS / panel
            │     assumption: no time-varying confounders (selection-on-observables within unit)
            └─ none of the above, adjust for measured confounders only → OBSERVATIONAL / SELECTION-ON-OBSERVABLES
                  assumption: CONDITIONAL IGNORABILITY (no unmeasured confounding) — the weakest, name it as such

3. Is the aim interpretive / theory-building rather than effect estimation?
   ├─ YES → QUALITATIVE design (route to alterlab-qualitative-methods)
   │         "power" is SATURATION / information power, not a sample-size formula (see alterlab-ssci-sampling-gate)
   └─ combine strands → MIXED METHODS (route to alterlab-mixed-methods)
```

Full branch logic, the five quasi-experimental designs and their threats, and worked routing
examples: `references/design_decision_tree.md`. A stdlib router that prints the design family
and its required assumption from your answers: `scripts/design_router.py`.

## "You Buy Credibility by Burning Information"

Every step from a true experiment toward pure observation trades statistical control for an
assumption you must defend. Name the trade honestly:

| Excuse | Reality |
|---|---|
| "It's basically an experiment — people just chose their own group." | Self-selection is exactly what randomization removes. This is observational; name the confounding you are assuming away. |
| "I have before-and-after data, so it's causal." | A single pre/post has no counterfactual. You need parallel trends (DiD) or a modeled counterfactual (ITS) — state which. |
| "I controlled for everything relevant." | You controlled for what you *measured*. Conditional ignorability assumes no *unmeasured* confounders — the strongest, least testable assumption. |
| "Instrumental variables fix endogeneity." | Only if the exclusion restriction holds. An instrument that affects the outcome through any other path is invalid — defend exclusion, don't assert it. |
| "Regression discontinuity is quasi-random at the cutoff." | Only if units cannot manipulate the running variable and outcomes are continuous there. Check for sorting/bunching. |

## The Design Passport (hand-off)

On exit, emit or update the pipeline's YAML **Design Passport** with:
`research_question`, `design_type`, `identifying_assumption` (the named assumption + why it is
defensible), and `claim_type` (`causal` | `associational` | `descriptive`). Downstream,
`alterlab-ssci-measurement-gate` and `alterlab-ssci-sampling-gate` append to it, and
`alterlab-ssci-inference-gate` audits final claims against `design_type` + `identifying_assumption`.

## Self-Check Before Advancing

- Is the design chosen by the data-generating process, not the desired conclusion?
- Is exactly one identifying assumption named, with a sentence on why it is defensible here?
- If observational, is the claim explicitly downgraded to associational unless a QED assumption holds?
- For qualitative aims, is "how many" deferred to saturation logic (not a power formula)?
- Is the Design Passport populated for the next gate?

## References

- `references/design_decision_tree.md` — full branch logic, the five QEDs, threats, examples.
- `scripts/design_router.py` — stdlib router printing the design family + required assumption.

Part of the AlterLab Academic Skills suite.
