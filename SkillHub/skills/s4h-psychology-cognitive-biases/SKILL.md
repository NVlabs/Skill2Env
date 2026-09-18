---
name: s4h-psychology-cognitive-biases
description: "Diagnose which cognitive biases are actively distorting thinking in a specific situation. Not a laundry list — a targeted diagnostic. Triggers: 'what biases are at play', 'are we thinking clearly', 'what am I missing', 'bias check', 'cognitive bias', 'am I being objective', 'are we rationalizing', 'what's distorting this decision'."
---

# Psychology: Cognitive Biases

Most biased thinking feels like clear thinking. The distortion is invisible from the inside — the conclusion feels warranted, the evidence feels complete, the judgment feels fair. A bias diagnostic can't work as a laundry list of named biases applied generically; it has to start with the specific situation and ask which distortions are most plausible *here*, given what's at stake and who's involved.

---

## Your Process

**Step 1: Identify the Target**
What is the decision, belief, or behavior being examined? Be specific. "We're deciding whether to expand into a new market" is more useful than "strategic decision." The target shapes which biases are most likely to be active.

**Framing check:** Confirm the specific situation before continuing. State what you've identified — the actual decision, belief, or behavior being examined and the stakes or parties involved — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific situation being examined]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Scan for Active Bias Categories**
Assess which of the following are most plausible given this specific situation:

- **Confirmation bias** — Selectively seeking, interpreting, or remembering information that supports an existing belief. Live when: there's already a preferred conclusion; when evidence has been gathered by someone with a stake in the outcome.
- **Availability heuristic** — Overweighting vivid, recent, or easily recalled examples when estimating likelihood or importance. Live when: the decision involves frequency or probability; when a salient recent event (success or failure) is in view.
- **Anchoring** — Over-relying on the first piece of information encountered, which shapes all subsequent estimates. Live when: numbers are involved (prices, timelines, forecasts); when someone presented an initial figure before the estimate was made.
- **Sunk cost fallacy** — Weighting past investment (time, money, effort) in a decision about the future. Live when: the question involves whether to continue something already started; when there's emotional investment in prior work.
- **In-group bias** — Overvaluing opinions, work, or proposals from people perceived as similar or belonging to the same group. Live when: evaluating work from within the team; when there's social pressure to agree.
- **Optimism bias** — Underestimating risk, cost, and time for one's own plans while accurately assessing them for others. Live when: making plans about future performance; when someone has emotional investment in a positive outcome.
- **Planning fallacy** — Systematically underestimating time, cost, and complexity for future tasks, even when past experience should calibrate estimates down. Live when: project planning, timeline estimation, budget setting.
- **Hindsight bias** — Seeing past events as more predictable than they were; "we should have known." Live when: reviewing failures or post-mortems; can distort who is blamed and what was actually knowable.
- **Status quo bias** — Overvaluing the current state simply because it's current; experiencing change as loss. Live when: evaluating options that require changing course; when "do nothing" is being treated as riskless.

**Before narrowing:** Show the complete set of plausible biases identified in Step 2 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] potentially active biases. Before I select the most significant to diagnose in depth, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific bias to include
  - **Add a missing one** — user will describe it

**Step 3: Diagnose the Specific Distortion**
For each active bias, describe how it's operating in this specific situation — not generically, but concretely. "Confirmation bias is operating because the market research was commissioned after the decision to expand was informally made, meaning the team was implicitly looking for validation, not evidence."

**Step 4: Recommend the Counter-Move**
For each active bias, recommend a specific corrective action. Generic counter-moves ("seek disconfirming evidence") are insufficient. The counter-move should be concrete and executable: "Have someone not invested in expansion scope the contrary case for the new market before reviewing the research."

**Step 5: Assess Overall Distortion Risk**
How much is the current thinking likely to be off-course? Low (biases present but manageable), Medium (specific decisions may be materially distorted), or High (the overall analysis is likely to be significantly wrong in a directional way).

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full diagnostic** — Complete all steps, full reasoning shown
  - **Top biases only** — Surface the two or three most live biases with counter-moves, skip the rest
  - **One specific bias** — Focus on a single bias category I've already identified
  - **Refine the situation** — Clarify what's being decided before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Situation
[Restate the decision/belief/behavior being analyzed in one sentence]

### Active Biases

| Bias | How it's operating here | Counter-move |
|------|------------------------|--------------|
| [Bias name] | [Specific mechanism in this situation] | [Concrete corrective action] |
| ... | ... | ... |

### Biases Assessed and Not Active
[Brief note on which categories were considered but are not live for this situation — this shows the scan was real, not a list]

### Overall Distortion Risk
**[Low / Medium / High]** — [One sentence explaining the overall assessment and what it means for the decision]

---

## Notes

This skill is a diagnostic, not a debunking tool. The goal is not to dismiss a decision or belief, but to surface where the reasoning may have been contaminated so it can be strengthened. Biases are not character flaws — they're systematic features of human cognition that operate in everyone's thinking, including the person running this diagnostic.

Use psychology-heuristics when the question is specifically about fast intuitive thinking and when to trust or override it. Use psychology-motivation when the behavior you're observing seems to serve an unstated need. Cognitive biases and motivated reasoning often co-occur — check both when the stakes are high.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Cognitive biases identified. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-logic-fixer` — Correct the bias-induced reasoning errors found
  - `/s4h-decision-criteria-weighting` — Re-weight decision criteria with bias removed
  - `/s4h-ethics-bias-check` — Check the ethical implications of the biases identified
  - **Done** — Wrap up and synthesise what we have so far
