---
name: s4h-narrative-structure-mapping
description: "Applies story architecture to any communication — proposal, presentation, strategy doc — so it moves people rather than informing them. Use when asked to 'structure this as a story', 'make this compelling', 'narrative arc', 'how do I present this', or 'story structure'."
---

# Narrative Structure Mapping

Facts don't change behavior; narrative does. The same information delivered as a story is more persuasive, more memorable, and more likely to produce action than the same information delivered as a report. Three-act structure works because it mirrors how humans process change: there is a world, the world is disrupted, a new world becomes possible. Any communication that needs to move people — not just inform them — benefits from this architecture.

---

## Your Process

**Step 1: Identify Audience and Current Belief**
Who is the specific audience? What do they already believe about this situation? You are not starting from zero — you are moving them from where they are.

**Framing check:** Confirm the specific communication and its audience before continuing. State what you've identified — the actual content being structured and who it is for — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific communication, its audience, and the intended outcome]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Find the Tension**
What is the gap between current state and desired state? If there is no tension, there is no story. The tension must be real to the audience, not just to the sender.

**Step 3: Map Three-Act Structure**
- **Act 1 — Setup:** The world as it is. Establish the context the audience already inhabits. Then: the disruption — something has changed, is at risk, or is being missed.
- **Act 2 — Confrontation:** The struggle. What makes resolution non-obvious? What are the stakes if the problem isn't addressed? This is where complexity lives.
- **Act 3 — Resolution:** The new world. What becomes possible if the audience acts or accepts the argument? Make it concrete.

**Step 4: Locate the Transformation**
What must the audience feel or understand at the turning point that makes the resolution feel earned rather than asserted? This is the moment of insight — the structural heart of the communication.

**Step 5: Place Evidence Inside the Story**
Data supports narrative; it does not replace it. Assign each data point or proof element to its place in the arc — evidence that arrives before the audience is ready to receive it doesn't land.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Missing elements only** — What story components are absent from this communication
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Audience:** [who + current belief]

**Tension:** [current state → desired state → gap]

**Narrative Outline**

| Section | Content | Function |
|---------|---------|---------|
| Hook | | Opens with tension, not context |
| Setup | | World as audience knows it |
| Disruption | | What has changed or is at risk |
| Confrontation | | Stakes and complexity |
| Turning Point | | The insight that makes resolution possible |
| Resolution | | The new world; what becomes possible |
| Call to Action | | Specific ask |

**Where Data Fits:** [data point → narrative position]

---

## Notes

The most common failure is leading with resolution — announcing the answer before the audience has felt the tension. Make them need the answer before you give it.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Narrative structure mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-restructure` — Restructure based on what the structure mapping found
  - `/s4h-narrative-tension-mapping` — Map tension points within the structure
  - `/s4h-writing-arc-design` — Design the arc from the structure map
  - **Done** — Wrap up and synthesise what we have so far
