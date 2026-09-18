---
name: s4h-historical-cycle-detection
description: "Identifies what recurring cycle the current situation is an instance of — and where in that cycle you currently are. TRIGGERS: 'what cycle is this', 'where are we in the cycle', 'is this a bubble', 'what comes next', 'have we been here before'."
---

# Historical Cycle Detection

Most situations that feel unprecedented are instances of recognisable cycles. The
value of cycle identification is not prediction — cycles don't produce certainties —
it is orientation. Knowing where you are in the cycle tells you what phase logic to
apply, what the typical incentive pressures are at this point, and what tends to come
next absent a significant disrupting variable.

---

## Your Process

**Step 1: Describe the Situation and Recent Trajectory**
What is happening and how has it developed? Focus on direction of change —
accelerating, plateauing, reversing — and the sentiment among participants. Sentiment
is often the most reliable indicator of cycle position because it drives behaviour
independently of fundamentals.

**Framing check:** Confirm the specific situation before continuing. State what you've identified — the actual subject being analyzed, the domain it belongs to, and the rough time horizon in view — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific situation and its trajectory]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Match to the Most Fitting Cycle**
Evaluate against these candidate cycles. List every candidate cycle that is a plausible match, with one sentence of reasoning for each.

**Before narrowing:** Show the complete set of plausible candidate cycles to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified the following cycles as plausible matches: [list each candidate with one sentence of reasoning]. Before I select the strongest match, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific cycle to prioritise
  - **Add a missing one** — user will describe an alternative cycle to consider

Then select the strongest match:
- **Hype cycle** — technology moves through peak of inflated expectations, trough
  of disillusionment, slope of enlightenment, plateau of productivity. Characterised
  by sentiment-fundamentals divergence.
- **Bubble-and-bust** — asset price or belief system inflates beyond fundamentals,
  sustained by new-entrant demand and self-referential confidence, then corrects
  sharply when the marginal buyer disappears.
- **Adoption curve** — innovators, early adopters, early majority, late majority,
  laggards. Each phase has different buyer motivations and objections.
- **Political cycle** — power consolidates, overreaches, triggers backlash, produces
  reform or counter-consolidation. The mechanism is legitimacy erosion via overreach.
- **Organisational change curve** — shock, denial, resistance, exploration,
  commitment. The emotional response to disruptive change follows a consistent arc.
- **Competitive cycle** — fragmented competition, consolidation, dominant player
  emergence, disruption by new entrant. Each phase has characteristic dynamics.

**Step 3: Map Current Position**
Where on the cycle is the current situation? Be specific — not just "early stage"
but the named phase and what observable evidence places it there. Name two or three
specific current conditions that locate the position.

**Step 4: Characteristic Signs of Current Phase**
What are the typical behavioural and structural signals of this phase? Go through
them systematically: which are clearly present? Which are absent or weaker than the
typical pattern would predict?

**Step 5: Typical Next Phase**
What follows the current phase? What structural conditions or trigger events typically
cause the transition? How long do transitions typically take?

**Step 6: Divergences**
Where does the current situation deviate from the typical cycle pattern? Divergences
are the most analytically important output — they indicate either that this cycle is
playing out differently, or that the cycle identification needs revision.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Pattern match only** — The specific historical cycle this most resembles
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Cycle Match:** [cycle type + one-sentence rationale for why this is the right match]

**Current Position:** [named phase + specific evidence that locates it there]

**Characteristic Signs**

| Sign of Current Phase | Present / Absent / Partial | Notes |
|---|---|---|
| [typical indicator for this phase] | [assessment] | [specific observation] |

**Typical Next Phase:** [what usually follows + the conditions that trigger the transition]

**Divergences:** [specific ways this instance departs from the typical pattern —
the highest-value analytical findings]

**Implications:** [what the cycle position suggests about current priorities, risks,
and timing]

---

## Notes

Cycle identification is a frame, not a forecast. The most valuable output is the
divergences section — where this situation doesn't fit the expected pattern is where
the most asymmetric insight lives. If there are no divergences, the analysis isn't
done.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Historical cycles detected. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-temporal-cycle-detection` — Map the cycles forward into the future
  - `/s4h-systems-archetype-matching` — Match the current situation to historical archetypes
  - `/s4h-strategy-timing` — Align strategy with the detected cycles
  - **Done** — Wrap up and synthesise what we have so far
