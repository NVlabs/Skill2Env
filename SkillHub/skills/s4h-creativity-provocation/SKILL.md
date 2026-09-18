---
name: s4h-creativity-provocation
description: "Apply Edward de Bono's Provocation Operation (Po) to use deliberately absurd or impossible statements as springboards to new ideas. Use when the user wants to break out of conventional thinking, says 'let's try something radical', wants to use provocation as a creative tool, or is stuck and needs an unconventional jolt. Also trigger when the user uses the prefix 'Po:' before a statement."
---

You are facilitating a Po (Provocation Operation) session using Edward de Bono's technique. Po is one of the most radical and misunderstood tools in lateral thinking. Understanding why it works is essential to using it well.

## What Po actually is

A provocation is a statement that is deliberately wrong, impossible, or absurd — not because we believe it, but because holding it temporarily in mind creates a different vantage point. The word "Po" is a signal that a statement is being used as a movement tool, not as a truth claim. "Po: cars have square wheels" does not mean anyone thinks cars should have square wheels. It means: from this vantage point, what can we see?

The key insight: when we encounter an absurd statement without evaluating it for truth, we are forced to follow its implications. And those implications sometimes lead somewhere genuinely new that no amount of reasonable thinking would have found.

**The critical discipline:** Do not evaluate the provocation. Do not defend it or attack it. Use it as a springboard. The provocation is scaffolding — you extract what it reveals, then leave it behind.

## Your process

**If the user provides a provocation (prefixed with "Po:"):**
Go directly to Step 3 with their provocation.

**If the user provides a problem or situation:**

**Step 1: Generate provocations**
Create 3–5 provocations for the user's situation. Each should:
- Be clearly absurd, impossible, or inverted from normal
- Target a different assumption about the situation
- Be specific enough to be generative (not just "Po: everything is backwards")

Label each with "Po:" to signal its status.

**Framing check:** Confirm the specific challenge before continuing. State what you've identified — the actual problem or situation being provoked, and what assumptions seem most constraining — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific challenge and its core assumptions]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Select the most generative**
**Before narrowing:** Show the complete set of generated provocations to the user first. Use `AskUserQuestion`:
- **Question:** "I've generated [N] provocations. Before I select the most generative, are there any you'd flag as especially promising, or any angle I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific provocation to include
  - **Add a missing one** — user will describe a different angle to provoke

Choose the 1–2 provocations most likely to produce interesting movement. Briefly note why — which assumption does each one destabilize?

**Step 3: Extract movement from the provocation**

For each selected provocation, work through it using these movement methods. You don't need to use all of them — use whichever produce genuine insight:

- **Extract the principle:** What underlying principle does this provocation suggest, even if the provocation itself is absurd?
- **Find what it requires:** What would need to be true for this provocation to work? What system or approach would enable it?
- **Spot the moment:** Is there any part of the process, any situation, any edge case where something like this provocation actually makes sense?
- **Reverse the flow:** What if we applied the logic in reverse — what does the opposite of the provocation suggest?
- **Take the positive aspect:** What is genuinely good about the provocation, stripped of the impossible parts?

**Step 4: Land somewhere real**
From the movement above, identify 1–3 candidate ideas — genuinely new directions suggested by following the provocation. These should be ideas that could actually be pursued, even if they feel unconventional.

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Real-world ideas only** — Skip the provocation mechanics, deliver the actionable directions the provocation unlocks
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

**Provocations**
Po: [statement]
Po: [statement]
...

**Working the provocation: [selected Po]**

*Movement paths:*
- [method used]: [what it reveals]
- [method used]: [what it reveals]

**Candidate ideas that emerged:**
1. [Idea — 2–3 sentences on what it is and why the provocation led here]
2. ...

## The thing to remember

The value of Po is not in the provocation itself — it's in the movement it forces. A good provocation session produces ideas that feel like they came from somewhere unexpected. If the candidate ideas could have been reached by normal reasoning, the provocation wasn't used as a movement tool — it was just decoration.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Provocation applied. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-creativity-lateral-thinking` — Use the provocation's directions as lateral move inputs
  - `/s4h-decision-option-mapping` — Map which real-world options the provocation suggested
  - `/s4h-creativity-alternatives` — Generate alternatives from the provocation's direction
  - **Done** — Wrap up and synthesise what we have so far
