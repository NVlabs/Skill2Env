---
name: s4h-narrative-tension-mapping
description: "Finds or creates the tension that makes communication worth paying attention to. Use when asked 'this feels flat', 'no one's engaging', 'make this compelling', 'find the tension', 'what's the story here', or 'add stakes'."
---

# Narrative Tension Mapping

Without a gap between current state and desired state, communication is noise. Tension is not drama or manufactured urgency — it is the honest articulation of what is wrong, at risk, or missing. Audiences disengage not because a topic is unimportant but because the communication fails to make the gap visible and real. The tension must be felt before the solution can land.

---

## Your Process

**Step 1: State the Communication**
What is the communication — its subject, its argument, its ask? State it plainly before analyzing what's missing.

**Framing check:** Confirm the specific communication before continuing. State what you've identified — the actual content being analyzed, its intended audience, and its core ask — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the communication, its audience, and its intended ask]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Locate the Tension**
Ask: what is wrong, at risk, or missing in the world this communication addresses? That is the tension. It should be a gap between where things are and where they need to be. If you can't find it, note that — it's diagnostic.

**Step 3: Test for Genuine Tension**
If no tension is apparent: ask why this communication matters at all. If the honest answer is "it doesn't," that is the real problem to solve — the communication should not exist yet or should be restructured around something that does matter.

**Step 4: Test for Audience Relevance**
Is this tension real to the audience, or only to the sender? A tension that only the sender feels is not yet a tension — it requires first making the audience care about the domain before the gap can register.

**Step 5: Surface It Plainly**
State the tension explicitly, early, without burying it in qualifications. The single most common failure: putting the tension in the middle or end after extensive context-setting. Audiences stop paying attention before they reach it.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Central tension only** — The one conflict that makes this worth attending to
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Tension Statement**
- Current state: [what is true now]
- Desired state: [what needs to be true]
- Gap: [what separates them]
- Stakes: [what happens if the gap persists]

**Audience Relevance:** [real to audience? Y/N + explanation]

**Opening Line:** [how to open with the tension, not context]

**Diagnosis (if no tension found):** [what the absence of tension means for the communication]

---

## Notes

Tension is not negativity. Stating what is at risk is not pessimistic — it is the precondition for the audience to care about your resolution. A solution without a stated problem is just noise.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Tensions mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-arc-design` — Design the arc to resolve the mapped tensions
  - `/s4h-writing-plot-structure` — Structure the plot around the tension points
  - `/s4h-decision-premortem-analysis` — Stress-test whether the tensions actually resolve
  - **Done** — Wrap up and synthesise what we have so far
