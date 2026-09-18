---
name: s4h-writing-worldbuilding
description: "Audits a fictional world for internal consistency, texture, economy, and constraint-story alignment. Use when a world feels thin, generic, like a backdrop rather than a place people actually inhabit. Triggers: 'the world feels thin', 'worldbuilding', 'my world doesn't feel real', 'the setting is generic', 'world audit', 'the world feels like a backdrop'."
---

# Writing: Worldbuilding

Worlds fail when they are described rather than inhabited. The difference is texture. A described world tells you what things are — "a dystopian future where technology controls society." An inhabited world shows you what it costs to live there: what people eat, what they fear, what they fight over, what they take for granted, what they lie about. The first is a category. The second is a place.

The test of a well-built world is not comprehensiveness — it's necessity. Does the world create the story's conflict, or is it merely a backdrop? In a well-integrated world, the story's central problem could only happen in this world, in this configuration. The colony's resource scarcity creates the political structure that creates the protagonist's impossible choice. Remove the world, and the story doesn't exist. In a backdrop world, you could set the same story in contemporary New York without changing anything essential.

The second test: specificity of texture. The world must feel inhabited not through encyclopaedic exposition, but through specific, surprising detail that implies a larger reality. One specific food item, one specific ritual, one specific slang term tells the reader more about the world than three pages of history. The detail does double duty — it characterises the world and implies the systems that produced it.

---

## Your Process

**Step 1: Rules**
Map the world's governing systems: physical, social, technological, magical, or political. What are the rules that cannot be broken? Are they internally consistent — does the magic system create loopholes the story conveniently exploits? Does the technology appear and disappear based on plot convenience? Rules only function as worldbuilding if they constrain the story.

**Framing check:** Confirm the specific world being audited before continuing. State what you've identified — the fictional world, its genre/setting, and the story context it operates within — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the world, its genre, and the core story context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: History**
What happened before the story? How does it shape present conditions? The world's history should be visible in the present: in architecture, language, prejudice, ritual, scar tissue. If the history is not visible in the present, it has no function — it's backstory for the author, not texture for the world.

**Step 3: Economy**
How do people survive? How is power acquired and maintained? What do people trade, compete for, hoard, or sacrifice? Economy is the hidden architecture of any world — it determines who has leverage over whom, what choices are available to which people, and what the stakes of any conflict actually are. Worlds without a legible economy feel arbitrary.

**Step 4: Texture**
Specific details that make the world inhabited — not the large-scale facts, but the granular particulars: food, clothing, speech patterns, rituals, insults, jokes, signs, smells. For each world zone (a location, a social class, a faction), identify what specific sensory details are present and what is missing. The test: could these details only exist in this world, or are they generic?

**Step 5: Constraint-Story Alignment**
Does the world's structure create the story's conflict, or is the world irrelevant to the plot? This is the integration test. Map the connection: world rule → social consequence → character situation → story problem. If the chain breaks at any point, the world is decorative rather than load-bearing.

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

### World Audit

**Rules Inventory:** [Physical / social / technological / magical governing rules — internal consistency check — loopholes or conveniences flagged]

**History:** [Pre-story events + how they're visible in the present / missing historical presence flagged]

**Economy:** [Survival mechanisms / power acquisition / what is competed over / leverage structures / gaps or arbitrary elements]

**Texture:** [Present specific details — per zone if relevant / Missing sensory/cultural particulars / World-specific vs. generic details distinguished]

**Constraint-Story Alignment:** [The chain: world rule → social consequence → character situation → story problem / Where the chain breaks]

**Gaps and Inconsistencies:** [Internal contradictions / rules violated by plot convenience / areas requiring further development]

---

## Notes

- The most common worldbuilding error is exposition: delivering world information through characters explaining things to each other. World texture should emerge through action, conflict, and specific detail — not through characters lecturing.
- Comprehensiveness is not the goal. A world that feels real is not one where every question has been answered — it's one where the questions the story raises are answered, and the answers feel like part of a larger coherent system.
- Pairs with `/s4h-writing-inconsistency-audit` for world-rule violations throughout the manuscript — worldbuilding establishes the rules; the audit finds where they're broken.
- Pairs with `/s4h-writing-character-development` because characters are produced by their world: their wound, defence, and want are shaped by the economy, history, and social rules they grew up inside.
- Pairs with `/s4h-writing-scene-construction` for deploying world texture at the scene level — what sensory details make this specific location feel inhabited.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "World built. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-scene-construction` — Construct scenes in the world
  - `/s4h-narrative-structure-mapping` — Map the narrative structure of the world
  - `/s4h-writing-character-development` — Develop characters native to the world
  - **Done** — Wrap up and synthesise what we have so far
