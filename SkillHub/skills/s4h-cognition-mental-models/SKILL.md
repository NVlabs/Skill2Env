---
name: s4h-cognition-mental-models
description: "Surfaces and audits the internal representations that drive perception and decision-making. Use when asked 'what assumptions am I making', 'why do I keep seeing this the same way', 'what model is driving this decision', 'I think I'm missing something about how this works', 'what's my mental model here', or when a belief or decision pattern needs to be examined from the inside."
---

# Cognition: Mental Models

Every perception, judgment, and decision runs through a mental model. Philip Johnson-Laird's model theory, developed through decades of research at Princeton, demonstrated that human reasoning does not operate on formal logical rules — it operates on internal simulations of situations. We construct small-scale models of reality, reason by running those models mentally, and check conclusions against them. The problem is not that we use mental models — it's that the models become invisible.

When a mental model is invisible, it cannot be examined. Its assumptions are treated as facts. Its gaps become blind spots. Its distortions shape what evidence we notice and what options we can imagine, all without our awareness. The executive who can't understand why their strategy isn't working is often running an accurate model of the organisation as it was three years ago. The negotiator who keeps being surprised by the other party's responses is modelling a different game than the one being played.

This skill makes the implicit explicit. It identifies which models are active in a situation, extracts their assumptions, tests those assumptions against available evidence, and identifies where the model is incomplete, outdated, or simply wrong. The output is not just a list of flaws — it's a more accurate replacement model, ready to use.

---

## Your Process

**Step 1: Identify the Model in Use**
Ask: what are the implicit beliefs about how this domain works that are driving the current perception or decision? A mental model has three components:
- **Entities:** the actors, objects, or forces in the model
- **Relationships:** how those entities interact and influence each other
- **Dynamics:** how the model behaves over time — what causes what, what follows from what

Name the current model in explicit terms. If the user hasn't articulated it, infer it from the decisions or conclusions they're describing.

**Framing check:** Confirm the specific model and situation before continuing. State what you've identified — the domain being modelled and the decision or belief the model is shaping — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the domain, the current model, and the decision it's shaping]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Surface the Assumptions**
Dig into the model's foundations. For each core relationship in the model, ask: what has to be true for this to hold? List these as explicit assumptions. Common categories:
- **Causal assumptions:** "A causes B" — is this direction correct? Is it bidirectional?
- **Stability assumptions:** "this relationship is stable over time" — is it?
- **Scope assumptions:** "this applies here" — does it?
- **Actor assumptions:** "the relevant entities are X, Y, Z" — who or what is missing?

**Step 3: Test Against Evidence**
For each assumption, ask: what evidence supports it? What evidence contradicts it? What evidence would you expect to see if it were true that you don't actually see? Be specific. Surface the evidence that the current model is filtering out or explaining away.

**Before narrowing:** Use `AskUserQuestion` to confirm the assumption list before assessing accuracy:
- **Question:** "I've surfaced [N] assumptions in the current model. Before I test each one, are there any assumptions you'd add, or any that stand out as especially load-bearing?"
- **Header:** "Assumptions"
- **Options:**
  - **Proceed** — the assumption set looks right
  - **Add an assumption** — user will name one to include
  - **Flag a load-bearing one** — user will identify which to examine first

**Step 4: Identify Gaps and Distortions**
What does the current model systematically miss or misrepresent? Two types:
- **Gaps:** entities, relationships, or dynamics that exist in reality but are absent from the model (the stakeholder group not accounted for; the feedback loop not included)
- **Distortions:** things that are in the model but represented inaccurately (the causal direction reversed; the magnitude wrong; the relationship oversimplified)

**Step 5: Construct the Updated Model**
Revise the model to incorporate what the audit found. State the updated model explicitly using the same three-component structure (entities, relationships, dynamics). Identify what changes in practical terms: what decisions would look different? What would you now notice that you were filtering out?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what model is being audited and what the most consequential gap or distortion appears to be — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete model audit: assumptions, evidence test, gaps, distortions, updated model
  - **Key findings only** — The most consequential gaps and distortions, bottom-line updated model
  - **Single assumption deep-dive** — Focus the whole analysis on the most load-bearing assumption
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Current Model (Explicit)**
- Entities: [list]
- Relationships: [list]
- Dynamics: [how it behaves over time]

**Assumption Audit**

| Assumption | Supported by | Contradicted by | Status |
|---|---|---|---|
| | | | |

**Gaps:** [What is missing from the model — entities, relationships, dynamics not included]

**Distortions:** [What is present but represented inaccurately]

**Updated Model**
- Entities: [revised list]
- Relationships: [revised list]
- Dynamics: [revised]

**Practical Implications:** [What decisions or perceptions would change under the updated model]

---

## Notes

Mental model audits are uncomfortable by design — the point is to find where your current understanding is wrong. Frame the output as an upgrade, not a repudiation. The goal is not to discard the model (it likely captures real structure) but to make it more accurate.

The nearest neighbor is `/s4h-epistemology-justification` — which examines whether beliefs are adequately grounded. Mental model auditing operates at the structural level (the model itself), while epistemology-justification operates at the evidentiary level (whether specific claims are supported). Use both when a deeply held belief is driving a high-stakes decision.

For beliefs driven primarily by emotional or identity stakes rather than cognitive models, `/s4h-emotional-trust-audit` and `/s4h-identity-values-clarification` are more appropriate entry points.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Mental model audit complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-cognition-metacognition` — Apply thinking-about-thinking to monitor how you're now using the updated model
  - `/s4h-epistemology-justification` — Examine whether the updated model's key claims are adequately supported
  - `/s4h-decision-option-mapping` — Use the updated model to generate options that the old model couldn't see
  - **Done** — Wrap up and synthesise what we have so far
