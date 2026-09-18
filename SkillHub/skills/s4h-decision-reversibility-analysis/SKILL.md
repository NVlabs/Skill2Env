---
name: s4h-decision-reversibility-analysis
description: "Categorises a decision by reversibility and applies the appropriate level of process rigour. Triggers: 'is this reversible', 'how much should I think about this', 'one-way door', 'two-way door', 'decision type', 'how committed is this'."
---

# Decision Reversibility Analysis

Most people apply the same amount of thinking to every decision. This is wrong in both
directions: it produces analysis paralysis on easy reversible choices, and recklessness on
decisions that cannot be undone. The right question before deciding is not "what should
I choose?" — it is "how much should I invest in choosing?"

---

## Your Process

**Step 1: State the Decision**
Write the decision clearly. Include what is actually being committed to — not the
framing, the underlying commitment.

**Framing check:** Confirm the decision and its underlying commitment before continuing. State what you've identified — the actual decision being assessed and what would be locked in if made — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the decision and its underlying commitment]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different decision than read; incorporate the correction before proceeding

**Step 2: Assess Reversal Cost**
If this decision turns out to be wrong, how expensive is it to undo? Consider: financial
cost, time cost, relationship or trust cost, technical debt introduced, market position
lost, and optionality foreclosed. Be concrete — not "expensive" but "six months of
re-architecture and two broken partnerships."

**Step 3: Classify — Type 1 or Type 2**
- **Type 1 (one-way door)**: reversing is very costly or practically impossible. Wrong
  here means significant, durable damage.
- **Type 2 (two-way door)**: can be walked back at low cost if wrong. A review point or
  small experiment can reveal the error before it compounds.

**Step 4: Apply the Appropriate Process**
- Type 1: slow down. Consult broadly. Surface dissent. Apply full analytical rigour.
  Set explicit criteria for what "good" looks like before committing.
- Type 2: decide quickly. Set a review point. Move. Do not let this consume the time
  budget of a Type 1 decision.

**Step 5: Flag Misclassification Risk**
Some decisions feel reversible but aren't. Network effects, sunk cost psychology,
technical lock-in, and relationship damage can make nominal two-way doors practically
one-way. Identify these explicitly.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Reversibility verdict only** — Is this reversible or not, and what that means for how much deliberation it deserves
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Decision:** [Statement — including the underlying commitment]

**Reversal cost:**
> [Concrete statement of what undoing this actually costs — time / money /
> relationships / technical / optionality]

**Classification:** Type 1 (one-way door) / Type 2 (two-way door)

**Recommended process level:**

| Type | Process |
|------|---------|
| Type 1 | Slow down — broad consultation, explicit success criteria, full rigour |
| Type 2 | Decide quickly — set review point, move, learn |

**Misclassification risk:**
> [Reasons this might be harder to reverse than it appears — or easier]

**Recommendation:**
> [Classification + what to do next based on it]

---

## Notes

The most expensive error is treating a Type 1 decision as Type 2 — deciding quickly on
something that cannot be undone. But the second-most expensive error is treating Type 2
decisions as Type 1, because the opportunity cost of delay is real and cumulative.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Reversibility assessed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-premortem-analysis` — If it's a one-way door, stress-test it thoroughly
  - `/s4h-decision-criteria-weighting` — Weight decision criteria differently given reversibility level
  - `/s4h-resource-allocation-analysis` — Calibrate resource investment to match reversibility
  - **Done** — Wrap up and synthesise what we have so far
