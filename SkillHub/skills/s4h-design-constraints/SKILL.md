---
name: s4h-design-constraints
description: "Uses constraints productively — maps hard limits, soft preferences, and how the tightest constraints define the solution space. Triggers: 'what are the design constraints', 'map the constraints', 'what are we working within', 'what's fixed', 'constraint-driven design', 'what does the solution space look like', 'working within limits'."
---

# Design: Design Constraints

Every design problem has a solution space — the set of forms that could satisfy the need. Constraints are not what prevent good design; they are what define the problem precisely enough to be solved. A problem with no constraints has no solution because it has no shape. The designer's task is to understand the constraint set completely: which limits are genuinely fixed, which are preferences that could move, and what territory they collectively leave open.

Christopher Alexander's work on pattern languages makes this explicit: every good design form is a response to a specific set of forces in tension. Understanding those forces — what they require, where they conflict, where they align — is how a designer finds the form that resolves them. Jony Ive's approach at Apple was similar: start with the hardest constraints (manufacturing tolerances, material properties, thermal dissipation) and let design decisions cascade from there. The hardest constraint is often the most generative.

This skill maps the full constraint set, classifies each constraint by hardness, surfaces the interactions between them, and identifies where the productive design space lies within the boundaries they collectively draw.

---

## Your Process

**Step 1: Elicit the Full Constraint Set**
List every known constraint. Do not classify or judge yet — just enumerate. Include:
- Technical constraints (what the medium or material allows)
- Physical constraints (size, weight, space, material properties)
- Economic constraints (cost, time, resources)
- Regulatory or legal constraints (requirements that must be met)
- Organisational constraints (what the team, system, or process can support)
- User constraints (what users can understand, do, or accept)
- Aesthetic or brand constraints (what must be consistent with existing forms)

**Framing check:** Confirm the design context and the constraint domain before continuing. State what you've identified — the thing being designed and the primary constraint types in play — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the design context and constraints]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Classify by Hardness**
For each constraint, classify:
- **Hard:** genuinely fixed — physical law, signed contract, technical impossibility, binding regulation
- **Soft:** real but negotiable — someone's preference, a policy that could be changed, a convention rather than a rule
- **Assumed:** stated as a constraint but never tested — habit, fear, or unknown origin

For each soft or assumed constraint, note what it would take to move it.

**Step 3: Map Constraint Interactions**
Some constraints compound: two constraints together rule out more territory than either does alone. Some constraints conflict: they cannot be satisfied simultaneously at full strength, requiring a trade-off. Some constraints are redundant: satisfying one automatically satisfies another.

Identify:
- **Compounding pairs:** constraints that together eliminate a class of solution
- **Conflicting pairs:** constraints that create a trade-off requiring a design decision
- **Redundant constraints:** where satisfying one satisfies another for free

**Step 4: Find the Tightest Constraint**
The tightest genuine constraint is the one with the smallest solution set. It determines where to start design. It is usually the most generative constraint — because it narrows the field to what's actually possible and often points toward what's uniquely possible within those limits.

Identify the tightest constraint or constraint pair. Ask: what does design look like if this constraint is accepted fully and treated as a design requirement?

**Step 5: Map the Solution Space**
Given the hard constraint set, describe the territory that remains open. What categories of solution are viable? What are the dimensions of variation within that territory? Where are the most interesting sub-regions — areas with multiple viable directions, or areas where constraints interact in generative ways?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being designed and which constraints seem most significant — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Solution space focus** — Skip individual constraint analysis; describe the territory directly
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Constraint inventory:**

| Constraint | Domain | Classification | Notes |
|---|---|---|---|
| [Constraint] | [Domain] | Hard / Soft / Assumed | [What it would take to move, if soft] |

**Constraint interactions:**

| Pair | Type | Effect |
|---|---|---|
| [A] + [B] | Compounding / Conflicting / Redundant | [What this means for design] |

**Tightest constraint:**
> [State it. What category of design decisions it forces.]

**Solution space:**
[3–5 sentences describing the design territory that remains viable. What categories of solution are open, what dimensions of variation exist, and where the most interesting territory is.]

**Design direction implied:**
> [One to two sentences. Given this constraint set, what kind of solution is it pointing toward?]

---

## Notes

This skill is a close neighbour of `/s4h-constraint-hardness-testing`, which focuses on testing whether individual constraints are actually real. Design constraints goes further: it treats the full constraint set as a system and asks what solution space it collectively defines. Use hardness-testing when you need to challenge a specific constraint; use this skill when you need to understand how the full constraint map shapes the design problem.

The most common error is treating all constraints as equally hard and using them to justify not exploring territory that's actually open. Separate the hard from the soft before concluding that a class of solution is impossible.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Constraints mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-design-user-needs` — Revisit what the user actually needs within this solution space
  - `/s4h-design-iteration` — Begin the design cycle within the solution space you've mapped
  - `/s4h-constraint-rule-inversion` — Flip the tightest constraint into a creative driver
  - **Done** — Wrap up and synthesise what we have so far
