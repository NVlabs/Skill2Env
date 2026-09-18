---
name: s4h-ethics-crisis-triage
description: "Rapid multi-framework ethical assessment when something has already gone wrong — a data breach, a harmful outcome, a discriminatory incident, a policy failure, or any situation requiring an urgent ethical response. Use when the user is dealing with an active incident or has just discovered something went wrong. TRIGGERS: 'ethics triage', 'something went wrong', 'incident ethics', 'how do we handle this', any post-incident or mid-incident situation where the ethical dimensions of a response need to be worked out fast."
---

# Ethics Crisis Triage

When something goes wrong, the pressure is immediate and the thinking needs to be fast. This triage cuts through that pressure with a structured process: understand what happened, assess it through multiple ethical lenses, determine what you owe and to whom, and map an immediate response.

It is not the full ethics council — that is for deliberate decisions. Triage is for when you don't have the luxury of deliberation. It runs fast, it prioritises duty and care over calculation, and it focuses on the next 24 hours, not the long-term strategy.

---

## Your Process

**Step 1: Establish the facts**
Before any ethical analysis, get clear on what is actually known:
- What happened? What do we know for certain vs. what is inferred?
- Who is affected and how?
- What is the current state — is the harm ongoing or contained?
- What decisions need to be made in the next hour? The next 24 hours?

Resist the urge to analyse before the facts are clear. Ethics analysis on wrong assumptions produces wrong conclusions.

**Framing check:** Confirm the ethical situation before continuing. State what you've identified — the incident or failure, who is affected, and whether harm is ongoing or contained — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the incident, affected parties, and current harm status]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Rapid framework sweep**
Run each lens quickly — this is triage, not a full audit.

**Utilitarian lens (2 minutes):**
- What is the total harm if nothing changes?
- What action minimises aggregate harm from here?
- Are there responses that help some but make things worse for others?

**Deontological lens (2 minutes):**
- What do you owe the affected parties, regardless of what's expedient?
- Are there people whose rights have been violated? What does restitution look like?
- What would you be obligated to do even if it's costly?

**Care ethics lens (2 minutes):**
- Who is most vulnerable in this situation?
- What does the relationship you have with affected people demand of you?
- Who needs to hear from you directly, not through a public statement?

**Justice lens (2 minutes):**
- Is the harm falling disproportionately on people who had less power to protect themselves?
- Is your response fair — or are you prioritising protecting yourself over making people whole?

**Step 3: Determine immediate obligations**
Based on the sweep, identify:
- **Who must be notified now** — affected parties who have a right to know
- **What must stop now** — any ongoing harm or action that must be halted immediately
- **What must be preserved** — evidence, logs, records that will matter for accountability
- **Who must decide** — what decisions require human authority, and who holds it

**Before synthesising:** State what each framework surfaced in one sentence each. Use `AskUserQuestion`:
- **Question:** "Here's what each lens found: [one bullet per framework — utilitarian, deontological, care ethics, justice]. Before I synthesise into a response framework, does any direction stand out, or is anything missing?"
- **Header:** "Synthesis direction"
- **Options:**
  - **Synthesise as planned** — frameworks covered the ground
  - **Weight [direction]** — user will name which ethical thread to emphasise
  - **Add a missing angle** — user will name a dimension not yet covered

**Step 4: Draft the response framework**
Not the communications plan — the ethical framework for how you respond:
- **Transparency**: What are you obligated to disclose, to whom, and when?
- **Accountability**: Who owns this? Is accountability being taken or deflected?
- **Remedy**: What are you offering to affected parties? Is it proportionate to the harm?
- **Prevention**: What do you commit to so this doesn't recur?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Immediate harm only** — Who's being harmed right now and what stops it fastest
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Incident:**
[What happened, what is known, who is affected, what is ongoing]

**Rapid Framework Sweep**

| Framework | Key Finding | Urgency |
|---|---|---|
| Utilitarian | [what minimises harm from here] | 🔴 / 🟡 |
| Deontological | [what you owe regardless of cost] | 🔴 / 🟡 |
| Care Ethics | [who is most vulnerable, what relationship demands] | 🔴 / 🟡 |
| Justice | [is response fair; disproportionate harm?] | 🔴 / 🟡 |

**Immediate Obligations**
- Notify now: [who]
- Stop now: [what]
- Preserve: [what]
- Decisions requiring authority: [what decisions, who decides]

**Response Framework**
- Transparency: [what to disclose, to whom, when]
- Accountability: [who owns this; is it being taken or deflected]
- Remedy: [what is being offered; is it proportionate]
- Prevention: [what commitment is being made]

**Key Ethical Risk in the Response**
[One sentence: the single biggest ethical risk in how this is being handled — e.g. "The current response prioritises legal protection over user notification, which risks compounding the original harm with a transparency failure."]

---

## Notes

Triage identifies what you're obligated to do. Whether you do it is a leadership decision, not an ethical analysis decision.

Where the triage surfaces a significant ethical dimension that wasn't being weighed in the response — name it explicitly. The value of this skill in a crisis is not reassurance; it is surfacing the thing that would later be described as "what we should have done."

For complex incidents with significant ongoing consequences, follow triage with a full `ethics-council` session once the immediate crisis is stabilised.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Crisis triaged. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-premortem-analysis` — Stress-test the crisis response plan
  - `/s4h-communication-audience-modeling` — Model how affected parties will receive the response
  - `/s4h-ethics-empathy-circle` — Apply structured empathy to those affected by the crisis
  - **Done** — Wrap up and synthesise what we have so far
