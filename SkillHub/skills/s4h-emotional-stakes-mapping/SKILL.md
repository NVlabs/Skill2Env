---
name: s4h-emotional-stakes-mapping
description: "Maps what each stakeholder actually cares about underneath their stated position — because addressing the stated position while missing the real stake accomplishes nothing. TRIGGERS: 'what do they actually want', 'underlying stakes', 'what's really at stake', 'beneath the position', 'why won't they agree'."
---

# Emotional Stakes Mapping

People argue about positions. They care about stakes. Addressing the stated position
while missing the real stake is the most common reason negotiations, decisions, and
alignment efforts fail. This skill maps the gap between the two — not by guessing,
but by working systematically through what each party stands to lose if the outcome
goes against them.

---

## Your Process

**Step 1: List Stakeholders**
Identify every party with a meaningful stake in the outcome — including silent ones
who will be affected but aren't in the room. Passive non-participants often have the
highest stakes; they just have no forum to name them.

**Framing check:** Confirm the specific situation and its stakeholders before continuing. State what you've identified — the actual conflict or decision being mapped and the parties involved — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation, the core tension, and the parties involved]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Stated Position**
What is each stakeholder explicitly asking for, pushing toward, or resisting? Keep
this behaviorally specific — "they want sign-off authority" not "they want control."
Surface the precise ask.

**Step 3: Real Fear**
What are they actually afraid of losing? Common real fears: status within their
organisation, control over resources they currently hold, credit for outcomes they've
invested in, relevance if the change makes their expertise obsolete, relationships
that depend on the current arrangement, safety from blame if things go wrong. Fears
drive positions — find the fear beneath the ask.

**Step 4: Minimum Conditions for Agreement**
What would need to be true — not just what would help, but what is the floor — for
each stakeholder to feel safe enough to say yes? The minimum condition is often
surprisingly specific once the real fear is named: "I need to be cited as a
contributor" or "I need a fallback option if this fails."

**Step 5: Face-Saving Explanation**
How would they explain agreement to their team, their boss, or themselves? A
stakeholder may privately accept a compromise but publicly need a narrative that
doesn't look like capitulation. Agreement that can't be explained is agreement that
won't hold — or won't be delivered.

**Step 6: Map Alignment and Conflict Zones**
Find where underlying stakes actually overlap (alignment zones) and where they
genuinely compete (conflict zones). Alignment at the stake level often exists even
when surface positions look completely opposed. Conflict zones where one party's win
structurally requires another's loss cannot be resolved through reframing — they
require explicit negotiation.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Highest stakes only** — What each person cares about most, skip secondary concerns
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Stakeholder Table**

| Stakeholder | Stated Position | Real Fear | Minimum Condition | Face-Saving Explanation |
|---|---|---|---|---|
| [name/role] | [explicit ask] | [underlying fear] | [the floor for agreement] | [how they'd narrate agreement] |

**Alignment Zones**
Stakes that multiple stakeholders share underneath apparently conflicting positions.
List the shared underlying interest and which parties share it.

**Conflict Zones**
Stakes that genuinely compete — where one party's win requires another's loss. Name
each conflict zone explicitly and identify what explicit negotiation or trade-off it
requires.

**Next Move**
Given the alignment and conflict zones: what is the highest-leverage first
conversation or action?

---

## Notes

Surface-level positions are negotiating stances; underlying stakes are the actual
terrain. Work on the terrain. Conflict zones that can't be resolved through alignment
require explicit trade-off decisions — don't paper over them with language that
pretends everyone wins when they don't. The face-saving explanation step is often
what makes agreement stick in practice even after it's been reached in principle.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Stakes mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-decision-premortem-analysis` — Stress-test with highest-stakes outcomes in mind
  - `/s4h-ethics-empathy-circle` — Apply structured empathy to the highest-stakes people
  - `/s4h-communication-audience-modeling` — Model the audience through their stakes
  - **Done** — Wrap up and synthesise what we have so far
