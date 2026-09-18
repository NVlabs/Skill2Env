---
name: s4h-aesthetic-coherence-check
description: "Tests whether the parts of something form a unified whole — finding the jarring inconsistencies that accumulate when different contributors work without a shared vision. TRIGGERS: 'coherence check', 'does this feel unified', 'something feels off', 'inconsistent', 'check the whole', 'does this hang together'."
---

# Aesthetic Coherence Check

Incoherence is the default product of collaboration without a shared vision. Each part
may be locally defensible — sensible in isolation, reasonable given what that contributor
was optimising for — while the whole communicates nothing clearly. A perceptive reader
or user feels this before they can name it. This skill makes the incoherence legible
so it can be fixed.

---

## Your Process

**Step 1: State the Artefact and Its Intended Identity**
What is being examined — a product, document, strategy, brand, presentation, process?
What identity or effect is it supposed to produce? "Should feel authoritative but
approachable" or "Should communicate a single strategic bet" or "Should make a
first-time user feel capable in under three minutes." The intended identity is the
standard everything else will be measured against.

**Framing check:** Confirm the specific artefact and its intended identity before continuing. State what you've identified — the actual object being analyzed and the identity or effect it is supposed to produce — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the artefact and its intended identity]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Examine Each Part**
Break the artefact into its major components. For each: what does it communicate?
What does it prioritise implicitly — speed vs depth, confidence vs humility,
complexity vs accessibility? What does it assume about the audience or context?
Extract these qualities as observations, not evaluations.

**Step 3: Compare Parts to Each Other**
Where do assumptions conflict across parts? A section written for technical readers
next to one written for executives. A formal tone in one component, casual in another.
A design that prioritises simplicity in navigation but complexity in content. Name
the specific conflict, not just that something feels inconsistent.

**Step 4: Compare Parts to the Whole**
Which parts are faithful to the intended identity? Which stray — and in what
direction? Is the straying random (different contributors with different instincts)
or directional (a competing version of what the thing should be is quietly winning
in parts of it)?

**Step 5: Identify the Most Jarring Inconsistencies**
**Before narrowing:** Show the complete set of inconsistencies identified across Steps 3 and 4 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] inconsistencies. Before I select the most damaging, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific inconsistency to include
  - **Add a missing one** — user will describe it

Find 2-3 specific moments where the lack of coherence is most damaging — where a
perceptive reader or user would feel something is wrong, even if they can't say why.
Prioritise by impact on the intended identity.

**Step 6: Recommended Adjustments**
For each jarring inconsistency: what specific change — to which part, in which
direction — would bring it into alignment with the intended identity?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Incoherence only** — Where the parts fail to form a whole, skip confirming what works
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Intended Identity:** [what the artefact is supposed to be/feel/communicate]

**Parts Assessed**

| Part | What It Communicates | What It Prioritises | What It Assumes |
|---|---|---|---|
| [component] | [signal it sends] | [implicit value] | [audience/context assumption] |

**Inconsistencies**

| Inconsistency | What Conflicts | Why It Jars | Recommended Adjustment |
|---|---|---|---|
| [name it precisely] | [the specific conflict] | [effect on the reader/user] | [what to change] |

**Overall Coherence Assessment:** [unified / partially coherent / incoherent + rationale]

---

## Notes

Coherence is not uniformity — contrast and tension can serve a unified vision. The
question is whether every element is working toward the same intended identity, even
if they take different forms to do it. The most common source of incoherence is not
bad judgment but absent shared vision — people optimised locally for different things.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Coherence checked. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-aesthetic-elegance-testing` — Test the elegance of the coherent elements
  - `/s4h-writing-restructure` — Restructure incoherent elements
  - `/s4h-logic-consistency-check` — Check logical consistency alongside aesthetic coherence
  - **Done** — Wrap up and synthesise what we have so far
