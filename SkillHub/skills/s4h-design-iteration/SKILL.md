---
name: s4h-design-iteration
description: "Structures the feedback loop between making and learning — prototyping, testing, and convergence toward fit. Triggers: 'prototype and test', 'iterate on the design', 'how do we test this', 'get feedback on the design', 'what should we prototype', 'design feedback loop', 'test and learn', 'are we converging'."
---

# Design: Iteration

No design survives first contact with the real world intact. The best designers know this and plan for it: they make something quickly, put it in front of reality, learn what's wrong, and make something better. The iteration cycle is not a failure mode — it is the mechanism by which design improves. The question is not whether to iterate, but how to structure each cycle so it produces the most learning for the least effort.

Dieter Rams designed and redesigned Braun products over decades of close observation — not because the first version was wrong but because fit is discovered, not planned. Don Norman's fundamental insight in *The Design of Everyday Things* is that designers are wrong about users — systematically, predictably, and in ways they can't detect by reasoning alone. The only cure is observation: put the thing in front of people and watch what happens without explaining it.

This skill structures the iteration cycle. It distinguishes what kind of test is needed at each stage (divergent versus convergent), specifies the right prototype fidelity for the question being asked, and defines the decision criteria that determine when to narrow, when to pivot, and when enough learning has accumulated to commit.

---

## Your Process

**Step 1: State the Current Hypothesis**
Every prototype is a test of a hypothesis. State it explicitly: "We believe [specific design choice] will [produce this outcome] for [this user doing this job]." If the hypothesis is vague, the test will be uninformative. Specificity is not premature commitment — it is what makes learning possible.

**Framing check:** Confirm the design stage and the hypothesis being tested before continuing. State what you've identified — the design being iterated and the key question it needs to answer — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the hypothesis and stage]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify the Iteration Type**
Two distinct types of test require different setups:

- **Divergent test:** "Which direction is most promising?" Used when there are multiple competing design directions and you need to narrow. Set up multiple options. Vary one thing at a time. Measure preference, comprehension, or engagement.
- **Convergent test:** "Does this work?" Used when a direction has been chosen and you're refining fit. Test the specific design against real use. Measure success on the actual task.

Identify which type is needed. Mixing them produces muddled learning.

**Step 3: Specify the Prototype**
Match prototype fidelity to the question being asked:

- **Sketch/paper:** for testing whether an interaction model makes sense, before any investment in appearance
- **Wireframe/low-fi:** for testing structure, navigation, and information hierarchy
- **Mid-fi prototype:** for testing comprehension, flow, and whether the sequence works
- **High-fi prototype:** for testing response to the complete experience — aesthetics, tone, emotional reaction
- **Live/functional:** for testing real behaviour under real conditions

The most common error is over-building the prototype for the stage. A high-fidelity prototype for a question that could be answered by a sketch wastes time and creates attachment that biases the test.

Specify: what to make, at what fidelity, and what it should and should not include.

**Step 4: Design the Test**
A test that doesn't answer the hypothesis isn't a test. Define:

- **The question:** What specific thing are you trying to learn?
- **The method:** Observation, task completion, interview, A/B, diary study — each is suited to different questions. Observation reveals what people do; interviews reveal what they believe; task completion reveals where design fails.
- **Who:** Which users, how many, which context. The smaller and more specific the group, the cleaner the signal.
- **What counts as a result:** Define in advance what a positive result looks like, and what would indicate a need to pivot.

**Step 5: Read the Signal**
After testing, separate observation from interpretation. What did people actually do, say, or fail to do? Where did they hesitate, ask questions, or deviate from the intended path? Those moments are the data. Interpretations follow from data — not the reverse.

Classify findings:
- **Confirms hypothesis:** evidence the direction is correct
- **Disconfirms hypothesis:** evidence to pivot or remove
- **Unexpected signal:** something that wasn't hypothesised but appeared; note it without immediately incorporating it

**Step 6: Set the Next Cycle**
Based on findings, decide:
- **Continue and refine:** hypothesis confirmed; next iteration sharpens the same direction
- **Pivot:** hypothesis disconfirmed; change direction before next prototype
- **Narrow:** multiple directions tested; eliminate one or more; next cycle goes deeper on the survivor(s)
- **Commit:** enough learning has accumulated; convergence is appropriate

State the decision and the reasoning.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what stage the design is at and what the key uncertainty is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full cycle plan** — Plan the complete iteration cycle with prototype spec and test design
  - **Prototype spec only** — Focus on what to make and at what fidelity
  - **Test design only** — Focus on how to test the design that already exists
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Hypothesis:**
> We believe [design choice] will [produce outcome] for [user doing job].

**Iteration type:** Divergent / Convergent

**Prototype specification:**

| Dimension | Specification |
|---|---|
| Format | [Sketch / wireframe / mid-fi / high-fi / functional] |
| What to include | [Specific elements] |
| What to exclude | [What would over-build for this question] |
| Estimated time to build | [Order of magnitude] |

**Test design:**

| Element | Detail |
|---|---|
| Question | [What we're trying to learn] |
| Method | [Observation / task completion / interview / A/B / other] |
| Participants | [Who, how many, in what context] |
| Success signal | [What counts as confirmation] |
| Pivot signal | [What would indicate a directional change is needed] |

**After this cycle, decide:**
[One sentence on what decision this test enables — what will be known that isn't known now.]

---

## Notes

The most common failure mode in iteration is "learning without deciding" — each test produces findings that inform a slightly modified next test, but the cycle never converges because no one is willing to commit to a direction. Define decision criteria before testing, not after. The second most common failure is testing the wrong thing at the wrong fidelity — usually over-building — which makes the prototype expensive to change and biases toward incremental refinement over genuine learning.

This skill pairs naturally with `/s4h-design-user-needs` (which defines what the prototype should be testing against) and `/s4h-design-simplicity` (which removes what's not needed before the next iteration). For generating alternative directions to test, `/s4h-creativity-alternatives` produces options efficiently.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Iteration cycle planned. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-design-simplicity` — Before building, remove what isn't necessary from the current design
  - `/s4h-design-user-needs` — Re-examine what the prototype is testing against
  - `/s4h-creativity-alternatives` — Generate alternative directions if the current hypothesis needs more options
  - **Done** — Wrap up and synthesise what we have so far
