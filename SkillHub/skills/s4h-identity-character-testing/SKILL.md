---
name: s4h-identity-character-testing
description: "Asks what a person or organisation of genuine integrity would do — grounding decisions in character rather than calculation. Triggers: 'character test', 'what would a person of integrity do', 'what does this say about us', 'gut check', 'would I be proud of this', 'are we being who we want to be'."
---

# Character Testing

Ethical calculation — weighing outcomes, mapping trade-offs — can be gamed. Character cannot. The question "what would a person of genuine integrity do here?" cuts through rationalisation by anchoring to identity rather than optimisation. It works best when something feels wrong but is hard to name.

---

## Your Process

**Step 1: Describe the Situation and Decision**
State what is happening and what is being considered. Be honest about the version of the decision that creates discomfort — not the version that sounds best.

**Framing check:** Confirm the specific situation and decision before continuing. State what you've identified — the actual situation, the decision being considered, and who it concerns — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation and decision at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Describe the Character**
Not aspiration, but genuine commitment — what kind of person or organisation is this, when at its best? What does it actually stand for? Describe this in concrete behavioural terms, not in values words.

**Step 3: Ask What Character Requires**
Not what is permitted — what is consistent with the character described? A person of this character, in this situation, would do what, specifically?

**Step 4: Examine What the Proposed Decision Reveals**
If this decision were repeated as policy — applied consistently in all similar situations — what would it reveal about character? If it were made public and described plainly, what would it say about who this person or organisation is?

**Step 5: Apply the Future-Self Test**
Five years from now, looking back at this decision: would you be proud of it? Not pleased with the outcome — proud of the decision itself, how it was made, and what it showed about character.

**Step 6: Analyse the Divergence**
If the character test points in a different direction from the proposed decision: what is driving that divergence? Is it a genuine competing consideration — or is it pressure, convenience, or fear? Is the divergence legitimate?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Character verdict only** — What a person of genuine integrity would do, without elaboration
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Situation and Decision
[Honest description — including the uncomfortable version]

### Character Description
[Concrete, behavioural — not abstract values words]

### What Character Requires
In this situation, a person or organisation of this character would: [specific]

### What the Proposed Decision Reveals
If repeated as policy or made public: [what it would say about character]

### Future-Self Test
Looking back in five years: proud / uncomfortable / regretful — and why?

### Divergence Analysis
| The character test points toward | The proposed decision points toward | What's driving the divergence | Is it legitimate? |
|----------------------------------|-------------------------------------|-------------------------------|-------------------|
| ... | ... | ... | Yes / No |

### Recommendation
[What the character test implies — and whether it should override the original proposal]

---

## Notes

This test is most valuable when the calculation says one thing and something else says no. The discomfort is information — it deserves analysis rather than suppression.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Character tested. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-identity-values-clarification` — Clarify values that the character test revealed tensions in
  - `/s4h-ethics-check` — Check whether character under pressure met ethical standards
  - `/s4h-decision-premortem-analysis` — Stress-test decisions for consistency with character
  - **Done** — Wrap up and synthesise what we have so far
