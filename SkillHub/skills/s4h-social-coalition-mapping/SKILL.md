---
name: s4h-social-coalition-mapping
description: "Maps who needs to be aligned, who already is, and how to build the coalition a proposal needs to succeed. Triggers: 'coalition building', 'who do I need to get on board', 'map the support', 'build alignment', 'who will support this', 'who will block this'."
---

# Coalition Mapping

Proposals fail not because they are wrong, but because they lack the support needed to move. Coalition mapping makes the social landscape explicit: who is already on board, who is opposed, who is persuadable, and what sequence of engagement gives the best chance of success.

---

## Your Process

**Step 1: Define the Required Support**
What does success require? Formal approval from whom? Informal buy-in from whom? What is the minimum needed for the proposal to move?

**Framing check:** Confirm the specific proposal and its success conditions before continuing. State what you've identified — the actual proposal being mapped, who owns it, and what "winning" looks like — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the proposal, its goal, and the decision-making context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: List All Relevant Stakeholders**
Everyone who could affect whether this succeeds — including those who are currently uninvolved.

**Step 3: Map Current Stance and Intensity**
For each stakeholder: current position (Supportive / Neutral / Resistant / Unknown) and intensity (Strong / Mild).

**Step 4: Analyse Supportive Stakeholders**
Who does each supporter influence? Whose support can they bring along? How can they be activated rather than staying passive?

**Step 5: Analyse Resistant Stakeholders**
What is the specific objection driving resistance — not what you assume, but what you know or can find out? What would genuinely move them? What would they need to be true?

**Step 6: Identify the Minimum Viable Coalition**
**Before narrowing:** Show the complete stakeholder list from Step 2–3 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] stakeholders. Before I select the minimum viable coalition, are there any you'd flag as especially critical, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific stakeholder to include
  - **Add a missing one** — user will describe them

What is the smallest set of stakeholders that, if aligned, makes success likely? Focus energy on this set first.

**Step 7: Design the Engagement Sequence**
Who should be approached first? Whose support makes others more likely to join? Whose endorsement unlocks a key gatekeeper?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Critical allies only** — Who must be on board without whom this fails
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Stakeholder Stance Map
| Stakeholder | Current Stance | Intensity | Influence Over Others |
|-------------|---------------|-----------|----------------------|
| ... | Supportive / Neutral / Resistant / Unknown | Strong / Mild | [Who they influence] |

### Minimum Viable Coalition
Name the core set and explain why their alignment is sufficient for success.

### Engagement Sequence
1. [First contact — why them first]
2. [Second — whose support they unlock]
3. [Continue...]

### What Moves Resistant Stakeholders
| Stakeholder | Specific Objection | What Would Move Them |
|-------------|-------------------|---------------------|
| ... | ... | ... |

---

## Notes

The engagement sequence matters as much as the coalition map — the order in which you build support shapes whether the coalition holds or fragments under pressure.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Coalition mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-alliance` — Build strategy to expand or strengthen the coalition
  - `/s4h-game-theory-coalition` — Analyse the game dynamics within the coalition
  - `/s4h-social-incentive-analysis` — Align incentives to hold the coalition together
  - **Done** — Wrap up and synthesise what we have so far
