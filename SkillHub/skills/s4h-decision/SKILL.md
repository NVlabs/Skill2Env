---
name: s4h-decision
description: "Entry point for the decision toolkit. Routes to the right decision skill based on your situation. Use when you say 'decision', 'help me decide', 'should I', 'which option', 'what are my choices', 'what could go wrong', 'is this reversible', or want decision help without knowing which specific tool fits."
---

# Decision

Applies structured decision thinking to any choice. Diagnoses what kind of decision work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Make sure you're seeing all the real options | option-mapping |
| Compare options against weighted criteria | criteria-weighting |
| Stress-test a decision by imagining it failed | premortem-analysis |
| Calibrate how much process this decision deserves | reversibility-analysis |

## Routing Decision

**Framing check:** Confirm the decision and its intended outcome before routing. State what you've identified — the actual choice being faced and what the user is trying to achieve — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific decision and its intended outcome]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **About to decide between 2 options — may be missing others** → option-mapping first
- **Options are visible, need to compare them systematically** → criteria-weighting
- **Leaning toward a direction, want to stress-test it** → premortem-analysis
- **Unsure how much time to spend on this decision** → reversibility-analysis
- **Unclear** → option-mapping; the option space is almost always narrower than it should be

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Option Mapping

*Ensures all real options are visible before choosing.*

Counter the false dichotomy: the first two options that come to mind are rarely all that exists. Generate options across three levels: (1) direct solutions to the stated problem, (2) alternative framings of the problem that suggest different solutions, (3) options that combine or transcend the initial set. Apply the deliberate quota: find at least 5 options. Don't evaluate until the inventory is complete.

**Output:** Option inventory (5+ minimum), including options that reframe the problem, with brief descriptions. No evaluation yet — just the full map.

---

## Criteria Weighting

*Runs a weighted multi-criteria analysis.*

Step 1: List what actually matters for this decision. Step 2: Weight each criterion by importance (1-5 scale). Step 3: Score each option on each criterion (1-5). Step 4: Calculate weighted scores. Step 5: Check the winner against intuition — if the numbers say X but your gut says Y, that gap is information worth understanding, not a flaw in the method.

**Output:** Weighted decision matrix, ranked options, and an interpretation of whether the quantitative result matches or challenges intuition.

---

## Premortem Analysis

*Imagines the decision was made and failed — then diagnoses why.*

Set the scene: it's 12 months from now. The decision was made, and it failed badly. Write the failure story: what went wrong? Be specific — not "it didn't work" but the actual mechanism of failure. Generate 5+ distinct failure paths. Now: which failure modes are most probable? Which are most damaging if they occur? Which can be mitigated before committing?

**Output:** 5+ failure paths, ranked by probability and severity. For each high-priority failure mode: the mitigation that reduces it. The adjusted decision recommendation.

---

## Reversibility Analysis

*Categorises a decision by reversibility to apply the right level of process.*

Two-way door decisions (easily reversible) should be made quickly with less process — the cost of deliberating exceeds the cost of being wrong. One-way door decisions (hard or impossible to reverse) deserve thorough analysis. Classify this decision: what would it take to undo it? How quickly? At what cost? Many decisions that feel irreversible aren't. Many that feel casual are more binding than they appear.

**Output:** Decision classification (reversibility score 1-5), what undoing it would require, and the recommended level of process given that classification.
