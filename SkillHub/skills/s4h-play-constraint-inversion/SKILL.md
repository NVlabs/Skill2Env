---
name: s4h-play-constraint-inversion
description: "Removes or inverts the main constraint to see what becomes possible — then uses those unconstrained solutions to find real ones. TRIGGERS: 'what if there were no constraints', 'rule inversion', 'what if we could do anything', 'break the rules', 'invert the assumption'."
---

# Play: Constraint Inversion

Most constraints are treated as fixed when they are actually assumed. The ones that
are genuinely fixed are fewer than people believe — and the ones that are assumed
become invisible over time because they've been treated as given for so long.
Inverting a constraint — imagining its complete opposite — reveals what underlying
goal it has been blocking and often generates solutions that work within the real
constraint once the goal becomes visible.

---

## Your Process

**Step 1: Name the Main Constraint**
What is the primary constraint on the current problem or design? Be specific — not
"we don't have enough resources" but "we have 6 weeks and two engineers available
after existing commitments." Not "the budget is limited" but "the approved budget
is $40k with no variance mechanism." Specificity matters because vague constraints
produce vague inversions.

**Framing check:** Confirm the specific constraint and the goal it is blocking before continuing. State what you've identified — the actual constraint and what it is preventing — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific constraint and the goal it blocks]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Invert Completely**
State the opposite world. Don't soften or partially invert — flip it completely.
"6 weeks and two engineers" becomes "18 months and a team of twelve." "Budget of
$40k" becomes "unlimited funding with board approval." The inversion should feel
unrealistic. That is the design — if it feels achievable, it isn't inverted enough.

**Step 3: Generate Freely in the Inverted World**
What would you do if the constraint were fully removed? Generate without filtering.
No "but we can't" or "in reality though" — those are prohibited at this stage. Generate the full set of unconstrained approaches you can identify.

**Before narrowing:** Show the complete generated set to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] unconstrained approaches. Before I select the most substantially different ones to carry forward, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific approach to include
  - **Add a missing one** — user will describe it

Then narrow to 3–5 substantially different approaches based on the user's input.

**Step 4: Find the Underlying Goal of Each**
For each unconstrained solution: strip away the specifics and name the underlying
goal it's pursuing. What is it actually trying to accomplish? This step converts
"hire a team of specialists" into "access deep expertise quickly." The goal is more
transferable than the method.

**Step 5: Reintroduce Real Constraints**
For each identified goal: is there a way to pursue this goal within the real
constraints? Sometimes yes — the unconstrained version was solving the right problem
in an impossible way, and a constrained version exists. Sometimes no — the goal is
genuinely blocked by the constraint. Both are real findings.

**Step 6: Map Real vs Assumed Constraints**
The gap between constrained and unconstrained versions shows where each constraint
is doing real work versus assumed work. A constraint does real work when it genuinely
prevents a goal. It does assumed work when the goal is achievable within it — just
not obviously. Assumed constraints are the most valuable finding.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **One inversion only** — The strongest constraint removal and what it makes possible
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Constraint:** [the specific, concrete real constraint]

**Inverted World:** [the fully opposite assumption — stated without softening]

**Unconstrained Solutions**

| Solution | Underlying Goal |
|---|---|
| [what you'd do with no constraint] | [what it's actually trying to achieve] |

**Constrained Versions:** For each goal — does a within-constraint version exist?
If yes, describe it.

**Real vs Assumed Constraints**
- Constraints doing real work (goal genuinely blocked): [list + explanation]
- Constraints doing assumed work (goal achievable within): [list — highest-value findings]

---

## Notes

The most productive output is usually not the unconstrained solutions themselves but
the underlying goals they expose — goals that were invisible while the constraint
was accepted as fixed. Those goals are the real design brief. Once visible, they
often turn out to be achievable within the actual constraints through routes that
the constrained framing had ruled out prematurely.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Constraints inverted. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-creativity-lateral-thinking` — Use the inverted constraints as lateral move springboards
  - `/s4h-decision-option-mapping` — Map options that become available in the inverted world
  - `/s4h-constraint-hardness-testing` — Test which inverted constraints are actually achievable
  - **Done** — Wrap up and synthesise what we have so far
