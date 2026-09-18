---
name: s4h-strategy-timing
description: "Analyzes whether to act now or wait, reads your opponent's rhythm, and identifies trigger conditions for the right moment. Triggers: 'when should I act', 'timing analysis', 'is now the right moment', 'should I wait', 'when to launch', 'when to make my move', 'is the window closing', 'am I too early', 'am I too late'."
---

# Strategy: Timing

Miyamoto Musashi opens *The Book of Five Rings* with a meditation on timing: "Timing exists in everything." His insight is not simply that timing matters — it is that timing must be actively read rather than passively experienced. A swordsman who ignores his opponent's rhythm and attacks on his own preferred schedule will find the interval closed. A swordsman who reads when the opponent is overextended, committed, or off-balance will find the interval open.

Sun Tzu's complementary metaphor: "Water shapes its course according to the nature of the ground over which it flows; the soldier works out his victory in relation to the foe he is facing." Water does not insist on a fixed form. It adapts to the terrain continuously. The question is never simply "should I act?" — it is: "does the current moment give me an advantage that waiting would not compound, or does waiting improve conditions beyond what action now delivers?"

Both Musashi and Sun Tzu agree on one further principle: the opponent's timing is as important as your own. Attacking when your opponent is preparing is different from attacking when they are overextended. The interval is not a point on your schedule; it is a relationship between two rhythms.

---

## Your Process

**Step 1: Conditions favoring action now**
What is true right now that will not be true later? What windows are closing — competitor moves, decision-maker availability, market conditions, relationships, information advantages that decay? What cost do you pay for each week of delay?

**Framing check:** Confirm the specific timing situation before continuing. State what you've identified — the action being considered, the actor, the opponent or environment creating pressure, and the core temporal tension — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the timing situation — the action, who is acting, what is creating the window or pressure, and what the core timing trade-off is]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Conditions favoring waiting**
What conditions are improving with time on your side? What intelligence is still missing that would increase your confidence? What resources are still being built? What opponent conditions are approaching that would favor you (an opponent is about to be overextended, a regulatory decision is pending, a key hire is coming)?

**Step 3: Situation type**
Classify the situation:
- **Flowing** — conditions are changing rapidly; the window is finite and shortening. Waiting compounds the disadvantage. Act or lose the window.
- **Stable** — conditions are largely fixed; time is not an enemy. Patience is strategic. The cost of acting too early outweighs the cost of delay.
- **Turning** — conditions are about to shift in a direction you can read. The question is not whether to act but exactly when the shift creates the optimal moment.

**Step 4: Opponent's rhythm**
Musashi's "interval": where is your opponent in their cycle? Are they overextended, mid-commitment, distracted, preparing, or at ease? When are they most off-balance? The best moment to act is rarely when you are most ready — it is when they are most unable to respond effectively.

**Step 5: Cost asymmetry**
What is the cost of acting too early? What is the cost of acting too late? Which error is more recoverable? In most situations, one error is reversible and one is not — name which, and let that asymmetry weight the timing decision.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one aspect of this analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Timing Analysis

**Conditions Favoring Action Now**
[Windows closing, costs of delay, time-sensitive advantages]

**Conditions Favoring Waiting**
[Improving conditions, intelligence gaps, opponent developments approaching]

**Situation Type**
[Flowing / Stable / Turning — with brief rationale]

**Opponent's Rhythm**
[Where they are in their cycle, when they are most off-balance, what the interval looks like]

**Cost Asymmetry**
[Cost of acting too early vs. too late — which error is less recoverable]

**Recommended Timing**
[Act now / Wait for trigger / Wait for specific condition] — with trigger conditions stated explicitly: "Act when X occurs" or "Do not act before Y is true"

---

## Notes

Timing decisions depend heavily on intelligence quality — pair with `/s4h-strategy-intelligence` when your picture of the opponent's current state is uncertain. Timing and position interact: sometimes the right timing is simply "when your position is ready" — pair with `/s4h-strategy-positioning` when that's the case. For flowing situations with closing windows, force economy becomes critical — pair with `/s4h-strategy-force-economy` to identify the minimum effective action before the window closes.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Timing mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-positioning` — Execute the position at the right time
  - `/s4h-decision-premortem-analysis` — Stress-test the timing assumptions
  - `/s4h-temporal-timing-analysis` — Validate the timing with temporal analysis
  - **Done** — Wrap up and synthesise what we have so far
