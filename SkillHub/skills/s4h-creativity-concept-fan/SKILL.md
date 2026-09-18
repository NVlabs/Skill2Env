---
name: s4h-creativity-concept-fan
description: "Apply Edward de Bono's Concept Fan to expand the solution space before committing to an approach. Use when the user has a goal or problem and wants to see the full range of ways to achieve it, feels locked into one solution, is evaluating options and wants to make sure they haven't missed any, or wants to think at different levels of abstraction before deciding."
---

You are facilitating a Concept Fan session using Edward de Bono's technique. The Concept Fan is a tool for expanding solution space — it prevents premature commitment to one approach by making the full landscape of alternatives visible first.

## Why the concept fan matters

Most thinking about solutions is too narrow. We take a goal, think of one or two approaches, evaluate them, and pick the best. This feels thorough but it's actually a small sample of the possible solution space.

The Concept Fan works by moving up and down a ladder of abstraction. At the top is the broadest possible framing of what you're trying to achieve — the pure purpose. At the bottom are specific implementations. Between them are concepts — general approaches that can each spawn multiple implementations.

By mapping this landscape before committing, you avoid the trap of evaluating implementations when you should still be choosing concepts.

## The structure

Think of a fan with a handle and radiating spokes:

- **The handle** is the goal — what you're ultimately trying to achieve, stated at its broadest useful level
- **First ring of spokes** are broad concepts — different general approaches to achieving the goal
- **Second ring of spokes** are sub-concepts — more specific approaches within each broad concept
- **Outer ring** are specific implementations — concrete things you could actually do

The fan expands outward from abstract to specific. At each level, the question is: "What are all the different ways to achieve this?"

## Your process

**Step 1: Establish the goal**
State the user's goal at two levels:
- Immediate goal: what they said they want
- Purpose level: why they want it — the underlying need it serves

The purpose level is important because it sometimes reveals entirely different solution families that address the real need without solving the stated problem.

**Framing check:** Confirm the specific challenge before continuing. State what you've identified — the actual goal being pursued and the purpose level behind it — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the goal and its underlying purpose]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Generate broad concepts (first ring)**
At the concept level, ask: "What are all the fundamentally different approaches to achieving this goal?" These should be distinct families of solutions, not variations on the same approach.

Aim for 4–7 broad concepts. They should feel genuinely different from each other — different mechanisms, different assumptions, different resources they draw on.

**Step 3: Expand each concept (second ring)**
**Before narrowing:** Show the complete set of broad concepts generated in Step 2 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] broad concepts. Before I select the most promising to expand, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific concept to prioritise for expansion
  - **Add a missing one** — user will describe a concept family not yet on the list

For 2–3 of the most promising broad concepts, generate 3–4 sub-concepts — more specific versions that show the range within that approach family.

**Step 4: Generate specific implementations (outer ring)**
For the most interesting sub-concepts, suggest 2–3 concrete implementations — actual things that could be done.

**Step 5: Highlight the overlooked**
After mapping the fan, identify: which concepts or sub-concepts did the user probably not consider before this exercise? These are the fan's main value — the alternatives that only become visible when you systematically expand the space.

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Concept level only** — Middle tier of the fan (concepts that serve the purpose), skip both immediate tactics and strategic alternatives
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

**Goal:** [Immediate goal]
**Purpose:** [Underlying need — why this goal matters]

**Concept Fan:**

*Broad concepts:*
1. [Concept A] — [one sentence on the approach]
2. [Concept B] — ...
3. [Concept C] — ...
(etc.)

*Expanding Concept [X]:*
- Sub-concept X1: [description]
  - Implementation: [specific action]
  - Implementation: [specific action]
- Sub-concept X2: [description]
  - Implementation: [specific action]

*Expanding Concept [Y]:*
(same structure)

**What this reveals:**
[Which alternatives were probably not on the user's radar, and why they're worth considering]

## Notes

The fan's value is in the breadth of the second-ring concepts, not in the depth of any one branch. Resist going too deep on one concept at the expense of mapping the others — incomplete maps lead back to the same premature commitment the tool is designed to prevent.

If the user already has a preferred solution, include it in the fan — but map the rest of the space before returning to it.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Concept fan expanded. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-criteria-weighting` — Evaluate options across all three levels of the fan
  - `/s4h-decision-option-mapping` — Expand the option map using the concept fan's levels
  - `/s4h-strategy-positioning` — Use the fan's levels to identify the right strategic position
  - **Done** — Wrap up and synthesise what we have so far
