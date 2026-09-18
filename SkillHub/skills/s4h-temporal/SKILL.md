---
name: s4h-temporal
description: "Entry point for the temporal thinking toolkit. Routes to the right temporal skill based on your situation. Use when you say 'temporal', 'timing', 'when', 'long term', 'what happens in 5 years', 'what cycle is this', 'should we wait', 'possible futures', or want time-horizon thinking applied without knowing which specific tool fits."
---

# Temporal

Applies temporal reasoning to timing, horizons, cycles, and futures. Diagnoses what kind of time-based analysis is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Identify what cycle this is and where in it you are | cycle-detection |
| Map consequences across short, medium, and long horizons | horizon-mapping |
| Explore possible, probable, and preferable futures | futures-mapping |
| Assess whether now is the right time to act | timing-analysis |

## Routing Decision

- **Situation feels like a pattern that repeats — want to know where in it** → cycle-detection
- **Decision has different implications at different time scales** → horizon-mapping
- **Planning for an uncertain future with multiple possible paths** → futures-mapping
- **Wondering whether to act now or wait** → timing-analysis
- **Unclear** → horizon-mapping; mapping consequences across time scales usually surfaces timing questions, cycles, and futures simultaneously

**Framing check:** Confirm the temporal situation before routing. State what you've identified — the specific situation, the time dimension in focus, and the decision or question at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the temporal situation and what kind of time-based analysis is needed]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Cycle Detection

*Identifies what recurring cycle this is and where you currently are.*

Most situations are instances of known cycles: hype cycles, market cycles, innovation S-curves, organizational life cycles, political pendulums. Name the cycle candidates. Test each: does the current situation match the structural characteristics of this cycle? What is the evidence for each phase position? Knowing where in the cycle you are changes what the right action is — the same move is correct in one phase and disastrous in another.

**Output:** Cycle identified with evidence, current phase, what the cycle predicts comes next, and what the phase position implies for current decisions.

---

## Horizon Mapping

*Maps consequences of a decision across short, medium, and long time horizons.*

Many decisions that look good in the short term are harmful in the long term, and vice versa. Map the consequences of each option at three horizons: (1) Short — what changes in the next 1-3 months? (2) Medium — what does this look like in 1-2 years? (3) Long — what is the 5-10 year trajectory? Look especially for short-term gains that create long-term lock-in or erosion, and short-term costs that build long-term capacity.

**Output:** Three-horizon consequence map for each option, with particular attention to short-term/long-term trade-offs and lock-in risks.

---

## Futures Mapping

*Explores possible, probable, and preferable futures.*

Use the futures cone: (1) Possible — what could happen (full range), (2) Plausible — what could reasonably happen given current trends, (3) Probable — what is likely to happen if current trajectories continue, (4) Preferable — what should happen and how to move toward it. For each quadrant: identify the key uncertainties driving divergence. Build 3 distinct scenarios: the continuation, the disruption, and the transformation.

**Output:** Futures map across all four quadrants, key uncertainties, three scenarios (continuation/disruption/transformation), and what this implies for decisions being made today.

---

## Timing Analysis

*Assesses whether now is the right time to act, wait, or prepare.*

Timing matters as much as the action itself. Assess four dimensions: (1) Readiness — is the capability to execute actually present? (2) Window — is there a time-limited opportunity or threat? (3) Momentum — is the context moving toward or away from favorable conditions? (4) Cost of waiting — does delay make things harder, or allow important information to emerge? The right action at the wrong time often fails; the same action at the right time succeeds.

**Output:** Assessment across all four dimensions, the timing recommendation (act now / wait / prepare to act), and the conditions that would trigger reassessment.
