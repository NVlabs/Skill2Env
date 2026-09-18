---
name: s4h-design
description: "Entry point for the design thinking toolkit. Routes to the right design skill based on your situation. Use when you say 'design', 'user needs', 'what do people actually want', 'design constraints', 'prototype and iterate', 'simplify this', 'remove what's unnecessary', or want design thinking applied without knowing which specific tool fits."
---

# Design

Applies design thinking to problems of form, function, and fit — finding what people actually need, using constraints productively, shaping through iteration, and cutting to the essential. Diagnoses what kind of design work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Find what people actually need, beneath what they say they want | user-needs |
| Map hard limits versus soft preferences and understand the solution space they define | design-constraints |
| Structure a feedback loop between making and learning | iteration |
| Remove what's unnecessary and find the essential form | simplicity |

## Routing Decision

**Framing check:** Confirm the design situation and the core question before routing. State what you've identified — the object being designed and the problem it needs to solve — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the design situation and the core question]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Don't know what the user actually needs, or the stated need feels like a proxy** → user-needs
- **Have a list of constraints and need to understand what design space they leave** → design-constraints
- **Have a direction but need to test and improve it through cycles** → iteration
- **Something exists but feels bloated, cluttered, or over-engineered** → simplicity
- **Unclear** → user-needs first; most design failures begin with the wrong problem

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## User Needs

*Finds what people actually need, beneath what they say they want.*

People state solutions, not needs. "I want a faster horse" is a solution; the underlying need is faster travel. This skill uses jobs-to-be-done framing and latent need mapping to separate the real need from the stated want. It surfaces the functional job (what they're trying to accomplish), the emotional job (how they want to feel), and the social job (how they want to be seen). The output is a need hierarchy that design can actually solve against.

**Output:** Stated want versus real need, jobs-to-be-done mapping (functional/emotional/social), latent needs not yet articulated by users, and the design target stated as a need rather than a solution.

---

## Design Constraints

*Uses constraints productively — mapping hard limits and soft preferences to understand what the solution space actually is.*

Constraints are not the enemy of design; they are the definition of the problem. Every design exists within a set of limits — technical, physical, economic, regulatory, temporal. This skill distinguishes hard constraints (genuinely fixed) from soft preferences (negotiable), maps how they interact, and identifies where the tightest constraints focus the design space. The tightest genuine constraint often points directly to the solution.

**Output:** Constraint map (hard versus soft, by domain), interactions between constraints, the solution space they collectively define, and where productive design territory lies within that space.

---

## Iteration

*Structures the feedback loop between making and learning.*

Good design cannot be planned in full from the start — it is discovered through cycles of making and testing. This skill structures the iteration loop: what to prototype, at what fidelity, with what question to answer, and how to read the signal from each test. It separates convergent tests (does this work?) from divergent tests (which direction?) and defines when enough learning has accumulated to narrow. Dieter Rams' ten principles and Don Norman's design of everyday things both emerge from this disciplined cycle of making and observing.

**Output:** Current design hypothesis, prototype specification (fidelity, format, what to make), test design (question, method, who to test with), decision criteria for converging or pivoting, and the next cycle.

---

## Simplicity

*Finds the form that does exactly what is needed — nothing more.*

Rams' principle: good design is as little design as possible. The goal is not minimalism for its own sake but fitness — the form that serves the function completely, without residue. This skill applies systematic subtraction: identifying every element, testing what job each does, and removing what isn't load-bearing. The test is not "can this be removed?" but "does removing it break the function?" Edward Tufte's data-ink ratio applies this logic to information design; the same principle applies to every designed artefact.

**Output:** Inventory of elements, job each element does, what can be removed without function loss, what is truly load-bearing, and the simplified form with reasoning.
