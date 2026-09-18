---
name: s4h-resource-bottleneck-analysis
description: "Identifies what is actually constraining throughput — using Theory of Constraints logic: the system can only move as fast as its slowest point. Triggers: 'bottleneck analysis', 'what's actually slowing this down', 'where's the constraint', 'theory of constraints', 'find the bottleneck', 'why are we moving slowly'."
---

# Bottleneck Analysis

A system can only move as fast as its slowest stage. Improving any stage other than the bottleneck does not improve overall throughput — it just creates more work waiting in front of the constraint. Finding and addressing the bottleneck is the highest-leverage intervention available.

---

## Your Process

**Step 1: Map the Process or Value Chain**
Describe all the stages in sequence. What enters each stage, what happens, and what exits? The map should cover the full flow from input to output.

**Framing check:** Confirm the specific system before continuing. State what you've identified — the process or value chain being mapped and its start and end points — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific process or value chain, including what the input and output are]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different system than read; incorporate the correction before proceeding

**Step 2: Identify Throughput per Stage**
For each stage: what is the throughput rate? How much work can it process per unit of time? Where does work visibly queue up, wait, or accumulate? Queuing upstream of a stage is the most reliable indicator of a bottleneck.

**Step 3: Identify the Current Bottleneck**
**Before narrowing:** Show the complete set of candidate stages — all stages where queuing, delays, or throughput gaps were observed — to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] stages showing constraint signals. Before I select the primary bottleneck, are there any you'd flag as especially critical, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific stage to treat as highest priority
  - **Add a missing one** — user will describe a stage or constraint not yet captured

The bottleneck is the stage with the lowest throughput that gates everything downstream. Name it specifically. Everything else in the system is constrained by its capacity.

**Step 4: Exploit the Bottleneck (No New Investment)**
Before investing in more capacity: are we getting maximum output from the bottleneck as it currently exists? What work is arriving at the bottleneck that shouldn't be there? Can quality gates be moved earlier to protect bottleneck time? Can idle time at the bottleneck be eliminated?

**Step 5: Subordinate Everything Else to the Bottleneck**
Non-bottleneck stages should operate at the rate the bottleneck can consume. Optimising non-bottleneck stages creates inventory, not throughput. Identify any optimisations elsewhere in the system that are making the bottleneck problem worse.

**Step 6: Elevate the Bottleneck**
Only after Steps 4–5: what investment would increase the bottleneck's capacity? What would it cost, and what throughput improvement would result?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Constraint identification only** — What's actually limiting throughput, skip the relief analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Process Map
[Stage 1] → [Stage 2] → [Stage 3] → ... → [Output]

### Throughput per Stage
| Stage | Throughput Rate | Queue Size / Wait Time | Bottleneck? |
|-------|----------------|----------------------|-------------|
| ... | ... | ... | Yes / No |

### Current Bottleneck
**Stage:** [Name]
**Why it's the constraint:** [Throughput evidence]

### Exploit Options (No New Investment Required)
- [Specific action to get more from the existing bottleneck]

### Subordination Recommendations
- [What should stop being optimised because it feeds the bottleneck]

### Elevation Options (Investment Required)
| Option | Investment | Throughput Improvement |
|--------|-----------|----------------------|
| ... | ... | ... |

---

## Notes

The bottleneck moves after you fix it — the next constraint becomes the new bottleneck. Repeat the analysis after each intervention rather than assuming the system is now optimised.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Bottlenecks identified. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-resource-leverage-mapping` — Find leverage at the bottlenecks
  - `/s4h-constraint-workaround-mapping` — Work around the bottlenecks that can't be removed
  - `/s4h-strategy-force-economy` — Apply force economy principles at the bottlenecks
  - **Done** — Wrap up and synthesise what we have so far
