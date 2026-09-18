---
name: s4h-play-stimulus-generation
description: "Introduces a random, unrelated element to break mental fixation — forcing new associations that bypass the groove of familiar thinking. TRIGGERS: 'random stimulus', 'random word technique', 'break the fixation', 'I keep thinking of the same things', 'unstick this', 'force new associations'."
---

# Play: Stimulus Generation

When thinking is stuck it is usually stuck in a groove — a narrow set of associations
that keeps returning to the same territory because the same concepts keep activating
the same networks. A random, unrelated stimulus forces the mind out of that groove by
requiring it to build a bridge between an irrelevant input and the actual problem.
The bridges that form are often the most original ideas, because they come from
outside the problem's own conceptual neighbourhood.

---

## Your Process

**Step 1: State the Stuck Problem**
What is the problem, and what makes it stuck? What solutions have already been
considered and found inadequate? What territory keeps getting returned to? Naming
the groove is the first step to breaking it.

**Framing check:** Confirm the specific challenge before continuing. State what you've identified — the actual problem and the groove it keeps returning to — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the stuck problem and its groove]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Generate a Random Stimulus**
Introduce something genuinely unrelated to the problem domain — the less obviously
connected the better. Options:
- Open a dictionary, encyclopedia, or any book to a random page; use the first
  concrete noun
- Use a recent news headline from a completely unrelated field
- Name a physical object currently visible in the room
- Choose a domain entirely unlike the problem: if the problem is software, use
  marine biology or medieval architecture; if it's business strategy, use cooking
  or materials science

The stimulus should feel irrelevant. That is the point.

**Step 3: List Attributes and Associations**
Name 5-7 properties, behaviours, qualities, structures, or associations of the
stimulus. Go beyond the obvious surface properties — consider how it behaves under
pressure, what it requires to function, how it fails, what it produces, what
constrains it, what it optimises for. The richer the attribute list, the more
bridges are available.

**Step 4: Force Connections**
For each attribute: ask "how could this apply to the stuck problem?" No filtering,
no immediate rejection. Some connections will be useless — make them anyway. The
goal is volume of bridges, not quality filtering at this stage. Quantity first.

**Step 5: Identify Promising Directions**
**Before narrowing:** Show the complete forced connections table to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] forced connections. Before I select the most promising, are there any you'd flag as especially worth developing, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific connection to include
  - **Add a missing one** — user will describe it

Which forced connections suggest a genuinely new direction — even partially? Which
reframe the problem itself rather than just suggesting a surface solution? A
connection that reveals a new way of seeing the problem is often more valuable than
one that suggests a specific solution.

**Step 6: Develop the Most Promising**
Take the strongest connection and develop it into a concrete idea. What would it
look like if implemented in the actual problem context? What would need to be true
for it to work? What is the testable version?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Three connections only** — Strongest forced connections between the stimulus and the problem
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Stuck Problem:** [description of the problem and what the stuck groove looks like]

**Random Stimulus:** [the word, object, headline, or concept introduced]

**Stimulus Attributes:** 1. [attribute] 2. [attribute] 3. [continue to 5-7]

**Forced Connections**

| Attribute | Connection to the Stuck Problem | Worth Developing? |
|---|---|---|
| [attribute] | [how it might apply — no filtering] | [yes / no / maybe] |

**Most Promising Direction:** [the connection or reframe worth developing, and why]

**Developed Idea:** [what it looks like as a concrete proposal — specific enough
to test or act on]

---

## Notes

The random stimulus works not because it contains the answer but because connecting
to it forces abandonment of the stuck groove. A connection that seems absurd at first
may open a direction that a rational search would never find. Resist the urge to
discard connections quickly — the most useful ones often require a second look.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Stimuli generated. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-creativity-lateral-thinking` — Use the stimuli as lateral move inputs
  - `/s4h-creativity-random-entry` — Build further on the generated stimuli
  - `/s4h-creativity-assumption-excavator` — Use the stimuli to surface hidden assumptions
  - **Done** — Wrap up and synthesise what we have so far
