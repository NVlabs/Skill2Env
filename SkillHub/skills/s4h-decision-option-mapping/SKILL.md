---
name: s4h-decision-option-mapping
description: "Ensures all real options are visible before choosing — countering the false dichotomy that limits consideration to the first two options that came to mind. Triggers: 'what are all the options', 'false dichotomy check', 'expand the option set', 'what else could we do', 'options inventory'."
---

# Decision Option Mapping

The options people choose between are usually not all the options that exist — they are
the first options that were named, which then anchored the frame. This skill expands the
option set before analysis begins, using four specific moves that reliably surface options
the natural framing excludes.

---

## Your Process

**Step 1: State the Decision and Currently-Considered Options**
Write the decision as currently framed and list all options currently on the table. Don't
filter yet — include the options even if they seem weak.

**Framing check:** Confirm the specific decision and its intended outcome before continuing. State what you've identified — the actual decision being mapped and the goal it serves — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the decision and its intended outcome]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Challenge the Frame**
Is this decision actually forced? Are you choosing between options A and B because those
are the real options, or because those are the options that were generated first? What
would have to be true for there to be no decision to make?

**Step 3: Four Expansion Moves**

**(a) Expand**: Generate 3 more ways to achieve the underlying goal. Not variations on
existing options — genuinely different approaches. Ask: if none of the current options
existed, what would we try?

**(b) Defer**: Is "decide later" viable? At what cost? Deferral is a real option — it
has costs and benefits like any other. When can this be decided without foreclosing
anything important?

**(c) Hybrid**: Can elements of multiple options be combined? Hybrids often emerge when
options are treated as mutually exclusive when they aren't.

**(d) Reframe**: If the goal were slightly different, what options appear? Sometimes
the option set is limited by the goal framing, not the constraints.

**Step 4: Add Viable New Options**
**Before narrowing:** Show the complete generated set to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] options across the four expansion moves. Before I select the genuinely viable ones, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific option to include
  - **Add a missing one** — user will describe it

From the four moves, add the options that are genuinely viable. Discard the ones that
don't survive basic scrutiny — not to narrow prematurely, but to keep the set useful.

**Step 5: Recommend Next Step**
With the expanded set, recommend which analytical tool to apply: decision-criteria-
weighting (multiple comparable options), decision-reversibility-analysis (one option being
considered), or decision-premortem-analysis (a direction already being leaned toward).

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Hidden options only** — Surface the options not currently being considered
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Decision as framed:** [Statement]
**Currently-considered options:** [List]

**Frame challenge:**
> [Is this decision forced? What assumptions are built into the current option set?]

**Expanded option set:**

| Option | Source (original / expand / defer / hybrid / reframe) | Viable? | Reason |
|--------|------------------------------------------------------|---------|--------|
| | | | |
| | | | |

**Options to add to the decision:**
> [Bulleted list with one-line rationale each]

**Recommended next step:**
> [Which analytical skill to apply, and to which expanded option set]

---

## Notes

The most commonly missed option is deferral. "Decide now" is itself a choice with costs —
urgency is often assumed rather than real, and deferral with a defined review point is
frequently the most rational option on the table.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Options mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-criteria-weighting` — Evaluate the options you've mapped against weighted criteria
  - `/s4h-decision-premortem-analysis` — Stress-test the leading option before committing
  - `/s4h-probability-scenario-weighting` — Weight options by their probability of success
  - **Done** — Wrap up and synthesise what we have so far
