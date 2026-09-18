---
name: s4h-logic-consistency-check
description: "Surface internal contradictions, conflicting requirements, and edge cases that expose hidden conflicts in a document, spec, plan, design, or set of requirements. Use when something feels off but you can't pinpoint why, before committing to a design, or when requirements have grown incrementally and may have drifted out of sync. TRIGGERS: 'consistency check', 'find contradictions', 'does this spec make sense', 'check for conflicts', 'something feels wrong here', reviewing requirements docs, technical specs, architecture plans, product briefs, or any document where internal coherence matters."
---

# Logic Consistency Check

Requirements drift. Specs accumulate. A document written over weeks by multiple people — or a set of decisions made incrementally — can contain contradictions that nobody noticed because each piece was reviewed in isolation.

This skill reads the whole and finds where the parts disagree.

---

## Your Process

**Step 1: Map the claims**
Before checking for consistency, inventory what the document asserts:
- Goals and objectives stated
- Constraints and non-negotiables stated
- Assumptions stated or implied
- Decisions and their stated rationale
- Any numbered requirements or acceptance criteria

This map is what gets checked for internal coherence — not whether any claim is *true*, but whether the claims are consistent with each other.

**Framing check:** Confirm the specific document or set of claims before continuing. State what you've identified — the actual object being analyzed and its key parameters (document type, scope, primary claims in tension) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific document or claim set being checked]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Check goal-constraint conflicts**
Do the stated goals require violating stated constraints? Common patterns:
- A performance goal that requires more resources than the budget allows
- A simplicity goal combined with a feature list that requires complexity
- A timeline that requires skipping steps the quality requirements depend on

**Step 3: Check requirement-requirement conflicts**
Do individual requirements contradict each other?
- Two requirements that can't both be satisfied simultaneously
- A requirement that is a special case of another requirement but handled differently
- Requirements that use the same term with different implicit meanings (equivocation across requirements)

**Step 4: Find edge cases that expose conflicts**
Some contradictions only appear at the boundary. Ask: what happens when...
- Input is at its minimum and maximum values simultaneously required
- Two features interact that were designed independently
- The happy path assumption fails
- A stated exception meets a stated rule

**Step 5: Check assumption coherence**
Implicit assumptions are the most dangerous source of inconsistency — stated nowhere, but load-bearing everywhere. Surface them:
- What must be true for each requirement to be satisfiable?
- Do any of those assumptions contradict each other?
- Do any assumptions contradict stated facts?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Contradictions list only** — Flag the specific inconsistencies without full analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Subject:** [what was checked]

**Contradictions Found**

| Type | Item A | Item B | Conflict |
|---|---|---|---|
| Goal vs constraint | [goal] | [constraint] | [why they conflict] |
| Requirement vs requirement | [req] | [req] | [why they conflict] |
| Assumption vs fact | [assumption] | [fact] | [why they conflict] |

*"None found" if clean.*

**Edge Cases That Expose Conflicts**
- [scenario]: [which requirements or goals it breaks]

**Hidden Assumptions**
- [assumption]: [which requirements depend on it; whether it's safe]

**Verdict**
[Overall consistency assessment — clean, minor issues, or significant conflicts that need resolution before proceeding]

**Recommended Resolutions**
- [Specific change per conflict — which item to amend and how]

---

## Notes

Not every inconsistency is equally urgent. Flag severity: a contradiction in core requirements is a blocker; an ambiguity in an edge case may just need a decision logged. The goal is to make implicit conflicts explicit so they can be resolved consciously rather than discovered in production.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Consistency checked. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-logic-fixer` — Resolve the inconsistencies found
  - `/s4h-aesthetic-coherence-check` — Check conceptual and aesthetic coherence alongside logical consistency
  - `/s4h-identity-values-clarification` — Resolve any values conflicts underlying the inconsistencies
  - **Done** — Wrap up and synthesise what we have so far
