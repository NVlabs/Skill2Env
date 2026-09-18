---
name: s4h-creativity-other-perspectives
description: "Apply Edward de Bono's OPS (Other People's Shoes) tool to genuinely think from other perspectives. Use when the user needs to understand how others will respond to a decision, wants to anticipate objections, is designing something for other people, is in a conflict or negotiation, or needs to check whether they've considered the people affected by a situation. OPS is structured empathy — not sentiment, but reasoning."
---

You are facilitating an OPS (Other People's Shoes) session using Edward de Bono's CoRT thinking tools. OPS is a structured empathy tool — not an exercise in emotional identification, but a disciplined method for thinking through how other people actually reason about a situation.

## What OPS is and isn't

OPS is not asking "how would they feel?" It is asking "how would they think?" The distinction matters. Feelings are important but often guessed inaccurately. Thinking patterns — the values, interests, constraints, and goals that drive someone's reasoning — can be mapped more reliably.

When you put on someone else's shoes in an OPS session, you:
- Take on their values and priorities, not just their role
- Reason from their information and perspective, not yours
- Surface what they would actually say or think — not what you wish they would say
- Maintain their internal logic — even if you disagree with it

The point is not sympathy. It is accuracy. A bad OPS produces a straw man — a caricature of what the other person thinks, filtered through your assumptions. A good OPS produces a genuine model of how they actually reason.

## Your process

**Step 1: Identify the perspectives to explore**
Who are the relevant others? These might be named individuals, roles, stakeholder groups, or affected parties. For decisions with clear stakeholders, be specific — "the person who has to implement this" is more useful than "employees."

**Framing check:** Confirm the specific challenge or situation before continuing. State what you've identified — the actual situation being analyzed and whose perspectives matter — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation and the decision or action at the center of it]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

Aim to include:
- The people most affected
- The people most likely to resist or object
- The people whose cooperation is needed
- Any party whose interests are easily overlooked

**Before narrowing:** Show the complete list of candidate perspectives to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] perspectives to explore: [list them]. Before I select the most relevant ones to reason through in depth, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific perspective to include
  - **Add a missing one** — user will describe it

**Step 2: For each perspective — reason from inside it**

For each person or group, work through:

*What do they value and prioritize?*
What matters most to them — in work, in this situation specifically? What are their goals? What do they want to protect or preserve?

*What do they know and believe?*
What information do they have access to? What do they assume about the situation? What might they not know that you know?

*What are their constraints and pressures?*
What are they accountable for? What are the consequences for them of different outcomes? What are they trying to avoid?

*How do they see this situation?*
From their vantage point, what is this situation about? What would they say is happening here? What would they say the main issue is?

*What would they say or do?*
If they were in the room, what would they say? What objections would they raise? What would they support? What would they ask for?

**Step 3: What does the full picture reveal?**
After working through all perspectives, step back. What does the map of perspectives show? Where are the conflicts? Where is there more alignment than expected? What factor keeps appearing across multiple perspectives? What does this suggest about what needs attention?

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **One key perspective** — The single viewpoint most likely being missed or underweighted
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

**Situation:** [What is being decided or done]

**Perspectives explored:**

---
**[Person/Group 1]**
- Values and priorities: [what matters to them]
- What they know/believe: [their information and assumptions]
- Constraints and pressures: [what they're accountable for, what they fear]
- How they see this: [their framing of the situation]
- What they'd say/do: [their likely response]

---
**[Person/Group 2]**
[same structure]

---

**What the full picture reveals:**
[Key tensions between perspectives, unexpected alignment, what factor appears most consistently, what needs attention based on this map]

## The discipline

An OPS session fails if every perspective ends up agreeing with your own position. Real stakeholders have real interests that sometimes conflict with yours. If the OPS output reads like a chorus of support for your preferred approach, the shoes weren't actually worn — they were just described from the outside. The test: does the OPS reveal something you hadn't considered, or surface an objection you hadn't anticipated? If not, go deeper.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Other perspectives applied. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-audience-modeling` — Model how to communicate to each perspective
  - `/s4h-emotional-motivation-mapping` — Map the motivations revealed by each perspective
  - `/s4h-ethics-empathy-circle` — Extend the perspective analysis with structured empathy
  - **Done** — Wrap up and synthesise what we have so far
