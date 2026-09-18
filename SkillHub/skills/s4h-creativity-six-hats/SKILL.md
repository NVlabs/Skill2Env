---
name: s4h-creativity-six-hats
description: "Apply Edward de Bono's Six Thinking Hats for structured parallel thinking. Use when the user wants to think through a decision, plan, or idea from multiple angles; wants to avoid groupthink or one-dimensional analysis; is preparing for a meeting or discussion; or wants a complete map of a situation before committing. Also use when the user mentions 'devil's advocate', 'playing it safe', 'gut feeling', or wants both optimism and caution applied to the same thing."
---

You are facilitating a Six Thinking Hats session using Edward de Bono's methodology. Six Hats is not a personality exercise or a debate format. It is a discipline for *parallel thinking* — separating different types of thinking so they can each be done properly, without contamination.

## Why parallel thinking matters

Conventional discussion mixes thinking modes together. Someone raises an idea; someone else immediately critiques it; a third person defends it; a fourth adds data that supports one side. The result is argument — positions harden, egos attach to outcomes, and the quality of thinking suffers.

Six Hats replaces this with parallel thinking: everyone (or in this case, the full analysis) explores the same direction at the same time. All the yellow-hat thinking happens together. All the black-hat thinking happens together. The hats don't argue with each other — they each do their job fully, and the map produced by all six together is richer than any argument could produce.

## The six hats

**White Hat — Facts and Information**
What do we know? What data exists? What information is missing or uncertain? What are the verified facts? White Hat does not interpret or argue — it only deals with what is known and what gaps exist.

**Red Hat — Feelings and Intuition**
What is the gut reaction? What emotions does this situation produce — excitement, anxiety, enthusiasm, unease? Red Hat does not justify feelings or explain them — it simply gives them space. "I feel uneasy about this" is a complete Red Hat statement.

**Black Hat — Caution and Critical Judgment**
What could go wrong? What are the risks, flaws, dangers, and weaknesses? Why might this not work? Black Hat is not pessimism — it is rigorous caution. It is the hat that protects against bad decisions. It must be thorough and honest.

**Yellow Hat — Value and Optimism**
What is good about this? What value does it create? Why might it work? What opportunities does it open? Yellow Hat is not cheerleading — it is the disciplined search for genuine benefit, even in unpromising situations.

**Green Hat — Creativity and Alternatives**
What else is possible? What new ideas does this situation suggest? Are there different approaches, modifications, or alternatives worth considering? Green Hat generates without evaluating — it is the hat of possibility and movement.

**Blue Hat — Process and Overview**
What is the thinking process itself? What has the analysis revealed? Where should focus go next? Blue Hat steps back from the content to assess the quality and direction of the thinking. It often opens and closes the session.

## Your process

**If the user specifies a hat:** Apply only that hat fully and deeply. This is valid — sometimes one perspective is what's needed.

**If the user wants a full session:** Run all six hats in this sequence: White → Red → Black → Yellow → Green → Blue. This sequence is deliberate: ground in facts, acknowledge feelings, surface risks, find value, generate alternatives, then step back to synthesize.

For each hat:
- Name it clearly with its color and function
- Apply it fully to the user's situation — don't just define it, actually do the thinking
- Be honest within each hat's discipline. Black Hat should be genuinely cautionary. Yellow Hat should find real value, not forced positivity.

**Before synthesising:** State what each hat surfaced in one sentence each. Use `AskUserQuestion`:
- **Question:** "Here's what each hat found: [one bullet per hat — e.g. White: the key data gaps; Red: the dominant emotional signal; Black: the sharpest risk; Yellow: the strongest value case; Green: the most promising alternative]. Before I run the Blue Hat synthesis, does any direction stand out, or is anything missing?"
- **Header:** "Synthesis direction"
- **Options:**
  - **Synthesise as planned** — the hats covered the ground
  - **Weight [direction]** — user will name which hat's thread to emphasise
  - **Add a missing angle** — user will name a dimension not yet covered

**Blue Hat close:** After the other five hats, the Blue Hat synthesis should answer: What does the full map tell us? What stands out? What deserves most attention? What is the recommended next step, if any?

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Black and yellow hats only** — Critical risks and genuine benefits, skip the other four hats
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

## 🎩 White Hat — Facts
[What is known, what is uncertain, what data is missing]

## ❤️ Red Hat — Feelings
[Emotional reactions, intuitions, gut responses — stated without justification]

## 🖤 Black Hat — Caution
[Risks, flaws, what could go wrong, why it might not work]

## 💛 Yellow Hat — Value
[What's genuinely good here, what opportunities exist, why it could work]

## 💚 Green Hat — Creativity
[New ideas, alternatives, modifications, different approaches]

## 💙 Blue Hat — Overview
[What the full map reveals, what deserves attention, recommended next step]

## Notes

Each hat should feel distinct. If the Black Hat section sounds like the Yellow Hat section with hedges, or if the Green Hat section is just a refined version of the existing plan — the hats aren't being worn properly. Each hat requires temporarily setting aside the others. A strong Black Hat session means genuinely looking for failure modes, not softening them. A strong Yellow Hat session means genuinely looking for value, not dismissing it.

The power of Six Hats is that *all six get to be right* — within their own domain. There is no winner.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Six hats complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-criteria-weighting` — Weight decision criteria from Black and Yellow hat findings
  - `/s4h-decision-premortem-analysis` — Run a premortem on the risks the Black hat identified
  - `/s4h-communication-audience-modeling` — Use Red hat findings to model how others will react
  - **Done** — Wrap up and synthesise what we have so far
