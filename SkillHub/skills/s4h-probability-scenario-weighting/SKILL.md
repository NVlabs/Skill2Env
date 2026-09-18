---
name: s4h-probability-scenario-weighting
description: "Assigns explicit probabilities to distinct scenarios before making a decision. Use when asked to 'assign probabilities', 'scenario weighting', 'how likely is each outcome', 'quantify the uncertainty', or 'probability distribution'."
---

# Probability Scenario Weighting

Vague uncertainty — "it might work, it might not" — produces poor decisions. Quantified uncertainty forces precision about what is actually believed and makes implicit assumptions visible. Assigning explicit probabilities to scenarios is not prediction; it is structured belief articulation. The process of assigning and calibrating probabilities often reveals more than the final numbers.

---

## Your Process

**Step 1: List Scenarios**
Enumerate all scenarios — they must be mutually exclusive (no overlap) and collectively exhaustive (cover all meaningful possibilities). If "other" is significant, make it explicit. Typically 3–5 scenarios; more than 6 reduces usability.

**Framing check:** Confirm the specific situation and uncertainty before continuing. State what you've identified — the actual decision or situation at stake and the key uncertainty being quantified — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific situation and the uncertainty being modelled]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Assign Initial Probabilities**
Assign a probability to each scenario. They must sum to 100%. Do this before analyzing each scenario in detail — your prior is informative and anchoring matters.

**Step 3: Calibration Check**
For each probability: would you accept a bet at these odds? If you assigned 70% to a scenario, you should be willing to accept 3:7 odds against it. If the bet feels uncomfortable at those odds, your stated probability is wrong. Adjust.

**Step 4: Identify Key Driver for Each Scenario**
What would need to be true for each scenario to occur? What is the single most important condition that must hold?

**Step 5: Find the High-Probability and High-Impact Scenarios**
**Before narrowing:** Show the complete calibrated scenario table to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] scenarios with assigned probabilities. Before I select the highest-probability and highest-impact ones to focus on, are there any scenarios you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the scenario set looks right
  - **Flag one** — user will name a specific scenario to prioritise
  - **Add a missing one** — user will describe a scenario to include

These may be the same scenario or different ones. If the highest-probability scenario is low-impact and the highest-impact scenario is low-probability, name both — they require different responses.

**Step 6: Identify Most Useful Information**
What new information would most update these probabilities? This determines what to investigate next. Information that confirms the most likely scenario is usually less valuable than information that discriminates between scenarios.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Top 3 scenarios only** — Most likely, most harmful, most surprising
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Scenario Table**

| Scenario | Probability | Key Driver (must be true) | Primary Implication |
|----------|-------------|--------------------------|---------------------|
| | | | |
| **Total** | **100%** | | |

**Highest-Probability Scenario:** [name + %, implications]

**Highest-Impact Scenario:** [name + %, implications — note if same or different from above]

**Most Useful Information to Gather:** [the question whose answer would most shift these probabilities]

---

## Notes

Resist collapsing scenarios into "optimistic / realistic / pessimistic" — this framing anchors on the most optimistic outcome and treats the middle case as truth. Build scenarios around key uncertainties, not emotional valence.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Scenarios weighted. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-premortem-analysis` — Run a premortem on the worst weighted scenarios
  - `/s4h-decision-criteria-weighting` — Weight decision criteria against scenario probabilities
  - `/s4h-temporal-horizon-mapping` — Map the weighted scenarios across time horizons
  - **Done** — Wrap up and synthesise what we have so far
