---
name: s4h-creativity-brainstorm
description: "Run an orchestrated multi-method creative thinking sprint on a challenge. Use when the user wants to make real progress on a hard problem, says 'I need to think through this properly', wants a thorough creative exploration rather than a single technique, has a big decision or challenge and wants the full toolkit applied, or just says 'help me think through this'. This is the entry point for serious creative work — it selects and sequences the right tools automatically."
---

You are running an orchestrated creative thinking session. Rather than applying a single tool, this session selects and sequences the most appropriate thinking methods for the user's specific situation, then synthesizes across their outputs.

## How to read the situation

Before selecting methods, diagnose what kind of thinking challenge this is:

**Is the problem itself unclear or stuck?**
→ Start with `assumption-excavator`. The problem framing may be what's blocking progress, not the problem itself.

**Is the user locked into one approach?**
→ Start with `lateral-thinking`. The dominant idea needs to be named and escaped before other tools are useful.

**Is it early-stage exploration?**
→ Start with `water-logic` or `random-entry`. Generate movement and map the territory before applying structured tools.

**Does the user need to see the full solution space?**
→ Use `concept-fan` or `apc`. Expand options systematically before evaluating any of them.

**Does the user need to evaluate something?**
→ Use `cort-pmi` (for a specific idea) or `six-hats` (for a full multi-perspective analysis).

**Are people and their reactions central?**
→ Include `cort-ops` to map the perspectives of those affected.

**Does the situation need a provocation to break it open?**
→ Use `po` for a deliberate jolt into non-obvious territory.

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Two methods only** — Most relevant pair of tools applied at full depth, skip synthesis across more
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Session structure

### Opening: Diagnose the challenge
Briefly state your read of the situation: what kind of thinking challenge is this, and why? This surfaces your reasoning and gives the user a chance to correct it before work begins.

**Framing check:** Confirm the specific challenge before continuing. State what you've identified — the actual problem being explored and its key parameters — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific challenge and what's at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

### Middle: Apply 2–4 methods in sequence
Select the methods that best fit the diagnosis.

**Before narrowing:** Show the full set of candidate methods to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] methods that fit this challenge: [list them with one-line rationale each]. Before I select the most relevant 2–4, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific method to include
  - **Add a missing one** — user will describe it

Apply each selected method fully — do not abbreviate to get through more methods. A thorough application of 2 methods produces more value than a superficial pass through 5.

**Between methods, make the connection explicit:** "The lateral thinking session revealed [X]. Now the concept fan will explore [Y] by treating [X] as the starting point." Methods should build on each other, not run in parallel.

### Close: Synthesize
**Before synthesising:** State what each method surfaced in one sentence each. Use `AskUserQuestion`:
- **Question:** "Here's what each method found: [one bullet per method]. Before I synthesise, does any direction stand out, or is anything missing?"
- **Header:** "Synthesis direction"
- **Options:**
  - **Synthesise as planned** — methods covered the ground
  - **Weight [direction]** — user will name which thread to emphasise
  - **Add a missing angle** — user will name a dimension not yet covered

After the methods are complete, synthesize across the outputs. This is not a summary — it is an integration. What do the different methods, taken together, reveal that no single method showed on its own?

The synthesis should answer:
- What is the most important insight this session produced?
- What direction deserves the most attention, and why?
- What should happen next?

## Output format

**Reading the situation:**
[Your diagnosis — what kind of challenge is this, what methods you're selecting and why]

---

## [Method 1 name]
[Full application of the method]

---

## [Method 2 name]
[Full application, building on method 1 where relevant]

---

## [Method 3 name if used]
[Full application]

---

## Synthesis
**What this session revealed:**
[2–3 paragraphs integrating across all methods — what the full picture shows]

**Most important direction:**
[The single most valuable direction to pursue, with reasoning]

**Recommended next step:**
[A specific, concrete action]

## Notes on quality

The session's value depends on the depth of each method application, not the number of methods used. It is better to run `assumption-excavator` and `lateral-thinking` thoroughly than to touch six methods superficially.

The synthesis is the hardest and most important part. Most sessions produce insights in the individual method sections. The synthesis should produce an insight that only becomes visible when those outputs are held together.

If the user's challenge shifts during the session — if the assumption excavator reveals that the real problem is different from the stated one — follow the actual problem, not the original framing.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Brainstorm complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-criteria-weighting` — Evaluate the brainstorm output against weighted criteria
  - `/s4h-creativity-plus-minus-interesting` — Assess the top ideas fairly before committing
  - `/s4h-constraint-hardness-testing` — Test which ideas are actually feasible
  - **Done** — Wrap up and synthesise what we have so far
