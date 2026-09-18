---
name: s4h-creativity-random-entry
description: "Apply Edward de Bono's Random Entry technique — use an unrelated word, object, or image as a creative springboard to break out of cognitive ruts. Use when the user is stuck, wants unexpected inspiration, asks for a random creative prompt, wants to approach something from a completely fresh angle, or says they've exhausted their usual thinking. The randomness is the point — don't skip it."
---

You are facilitating a Random Entry session using Edward de Bono's technique. Random Entry is the most counterintuitive tool in lateral thinking — and the one that most reliably proves the technique works.

## Why this works

The mind naturally follows established patterns. Every thought about a problem tends to flow through the same channels, reinforcing the same directions. Introducing a genuinely random stimulus breaks this by forcing the mind to build connections it would never have built on purpose.

The key word is *genuinely* random. A stimulus chosen because it seems relevant is not random — it is already connected to the problem by the person choosing it. True randomness means the connection doesn't exist yet. You have to build it. That building process is where the new ideas come from.

## Your process

**Step 1: Establish the problem or situation**
If the user hasn't provided one, ask: "What situation or challenge would you like to approach with a random stimulus?"

**Framing check:** Confirm the specific challenge before continuing. State what you've identified — the actual problem or situation and its key parameters — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the challenge and its context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Generate or accept a random word**
If the user provides a word or object, use it.

If not, generate one. Choose something genuinely arbitrary — an object, creature, natural phenomenon, tool, or place. Not abstract concepts. Physical, concrete things work best. Avoid anything with obvious relevance to the user's situation.

State the random word clearly: **Random stimulus: [word]**

**Step 3: Develop the stimulus**
Before connecting the stimulus to the problem, spend a moment expanding it. List 6–10 attributes, associations, functions, behaviors, or qualities of the stimulus. Do this without thinking about the problem yet — let the stimulus exist on its own terms.

**Step 4: Build bridges**
Now, systematically connect each attribute from Step 3 to the user's situation. For each attribute:
- State the attribute
- Describe the connection to the problem — however loose or strange it seems
- Note any idea, direction, or angle that emerges from the connection

Some connections will be weak. Some will feel forced. Keep going — the goal is to surface every possible bridge. The best ideas often come from connections that initially seem the most unlikely.

**Step 5: Identify the most generative connections**
Review all the bridges.

**Before narrowing:** Show the complete set of bridges to the user first. Use `AskUserQuestion`:
- **Question:** "I've built connections for all [N] attributes. Before I select the most generative, are there any bridges you'd flag as especially interesting, or any angle I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific bridge to include
  - **Add a missing one** — user will describe an angle to explore

Which 2–4 connections produced something genuinely interesting — a direction, reframing, or idea that you wouldn't have reached by thinking directly about the problem?

Develop these briefly: what is the idea, and why is it worth exploring?

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Raw associations only** — The forced connections before any filtering or evaluation
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

**Random stimulus:** [word]

**Attributes of [word]:**
[6–10 attributes, one per line]

**Bridges to [user's situation]:**
| Attribute | Connection | Idea/Direction |
|-----------|------------|----------------|
| ... | ... | ... |

**Most generative:**
[2–4 developed ideas, 2–3 sentences each]

## Notes on quality

The test of a good Random Entry session: did it produce at least one idea that the user genuinely didn't see coming? If all the ideas were predictable, the random stimulus probably wasn't used as an entry point — it was evaluated for relevance and discarded when it didn't seem useful. Force the connections. The seemingly absurd ones are often the most valuable.

Resist the urge to choose a "good" random word. Randomness is the mechanism. Trust it.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Random entry applied. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-creativity-lateral-thinking` — Use the forced connections as lateral move inputs
  - `/s4h-creativity-alternatives` — Generate alternatives from the most interesting connections
  - `/s4h-creativity-assumption-excavator` — Use the random entry to surface hidden assumptions
  - **Done** — Wrap up and synthesise what we have so far
