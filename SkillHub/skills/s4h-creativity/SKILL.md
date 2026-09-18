---
name: s4h-creativity
description: "Entry point for the creativity toolkit. Routes to the right creative thinking technique based on your situation. Use when you say 'creativity', 'think creatively', 'I need fresh ideas', 'help me think differently', 'I'm stuck', or want creative help without knowing which specific tool applies. For comprehensive multi-method sessions, this runs them in sequence."
---

# Creativity

Applies creative thinking to any challenge. Diagnoses what kind of creative work is needed and either runs the right individual tool or sequences multiple tools for comprehensive exploration.

## Which tool fits

| You need to... | Tool |
|---|---|
| Question whether the problem itself is framed correctly | assumption-excavator |
| Escape a dominant idea you keep returning to | lateral-thinking |
| See all options before choosing any | alternatives / concept-fan |
| Evaluate a specific idea fairly, without snap judgment | plus-minus-interesting |
| Think through something from multiple perspectives | six-hats |
| Think from other people's actual positions | other-perspectives |
| Explore without premature judgment | water-logic |
| Break fixation with a random jolt | random-entry |
| Use an absurd premise as a springboard | provocation |
| Consider all factors before deciding | consider-factors |
| Comprehensive multi-method session | run the full sequence below |

## Routing Decision

**Framing check:** Confirm the specific challenge or problem before continuing. State what you've identified — the actual creative challenge and its key parameters — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific challenge]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Problem framing might itself be wrong** → assumption-excavator (run before anything else)
- **Stuck in one direction, keep returning to the same idea** → lateral-thinking
- **Need to see the full option space before choosing** → alternatives or concept-fan
- **Have a specific idea to evaluate** → plus-minus-interesting
- **Need full multi-perspective analysis** → six-hats
- **Decision affects other people** → other-perspectives
- **Early exploration, premature judgment is the enemy** → water-logic
- **Thoroughly stuck, need outside stimulus** → random-entry
- **Need a deliberate jolt into the impossible** → provocation
- **About to act, want to make sure nothing is missed** → consider-factors
- **Big challenge, want everything applied** → run the full brainstorm sequence

---

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

## Assumption Excavator

*Surfaces and challenges hidden assumptions.*

List every assumption embedded in the current problem framing — about what's possible, what's wanted, what's fixed, who's involved. Challenge each: what if this assumption were false? Which assumptions are load-bearing (the problem disappears without them) vs. incidental? Find the assumption that, if wrong, would most change the approach.

**Output:** Full assumption inventory, classified by how hard they are to question, and the one reframe that most changes the problem.

---

## Lateral Thinking

*Escapes dominant patterns to generate genuinely new directions.*

Name the dominant idea — the direction that keeps surfacing. Suspend it deliberately: set it aside for the rest of this exercise. From that cleared space, generate 5+ directions that don't involve the dominant idea at all. Use movement thinking: don't evaluate, just move. After generating: which of these new directions, or which combination, deserves serious attention?

**Output:** Dominant idea named and set aside. 5+ genuinely different directions. The 1-2 that deserve development.

---

## Alternatives (APC)

*Deliberately generates options before evaluating any.*

Apply Alternatives, Possibilities, Choices: set a quota — find at least 5 alternatives to the current approach before evaluating any of them. Prevent evaluation from entering the generation phase. After generating: now compare. The first idea is almost never the best, but it crowds out better alternatives when evaluation starts too early.

**Output:** 5+ alternatives generated without judgment, then a brief comparative assessment.

---

## Concept Fan

*Expands the solution space at different levels of abstraction.*

Define the immediate solution being considered. Step back one level: what concept does it serve? Now generate multiple ways to serve that concept. Step back again: what broader purpose does the concept serve? Generate multiple concepts that could serve the purpose. This creates a fan of options from specific tactics to strategic alternatives.

**Output:** Three levels — immediate solutions, serving concepts, and underlying purposes — each with multiple options.

---

## Plus/Minus/Interesting (PMI)

*Evaluates an idea fairly before accepting or rejecting it.*

Apply Plus/Minus/Interesting to the idea: (1) Plus — what is genuinely good about it, including non-obvious positives? (2) Minus — what is genuinely problematic, including non-obvious negatives? (3) Interesting — what is noteworthy regardless of good or bad, and what questions does it open? PMI is the antidote to snap judgment.

**Output:** PMI table. Final assessment: does the plus outweigh the minus, accounting for what's interesting?

---

## Six Hats

*Structured parallel thinking from six distinct angles.*

Apply each hat in sequence: (1) White — facts and data only, (2) Red — emotional and intuitive response, (3) Black — risks, problems, and critical analysis, (4) Yellow — optimism and genuine benefits, (5) Green — creative alternatives and new possibilities, (6) Blue — process, what thinking is needed. Each hat is pure — no mixing.

**Output:** Six-section analysis, one per hat. Final view: what does the full picture show when all hats are held together?

---

## Other Perspectives (OPS)

*Genuinely thinks from other people's positions.*

Identify the key people affected by or involved in this situation. For each person: what is their actual goal? What do they see as the problem? What are they worried about? What would a good outcome look like from their position? OPS is structured empathy — not sympathy, but actually reasoning from within someone else's constraints and goals.

**Output:** Per-person analysis. Synthesis: what does thinking from all these positions reveal that your own position missed?

---

## Water Logic

*Explores without premature judgment.*

Enter flow mode: follow where ideas lead without asking "is this right?" Water logic doesn't judge, it maps. Start with the situation and ask: what does this lead to? Where does it flow naturally? What does it connect to? Build the territory before deciding what matters. Rock logic asks "is this true?"; water logic asks "where does this go?"

**Output:** A map of where the situation flows — connections, directions, and possibilities — before any evaluation.

---

## Random Entry

*Uses an unrelated stimulus to break cognitive ruts.*

Select a random word or object (or have one provided). Apply it to the problem: what does this word make you think of? How does that relate to the challenge? Force connections, even absurd ones — absurd connections are the point. The randomness bypasses the grooves of familiar thinking.

**Output:** Random word used, forced connections generated, and the 1-2 connections worth pursuing.

---

## Provocation (Po)

*Uses an impossible or absurd statement as a springboard.*

State a deliberate provocation — something obviously wrong or impossible: "Po: [impossible premise]." Don't evaluate the provocation. Instead: what does the world look like if this were true? What would we do? Now: which of those ideas could work in the real world? The provocation is scaffolding, not a destination.

**Output:** The provocation stated, the ideas it generates from, and the real-world ideas those lead to.

---

## Consider All Factors (CAF)

*Maps every relevant factor before acting.*

List every factor that could affect the outcome: stakeholders, risks, resources, timing, dependencies, second-order effects. CAF is a pre-flight checklist — it doesn't evaluate, it inventories. After listing: which factors were you about to ignore? Which are more important than they appeared?

**Output:** Full factor inventory. Factors most likely to be overlooked. Factors that most change the approach.

---

## Full Brainstorm Sequence

*Orchestrated multi-method session for complex challenges.*

For big challenges, sequence the tools: (1) Assumption-excavator to clear the framing, (2) Lateral thinking to escape the dominant idea, (3) Concept fan or alternatives to expand the option space, (4) Six hats or PMI to evaluate the best directions, (5) Consider-factors to catch what was missed. Between tools, make the connection explicit — each one builds on the previous.

Close with synthesis: what do the tools, taken together, reveal that no single tool showed on its own? What is the single most important direction? What is the concrete next step?
