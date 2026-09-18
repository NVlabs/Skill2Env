---
name: alterlab-ssci-sampling-gate
description: "Gates who is sampled, how, and how many before data collection — checks that the sampling FRAME matches the target population (coverage error), that the METHOD is named (probability vs non-probability: simple random, stratified, cluster, systematic, quota, convenience, snowball), that sample SIZE follows the inference paradigm (an a-priori power analysis for hypothesis tests, a precision/margin-of-error target for estimation, or saturation/information power for qualitative studies — never a rule of thumb or collect-until-significant), and that the generalization claim matches the sample (statistical generalization only from probability samples). Use when asking how many participants are needed, planning recruitment, running or checking a power analysis, or judging whether a sample supports a population claim. For questionnaire items prefer alterlab-survey-design; for choosing the statistical test prefer alterlab-test-selection-guard. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: No API key required. A discipline-enforcing sampling-and-power skill; the optional sample-size calculator runs locally via `uv run python` (standard library only).
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-survey-design (instrument), alterlab-qualitative-methods (saturation depth), alterlab-test-selection-guard, alterlab-statistical-analysis"
---

# Sampling Gate — The Sample Decides Who the Answer Is About

**Skill type: DISCIPLINE-ENFORCING.** Before a single case is collected, this gate fixes three
things — the *frame*, the *method*, and the *size logic* — and ties the generalization claim to
them. It does not run the study or pick the test; it refuses to let sizing and recruitment happen
by habit.

## The Core Rule

```
WHO YOU SAMPLE AND HOW MANY MUST FOLLOW THE INFERENCE YOU WANT —
POWER FOR TESTS, PRECISION FOR ESTIMATES, SATURATION FOR THEORY.
A BIGGER N NEVER FIXES A BROKEN FRAME.
```

Sample size is not one calculation; it is *whichever* logic matches the inference. A hypothesis
test needs an **a-priori power analysis** (effect size + alpha + power ⇒ N). An estimation goal
needs a **precision** target (a margin of error at a confidence level). A qualitative study is
governed by **saturation / information power**, not a formula. And none of these matters if the
**frame** — the list you actually draw from — omits or over-represents part of the target
population. Coverage error and self-selection are not cured by collecting more.

## When to Use This Skill

- "How many participants / interviews / respondents do I need?"
- "Is my sample big enough to detect the effect?" (← a-priori power)
- "I surveyed 300 students; can I generalize to all adults?" (← frame + method)
- "My result was not significant — should I just collect more until it is?" (← no; pre-specify)
- "What sampling method should I use — stratified, cluster, quota…?"

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Writing / wording the questionnaire items | `alterlab-survey-design` | Instrument construction, not sampling. |
| Which statistical test to run once data are in | `alterlab-test-selection-guard` | Test choice, downstream of sampling. |
| Executing the power analysis / analysis in software | `alterlab-statistical-analysis` | Computation; this gate sets the *logic*, hands execution off. |
| Deep grounded-theory / coding mechanics | `alterlab-qualitative-methods` | This gate sets saturation *logic*; that skill does the qual depth. |
| Choosing the design & identifying assumption | `alterlab-ssci-design-gate` | Design routing, upstream of sampling. |

## Three sizing logics — pick by the inference, not by habit

| Inference goal | Sizing logic | Inputs | Common failure |
|----------------|--------------|--------|----------------|
| **Test a hypothesis** | a-priori **power analysis** | expected effect size, α, target power (usually .80/.90), test | powering off an inflated pilot effect; post-hoc "observed power" |
| **Estimate a quantity** | **precision** / margin of error | desired half-width, confidence level, expected variance/proportion | reporting N with no CI target |
| **Build/refine theory (qual)** | **saturation / information power** | scope, sample specificity, dialogue quality, analysis strategy | quoting a fixed "N=12" as a rule instead of arguing information power |

A stdlib calculator for the first two (two-group mean or two-proportion designs):
`scripts/sample_size.py`. Full logic, stratified/cluster design effects, and finite-population
correction: `references/sampling_and_power.md`.

## Frame and method before size

1. **Frame vs target population.** Name the target population, then the frame you can actually
   draw from. The gap between them is **coverage error** — state it. A sample of your university's
   students is not a sample of adults.
2. **Probability vs non-probability.** Only a **probability** sample (each unit a known non-zero
   selection probability: SRS, stratified, cluster, systematic) supports **statistical**
   generalization with a sampling-error quantification. Non-probability samples (convenience,
   quota, snowball, purposive) support only **analytical/theoretical** generalization — say so and
   do not attach a margin of error as if it were random.
3. **Non-response & attrition.** A high non-response rate reintroduces selection bias even from a
   good frame. Plan for it; report it; consider weighting.

## Excuse vs Reality

| Excuse | Reality |
|---|---|
| "I'll collect as many as I can get." | Convenience size is not power. Name the target effect and compute N — or state you are estimating, not testing. |
| "It wasn't significant, so I'll add data until it is." | Optional stopping inflates the false-positive rate. Pre-register N (or a sequential design with corrected boundaries). |
| "300 is a big sample, so it generalizes." | Generalization comes from the *frame and method*, not the count. 300 self-selected students still only speak for self-selected students. |
| "Observed (post-hoc) power shows the test was fine." | Post-hoc power is a deterministic function of the p-value; it carries no new information. Use a-priori power. |
| "For qualitative work I'll do N=12 because that's standard." | Saturation/information power is argued from scope and data quality, not a fixed number copied from another study. |

## The Design Passport (hand-off)

Append: `target_population`, `sampling_frame` (+ named coverage gap), `sampling_method`
(probability/non-probability + specific design), `size_logic` (`power` | `precision` |
`saturation`) with its inputs and resulting N (or saturation argument), `expected_nonresponse`,
and `generalization` (`statistical` | `analytical`). `alterlab-ssci-inference-gate` later audits
the final generalization claim against `sampling_method` + `generalization`.

## Self-Check Before Advancing

- Is the sizing logic the one that matches the inference (power / precision / saturation)?
- For a test, is N from an **a-priori** power analysis on a defensible effect size — not a pilot's inflated one?
- Is the frame stated, with its coverage gap from the target population named?
- Is the sample probability or non-probability, and is the generalization claim scoped to match?
- Is non-response/attrition planned for, not ignored?

## References

- `references/sampling_and_power.md` — sizing logics, design effects, finite-population correction, reporting templates.
- `scripts/sample_size.py` — stdlib a-priori N for two-group mean and two-proportion designs.

Part of the AlterLab Academic Skills suite.
