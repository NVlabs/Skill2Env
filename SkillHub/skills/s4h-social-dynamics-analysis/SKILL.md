---
name: s4h-social-dynamics-analysis
description: "Identifies group psychology shaping a discussion or team — groupthink, status dynamics, coalition formation, psychological safety. Triggers: 'group dynamics', 'why does this team behave like this', 'groupthink check', 'why won't people speak up', 'meeting dynamics', 'team dysfunction'."
---

# Group Dynamics Analysis

Groups develop collective behaviours that are invisible from inside them. Premature consensus, status-based deference, and psychological unsafety all degrade decision quality — and they are self-reinforcing. Naming the dynamic is the first step to changing it.

---

## Your Process

**Step 1: Observe or Recall Group Behaviour**
Work from specific, concrete instances of how the group acts — not general impressions. What actually happened in the last meeting or decision? What was said? What was not said?

**Framing check:** Confirm the specific group and context before continuing. State what you've identified — the actual group being analyzed and the situation or event in focus — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the group and the situation or event in focus]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Check for Groupthink Signals**
- Premature consensus — agreement reached without exploring disagreement
- Self-censorship — individuals privately disagree but don't speak
- Illusion of unanimity — silence treated as agreement
- Pressure on dissenters — challenge is met with discomfort or social cost
- No contingency planning — "what if we're wrong?" is not asked

**Step 3: Assess Status Dynamics**
Who speaks most, and does speaking time correlate with expertise or with seniority? Who is deferred to regardless of subject matter? Whose ideas get attributed to someone else? Status often drives decisions more than merit.

**Step 4: Assess Psychological Safety**
Do people raise concerns, admit uncertainty, and challenge ideas — or do they signal alignment and hedge? Rate: high / medium / low.

**Step 5: Identify Coalition Patterns**
Are subgroups forming? Are decisions being pre-made outside formal meetings? Are there recurring alliances or persistent tensions?

**Step 6: Name the Dominant Dynamic**
**Before narrowing:** Show all dynamics surfaced across the previous steps. Use `AskUserQuestion`:
- **Question:** "I've identified the following dynamics: [list each dynamic observed — groupthink signals, status patterns, safety level, coalition patterns]. Before I select the one most affecting decision quality, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific dynamic to prioritise
  - **Add a missing one** — user will describe it

Which single dynamic is most affecting decision quality right now? That is where intervention has the highest leverage.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Dominant dynamic only** — The group pattern that most shapes this situation
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Groupthink Signals
| Signal | Present / Absent | Evidence |
|--------|-----------------|----------|
| Premature consensus | ... | ... |
| Self-censorship | ... | ... |
| Illusion of unanimity | ... | ... |
| Pressure on dissenters | ... | ... |
| No contingency planning | ... | ... |

### Status Dynamics
Describe who dominates, who defers, and where status overrides expertise.

### Psychological Safety Assessment
**Rating:** High / Medium / Low
**Evidence:** Specific behaviours supporting this rating.

### Coalition Patterns
- [Subgroups, pre-meeting decisions, recurring alliances or tensions]

### Dominant Dynamic and Recommended Intervention
**Dominant dynamic:** [Name it clearly]
**Recommended intervention:** [Specific, concrete action to shift the dynamic]

---

## Notes

Run this before a high-stakes decision or after a meeting that felt wrong but hard to name. The intervention should be structural where possible — changing the process, not asking people to behave differently.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Social dynamics analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-social-power-mapping` — Map power relationships within the dynamics
  - `/s4h-social-incentive-analysis` — Analyse what's driving the dynamics
  - `/s4h-strategy-positioning` — Position relative to the social dynamics
  - **Done** — Wrap up and synthesise what we have so far
