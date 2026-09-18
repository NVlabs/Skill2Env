---
name: alterlab-ssci-inference-gate
description: "Audits final inferential claims against the design, sample, and uncertainty before they are written or published — refuses causal language unless the design's identifying assumption is defended (else downgrades to associational), corrects p-value and confidence-interval misreadings (a p-value is not the probability the null is true, non-significance is not proof of no effect, a 95% CI is not a 95% probability the parameter is inside it), demands effect sizes with intervals rather than significance stars, flags uncorrected multiple comparisons and optional stopping / HARKing, and scopes generalization to the sampling frame. Use when writing or checking a results or discussion section, interpreting a p-value or confidence interval, or deciding whether a finding supports a causal or population claim. For choosing the statistical test prefer alterlab-test-selection-guard; to execute the analysis prefer alterlab-statistical-analysis. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: No API key required. A discipline-enforcing claim-audit skill; the optional claim linter runs locally via `uv run python` (standard library only).
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "consumes the Design Passport from alterlab-ssci-design-gate / alterlab-ssci-measurement-gate / alterlab-ssci-sampling-gate; hands clean claims to alterlab-paper-writer"
---

# Inference Gate — The Claim May Not Exceed the Design

**Skill type: DISCIPLINE-ENFORCING.** This is the terminal gate of the social-science methods
spine. It reads the accumulated **Design Passport** and audits every inferential sentence against
what actually identifies it — the design, the sample, and the uncertainty. It does not compute; it
refuses conclusions the study cannot support.

## The Core Rule

```
A CLAIM MAY NOT EXCEED ITS DESIGN, ITS SAMPLE, OR ITS UNCERTAINTY.
AUDIT EACH SENTENCE AGAINST WHAT ACTUALLY IDENTIFIES IT.
```

Three ceilings bound every claim. **Design**: causal language is licensed only if the design's
identifying assumption (pinned by `alterlab-ssci-design-gate`) is named and defended — otherwise
the claim is associational. **Sample**: a population generalization is licensed only by a
probability sample of a frame that covers the target population (`alterlab-ssci-sampling-gate`).
**Uncertainty**: a result is reported with an effect size and an interval, interpreted correctly —
not as a bare significant/not-significant verdict. A sentence that breaks any ceiling is rewritten
down to what the study supports.

## When to Use This Skill

- "Help me write / check the results or discussion section."
- "My p-value is 0.03 — what can I conclude?" / "p was 0.20, so there's no effect, right?"
- "Does this finding mean X *causes* Y?"
- "Can I say this holds for [the broader population]?"
- "I ran 30 comparisons and three were significant — what can I report?"

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Which statistical test to run | `alterlab-test-selection-guard` | Test choice, upstream of interpretation. |
| Executing the analysis / computing the estimate | `alterlab-statistical-analysis` | Computation, not claim audit. |
| Choosing the design & identifying assumption | `alterlab-ssci-design-gate` | Design routing happens first. |
| Reliability/validity of the measure | `alterlab-ssci-measurement-gate` | Measurement quality, a different ceiling. |
| Prose polish of an already-sound claim | `alterlab-paper-writer` | Writing, once the claim is audited clean. |

## The three ceilings

### 1. Design ceiling — causal language

Cross-check the claim's verb against `design_type` + `identifying_assumption` in the Passport:

- **Causal verbs** (causes, increases, reduces, improves, leads to, the effect of) require a
  design that identifies a causal effect *and* a defended assumption. Experiment → yes. QED → yes
  **only if** its assumption (parallel trends / exclusion / continuity / no time-varying
  confounders) is defended. Observational without a defended assumption → **downgrade** to
  associational (is associated with, predicts, correlates with).
- Never let a significant coefficient in an observational regression become "X causes Y."

### 2. Sample ceiling — generalization

- **Statistical generalization** to a population requires a probability sample of a covering frame
  (`generalization: statistical` in the Passport). Otherwise scope the claim to the sample
  ("among the surveyed students…") and offer only **analytical** generalization.
- Watch universal quantifiers ("adults", "people generally") attached to a convenience sample.

### 3. Uncertainty ceiling — p-values, CIs, effect sizes

| Misreading | Correction |
|---|---|
| "p = 0.03 means a 3% chance the null is true." | p is P(data this extreme \| null), **not** P(null \| data). |
| "p > 0.05, so there is no effect." | Absence of evidence ≠ evidence of absence. Report the CI; a wide CI around zero is *inconclusive*, not a null proof. |
| "The 95% CI means a 95% probability the true value is in it." | The parameter is fixed; 95% is the long-run coverage of the *procedure*. |
| "It's statistically significant, so it matters." | Significance ≠ importance. Report the **effect size** and its interval; judge practical significance against it. |
| "Three of my 30 tests were significant." | Uncorrected multiplicity. Pre-specify, or correct (FDR / Bonferroni); disclose the family. |
| "I found the hypothesis the data supported." | HARKing / optional stopping. Separate pre-registered confirmatory from exploratory claims. |

A stdlib linter that flags causal verbs, over-broad generalization, and p-value misuse against the
Passport facts: `scripts/claim_audit.py`. Fuller treatment (ASA statement on p-values, New
Statistics, multiplicity): `references/inference_audit.md`.

## Reading the Design Passport

The gate consumes what upstream gates wrote and audits against it:

```yaml
# from design-gate
design_type: observational
identifying_assumption: "conditional ignorability — NOT defended (no plausible ignorability argument)"
claim_type: associational
# from sampling-gate
sampling_method: convenience
generalization: analytical
```

Given this Passport, "remote work **increases** satisfaction **among adults**" fails two ceilings
and is rewritten to "remote work **is associated with** higher satisfaction **among the surveyed
employees**."

## Self-Check Before Publishing

- Does every causal verb trace to a design + a **defended** identifying assumption?
- Is each generalization scoped to what the sample/frame supports (statistical vs analytical)?
- Are results reported as effect size + interval, with p-values interpreted correctly?
- Is a non-significant result framed as inconclusive (CI shown), not as proof of no effect?
- Are multiplicity and any exploratory/optional-stopping caveats disclosed?

## References

- `references/inference_audit.md` — p-value/CI interpretation, multiplicity correction, the three-ceiling audit worked through.
- `scripts/claim_audit.py` — stdlib linter flagging causal-verb, generalization, and p-value overreach against Passport facts.

Part of the AlterLab Academic Skills suite.
