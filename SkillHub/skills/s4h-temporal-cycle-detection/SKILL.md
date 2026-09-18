---
name: s4h-temporal-cycle-detection
description: "Identifies what recurring cycle a situation is an instance of and where in that cycle you currently are. Use when asked 'what cycle is this', 'where are we in the cycle', 'have we seen this before', 'detect the pattern', 'hype cycle', or 'where in the curve'."
---

# Temporal Cycle Detection

Every situation that feels unprecedented is usually an instance of a recurring cycle. Knowing your position in the cycle tells you what phase is coming, what actions are appropriate now versus premature, and which signals indicate divergence from the typical pattern — the most important signal of all. Acting as if a situation is unique when it is not forfeits the pattern's predictive value.

---

## Your Process

**Step 1: Describe Current State and Trajectory**
State what is happening now and how the situation has moved over the past period. Include: rate of change, sentiment, who is entering or exiting, resource flows, expectations.

**Framing check:** Confirm the specific situation before continuing. State what you've identified — the actual phenomenon or domain being analyzed and its key observable parameters — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific situation and what is changing]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Match to a Candidate Cycle**
Compare against the most common cycles:
- **Technology Hype Cycle (Gartner):** trigger → peak of inflated expectations → trough of disillusionment → slope of enlightenment → plateau of productivity
- **Product Adoption Curve (Rogers):** innovators → early adopters → early majority → late majority → laggards
- **Business/Economic Cycle:** expansion → peak → contraction → trough → recovery
- **Organisational Change Curve (Kübler-Ross adapted):** shock → denial → frustration → depression → experiment → decision → integration
- **Competitive Cycle:** emergence → growth → shakeout → maturity → decline/renewal
- **Market Cycle:** accumulation → markup → distribution → markdown

**Step 3: Map Current Position**
Place the situation on the curve. Be specific about which phase and where within the phase (early, mid, late).

**Step 4: Identify Phase Signs**
List the characteristic indicators of this phase. Which are present? Which are absent? Absent expected signs are as informative as present ones.

**Step 5: State the Typical Next Phase**
What normally follows this phase? What are the leading indicators that the transition has begun?

**Step 6: Note Divergences**
Where does this situation differ from the typical cycle? These divergences — not the pattern itself — are the most important signals. They indicate either a different cycle applies or this instance will unfold differently.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Current position only** — Where in the cycle we are right now, skip the full cycle description
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Cycle Match:** [cycle name] — [why it fits]

**Current Position:** [phase name] — [early / mid / late within phase]

**Phase Signs**

| Expected Sign for This Phase | Present? |
|------------------------------|---------|
| | |

**Typical Next Phase:** [name + leading indicators of transition]

**Divergences:** [where this instance differs from the typical pattern + what that implies]

**Implications:** [what actions are appropriate now vs. premature vs. overdue]

---

## Notes

If no cycle fits well, that is itself a finding — either the situation is genuinely novel or it requires a composite of two cycles. Name the mismatch explicitly rather than forcing a fit.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Cycles detected. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-historical-cycle-detection` — Look for historical evidence that confirms the cycles
  - `/s4h-temporal-timing-analysis` — Time actions to the detected cycles
  - `/s4h-strategy-timing` — Align strategy with the cycle timing
  - **Done** — Wrap up and synthesise what we have so far
