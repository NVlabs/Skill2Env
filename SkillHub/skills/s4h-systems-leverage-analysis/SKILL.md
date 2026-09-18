---
name: s4h-systems-leverage-analysis
description: "Finds where small interventions produce large, lasting change using Donella Meadows' leverage point hierarchy. Use when asked 'where should we intervene', 'highest leverage', 'what actually changes this system', or 'find the lever'."
---

# Systems Leverage Analysis

Most interventions target low-leverage parameters — adjusting numbers, tweaking rates — when high-leverage structural points are available and being ignored. Donella Meadows identified 12 places to intervene in a system, ranging from parameters (nearly powerless) to paradigm (most powerful). The reason high-leverage points go unused is that they face the highest resistance; understanding this is part of the analysis.

---

## Your Process

**Step 1: List Candidate Interventions**
Gather all interventions currently being considered or tried. Include past attempts that failed.

**Framing check:** Confirm the specific system and the interventions in focus before continuing. State what you've identified — the system being analysed and the intervention set you're working with — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system and the interventions being examined]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Classify by Meadows Hierarchy**
Map each intervention to its leverage level:
- **Low:** numbers/parameters, buffer sizes, flow rates
- **Medium:** feedback loop strength, information flows, rules of the system
- **High:** goals of the system, system structure, paradigm (the beliefs that create the system)

**Step 3: Identify the Default Level**
What level is typically targeted — and why? Understand the political, cognitive, or practical reasons low-leverage points get chosen.

**Step 4: Surface Ignored High-Leverage Points**
**Before narrowing:** Show the complete classified set of interventions from Step 2 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] interventions across the leverage hierarchy. Before I select the highest-leverage options to focus on, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific intervention to include
  - **Add a missing one** — user will describe it

What higher-leverage interventions exist that are not being tried? Trace why they are being avoided (too costly, politically threatening, requires belief change, long time horizon).

**Step 5: Assess Feasibility**
High-leverage points often face disproportionate resistance. For each high-leverage option: what would be required to act on it? Is it feasible given current constraints?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Highest leverage point only** — Single best intervention, skip lower-leverage options
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Intervention Table**

| Intervention | Leverage Level | Leverage Type | Feasibility | Resistance Source |
|-------------|---------------|--------------|-------------|-------------------|
| | | | | |

**Default Level Being Targeted:** [level + reason]

**Highest-Leverage Feasible Point:** [intervention + why it's higher leverage + what unlocks it]

**Ignored High-Leverage Options:** [what they are + why they're being avoided]

---

## Notes

High-leverage points are often counterintuitive — pushing harder in the obvious direction can make things worse. Identify any points where the intuitive intervention is actually negative leverage.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Leverage points identified. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-positioning` — Use leverage points for strategic positioning
  - `/s4h-resource-allocation-analysis` — Allocate resources to the highest-leverage points
  - `/s4h-decision-premortem-analysis` — Stress-test the assumptions behind leverage estimates
  - **Done** — Wrap up and synthesise what we have so far
