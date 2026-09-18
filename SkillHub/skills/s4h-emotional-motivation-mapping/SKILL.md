---
name: s4h-emotional-motivation-mapping
description: "Maps what genuinely drives different people — beyond stated reasons and job descriptions. Use when incentives seem misaligned or individual behaviour is hard to predict. TRIGGERS: 'what motivates them', 'motivation map', 'why are they behaving like this', 'what drives this person', 'understand the incentives'."
---

# Emotional Motivation Mapping

People tell you what they think they should want. They behave according to what they
actually want. When the two diverge — when stated goals and actual behaviour don't
match, when someone ostensibly aligned keeps producing friction — the problem is almost
always that the real motivators haven't been surfaced. This skill maps them across
three levels: extrinsic, intrinsic, and social.

---

## Your Process

**Step 1: List Individuals or Groups**
Name each person or group whose motivation needs mapping. Be specific — "the
engineering team" and "the engineering manager" may have completely different dominant
motivators. Split when in doubt.

**Framing check:** Confirm the specific people or groups being mapped before continuing. State what you've identified — the actual individuals or groups and the situation driving the need for this mapping — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of who is being mapped and what situation is creating the motivation question]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Extrinsic Motivators**
What external rewards and penalties shape their behaviour? Consider: compensation
structure (base, bonus, equity), formal recognition mechanisms (awards, visibility,
attribution), advancement paths available, job security, and the specific performance
metrics they're formally evaluated against. These are the motivators the system is
designed to create — they may or may not match what actually drives behaviour.

**Step 3: Intrinsic Motivators**
What internal drives are they pursuing independently of external reward? Consider:
mastery (the desire to get better at something they care about), autonomy (control
over how and when they work), purpose (feeling the work connects to something that
matters), belonging (being part of a team or mission they identify with). These often
operate below the surface but produce the most durable behaviour.

**Step 4: Social and Political Motivators**
What does their standing among peers require? Consider: status within the group and
how they maintain or advance it, key relationships they're protecting and what those
require, reputation they're managing across different audiences, being seen as
credible, indispensable, or ahead of the curve.

**Step 5: Dominant Motivator**
**Before narrowing:** Show the complete set of motivators surfaced across Steps 2–4 for each person or group. Use `AskUserQuestion`:
- **Question:** "I've identified the following motivators across extrinsic, intrinsic, and social dimensions. Before I select the dominant one for each person or group, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific motivator to include or elevate
  - **Add a missing one** — user will describe a motivator not yet captured

Given all three categories, what is the single strongest driver for this person or
group? The dominant motivator is the one that, if frustrated, would produce the most
significant behavioural change — or that, if served, would unlock the most
discretionary effort.

**Step 6: Situation Assessment and Alignment Recommendations**
Does the current situation reward or punish their dominant motivator? Be specific
about the mechanism. If it punishes — and many organisations inadvertently punish
their people's dominant motivators — describe what specific changes would bring
motivators into alignment with the desired outcome.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Core driver only** — The deepest motivation beneath the stated reasons
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Motivation Map**

| Person/Group | Extrinsic | Intrinsic | Social/Political | Dominant Motivator |
|---|---|---|---|---|
| [name/role] | [key external rewards/penalties] | [mastery/autonomy/purpose/belonging] | [status/relationships/reputation] | [single strongest driver] |

**Situation Assessment**
For each dominant motivator: does the current situation reward or punish it? Name
the specific mechanism — the exact way the setup serves or frustrates the dominant
motivator.

**Alignment Recommendations**
What specific changes would align each dominant motivator with the needed outcome?
Prioritise by likely influence on actual behaviour.

---

## Notes

Dominant motivators rarely change — but the situation around them can be redesigned.
Look for the misalignment first; don't assume the solution is to change the person.
The most common failure is designing incentive systems around extrinsic motivators
while the dominant motivator is intrinsic — the system pulls in the wrong direction
and produces compliance without commitment.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Motivations mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-audience-modeling` — Model communication strategy based on motivations
  - `/s4h-social-incentive-analysis` — Connect motivations to incentive structures
  - `/s4h-emotional-resistance-diagnosis` — Identify where motivations create resistance
  - **Done** — Wrap up and synthesise what we have so far
