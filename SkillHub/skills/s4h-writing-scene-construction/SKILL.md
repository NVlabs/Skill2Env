---
name: s4h-writing-scene-construction
description: "Diagnoses and repairs individual scenes using the want/obstacle/outcome framework. Every scene must change the story's state. Use when a scene feels flat, static, or purposeless. Triggers: 'this scene isn't working', 'scene construction', 'scene feels flat', 'scene review', 'fix this scene', 'the scene doesn't do anything', 'should I cut this scene'."
---

# Writing: Scene Construction

Every scene is a mini-story. It needs a want, an obstacle, and an outcome. Without these three elements, it is not a scene — it is a passage of time. The reader experiences the difference viscerally, even if they can't name it: a scene without these elements reads as static, as nothing happening, as the story marking time.

The outcome is the most frequently broken element. Every scene must end in a different state than it began. The outcome must be one of four types: **yes-but** (protagonist gets what they want but at a cost or complication), **no-and** (denied, and things are worse), **no-but** (denied, but something else is gained), or **yes-and** (achieved, and something else follows). Any scene that ends with an unmodified yes or no is a scene that hasn't done its work.

The second most common failure: scenes that serve one function when they need to serve two. A scene that only reveals character, only provides information, or only advances plot is vulnerable to cutting. The best scenes do two or three things at once — and the obligation to do multiple things simultaneously is what generates the density that makes scenes feel necessary.

---

## Your Process

**Step 1: Scene Goal**
What does the POV character want in *this scene*? Not what they want in the story — what they want right now, from this specific situation. Be concrete: "to convince Marcus to lend her the money," not "to solve her financial problems." If the goal can't be stated specifically, the scene has no engine.

**Framing check:** Confirm the specific scene before continuing. State what you've identified — the scene's POV character, their immediate want, and the narrative moment it occupies — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the scene — POV character, their specific want, and where it sits in the story]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different scene or situation than read; incorporate the correction before proceeding

**Step 2: Obstacle**
What prevents the character from getting it? The obstacle should be active and specific — a person with their own opposing goal, a circumstance that makes the goal impossible, or an internal conflict that prevents the character from acting. Weak obstacles are vague ("things are difficult") or absent (the character just gets what they want).

**Step 3: Outcome Type**
Identify the outcome type:
- **Yes-and:** Gets it, and something further results (often raises stakes)
- **Yes-but:** Gets it, but at a cost or with a complication attached
- **No-but:** Denied, but gains something useful or shifts direction
- **No-and:** Denied, and the situation worsens

Flag any scene ending in an unmodified yes ("they agreed and left") or unmodified no ("he refused and she walked out"). These scenes have not changed the story's state in a way that matters.

**Step 4: Sensory Grounding**
Which senses are present in the scene? Which is doing the most work? What's missing? Scenes that live only in dialogue and action are often missing the physical world — temperature, smell, sound, texture — that makes the reader inhabit the space rather than read about it. Note: sensory detail should not be decoration; it should carry meaning (the smell of the room is connected to what the room means).

**Step 5: Subtext**
What is NOT being said, but is present in the scene? Great scenes carry at least two conversations — the surface exchange and the subterranean one. If the characters are saying exactly what they mean, the scene has no subtext and reads as flat. Identify what each character is not saying and why.

**Step 6: Scene Function**
What does this scene do? Mark all that apply:
- **Revelation** — something new is learned by a character or revealed to the reader
- **Escalation** — stakes rise or the situation worsens
- **Character** — character is revealed through choice or behaviour under pressure
- **Transition** — moves characters or situation from one state to another

If the scene serves only one function, it is at risk. Consider whether it can be combined with adjacent scenes or rewritten to serve a second function.

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

### Scene Diagnosis

**Goal:** [POV character's specific want in this scene]

**Obstacle:** [What prevents it — active and specific]

**Outcome Type:** [yes-and / yes-but / no-but / no-and / FLAGGED: unmodified]

**Sensory Inventory:** [Senses present / which dominates / what's missing / whether detail carries meaning]

**Subtext Present:** [What is not said + why / FLAGGED: no subtext]

**Scene Function:** [Revelation / Escalation / Character / Transition — mark all present, flag if only one]

**Verdict:** Keep / Cut / Combine / Rewrite

**Specific Recommendation:** [Concrete intervention — what to add, remove, shift, or rewrite]

---

## Notes

- The most useful diagnostic question: if you removed this scene, would the story notice? If the answer is no, the scene is failing.
- Subtext problems are often dialogue problems — see `/s4h-writing-dialogue` for subtext-specific repair.
- If the scene has a goal and obstacle but no sensory presence, see `/s4h-writing-prose-elevation` — the scene's architecture is right but the prose isn't delivering it.
- Pairs with `/s4h-writing-dialogue` for scene-specific dialogue repair.
- Pairs with `/s4h-writing-inconsistency-audit` for scene-level continuity errors (character knows something they shouldn't, objects change location, etc.).
- Pairs with `/s4h-writing-plot-structure` when diagnosing whether a scene is failing because the structural beat it belongs to is itself failing.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Scene constructed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-dialogue` — Add dialogue to the scene
  - `/s4h-writing-prose-elevation` — Elevate the scene's prose
  - `/s4h-aesthetic-coherence-check` — Check the scene coheres with the whole
  - **Done** — Wrap up and synthesise what we have so far
