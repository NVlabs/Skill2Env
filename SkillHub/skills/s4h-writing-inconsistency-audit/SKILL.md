---
name: s4h-writing-inconsistency-audit
description: "Runs four systematic passes to identify timeline errors, character logic violations, world-rule breaks, and physical continuity errors. Use when a manuscript has contradictions, continuity problems, or logic violations. Triggers: 'there are contradictions', 'continuity errors', 'inconsistency check', 'the character shouldn't know that', 'timeline doesn't add up', 'continuity audit', 'inconsistencies in the manuscript'."
---

# Writing: Inconsistency Audit

Inconsistencies undermine the reader's trust more efficiently than almost any other flaw — because they signal that the author lost track of their own world. The reader's contract with a story is: I will suspend disbelief in exchange for internal coherence. One visible inconsistency tells the reader the author may have lost the thread, and the reader will spend the rest of the story half-watching for the next crack rather than being inside the experience.

Four types of inconsistency require separate passes, because they operate at different levels and have different causes:

**Timeline inconsistency:** Events that are out of chronological order, time spans that don't add up, characters who are in two places at once, seasons that shift unexpectedly.

**Character logic inconsistency:** Characters who act contrary to their established psychology without earned cause, who know things they couldn't know, who forget things they must know, who respond to situations in ways their established temperament doesn't allow.

**World-rules inconsistency:** The story's established physics, magic, technology, or social rules that function differently in different scenes — usually because the plot needs them to.

**Physical continuity inconsistency:** Objects that change hands, locations, or appearance without explanation; characters whose physical description changes; room layouts that contradict themselves.

Each pass requires a different diagnostic lens. Running all four in sequence is the only way to catch inconsistencies that don't show up in a single read.

---

## Your Process

**Pass 1: Timeline Audit**

**Framing check:** Confirm the specific manuscript and its scope before continuing. State what you've identified — the work being audited, its genre/setting, and the portion in scope (full manuscript, a chapter range, a specific scene) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the manuscript, e.g. 'a fantasy novel manuscript, full text, set in a world with established magic rules']. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different scope or work than read; incorporate the correction before proceeding

Reconstruct the chronological order of events. Note every time marker: "the next morning," "three weeks later," "before she left," "the day after Marcus died." Build a timeline and check:
- Are events in order consistent with stated time markers?
- Do stated durations (travel times, healing times, gestation times) match what the story shows?
- Can characters be where they need to be at the times required?
- Are ages consistent with established birthdates and story duration?

Flag: any event whose placement contradicts a stated time marker; any duration that doesn't hold up to scrutiny.

**Pass 2: Character Logic Audit**
For each significant character, establish their baseline: what do they know, what is their temperament, what are they capable of? Then audit:
- Does any character act on knowledge they couldn't have acquired by this point in the story?
- Does any character act contrary to their established psychology without a scene that earns the change?
- Does any character forget established facts (their own history, another character's name, an agreement they made)?
- Does a character's relationship dynamic with another character contradict what was established earlier?

Flag: each instance with the character name, the violated baseline, and the location.

**Pass 3: World-Rules Audit**
List the established rules of the world (physical, social, magical, technological). Then audit each instance where those rules appear:
- Do the rules operate consistently throughout?
- Are there moments where the rules bend because the plot needs them to?
- Do characters know about the rules consistently with when they were established?
- Are there loopholes the story exploits that the rules don't actually permit?

Flag: each rule violation with the rule stated, the violation quoted, and whether it's a minor or structural inconsistency.

**Pass 4: Physical Continuity Audit**
Track key objects, locations, and physical descriptions:
- Key objects: do they stay where they were left, appear when needed, disappear when forgotten?
- Locations: do room layouts, relative positions, and environmental details remain consistent?
- Physical descriptions: do characters' appearances remain consistent? (Hair colour, injuries, distinguishing features)
- Scene-to-scene physical state: what does each character have, wear, and carry at the start of each scene? Does it match the end of the previous scene?

Flag: each contradiction with the original description, the contradicting description, and the locations of both.

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

### Inconsistency Report

**Timeline:**
- [Issue: quoted passage + location] — Severity: Minor / Breaks immersion / Breaks the story
- NONE FOUND if clean

**Character Logic:**
- [Issue: character, baseline violated, quoted passage + location] — Severity
- NONE FOUND if clean

**World Rules:**
- [Issue: rule stated, violation quoted + location] — Severity
- NONE FOUND if clean

**Physical Continuity:**
- [Issue: original description, contradicting description, locations of both] — Severity
- NONE FOUND if clean

**Summary:** [Total issues by category and severity / The most critical fix required]

---

## Notes

- Run the passes in order: timeline first, because timeline problems often explain character logic problems (a character knows something early because the scene was moved from later in the sequence).
- Severity rating guide: **Minor** = a reader might notice but won't lose the story. **Breaks immersion** = pulls the reader out momentarily. **Breaks the story** = the story's central premise or resolution depends on an inconsistency.
- Pairs with `/s4h-writing-character-development` for the character logic baseline — you need to know what was established before you can audit violations of it.
- Pairs with `/s4h-writing-worldbuilding` for the world-rules baseline — the audit can only flag violations if the rules are clearly stated.
- Pairs with `/s4h-writing-pov` because POV violations are a form of character logic inconsistency (the narration accesses knowledge the POV character doesn't have).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Inconsistencies found. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-voice-consistency` — Fix the voice inconsistencies
  - `/s4h-writing-restructure` — Restructure to resolve the structural inconsistencies
  - `/s4h-logic-consistency-check` — Validate logical consistency alongside writing consistency
  - **Done** — Wrap up and synthesise what we have so far
