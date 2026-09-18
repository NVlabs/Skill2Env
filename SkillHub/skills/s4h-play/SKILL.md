---
name: s4h-play
description: "Entry point for the play toolkit. Routes to the right playful thinking skill based on your situation. Use when you say 'play', 'think playfully', 'flip this', 'what if there were no constraints', 'steelman the opposition', 'random stimulus', 'worst possible idea', or want unconventional thinking applied without knowing which specific tool fits."
---

# Play

Applies playful, unconventional thinking to break fixed patterns and generate unexpected possibilities. Play isn't frivolous — it's a serious tool for accessing ideas that conventional thinking misses.

## Which tool fits

| You need to... | Tool |
|---|---|
| Remove or invert the main constraint to see what becomes possible | constraint-inversion |
| Fully inhabit the opposing perspective to find what you're missing | perspective-reversal |
| Introduce a random, unrelated element to break mental fixation | stimulus-generation |
| Design the worst possible version, then reverse it | worst-case-reversal |

## Routing Decision

- **Constraint feels like the ceiling on all thinking** → constraint-inversion
- **Missing what the other side sees — competitor, critic, user** → perspective-reversal
- **Stuck in the same circles, need a jolt from outside** → stimulus-generation
- **Polite brainstorming keeps producing safe ideas** → worst-case-reversal
- **Unclear** → perspective-reversal; inhabiting another view unblocks most stuck situations

**Framing check:** Confirm the specific challenge before routing. State what you've identified — the actual situation and what kind of stuck the user is in — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the challenge and what's blocking progress]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

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

## Constraint Inversion

*Removes or inverts the main constraint to see what becomes possible.*

State the primary constraint explicitly. Now remove it: what would you do if this limit didn't exist? Generate freely in the unconstrained space — don't evaluate, just explore. Now: for each unconstrained idea, ask what version of it could work within the real constraint? Often the unconstrained idea reveals a direction that a constrained version of it can actually reach.

**Output:** Unconstrained ideas generated without the limit, and constrained versions of the most promising ones that respect the actual boundary.

---

## Perspective Reversal

*Fully inhabits the opposing perspective to find what is invisible from your own position.*

Choose the opposing perspective: competitor, critic, user, regulator, skeptic, adversary. Step into it completely — not to dismiss it, but to genuinely reason from within it. What do they see that you don't? What are their legitimate points? What would they say is wrong with your approach? What would they do instead? The opposing perspective almost always contains information your own position is structurally unable to see.

**Output:** The opposing position stated from the inside, what it reveals that was invisible from the original position, and which legitimate points deserve a genuine response.

---

## Stimulus Generation

*Introduces a random, unrelated element to break mental fixation.*

Select a random word, object, or image — something genuinely unrelated to the problem (a random dictionary word, an object in the room, a Wikipedia random article). Now force connections: what does this word/object make you think of? How could that connect to the challenge? Generate without filtering — absurd connections are expected and valuable. The randomness is the point; it bypasses the grooves of familiar thinking.

**Output:** Random stimulus used, forced connections generated without filtering, and the 1-2 connections worth developing seriously.

---

## Worst-Case Reversal

*Deliberately designs the worst possible version, then reverses each failure mode into a design principle.*

Ask: how would you deliberately make this as bad as possible? What would guarantee failure, frustration, or harm? Generate the worst possible version without restraint — this removes the pressure of being right and unlocks creative honesty that polite brainstorming suppresses. Now reverse each failure mode: if X makes it terrible, then NOT-X is a design principle. The worst version is often the clearest map to the best version.

**Output:** The worst possible version described vividly, each failure mode listed, and the design principles generated by reversing each one.
