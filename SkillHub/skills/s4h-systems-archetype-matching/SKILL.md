---
name: s4h-systems-archetype-matching
description: "Applies the 8 classic system archetypes (Senge) to diagnose recurring system behavior. Use when asked 'this keeps repeating', 'the fix made it worse', 'we've solved this before', 'identify the pattern', or 'system archetype'."
---

# Systems Archetype Matching

Recurring system behaviors are not unique — they follow a small set of structural patterns that have known causes and known high-leverage responses. Senge's eight archetypes give names to these patterns. Matching the current situation to an archetype tells you what structure is producing the behavior and what intervention actually works, rather than re-discovering the same solution each cycle.

---

## Your Process

**Step 1: Describe the Recurring Behavior**
State what keeps happening. Include: what was tried, what temporarily worked, what came back. The more specific, the better the match.

**Framing check:** Confirm the specific system and its recurring behavior before continuing. State what you've identified — the system in question, the behavior that keeps repeating, and what has been tried — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system and recurring behavior]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Compare Against All Eight Archetypes**
Screen each archetype:
- **Limits to Growth:** growth slows unexpectedly as a constraint is hit
- **Shifting the Burden:** symptomatic fix used repeatedly, undermining fundamental solution
- **Eroding Goals:** goals lowered to close the gap instead of improving performance
- **Escalation:** two parties each respond to the other's actions by increasing their own
- **Success to the Successful:** winner gets more resources, making it harder for others to compete
- **Tragedy of the Commons:** shared resource overused because individual gain exceeds individual cost
- **Fixes that Fail:** short-term fix has delayed negative side effects that recreate the problem
- **Growth and Underinvestment:** growth slows because capacity investment lags demand

**Step 3: Select the Best Match**
**Before narrowing:** Show the complete screened set to the user first. List all archetypes that plausibly match — even partial fits — before selecting one. Use `AskUserQuestion`:
- **Question:** "I've identified [N] archetypes with some fit. Before I select the strongest match, are there any you'd flag as especially relevant, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific archetype to include or elevate
  - **Add a missing one** — user will describe a pattern not yet captured

Choose the archetype whose causal structure most closely matches the described situation. Note any secondary archetypes.

**Step 4: Map the Situation Onto the Archetype**
Translate the archetype's generic variables into the specific people, resources, decisions, and feedback loops of this situation.

**Step 5: Apply the Standard Intervention**
Each archetype has a known high-leverage response. State it for this situation specifically.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Archetype identification only** — Name the recurring system pattern, skip full dynamics analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Archetype Match:** [archetype name] (secondary: [if any])

**Why It Matches:** [2–3 sentences mapping behavior to archetype structure]

**Situation Mapped to Archetype Structure**

| Archetype Variable | This Situation |
|-------------------|---------------|
| | |

**Standard Intervention:** [what actually works for this archetype, made specific to this situation]

**What to Stop Doing:** [the low-leverage or counterproductive response the archetype predicts]

---

## Notes

If two archetypes both fit, that is meaningful — overlapping archetypes indicate a more entrenched structure. Apply the higher-leverage archetype's intervention first.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Archetype matched. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-systems-leverage-analysis` — Find leverage points within the matched archetype
  - `/s4h-systems-feedback-mapping` — Map feedback loops specific to the archetype
  - `/s4h-historical-precedent-analysis` — Find historical precedents for this archetype
  - **Done** — Wrap up and synthesise what we have so far
