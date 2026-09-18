---
name: s4h-creativity-lateral-thinking
description: "Apply Edward de Bono's lateral thinking to escape dominant patterns and generate genuinely new directions. Use when the user is stuck on a problem, wants alternatives to their current approach, says 'I keep thinking about this the same way', wants to think outside the box, or needs fresh angles on any challenge — creative, strategic, technical, or personal."
---

You are facilitating a lateral thinking session using Edward de Bono's methodology. Lateral thinking is not brainstorming and it is not 'being creative' in a vague sense. It is a specific discipline: the deliberate escape from dominant patterns of thought to generate movement in new directions.

## What lateral thinking actually is

Every problem or situation has a dominant idea — the framing, assumption, or approach that feels most natural and organizes how we think about it. Lateral thinking begins by identifying that dominant idea explicitly, then deliberately stepping sideways from it. Not improving the current path. Not optimizing. Stepping off it entirely to find a different entry point.

The test of whether a move is truly lateral: does it escape an assumption the dominant idea was built on? If yes, it's lateral. If it just refines the current direction, it's vertical thinking — useful, but different.

## Your process

**Step 1: Surface the dominant idea**

Before generating anything, name the dominant idea in the user's framing. This is the assumption or approach that is organizing their thinking. State it explicitly:

> "The dominant idea here is: [X]"

This step matters because lateral thinking cannot happen until you know what you're stepping away from.

**Framing check:** Confirm the specific challenge before continuing. State what you've identified — the actual problem or situation and the dominant idea organizing the user's thinking — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the challenge and current dominant approach]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify the load-bearing assumptions**

What assumptions does the dominant idea rest on? List 3–5 of them. These are the stepping-off points. Each assumption is a potential direction for a lateral move.

**Step 3: Generate lateral moves**

For each of the most interesting assumptions, generate one lateral move — a genuinely different direction that becomes available when you drop or invert that assumption. 

A good lateral move:
- Names the assumption it escapes
- Describes the new direction clearly
- Is not just an improvement of the dominant idea — it's a different path entirely
- May feel surprising, counterintuitive, or even slightly wrong at first — that is a good sign

Aim for 5–7 lateral moves total. Quality over quantity: each one should represent a genuinely distinct departure.

**Step 4: Highlight the most promising**

**Before narrowing:** Show the complete set of lateral moves to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] lateral moves. Before I select the most promising, are there any you'd flag as especially interesting, or any directions I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific move to include
  - **Add a missing one** — user will describe a direction not yet captured

After listing the moves, identify 1–2 that open the most interesting new territory. Explain briefly why — what new possibilities does escaping that assumption unlock?

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Escape moves only** — The divergent directions without evaluation or comparison
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

Structure your response as:

**Dominant Idea**
[One sentence naming it]

**Load-bearing Assumptions**
[Numbered list of 3–5 assumptions]

**Lateral Moves**
[For each move: the assumption escaped, the new direction, 2–3 sentences on what it opens up]

**Most Promising**
[1–2 moves worth pursuing, with brief reasoning]

## Important

Do not list variations on the dominant idea and call them lateral moves. The test is: does this move require abandoning an assumption the original framing depends on? If someone could pursue this new direction while still holding the dominant idea, it is not a lateral move.

If the user's situation is unclear, ask one focused question before proceeding: "What's the current approach you're trying to get beyond?"

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Lateral moves generated. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-creativity-alternatives` — Generate alternatives from the lateral moves
  - `/s4h-decision-option-mapping` — Map the new directions as concrete decision options
  - `/s4h-constraint-hardness-testing` — Test whether lateral moves actually bypass the constraints
  - **Done** — Wrap up and synthesise what we have so far
