---
name: s4h-historical-precedent-analysis
description: "Finds and applies genuinely similar historical situations to inform a current decision — distinguishing true precedents from superficial analogies. TRIGGERS: 'historical precedent', 'has this happened before', 'what does history say', 'find a precedent', 'what did others do in this situation'."
---

# Historical Precedent Analysis

History doesn't repeat — but structures do. The error is searching for surface
similarity (same industry, same technology, same geography) and missing structural
similarity (same underlying dynamics, same constraint set, same incentive conflicts).
Superficial precedents produce false confidence. Structural precedents produce genuine
insight. This skill finds the real ones.

---

## Your Process

**Step 1: Abstract the Situation**
Strip away domain-specific language and surface details. What is the underlying
structural pattern? Describe it in terms that could apply across industries and eras:
a new entrant facing incumbents with switching-cost moats; a coalition with aligned
goals but divergent interests trying to coordinate; a technology displacing a
profession whose members control the adoption decision. State the situation in these
structural terms — this is what you'll search for in history.

**Framing check:** Confirm the specific situation before continuing. State what you've identified — the actual situation being analyzed and its core structural pattern — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence structural framing of the situation]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Search for Structural Precedents**
Deliberately look outside the obvious domain. The most obvious precedent (same
industry, earlier decade) usually has the most surface similarity and the least
structural insight — the surface differences are visible but the structural
similarities are already assumed. Search across industries, eras, and scales for
situations with the same underlying dynamics.

**Before narrowing:** Show the complete generated set to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] candidate precedents. Before I select the most structurally similar, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific precedent to include
  - **Add a missing one** — user will describe it

Then find 2-3 with the strongest structural match.

**Step 3: Describe Each Precedent**
For each: what was the specific situation, what approaches were tried, what was the
outcome? Be concrete — vague historical reference ("like the industrial revolution")
is not a precedent. A precedent is a specific case with specific decisions and
specific results.

**Step 4: Structural Mapping**
For each precedent: where does the structural similarity hold most clearly? Where
does it break down? What are the key variables that differ between the historical
case and the current situation — and how might those differences change what the
precedent implies?

**Step 5: Extract the Lesson**
Not "do what they did" — that's surface imitation that ignores structural
differences. The lesson is: what does their experience suggest matters most in this
type of situation? What was the decisive variable? What would have changed the
outcome if it had been different?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Closest precedent only** — The single most structurally similar historical case, fully developed
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Situation (Abstracted):** [structural description in domain-neutral terms]

**Precedents**

| Precedent | What/When | What Was Tried | Outcome |
|---|---|---|---|
| [descriptive name] | [specific context] | [approach taken] | [what happened] |

**Structural Mapping**

| Precedent | Where It Maps | Where It Diverges | Key Differing Variables |
|---|---|---|---|
| [name] | [structural overlap] | [structural gap] | [variables that differ] |

**Lesson:** [the transferable principle — the underlying rule, stated without
domain-specific language]

**Caveats:** [where the precedent fails to apply and what would need to be different
for it to hold]

---

## Notes

The strongest precedent is often the most surprising one — from a completely
different domain that shares the underlying dynamics. Don't default to the obvious
comparison within the same industry. The abstractions done in Step 1 determine the
quality of everything that follows — spend time there.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Precedents analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-historical-lesson-extraction` — Extract lessons from the precedents found
  - `/s4h-decision-criteria-weighting` — Weight criteria against precedent outcomes
  - `/s4h-strategy-positioning` — Position relative to what happened in comparable cases
  - **Done** — Wrap up and synthesise what we have so far
