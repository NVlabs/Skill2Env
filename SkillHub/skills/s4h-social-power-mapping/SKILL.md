---
name: s4h-social-power-mapping
description: "Maps who holds power — formal authority, informal influence, gatekeeping, expertise — and how it flows. Triggers: 'power map', 'who has power here', 'who actually decides', 'map the politics', 'who do I need to get on board', 'who are the gatekeepers'."
---

# Power Mapping

Org charts describe formal authority. Power is different. It includes informal influence (whose opinion shifts decisions), gatekeeping (who controls access), and expertise (whose knowledge others depend on). A proposal that ignores actual power distribution will fail even if it is correct.

---

## Your Process

**Step 1: List Relevant Actors**
Name every person, role, or group that could affect or be affected by the situation. Include those who seem peripheral — they are sometimes the most important.

**Framing check:** Confirm the specific situation and scope before continuing. State what you've identified — the context, the decision or change at stake, and whose power dynamics are in question — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation, the decision or change involved, and the organisational context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map Each Actor Across Four Power Dimensions**
- **Formal authority** — what can they officially decide or approve?
- **Informal influence** — who listens to them? Whose decisions do they shape?
- **Gatekeeping** — what access, resources, or information do they control?
- **Expertise** — what knowledge gives them authority that others defer to?

**Step 3: Map Influence Flows**
Who influences whom? Who defers to whom in practice (which may differ significantly from the org chart)? Draw or describe the actual influence network.

**Step 4: Find Power Gaps**
Who needs to be on board but hasn't been engaged? Who could block progress but hasn't been considered? These are vulnerabilities in any plan.

**Step 5: Identify Invisible Stakeholders**
Who is affected by the situation but holds little or no power to shape it? Their interests may need explicit protection.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Informal power only** — Influence not visible in the formal structure
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Actor Inventory
| Actor | Formal Authority | Informal Influence | Gatekeeping | Expertise Power |
|-------|-----------------|-------------------|-------------|-----------------|
| ... | ... | ... | ... | ... |

### Influence Map
Describe the key influence flows: who shapes whom, where deference occurs, and where the org chart diverges from practice.

### Power Gaps
- [Actor who needs to be engaged but hasn't been — and why they matter]

### Invisible / Excluded Stakeholders
- [Affected parties without power — note whether their interests need explicit advocacy]

---

## Notes

Update the power map when the situation changes significantly — power is not static. The most important finding is usually the gap between the org chart and actual influence.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Power mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-positioning` — Position relative to the power dynamics
  - `/s4h-social-coalition-mapping` — Build coalitions around power concentrations
  - `/s4h-social-incentive-analysis` — Analyse what incentives map to each power centre
  - **Done** — Wrap up and synthesise what we have so far
