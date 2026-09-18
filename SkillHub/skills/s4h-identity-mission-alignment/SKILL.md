---
name: s4h-identity-mission-alignment
description: "Tests whether a proposed decision is genuinely aligned with stated mission — or is rationalising a departure from it. Triggers: 'mission alignment', 'is this on mission', 'are we drifting', 'mission check', 'does this serve our purpose', 'on brand'."
---

# Mission Alignment

Organisations drift from mission gradually — through decisions that are each individually justifiable but collectively represent a departure from purpose. The test is not whether a decision can be argued to be consistent with mission, but whether it genuinely serves it.

---

## Your Process

**Step 1: State the Mission Plainly**
Not the marketing version — the operational version. What is this organisation or person actually trying to achieve, for whom, and why? If the mission has multiple legitimate interpretations, name them.

**Step 2: State the Proposed Direction**
What is the decision, initiative, or direction being evaluated?

**Framing check:** Confirm the mission and the proposed decision before continuing. State what you've identified — the operational mission and the specific decision or initiative under evaluation — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the mission and the proposed decision being tested against it]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 3: Test for Direct Mission Service**
Does this directly serve the mission? If yes: how specifically — trace the connection. If no: what is it serving instead (growth, revenue, opportunity, stakeholder pressure)?

**Step 4: Test for Rationalisation**
Does the case for alignment require interpreting the mission more broadly than it was intended? Is this a genuine evolution of the mission — or is the mission being stretched to justify an attractive decision that doesn't actually fit?

**Step 5: Apply the Genuine Pursuer Test**
What would someone who genuinely, single-mindedly pursued this mission do? Does the proposal match that behaviour? If a person fully committed to the mission looked at this decision, would they find it obvious — or would they feel something was off?

**Step 6: Classify and Recommend**
Assign a classification and make a recommendation.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Misalignment only** — Where this decision diverges from stated mission
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Mission Statement (Plain Version)
[Operational description — not the tagline]

### Proposed Decision
[Clear description]

### Direct Mission Service
**Directly serves mission:** Yes / Partially / No
**Connection (if yes):** [Specific trace from decision to mission outcome]
**What it's actually serving (if no):** [Honest description]

### Rationalisation Risk Assessment
Is the mission being stretched to justify this decision? What is the evidence for or against?

### Genuine Pursuer Test
What would someone fully committed to this mission do? Does the proposal fit?

### Classification and Recommendation
**Classification:** On-Mission / Adjacent / Off-Mission / Mission-Expanding
**Recommendation:** [Proceed / Proceed with modification / Pause / Decline — with rationale]

---

## Notes

"Adjacent" and "Mission-Expanding" are not the same thing — adjacent means close but not serving the mission, while mission-expanding means the mission is genuinely growing. Be precise about which applies.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Mission alignment assessed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-identity-values-clarification` — Clarify the values behind the mission
  - `/s4h-decision-criteria-weighting` — Weight decisions against mission alignment
  - `/s4h-strategy-positioning` — Position strategy to serve the mission
  - **Done** — Wrap up and synthesise what we have so far
