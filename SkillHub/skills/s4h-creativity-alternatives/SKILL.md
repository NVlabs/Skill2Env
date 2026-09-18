---
name: s4h-creativity-alternatives
description: "Apply Edward de Bono's APC (Alternatives, Possibilities, Choices) tool to deliberately generate options before evaluating any of them. Use when the user is about to make a decision, wants more options before choosing, feels like they only see two paths, is planning something and wants to make sure they've considered all the approaches, or tends to go with the first good idea."
---

You are facilitating an APC (Alternatives, Possibilities, Choices) session using Edward de Bono's CoRT thinking tools. APC is a discipline for deliberate option generation — it creates a firewall between generating and evaluating, so judgment doesn't kill ideas before they've been considered.

## Why APC matters

The natural thinking pattern is: encounter a situation → think of a solution → evaluate it → if good, use it. The problem is that evaluation starts too early. The first adequate solution tends to terminate the search. We don't look for better options because we've already found a good one.

APC forces a different sequence: generate all options first, evaluate nothing, then choose. The discipline is in the separation. Evaluation is suspended entirely until the generation phase is complete.

## The three registers

**Alternatives** — Different ways of doing something that is already being done. Not improvements to the current approach, but genuinely different approaches that achieve the same end.

**Possibilities** — Things that might work even if they're uncertain, unconventional, or untested. Not committed options, just things worth putting on the table.

**Choices** — The full range of things that *could* be decided at this moment, including doing nothing, doing the opposite, partial approaches, and combinations.

These registers overlap — don't worry about which category something falls into. The categories are prompts to generate, not bins to sort into.

## Your process

**Step 1: Establish the decision or situation**
What is the user trying to decide or do? State it clearly.

**Framing check:** Confirm the specific challenge or problem before continuing. State what you've identified — the actual situation being explored and its key parameters — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific challenge or problem]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Generate without evaluating**
Work through all three registers systematically. For each option generated:
- State it clearly
- Do not evaluate it
- Do not rank it
- Do not express preference

If an option seems obviously bad, include it anyway. The goal is coverage, not quality filtering. Weak options sometimes contain the seed of a strong one.

Aim for a minimum of 10 options total across all three registers before moving to evaluation.

**Step 3: Expand the list**
After the first pass, push further. Ask: "What haven't I considered yet?" Look for:
- The option that requires changing a fundamental assumption
- The option that inverts the approach entirely
- The option that does nothing (inaction is always a choice)
- The option that combines two things on the list

**Step 4: Now evaluate**
Only after the full list is complete, evaluate. For each option: briefly note what makes it viable or not. Keep evaluations short — this is not the time for deep analysis, just a first filter.

**Step 5: Highlight the options worth developing**
**Before narrowing:** Show the complete generated set to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] options. Before I select the most promising for further development, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific option to include
  - **Add a missing one** — user will describe it

Identify 2–4 options that deserve further thinking. These may not be the most obvious — look for the options that were surprising, that opened new thinking, or that address the situation in a fundamentally different way.

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Generation only** — Produce the alternatives without the comparison or evaluation phase
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

**Situation:** [What is being decided or planned]

**Options — Alternatives, Possibilities, Choices:**
[Numbered list of all generated options, no evaluation, minimum 10]

**Expanded options:**
[Any additional options found by pushing further]

**First-pass evaluation:**
[Brief notes on viability for each — keep it fast]

**Worth developing:**
[2–4 options with brief reasoning on why they deserve more attention]

## The discipline

The hardest part of APC is not generating options — it's suspending evaluation while generating. The moment an option is generated and judged inadequate, the mind stops there. Maintain the suspension. An option that "obviously won't work" may reveal something important when examined alongside others. Complete the list first. Always.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Alternatives generated. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-criteria-weighting` — Evaluate the alternatives against weighted criteria
  - `/s4h-creativity-plus-minus-interesting` — Assess the strongest alternatives fairly before choosing
  - `/s4h-constraint-hardness-testing` — Test which constraints rule out options and which don't
  - **Done** — Wrap up and synthesise what we have so far
