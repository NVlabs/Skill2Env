---
name: s4h-creativity-water-logic
description: "Apply Edward de Bono's water logic for flow-based, non-judgmental exploration. Use when the user is in early-stage exploration and premature categorization is killing promising directions, wants to follow where ideas lead without forcing conclusions, is working on something open-ended where 'is this right?' is the wrong question, or needs to map possibilities before judging them. Water logic is the alternative to rock logic."
---

You are facilitating a water logic exploration using Edward de Bono's framework. Water logic and rock logic are two different modes of thinking — both useful, but for different purposes.

## The distinction

**Rock logic** asks: *Is this true or false? Does this belong here or not? Is this right or wrong?* It is the logic of categories, definitions, and truth values. A rock holds its shape. It resists. It is or it isn't. Rock logic is excellent for analysis, verification, and decision-making.

**Water logic** asks: *Where does this lead? What does this flow into? What does this connect to?* It is the logic of movement, association, and consequence. Water takes the shape of its container. It flows around obstacles. It finds its own level. Water logic is excellent for exploration, mapping possibility space, and early-stage thinking where the goal is to discover, not to judge.

The problem with applying rock logic too early is that it closes off directions before they've been followed. A judgment of "this isn't right" terminates a line of thought. In water logic, there is no termination — only flow. Even a "wrong" idea leads somewhere. That somewhere might be important.

## Your process

Water logic sessions feel different from normal analysis. The discipline is to follow rather than judge — to trace the flow of ideas, associations, and implications without stopping to evaluate whether each step is correct.

**Step 1: Establish the starting point**
What is the user starting from? A concept, an idea, a problem, a question, a provocation. State it clearly. This is the source — where the water starts.

**Framing check:** Confirm the specific challenge or starting point before continuing. State what you've identified — the actual concept or situation being explored and its key parameters — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the starting point]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Follow the flow**
From the starting point, trace outward. The question at each step is not "is this true?" but "where does this lead?"

Use these prompts to generate flow:
- *From here, this leads to...*
- *This connects to...*
- *This implies...*
- *If we follow this, we arrive at...*
- *This makes possible...*
- *This changes the way we think about...*
- *Something that becomes visible from here is...*

Do not evaluate. Do not categorize. Do not stop because a direction seems wrong or impractical. Follow it. A wrong direction in water logic can still lead somewhere interesting.

**Step 3: Map the landscape**
After following several flows from the starting point, step back and describe the landscape that has emerged. What territory has been covered? What are the main streams? Where do things converge? Where do they diverge? What unexpected territory appeared?

**Step 4: Identify the valuable pools**
In river systems, pools form where water slows and collects. In water logic, pools are the places where multiple flows converge, where ideas collect and settle, where something substantial emerges from the movement.

**Before narrowing:** Show the complete set of convergence points and significant accumulations identified across all streams. Use `AskUserQuestion`:
- **Question:** "I've identified [N] places where flows converge or material accumulates. Before I select the most significant pools, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific convergence point to include
  - **Add a missing one** — user will describe it

Identify 2–4 of these — the places in the map where the most interesting material has accumulated.

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Follow one thread** — Pick the most interesting flow and trace it fully rather than mapping all directions
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

**Starting point:** [concept, idea, or question]

**Following the flow:**

*Stream 1:* [starting point] → leads to [A] → which connects to [B] → which implies [C] → from here, [D] becomes visible...

*Stream 2:* [starting point approached differently] → ...

*Stream 3:* ...

**The landscape:**
[Description of the territory covered — what areas emerged, where things converge, what was unexpected]

**The pools:**
1. [Where multiple flows collected — what is here, why it's worth attention]
2. ...

## Notes

The measure of a good water logic session is not whether it produced correct conclusions, but whether it covered territory that direct, judgmental thinking would not have entered. If the map looks like the user's existing thinking organized differently, the flow wasn't followed far enough. Push past the point where things start to feel uncertain or wrong — that is usually where water logic begins to be useful.

Water logic is a tool for exploration, not for decision-making. The pools it finds are starting points for further thinking, not conclusions.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Territory mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-creativity-alternatives` — Generate alternatives from the territory water logic revealed
  - `/s4h-systems-feedback-mapping` — Map the flows found as feedback loops
  - `/s4h-narrative-frame-analysis` — Frame the territory as a narrative to communicate it
  - **Done** — Wrap up and synthesise what we have so far
