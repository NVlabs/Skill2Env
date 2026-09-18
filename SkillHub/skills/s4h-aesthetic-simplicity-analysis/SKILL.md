---
name: s4h-aesthetic-simplicity-analysis
description: "Finds the simpler version while preserving what matters — not arbitrary reduction, but finding the core and discarding what is not it. TRIGGERS: 'find the simple version', 'simplify this', 'what's the essence', 'less but better', 'strip it back', 'what could we remove'."
---

# Aesthetic Simplicity Analysis

Simplicity is not minimalism for its own sake — it is the clarity that emerges when
everything that obscures the essence has been removed. Most things accumulate layers:
additions made under pressure, elements that hedge against edge cases, features added
to satisfy someone who asked. The result is a thing that does everything adequately
and nothing powerfully. This skill finds the core and tests what must stay, what can
go, and what removal would actually cost.

---

## Your Process

**Step 1: State the Thing and Its Purpose**
What is it, and what is it supposed to do? Name the object — a strategy, product,
message, design, process, argument — and state its job in one sentence. If the
purpose isn't clear, clarifying it is the first act of simplification.

**Framing check:** Confirm the specific subject before continuing. State what you've identified — the actual object being analyzed and its intended purpose — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific object and its purpose]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Find the Essence**
If you could keep only one thing — one idea, one element, one mechanism — and it had
to carry the entire weight of the purpose, what would it be? State this as one
sentence. This is the essence. Everything else in the analysis flows from whether
it serves this or doesn't.

**Step 3: Classify Each Element**
Go through every component or layer. Assign each one of three classifications:
- **Essence** — it is the core, or it expresses the core directly and powerfully
- **Supporting the essence** — it helps the core do its job; without it the
  essence is harder to access or less effective
- **Obscuring the essence** — it dilutes the core, competes with it for attention,
  or adds noise that the reader or user must filter out to reach what matters

**Step 4: Remove and Reduce**
Eliminate everything classified as obscuring. Reduce everything classified as
supporting to the minimum required for the essence to land clearly. Each reduction
is a decision — name what it costs and why that cost is acceptable.

**Step 5: Test with What Remains**
With the reduced set: can the essence be felt clearly? Does the version with less
do the original job? If not, something was misclassified — a supporting element was
actually doing more work than was visible. Revise and keep it.

**Step 6: Name What Was Lost**
What was removed, and what did each removal cost? Some removals are free — the
element was noise that looked like signal. Some involve real trade-offs — the
removed element served a secondary purpose worth acknowledging even if not worth
keeping.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Removals only** — What can be cut while preserving what matters
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Essence:** [one sentence — the irreducible core of what this thing is and does]

**Element Classification**

| Element | Classification | Rationale |
|---|---|---|
| [component] | [essence / supporting / obscuring] | [why — what it does for the core] |

**Simplified Version:** [what remains after removal and reduction]

**What Was Lost**

| Removed Element | What It Did | Acceptable Loss? |
|---|---|---|
| [element] | [secondary function] | [yes — free / yes — acceptable trade-off / no — reclassify] |

**Verdict:** Does the simplified version deliver the essence clearly?
[yes / partial — state what's still competing / no — revise classification]

---

## Notes

The goal is not the shortest version but the clearest. A long thing can be simple if
every part serves the essence. A short thing can be incoherent if it's just been cut
without finding the core first. Simplicity is achieved when adding anything would be
wrong, and removing anything would be a loss.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Simplicity analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-aesthetic-elegance-testing` — Test the elegance of the simplified version
  - `/s4h-writing-line-editing` — Edit for the simplicity findings
  - `/s4h-aesthetic-coherence-check` — Check the simplified version still coheres
  - **Done** — Wrap up and synthesise what we have so far
