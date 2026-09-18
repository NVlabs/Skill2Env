---
name: s4h-constraint-hardness-testing
description: "Tests whether a stated constraint is real — distinguishing genuine limits from assumptions, habits, or politics dressed as facts. Triggers: 'is this really a constraint', 'challenge the assumption', 'who says we can't', 'is this actually fixed', 'test the constraint'."
---

# Constraint Hardness Testing

Organisations accumulate phantom constraints — rules that were real once and calcified, or
beliefs that were never tested, or someone's preference that got repeated until it sounded
like policy. This skill separates genuine limits from assumed ones before any energy is
spent working around or accepting them.

---

## Your Process

**Step 1: State the Constraint**
Write it exactly as it's been stated or assumed. Don't clean it up — the imprecision is
often where the phantom lives.

**Framing check:** Confirm the specific constraint and the goal it is blocking before continuing. State what you've identified — the exact constraint as you understand it and the goal or action it prevents — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the constraint and the goal it blocks]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Source It**
Who said this constraint exists? When? Is the source a law or regulation, a signed contract,
a technical impossibility, a leadership decision, a team preference, or unknown? The source
determines the hardness ceiling.

**Step 3: Consequence Test**
What actually happens if this constraint is violated? State the consequence concretely. If
the answer is "I'm not sure" or "someone would be unhappy," the constraint is not hard.
Distinguish real consequences (fine, contract breach, system failure) from assumed ones
(pushback, awkwardness, political cost).

**Step 4: Precedent Check**
Has anyone tried to change or violate this constraint before? What happened? No precedent
often means no one has tested it — not that it can't be changed.

**Step 5: Conditions Test**
Under what circumstances would this constraint not apply? A truly hard constraint has no
exceptions. If you can find a scenario where it wouldn't hold, the constraint is softer
than stated.

**Step 6: Classify**
- **Hard**: real source, concrete consequence, no exceptions, precedent confirms
- **Soft**: real but negotiable, consequence is political or preferential
- **Assumed**: no clear source, untested consequence
- **Outdated**: was once hard, circumstances have changed

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Real vs assumed verdict only** — Classify each constraint without full analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Constraint as stated:**
> [Exact wording]

**Source:** [Law/contract/technical/decision/preference/unknown] — [specific origin]

**Consequence if violated:**
> [Concrete statement] — Real / Assumed

**Precedent:** [What happened when tested, or "untested"]

**Conditions where it wouldn't apply:**
> [If any]

**Classification:** Hard / Soft / Assumed / Outdated

**Recommended action:**

| Classification | Action |
|----------------|--------|
| Hard | Accept — design around it |
| Soft | Negotiate explicitly |
| Assumed | Test it — ask the source directly |
| Outdated | Challenge it — propose removal |

---

## Notes

The most dangerous class is Assumed, because it looks like Hard. Before accepting any
constraint that cannot be sourced precisely, treat it as Assumed and test it — the cost of
testing is almost always lower than the cost of a permanent workaround.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Constraints tested. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-constraint-workaround-mapping` — Route around the hard constraints
  - `/s4h-constraint-scope-reduction` — Reduce scope to avoid constraints that can't be bypassed
  - `/s4h-decision-option-mapping` — See what options remain given hard and soft constraints
  - **Done** — Wrap up and synthesise what we have so far
