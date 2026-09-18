---
name: s4h-logic-causality-mapping
description: "Map causal relationships, trace dependencies, and reason about consequences before acting. Use when you need to understand what causes what, what breaks if something changes, or what must be true for a plan to work. TRIGGERS: 'map the dependencies', 'what causes this', 'what breaks if I change X', 'trace the root cause', 'if X then what', 'what has to be true for this to work', any situation involving root cause analysis, impact assessment, dependency tracing, or reasoning about chains of effect."
---

# Logic Causal Reasoning

Correlation isn't causation. Neither is sequence. "This happened, then that happened" is not the same as "this caused that" — but it's treated as equivalent constantly, and it produces wrong diagnoses, failed fixes, and surprised engineers.

This skill makes causal structure explicit: what actually depends on what, what change produces what effect, and what must be true for a plan to hold.

---

## Four Modes

Use the mode that matches the question.

**Framing check:** Confirm the specific causal situation before selecting a mode. State what you've identified — the system or situation, the observed effect or proposed change, and the core causal question — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific situation and causal question]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

### Mode 1: Root Cause Tracing
*"Why did this happen?"*

Work backwards from an observed effect to its cause — and to the cause of that cause.

**Process:**
1. State the observed effect precisely. Not "the system is slow" — "p95 latency increased from 120ms to 840ms after the Tuesday deploy."
2. Ask: what are the immediate causes that could produce this effect? List all plausible candidates.
3. For each candidate: what evidence would confirm or rule it out?
4. Eliminate candidates. For the survivors: what caused them?
5. Continue until you reach a cause that has no upstream cause within scope — or a point where further tracing requires different expertise or data.
6. Distinguish: **root cause** (the origin), **proximate cause** (the immediate trigger), **contributing factors** (conditions that allowed it).

### Mode 2: Impact Mapping
*"What breaks if I change X?"*

Work forwards from a proposed change through its downstream effects.

**Process:**
1. State the change precisely.
2. Identify direct dependents: what immediately relies on the thing being changed?
3. For each dependent: what behaviour changes, and what downstream systems rely on that behaviour?
4. Continue for two to three levels of dependency.
5. Mark irreversible effects — changes that, once made, cannot be cleanly undone.
6. Mark cascade risks — places where a small effect triggers a large one.

### Mode 3: Dependency Mapping
*"What must be true for this to work?"*

Identify the full set of conditions a plan depends on.

**Process:**
1. State the plan or goal.
2. Ask: what must be true in the environment for this to succeed? List all dependencies.
3. For each dependency: is it guaranteed, assumed, or unknown?
4. For each assumed dependency: what is the cost if the assumption is wrong?
5. Surface single points of failure — dependencies that, if they break, cause total plan failure with no fallback.

### Mode 4: Counterfactual Testing
*"Would Y still have happened without X?"*

Test a causal claim by reasoning about the counterfactual world.

**Process:**
1. State the causal claim: "X caused Y."
2. Imagine removing X. Would Y still happen via another path?
3. If yes: X is a contributing factor, not the root cause.
4. If no: X is necessary for Y — strong causal evidence.
5. Consider: was X sufficient alone, or did it require other conditions?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Direct causes only** — Map first-order causal links, skip downstream consequences
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Mode:** [Root Cause / Impact Mapping / Dependency Mapping / Counterfactual]

**Question:** [the specific causal question being answered]

**[Mode-appropriate structure]**

For Root Cause:
- Proximate cause: [immediate trigger]
- Root cause: [origin]
- Contributing factors: [conditions that enabled it]
- Evidence: [what confirms this vs what was ruled out]

For Impact Mapping:
- Direct effects: [level 1 dependencies affected]
- Downstream effects: [level 2-3]
- Irreversible effects: [flagged]
- Cascade risks: [flagged]

For Dependency Mapping:
- Dependencies: [each, with status: guaranteed / assumed / unknown]
- Single points of failure: [flagged]
- Highest-risk assumptions: [ranked]

For Counterfactual:
- Causal claim tested: [X caused Y]
- Counterfactual: [would Y happen without X?]
- Verdict: [necessary / contributing / coincidental]
- Conditions required alongside X: [if X alone wasn't sufficient]

**Summary**
[2-3 sentences on what the causal analysis reveals and what action it implies]

---

## Notes

Causal reasoning is always provisional — it produces the best available model given current evidence, not a proof. State explicitly what evidence would change the analysis. In complex systems, multiple causal chains often contribute to a single effect; resist the urge to stop at the first plausible explanation.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Causal chain mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-systems-feedback-mapping` — Turn the causal map into a feedback loop analysis
  - `/s4h-historical-precedent-analysis` — Check whether this causal chain has played out before
  - `/s4h-constraint-hardness-testing` — Test which causal link is the weakest and most brittle
  - **Done** — Wrap up and synthesise what we have so far
