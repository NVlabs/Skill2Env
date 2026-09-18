---
name: s4h-writing-character-development
description: "Engineers psychologically compelling characters by mapping want vs. need, wound, defence mechanism, and defining contradiction. Use when a character feels flat, underdeveloped, or unconvincing. Triggers: 'my character feels flat', 'character development', 'make this character feel real', 'this character isn't working', 'character work', 'how do I develop this character'."
---

# Writing: Character Development

Flat characters come from describing traits rather than engineering contradictions. When a writer says "she's brave and determined," they have a label — not a person. Compelling characters feel real because they hold two things in tension simultaneously: they want something and need something different; they have a strength that doubles as a weakness; they act from a wound they can't fully see. These tensions generate unpredictable, specific behaviour that no list of adjectives could produce.

The key diagnostic is the want/need split. The want is what the character consciously pursues — their stated goal, their driving motivation as they'd describe it. The need is what would actually fulfil them — which is always different, often the opposite, and usually something they're avoiding. This gap between want and need is where character lives. It generates internal conflict, drives the arc, and makes every action simultaneously understandable and complicated.

---

## Your Process

**Step 1: State the Core Want vs. Core Need**
Name what the character consciously wants (their goal as they understand it) and what they actually need (what would genuinely fulfil or redeem them). These should differ — the want is typically external, visible, and achievable; the need is internal, invisible to the character, and requires change. If want and need are identical, the character has no arc.

**Framing check:** Confirm the specific character before continuing. State what you've identified — the character's name or role, the story context, and the central tension as you've read it — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the character and their situation]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different character or situation than read; incorporate the correction before proceeding

**Step 2: Map the Wound**
Identify the formative experience that created their worldview and defences. The wound is not a backstory fact — it's the event or pattern that taught them something about the world that now governs how they move through it. Name the belief the wound installed: "People leave if you show need," "Strength is the only thing others respect," "I am not enough." This belief is the character's operating system.

**Step 3: Identify the Dominant Defence Mechanism**
The wound generates a defence. Name the character's primary defensive pattern:
- **Intellectualisation** — emotions managed through analysis; feelings translated into systems
- **Avoidance** — proximity to the wound's trigger is avoided, often without full awareness
- **Aggression** — threat is pre-empted by attacking first
- **People-pleasing** — safety maintained by managing others' approval
- **Controlling behaviour** — anxiety managed by controlling environment or others
- **Dissociation / performance** — the self is presented as a crafted persona to keep the real self safe

The defence should be visible in the character's behaviour patterns — how they handle conflict, intimacy, failure, and threat.

**Step 4: Map Their Relationship to the Story's Central Tension**
Is the character equipped or unequipped to handle the story's central challenge? The most powerful character-story alignment: the character's wound and defence are precisely the wrong tools for what the story requires. The story forces the character into exactly the territory their defence is designed to avoid.

**Step 5: Define the Arc Endpoint**
What must change internally for the character to reach the story's resolution? Not what they achieve externally — what must shift in their belief, their defence, their relationship to their wound? The arc endpoint should be the direct answer to the wound: if the wound installed "I am not enough," the arc endpoint might be "I am enough without proof."

**Step 6: Define the Contradiction**
Every compelling character holds two things in tension simultaneously — not one after the other, but at the same time. State the character's defining contradiction in one sentence. Examples: "Genuinely compassionate, uses that compassion as a weapon." "Desperate for connection, terrifies anyone who gets close." "The most honest person in the room, built on a foundational lie about themselves."

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one aspect of this analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Character Profile

**Core Want:** [What the character consciously pursues]

**Core Need:** [What would actually fulfil them — what they're avoiding]

**The Wound:** [The formative experience and the belief it installed]

**Defence Mechanism:** [Primary pattern + how it manifests behaviourally]

**Story Relationship:** [Equipped or unequipped to handle central tension, and why]

**Arc Endpoint:** [What must internally change for resolution]

**Defining Contradiction:** [The tension they hold simultaneously — one sentence]

**Before narrowing:** Show the complete set of candidate behavioural tells to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] candidate behavioural tells. Before I select the most scene-ready ones, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific tell to include
  - **Add a missing one** — user will describe it

**Behavioural Tells:** [3–5 specific, observable behaviours that express the above — concrete enough to write on the page]

---

## Notes

- Trait lists and adjectives produce flat characters. The wound, the defence, and the contradiction produce specific, unpredictable, recognisable people.
- The behavioural tells are the most important output for the practitioner: they give you something you can actually put in the scene.
- Pairs with `/s4h-writing-arc-design` when you need to map how this character's internal change aligns with the plot's external structure.
- Pairs with `/s4h-writing-inconsistency-audit` when a character is behaving in ways that violate their established psychology — often visible as "they would never do that" moments.
- Pairs with `/s4h-writing-dialogue` because voice flows from character: the wound and defence determine how a character speaks, evades, and misrepresents.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Character developed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-dialogue` — Write dialogue that brings the character to life
  - `/s4h-writing-arc-design` — Fit the character's development into the arc
  - `/s4h-narrative-tension-mapping` — Map tensions the character creates or resolves
  - **Done** — Wrap up and synthesise what we have so far
