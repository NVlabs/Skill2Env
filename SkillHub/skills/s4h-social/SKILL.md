---
name: s4h-social
description: "Entry point for the social dynamics toolkit. Routes to the right social skill based on your situation. Use when you say 'social', 'people', 'politics', 'who decides', 'group dynamics', 'who do I need to get on board', 'follow the incentives', 'who has power', or want social/organizational reasoning applied without knowing which specific tool fits."
---

# Social

Applies social and organizational reasoning to group dynamics, power, incentives, and coalition-building. Diagnoses what kind of social analysis is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Map who needs to be aligned and how to build support | coalition-mapping |
| Understand the group psychology shaping a team or discussion | dynamics-analysis |
| Find the actual incentives driving behavior | incentive-analysis |
| Map who holds formal and informal power | power-mapping |

## Routing Decision

**Framing check:** Confirm the social situation before diagnosing. State what you've identified — the specific group, relationship, or dynamic at stake and the core tension or goal — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific social situation, group, and what needs to happen]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Proposal needs stakeholder support — need to build alignment** → coalition-mapping
- **Team behaving in ways that are hard to understand or predict** → dynamics-analysis
- **Behavior seems misaligned with stated goals — incentives might be wrong** → incentive-analysis
- **Unsure who actually decides or influences decisions** → power-mapping
- **Unclear** → power-mapping; understanding who has power usually reveals the incentives, dynamics, and coalition targets

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Coalition Mapping

*Maps who needs to be aligned and how to build the coalition a proposal needs.*

Identify all stakeholders. For each: are they currently (1) supporters, (2) neutral, (3) opponents, or (4) unknown? For neutral and unknown: what would move them to support? For opponents: what is their actual objection, and can it be addressed? Identify the minimum coalition needed for the proposal to succeed. Map the path to building it.

**Output:** Stakeholder map by current position, minimum viable coalition, path to building it, and the blockers most worth addressing.

---

## Dynamics Analysis

*Identifies group psychology shaping a discussion or team.*

Look for: (1) Groupthink — are dissenting views being suppressed? (2) Status dynamics — are contributions being evaluated by who made them, not what they are? (3) Psychological safety — do people feel safe to say what they actually think? (4) Coalition formation — are subgroups forming with different agendas? (5) Silence patterns — who never speaks, and why? Group dynamics shape outcomes more than individuals realize.

**Output:** Dynamics inventory — which patterns are present, their specific manifestation, and the interventions that address each.

---

## Incentive Analysis

*Maps the actual incentives driving behavior.*

Stated motivations and real incentive structures often diverge. Ask: what does the system actually reward? What are people measured on? What do they fear? What behaviors does this structure select for over time? The most reliable predictor of behavior is not what people say they want, but what the system they operate in rewards. Follow the incentives.

**Output:** Actual incentive map — what the system rewards, what it punishes, how that explains current behavior, and what would need to change to change behavior.

---

## Power Mapping

*Maps who holds formal authority, informal influence, and gatekeeping power.*

Distinguish types of power: (1) Formal authority — who can officially approve or block, (2) Informal influence — who shapes thinking without formal authority, (3) Gatekeeping — who controls access or information flow, (4) Expertise power — whose judgment others defer to. For each power holder: what do they want? What do they fear? How does this affect what's possible?

**Output:** Power map across all four types. For each power holder: their position on the relevant issue and how to work with or around them.
