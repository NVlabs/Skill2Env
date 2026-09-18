---
name: s4h-emotional
description: "Entry point for the emotional intelligence toolkit. Routes to the right emotional skill based on your situation. Use when you say 'emotional', 'why are they behaving like this', 'what motivates them', 'why the resistance', 'what do they really want', 'trust issues', or want emotional/interpersonal reasoning applied without knowing which specific tool fits."
---

# Emotional

Applies emotional intelligence to interpersonal and organizational situations. Diagnoses what kind of emotional reasoning is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Understand what genuinely drives someone's behavior | motivation-mapping |
| Diagnose why people are resisting or not engaging | resistance-diagnosis |
| Find what someone actually cares about beneath their stated position | stakes-mapping |
| Map what's building or eroding trust in a relationship | trust-audit |

## Routing Decision

- **Behavior is hard to predict or incentives seem misaligned** → motivation-mapping
- **People are pushing back, won't get on board** → resistance-diagnosis
- **Negotiation or alignment is failing — stated positions aren't moving** → stakes-mapping
- **A relationship or team has trust problems** → trust-audit
- **Unclear** → stakes-mapping; understanding what's really at stake usually clarifies everything else

**Framing check:** Confirm the specific interpersonal or organizational situation before continuing. State what you've identified — the people involved, the emotional dynamic at play, and the context — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation, the people involved, and what's going wrong emotionally]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

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

## Motivation Mapping

*Maps what genuinely drives different people.*

Go beyond job descriptions and stated reasons. For each person: what do they actually want from their work (autonomy, mastery, belonging, recognition, security, impact)? What do they fear? What stories do they tell about themselves — and does this decision threaten or reinforce those stories? Stated motivations and real motivations often diverge; the gap is where behavior becomes hard to predict.

**Output:** Per-person motivation map: genuine drivers, fears, identity narrative, and how this situation activates or threatens each.

---

## Resistance Diagnosis

*Diagnoses why people are resisting.*

Resistance is information, not obstruction. It always has a source. Classify the resistance: (1) Misunderstanding — they don't understand what's being asked, (2) Disagreement — they understand but think it's wrong, (3) Fear — they understand but are worried about consequences, (4) Values conflict — they oppose the underlying direction, not just this decision. Each type requires a completely different response; treating all resistance as obstruction makes it worse.

**Output:** Resistance classification, the specific source underneath the pushback, and the appropriate response for that type.

---

## Stakes Mapping

*Maps what each stakeholder actually cares about beneath their stated position.*

In any negotiation, alignment challenge, or disagreement, stated positions are rarely the real issue. For each stakeholder: what is their stated position? What underlying interest does it serve? What would they actually need to see to move? Addressing stated positions while missing real stakes accomplishes nothing — the agreement collapses or the compliance is hollow.

**Output:** Per-stakeholder map: stated position, underlying interest, real stakes, and the minimum conditions for genuine alignment.

---

## Trust Audit

*Maps what is building and eroding trust in a relationship or situation.*

Trust degrades silently until it fails loudly. Audit trust across four dimensions: (1) Competence — do they believe you can deliver? (2) Integrity — do they believe you mean what you say? (3) Benevolence — do they believe you have their interests at heart? (4) Reliability — do they trust your follow-through? For each dimension: what recent events support or undermine trust? What actions would rebuild it?

**Output:** Trust audit across four dimensions, with specific evidence for each. Priority actions that most efficiently rebuild trust.
