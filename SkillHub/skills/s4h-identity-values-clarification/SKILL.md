---
name: s4h-identity-values-clarification
description: "Surfaces and tests actual operative values — distinguishing what is stated from what decisions actually reveal. Triggers: 'values clarification', 'what do we actually stand for', 'is this consistent with our values', 'values alignment check', 'test the values', 'what do our decisions reveal'."
---

# Values Clarification

Stated values are aspirational. Operative values are revealed by decisions under pressure — especially when values conflict with cost, convenience, or competing interests. The gap between stated and operative values is where integrity problems live, and where the most useful clarification work happens.

---

## Your Process

**Step 1: State the Values Being Invoked**
Not abstract words — translate each value into a behavioural definition. "What does this value mean in practice? What behaviour does it require, and what behaviour does it prohibit?"
- Instead of: "We value innovation."
- Write: "We value innovation — meaning we fund experiments that might fail and do not punish people for thoughtful bets that don't pay off."

**Framing check:** Confirm the specific subject before continuing. State what you've identified — the entity whose values are being examined and the set of stated values in scope — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the entity and the values under examination]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Find Recent Decisions That Confirmed Each Value**
For each value: what recent decision or action was consistent with the behavioural definition? Be specific — name the decision.

**Step 3: Find Recent Decisions That Contradicted Each Value**
For each value: what recent decision or action contradicted the behavioural definition? These are the most diagnostic data points.

**Step 4: Identify Where Values Conflicted**
Where did two values pull in opposite directions? When values conflict, one wins. The outcome reveals which value actually takes priority — the real priority order, not the stated one.

**Step 5: State the Operative Values**
Based on the evidence from Steps 2–4: what are the actual, operative values — as demonstrated by behaviour? Where do they differ from stated values?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Operative values only** — Values actually revealed by decisions, not stated ones
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Values Analysis
| Stated Value | Behavioural Definition | Confirming Decisions | Contradicting Decisions |
|-------------|----------------------|---------------------|------------------------|
| ... | ... | ... | ... |

### Value Conflicts and Revealed Priority Order
| Conflict | Which Value Won | What This Reveals About Priority |
|----------|----------------|----------------------------------|
| ... | ... | ... |

### Operative Values (As Evidenced)
State what the organisation or person actually values, based on decisions — not aspiration.

### Gaps Between Stated and Operative Values
- [Where the stated value diverges from the operative one — and what it would take to close the gap]

---

## Notes

The most productive use of this analysis is not to criticise but to surface hidden commitments — values that are being lived without being named, and values that are named without being lived.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Values clarified. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-identity-mission-alignment` — Connect the clarified values to mission
  - `/s4h-decision-criteria-weighting` — Weight decision criteria by values
  - `/s4h-ethics-check` — Check whether values are applied consistently
  - **Done** — Wrap up and synthesise what we have so far
