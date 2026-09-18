---
name: s4h-writing-arc-design
description: "Maps and repairs character arcs and thematic arcs by aligning external plot events with internal change. Use when an arc feels unearned, a change feels sudden, or the ending doesn't land. Triggers: 'the arc feels unearned', 'arc design', 'the ending doesn't land', 'character arc', 'thematic arc', 'the change feels sudden', 'the character just changes at the end'."
---

# Writing: Arc Design

Arcs feel unearned when the external plot and internal change are independent — when the character changes because the story requires it, not because the events forced it. This is the most common arc failure, and it produces the most visceral reader response: "the character just suddenly becomes a different person." The reader is right. The change happened on a schedule, not as a consequence.

The fundamental principle: the external must create the conditions for the internal. The plot does not just happen *alongside* the character — it *acts on* the character in ways that make the internal change not just possible but necessary. The protagonist's wound must be pressed on, repeatedly, by the specific events of the plot. The defence must be made untenable by the story's demands. The arc endpoint is not the character deciding to change — it is the character having no remaining option except to change, or to break.

The ending is not the change. The ending is the consequence of the change. This distinction matters enormously: if the character's internal shift and the external resolution happen simultaneously, the causation is lost. The internal shift must precede the external resolution, making it possible. The reader needs to see the new belief or new capacity tested against the story's central problem — and the test must require exactly what the old self couldn't have provided.

---

## Your Process

**Step 1: Start State**
What is the character's belief, wound, and worldview at the story's opening? Be specific: not "she is closed off" but "she believes that needing people is weakness — a belief installed by her mother's abandonment when she was nine, which she has managed by becoming self-sufficient to a degree that reads as coldness." The start state must be specific enough to be testable: you should be able to ask of any scene "is this character acting from their opening belief?" and get a clear answer.

**Framing check:** Confirm the specific character and arc before continuing. State what you've identified — the character being analyzed, their apparent wound or core belief, and the arc endpoint as you understand it — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the character, their wound/starting belief, and the arc being examined]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: End State**
What has changed? What is the new belief? Again, be specific. The end state should be the direct answer to the wound — not its opposite (which would be naive), but the more complex truth that the wound prevented the character from seeing. "She believes needing people is weakness" → "She learns that need is not weakness if the person chosen to be needed is trustworthy." The end state is not a lesson or a moral — it is a lived understanding, demonstrated in action.

**Step 3: Pressure Points**
Map the specific events that force the internal change. These must be caused by the plot — they are not random events that happen to push buttons; they are the story's central events landing on the character's specific vulnerability. For each pressure point: what does it press? What does the character's defence do in response? Does the defence hold, or does it start to crack?

The arc requires at least three pressure points, and they should escalate: the first press is deflected, the second is harder to deflect, the third (the dark night) cannot be deflected at all.

**Step 4: External-Internal Alignment**
Map the parallel tracks:
- External: [inciting incident → complication → midpoint shift → dark night → climax]
- Internal: [defence holds → defence strained → defence fails → wound exposed → new belief tested]

Do the external events directly generate the internal states? Or are they running on parallel tracks that don't connect? The test: could a different character, with a different wound and different defence, move through the same external events and arrive at the same ending? If yes, the plot is not doing character work — it is plot for its own sake.

**Step 5: Thematic Argument**
What does the story argue about the world? Not a message or a moral — an argument: a claim about how things are, how they should be, or what the cost of a particular way of living is. The ending should resolve this argument — not necessarily answer it definitively, but test it at full strength and show what the story believes.

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

### Arc Map

**Start State:** [Belief / wound / worldview — specific and testable]

**End State:** [New belief — the wound's answer, not its opposite / how it is demonstrated in action]

**Pressure Points:**
1. [Event → what it presses → character response → does defence hold?]
2. [Event → what it presses → character response → does defence crack?]
3. [Event → what it presses → character response → defence fails]

**External-Internal Alignment:** [Map of parallel tracks + diagnosis of where they connect or diverge]

**Thematic Argument:** [What does the story claim? / Does the ending resolve it at full strength?]

**Arc Verdict:** [Earned / Unearned / Partially earned — specific diagnosis of what is missing]

---

## Notes

- The change must be earned by the pressure points, and the pressure points must be caused by the plot. Any link in this chain that is missing produces an unearned arc.
- Slow arcs are not unearned arcs. A character who changes gradually across a long work can be completely earned if each pressure point genuinely presses and the defence genuinely fails. The problem is not pace — it is causation.
- Pairs with `/s4h-writing-plot-structure` — the external structure is the mechanism that generates the pressure points; if the plot structure is broken, the arc cannot be earned.
- Pairs with `/s4h-writing-character-development` — the arc endpoint must flow from the wound and defence; you cannot design the arc without the character profile.
- Pairs with `/s4h-writing-scene-construction` when individual scenes are failing to deliver the pressure points — the architecture is right but the scenes aren't performing their function.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Arc designed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-plot-structure` — Structure the plot within the arc
  - `/s4h-writing-character-development` — Develop characters to serve the arc
  - `/s4h-narrative-tension-mapping` — Map tensions the arc must resolve
  - **Done** — Wrap up and synthesise what we have so far
