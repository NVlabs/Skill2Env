---
name: s4h-writing-pov
description: "Audits point-of-view for violations, consistency, and fit. Use when narration feels inconsistent, when there is unwanted head-hopping, or when the chosen POV isn't serving the story. Triggers: 'POV problems', 'head-hopping', 'point of view', 'the narration feels inconsistent', 'POV violations', 'narrative perspective', 'sometimes we know things the character shouldn't'."
---

# Writing: Point of View

POV is a contract with the reader about what the narration can know. The moment that contract is violated — the moment the narration accesses something it has promised not to access — the reader's trust breaks. Usually they don't know why. They just feel the seam, the moment the author's hand becomes visible. "How did we know that?" is the diagnostic question.

Each POV type makes a different promise:

**First person:** The narrator tells us what they experienced, observed, thought, and felt. They cannot know what other characters are thinking unless they are told or infer it (and the inference should be flagged as inference). They can be unreliable — their account of events may be shaped by their psychology, their blindspots, their desire to present themselves well.

**Close third person:** Narration follows one character's subjective experience. The narration can access their thoughts and feelings but cannot access anyone else's interior. Physical details that the POV character couldn't observe (what their own face looks like, what's happening in a room they're not in) require specific handling. Thought and feeling are rendered from inside, not described from outside.

**Omniscient:** The narrator has access to any mind. But omniscient POV is not a licence for chaos — it must be used consistently. An omniscient narrator who dips into three minds in one scene and then goes external in the next has not chosen omniscient POV; they have abandoned POV control entirely.

The fit question is as important as the violation question: does the chosen POV serve what the story is trying to do? A story whose power lives in dramatic irony (the reader knows something the protagonist doesn't) may work better in third than first. A story whose power is unreliable memory may need first person. The POV choice is not arbitrary — the story's core effect often depends on it.

---

## Your Process

**Step 1: Identify Current POV Type**
First person / close third / omniscient / second person / mixed. If mixed, is it intentionally mixed (multiple POV characters with clear transitions) or unintentionally mixed (the narration drifts without structure)?

**Framing check:** Confirm the specific text and POV situation before continuing. State what you've identified — the POV type, the POV character (if applicable), and whether the concern is violations, fit, or both — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the text and its POV situation]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: State the Contract**
What does this POV promise about access to interiority? First person: access to the narrator's interior, inference about others. Close third: access to POV character's interior, not others'. Omniscient: access to any interior, but must be applied consistently. State the contract explicitly — it becomes the audit standard.

**Step 3: Scan for Violations**
Violations fall into four categories:
- **Interiority violations:** Narration accesses another character's thoughts or feelings without the POV character being told or inferring
- **Observation violations:** Narration describes something the POV character couldn't see, hear, or observe
- **Knowledge violations:** Narration assumes knowledge the POV character doesn't have
- **Inconsistency violations:** The POV type shifts without transition (close third suddenly going omniscient for one paragraph)

For each violation: quote the line, identify the type, name what was accessed that couldn't be accessed.

**Step 4: Fit Assessment**
Does the chosen POV serve the story's core effect? Consider:
- If the story's power is in *not knowing* something — close third may serve better than omniscient
- If the story's power is in the narrator's *voice and personality* — first person may be more powerful
- If the story requires events the protagonist can't witness — close third may be limiting; omniscient or multiple POV may be needed
- If dramatic irony is central — omniscient or multiple POV enables it; first-person limits it

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

### POV Audit

**Type Identified:** [First person / Close third / Omniscient / Second / Mixed — and whether mixed is intentional]

**Contract Stated:** [What this POV promises about access to interiority and observation]

**Violations:**
- [Quoted line] — Type: [Interiority / Observation / Knowledge / Inconsistency] — What was accessed that couldn't be
- [Repeat for each violation]
- NONE FOUND if clean

**Fit Assessment:** [Does this POV serve the story's core effect? What would be gained or lost by changing it?]

**Recommendation:** [Maintain current POV with fixes / Consider switching to X because Y]

---

## Notes

- POV violations are a type of continuity error, but they require their own audit pass because they operate at the narrative level rather than the story level.
- The hardest violations to catch in close third: the narrator describing what the POV character's own face looks like (characters don't see their own faces), and the narration accessing physical sensations the POV character has gone numb to (because the author needs the reader to feel them).
- Pairs with `/s4h-writing-voice-consistency` — POV and voice are linked; a close-third narration that suddenly takes on the author's philosophical voice rather than the character's is both a POV violation and a voice inconsistency.
- Pairs with `/s4h-writing-inconsistency-audit` — POV violations are logged there as a category; this skill provides the deeper analysis when they're numerous or the POV choice itself is the problem.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "POV established. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-voice-consistency` — Ensure POV is voice-consistent throughout
  - `/s4h-writing-scene-construction` — Construct scenes from the established POV
  - `/s4h-writing-character-development` — Develop the character whose POV this is
  - **Done** — Wrap up and synthesise what we have so far
