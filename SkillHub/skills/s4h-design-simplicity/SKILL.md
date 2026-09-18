---
name: s4h-design-simplicity
description: "Applies the design principle of removing rather than adding — finding the form that does exactly what is needed, nothing more. Triggers: 'simplify this', 'remove what's unnecessary', 'it's too complicated', 'what can we cut', 'reduce the design', 'it's bloated', 'make it simpler', 'find the essential form', 'what's really needed here'."
---

# Design: Simplicity

The hardest design work is not adding — it is knowing what to remove. Every element that is added must justify its presence. Every element that remains without justification is waste: it adds cognitive load, maintenance burden, visual noise, and the implicit message that the designer didn't finish the job.

Dieter Rams' tenth principle is the most demanding: good design is as little design as possible. He doesn't mean sparse aesthetics. He means form that is completely fit for purpose without excess — nothing that doesn't do work, nothing that does work that isn't needed. Rams reached this point by removing things from Braun products until removing anything more would break function. The test is not "is this minimal?" but "is this necessary?"

Edward Tufte applies the same principle to information design: data-ink ratio. Of all the ink on the page, what fraction encodes actual data? Everything else is chartjunk — it consumes attention without transferring information. Remove it. The principle extends to every designed artefact: of all the elements in this design, what fraction serves the function? The rest can go.

The difficulty is that subtraction feels destructive. Features that were added with reasons seem like they should stay. This skill provides the discipline to test each element against function and remove what doesn't pass.

---

## Your Process

**Step 1: Enumerate Every Element**
List every element in the current design. Be exhaustive. For a product: features, controls, labels, states. For a document: sections, headings, callouts, annotations, formatting choices. For a UI: screens, interactions, fields, error states, modals, navigation items. For a system: components, interfaces, parameters, configurations.

If the list is long, group by layer or component before enumerating.

**Framing check:** Confirm the design and the purpose it should serve before continuing. State what you've identified — the thing being simplified and its primary function — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the design and its purpose]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Define the Function**
State the primary function precisely: what is this design for? What job does it do? Everything else is subordinate to this. An element that serves a secondary function at the cost of obscuring the primary function is removing value, not adding it.

Also define: who is the user, what is the context of use, and what does success look like? These define the evaluation frame for every element.

**Step 3: Test Each Element**
For every element identified in Step 1, apply this test:

**The removal test:** If this element were removed, would the design fail to perform its primary function?
- **Yes:** Load-bearing — keep it.
- **No:** Candidate for removal — mark it.

For candidates, also ask:
- Does it serve a genuine secondary function that is worth its cost in complexity?
- Is it serving the user, or serving the designer's desire to seem thorough?
- Would a user notice it was gone? Would they care?

**Step 4: Identify Complexity Sources**
Some elements are individually justifiable but collectively produce unnecessary complexity. Identify:
- **Redundant elements:** two elements that do the same job
- **Over-specified elements:** an element that is more elaborate than its function requires
- **Fear-driven elements:** elements added because removing them felt risky, not because they're needed (extra confirmation dialogs, backup modes, fallback text, explanatory labels for things that should be self-evident)
- **Legacy elements:** things that existed for a reason that no longer applies

**Step 5: Apply Subtraction**
Remove. Start with the clearest candidates — elements that fail the removal test and have no secondary function. Then move to the more difficult calls: elements that have marginal secondary value but add meaningful complexity.

For each removal, state what it was doing and why it's not needed. This is the reasoning that prevents the elements from drifting back in future iterations.

**Step 6: Test the Simplified Form**
State what the simplified design consists of. Apply the function test: does it still do the primary job completely? If not, identify which removal went too far and restore only that element.

The simplified form should feel obvious in retrospect — like the only form the thing could have taken.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being simplified and what its core function is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Work through every element with reasoning
  - **Key removals only** — Identify the most significant things to cut, without full inventory
  - **Complexity diagnosis** — Focus on identifying sources of complexity rather than a removal list
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Design under review:** [Name and primary function in one sentence]

**Element inventory:**

| Element | Current function | Removal test | Verdict |
|---|---|---|---|
| [Element] | [What it does] | Breaks function / Doesn't break / Unclear | Keep / Remove / Reduce |

**Complexity sources identified:**
- [Redundancy / Over-specification / Fear-driven / Legacy] — [specific element] — [reasoning]

**What to remove:**
[List of elements to remove with one-line rationale for each]

**What remains:**
[The simplified form described in concrete terms]

**Function test on simplified form:**
> [Does the simplified design still do the primary job completely? Yes/No — with reasoning.]

**What the simplification achieves:**
[1–2 sentences on what was gained by removing these elements — reduced load, clearer signal, lower maintenance cost, etc.]

---

## Notes

The most common failure mode is treating simplicity as an aesthetic goal rather than a functional one. Removing a visible button and replacing it with a hidden gesture isn't simpler — it's differently complex, usually worse. Simplicity means less total complexity, not redistributed complexity.

This skill is closely related to `/s4h-aesthetic-simplicity-analysis`, which applies simplicity principles to visual and aesthetic form specifically. Design simplicity is broader: it applies to features, information architecture, interactions, and any designed system, not just appearance. For removing scope before building, see `/s4h-constraint-scope-reduction`.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Simplified. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-design-iteration` — Test whether the simplified design still satisfies users
  - `/s4h-aesthetic-simplicity-analysis` — Apply simplicity analysis specifically to the visual form
  - `/s4h-design-user-needs` — Verify the simplified design still serves the real need
  - **Done** — Wrap up and synthesise what we have so far
