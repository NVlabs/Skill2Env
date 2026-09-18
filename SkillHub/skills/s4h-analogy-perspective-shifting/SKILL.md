---
name: s4h-analogy-perspective-shifting
description: "Approaches a problem from completely different fields to break the assumption blindness that comes from domain expertise. Triggers: 'fresh eyes', 'outside perspective', 'what would a [different expert] say', 'beginner's mind', 'approach from another field'."
---

# Analogy Perspective Shifting

Domain expertise creates assumption blindness. The more you know about a field, the more
invisible its foundational assumptions become — they stop looking like choices and start
looking like facts. Bringing in genuine outsider perspectives breaks this. Not
hypothetically — by actually applying the diagnostic instincts and tools of people who
have never heard of your problem's usual framing.

---

## Your Process

**Step 1: State the Problem**
Describe the problem as you currently understand it. This is the insider framing — it will
contain the assumptions you're trying to surface.

**Framing check:** Confirm the specific problem before continuing. State what you've identified — the actual situation being examined and its domain — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the problem and its domain]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Choose 2-3 Genuinely Different Fields**
Select fields with fundamentally different training, tools, and instincts. For software
problems: film production, archaeology, emergency medicine, urban planning. For
organisational problems: ecology, military logistics, theatre direction, structural
engineering. Avoid fields that are adjacent — choose fields that would produce different
first questions.

**Step 3: Build Each Expert's Toolkit**
For each field: what are their core diagnostic tools and instincts? What do they always
check first? What patterns are they trained to spot? What would their first question be
when encountering an unknown problem?

**Step 4: Apply Each Lens**
Apply each expert's toolkit to your problem. What do they immediately notice that insiders
overlook? What would they try first that you haven't? What would strike them as obviously
wrong or unnecessarily complex? Don't moderate the outsider view — let it be naive.

**Step 5: Find Cross-Field Patterns**
What do multiple outsiders notice independently? When different fields converge on the
same observation, that observation has a strong claim to being real — it's visible from
multiple angles, not an artefact of one framing.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Shifted perspective only** — The view from the new field, skip the formal structural mapping
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Problem (insider framing):**
> [Current description]

**Field perspectives:**

| Field | Core instincts / tools | What they notice | What they'd try first |
|-------|------------------------|------------------|-----------------------|
| | | | |
| | | | |

**Cross-field patterns (what multiple outsiders see):**
> [Observations that appear across more than one field]

**Most useful foreign insight:**
> [The single observation or approach from outside that would most change how you work
> the problem — and why it's been invisible from inside]

---

## Notes

The exercise fails if the "outside" perspectives are just your own reasoning relabelled.
Each field's observations should surprise you. If they don't, you haven't actually left
your frame — you've just dressed it in different vocabulary.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Perspectives shifted. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-audience-modeling` — Model the audience through each shifted perspective
  - `/s4h-creativity-alternatives` — Generate alternatives from each perspective
  - `/s4h-emotional-motivation-mapping` — Map motivations visible from each perspective
  - **Done** — Wrap up and synthesise what we have so far
