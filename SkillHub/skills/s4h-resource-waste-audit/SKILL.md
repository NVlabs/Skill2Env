---
name: s4h-resource-waste-audit
description: "Finds where resources are being lost, duplicated, or underused — the seven wastes applied to knowledge work. Triggers: 'waste audit', 'where are we wasting resources', 'inefficiency audit', 'find the waste', 'what's being duplicated', 'resource leakage'."
---

# Resource Waste Audit

In manufacturing, Toyota identified seven categories of waste. They apply equally to knowledge work — with a different surface appearance but the same underlying structure. The goal is to find where resources are consumed without producing value.

---

## The Seven Wastes in Knowledge Work

| Waste | Description |
|-------|-------------|
| **Waiting** | Idle time between steps — work blocked pending a decision, review, or dependency |
| **Overproduction** | Producing more than is needed — reports no one reads, features no one uses |
| **Rework** | Fixing what should have been right — re-doing work due to unclear requirements or poor handoffs |
| **Duplication** | The same work being done in two places — parallel efforts, re-discovered knowledge |
| **Motion** | Unnecessary switching or handoffs — context switching, excessive meetings, process overhead |
| **Inventory** | Work in progress that is not flowing — large backlogs, features built but not shipped |
| **Over-processing** | More effort than the task requires — over-engineered solutions, unnecessary polish |

---

## Your Process

**Step 1: Map the Workflow or Resource Allocation**
Describe how work moves through the system — the full path from input to value delivery.

**Framing check:** Confirm the specific workflow or resource area before continuing. State what you've identified — the system or team being audited and its primary resource inputs — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the workflow or resource area being audited]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Scan Each Waste Category**
For each of the seven wastes: where does it appear in the workflow? Look for specific instances, not general impressions.

**Step 3: Quantify Each Waste**
Estimate roughly how much resource each waste consumes — time per week, headcount, or percentage of capacity. Rough estimates are fine; the goal is to rank, not to audit precisely.

**Step 4: Root Cause per Waste**
Why does this waste exist? Process design? Incentive structure? Unclear ownership? Identifying the root cause determines whether the fix is simple or systemic.

**Step 5: Rank by Impact and Recommend**
Which waste removal would free the most resource?

**Before narrowing:** Show the complete set of identified waste instances to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] waste instances across the seven categories. Before I select the top three by impact, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific waste instance to include in the top three
  - **Add a missing one** — user will describe a waste instance not yet identified

Prioritise the top three and propose specific actions.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Biggest waste items only** — Top 3 losses by magnitude, skip smaller inefficiencies
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Waste Inventory
| Waste Type | Where It Appears | Estimated Resource Cost | Root Cause |
|-----------|-----------------|------------------------|------------|
| Waiting | ... | ... | ... |
| Overproduction | ... | ... | ... |
| Rework | ... | ... | ... |
| Duplication | ... | ... | ... |
| Motion | ... | ... | ... |
| Inventory | ... | ... | ... |
| Over-processing | ... | ... | ... |

### Top 3 Waste Reductions (Ranked by Impact)
1. **[Waste type]** — [Specific action] — [Expected resource freed]
2. **[Waste type]** — [Specific action] — [Expected resource freed]
3. **[Waste type]** — [Specific action] — [Expected resource freed]

---

## Notes

Rework and duplication are usually the most expensive wastes in knowledge work, but waiting is often the most demoralising. Address the highest-cost waste first, but don't ignore the one most affecting morale.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Waste audited. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-resource-allocation-analysis` — Reallocate resources freed by eliminating waste
  - `/s4h-resource-leverage-mapping` — Reinvest freed capacity into high-leverage areas
  - `/s4h-decision-criteria-weighting` — Weight decisions after waste is removed from the picture
  - **Done** — Wrap up and synthesise what we have so far
