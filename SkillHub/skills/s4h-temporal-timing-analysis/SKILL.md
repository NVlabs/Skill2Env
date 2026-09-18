---
name: s4h-temporal-timing-analysis
description: "Assesses whether now is the right time to act, wait, or prepare. Use when asked 'is now the right time', 'should we wait', 'are we too early', 'timing this decision', 'when to move', or 'momentum'."
---

# Temporal Timing Analysis

Timing is often as consequential as the decision itself. The right action at the wrong time fails — too early before conditions are ready, too late after the window has closed. Most timing judgments are made implicitly, with the urgency of the moment substituting for analysis. Making timing explicit means identifying which conditions are present, which are absent, and whether the environment is moving toward or away from readiness.

---

## Your Process

**Step 1: State the Action and Current Context**
Name the action under consideration and describe current conditions — market, organizational, political, technical. The timing analysis is grounded in this specific context.

**Framing check:** Confirm the specific action and context before continuing. State what you've identified — the actual action being timed and the domain it sits in — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the action and its current context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify Readiness Conditions**
What observable conditions would make this optimal timing? These are specific and external — not "when we're ready" but "when X is true in the environment". For each condition: is it currently present or absent?

**Step 3: Assess Momentum**
Is the environment moving toward or away from ideal conditions? A missing condition that is approaching matters differently from one that is receding. Momentum changes the urgency calculation.

**Step 4: Cost of Waiting**
What is lost or foregone per unit of delay? Is the window closing — and how fast? Are competitors moving? Is the opportunity time-limited? Quantify where possible.

**Step 5: Cost of Acting Early**
What risks come from moving before conditions are right? First-mover disadvantage, resource waste, organizational fatigue from premature initiatives, credibility cost of a failed early attempt.

**Step 6: Define Trigger Signals**
What specific observable events should prompt action? These make timing a decision rule rather than a repeated judgment call.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Timing verdict only** — Act, wait, or prepare — and the single most important reason why
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Readiness Conditions**

| Condition | Present? | Momentum (toward / away) |
|-----------|---------|--------------------------|
| | | |

**Cost of Waiting:** [what is lost per period of delay; is the window closing?]

**Cost of Acting Early:** [risks of premature action]

**Timing Recommendation:** [act now / wait / prepare now, act at trigger] + rationale

**Trigger Signals:** [specific observable events that should prompt action]

---

## Notes

If both costs (waiting and acting early) are high, the situation requires a staged approach — begin preparation now, commit fully at the trigger. Identify what preparation can happen safely before the trigger is reached.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Timing analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-timing` — Translate timing analysis into strategy
  - `/s4h-decision-reversibility-analysis` — Assess reversibility given timing constraints
  - `/s4h-resource-allocation-analysis` — Allocate resources by timing priority
  - **Done** — Wrap up and synthesise what we have so far
