---
name: s4h-constraint-scope-reduction
description: "Finds the minimum that satisfies the actual requirement — stripping everything wanted but not needed. Triggers: 'minimum viable', 'what's the minimum', 'strip this back', 'what do we actually need', 'scope reduction', 'simplify the requirement'."
---

# Constraint Scope Reduction

Scope grows because wants accumulate alongside needs, and no one separates them. This skill
forces that separation. The goal is not to build less — it is to find the version where
every element is doing real work, and nothing is there because it sounded good in the
planning meeting.

---

## Your Process

**Step 1: State the Full Current Scope**
List everything in the current plan, feature set, or requirement. Be complete — you can
only strip what you've named.

**Framing check:** Confirm the constraint and the goal it is blocking before continuing. State what you've identified — the specific scope being reduced and the core job it must accomplish — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the scope and the core job it must accomplish]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Find the Core Job**
Ask: what is the single verb this must do? Not what it should do, what it must do. Strip
all nouns and adjectives until only the job remains. "A user can complete a purchase" is a
job. "A seamless, intuitive checkout experience" is not.

**Step 3: Classify Each Element — Must or Want**
For every element in scope: is it required for the core job (must) or desired beyond it
(want)? Apply pressure to musts — if you removed it, would the core job fail?

**Step 4: Remove All Wants and Test**
Drop every want. Confirm: can the core job still be done? If yes, the wants were not load-
bearing. If no, you've found a hidden must — reclassify and investigate why it felt optional.

**Step 5: Simplify the Musts**
For each must: is there a simpler way to achieve the same outcome? Simpler means fewer
moving parts, less code, lower cost, or faster delivery — not necessarily less effort to
design.

**Step 6: State the Minimum Viable Version**
Write the minimum scope in a single paragraph. It should be possible to build from this
description without the original scope document.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Minimum viable scope only** — The smallest version that still satisfies the actual need
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Current scope:**
> [Bulleted list of everything in scope]

**Core job (the verb):**
> [Single sentence]

**Must vs Want classification:**

| Element | Must / Want | Reason |
|---------|-------------|--------|
| | | |

**What was removed and why it's safe to remove:**
> [Brief list — each removal with one-line justification]

**Minimum viable scope:**
> [Single paragraph — buildable without further clarification]

---

## Notes

The most common mistake is reclassifying wants as musts when pressure is applied. Challenge
every must: "if we launched without this, what actually breaks?" The answer is usually
"nothing breaks, someone would be annoyed."

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Scope reduced. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-criteria-weighting` — Evaluate options within the reduced scope
  - `/s4h-resource-allocation-analysis` — Reallocate for the new scope
  - `/s4h-decision-premortem-analysis` — Stress-test the reduced scope plan
  - **Done** — Wrap up and synthesise what we have so far
