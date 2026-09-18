---
name: s4h-writing-tone-alignment
description: "Diagnoses and repairs tone drift — shifts in register, formality, warmth, or rhythm that make a piece feel like it was written by multiple people or in multiple moods. Use when the voice changes mid-piece without intention. Triggers: 'the tone keeps shifting', 'tone drift', 'tone alignment', 'inconsistent register', 'the voice changes mid-piece', 'this sounds like different writers'."
---

# Writing: Tone Alignment

Tone drift is what happens when a piece moves through multiple registers without intention — formal to casual, warm to clinical, urgent to contemplative — destroying the reader's sense of who is speaking. The reader cannot trust a voice they cannot locate. When they feel the voice shift, they become aware they are reading a *document* rather than inhabiting a communication. The intimacy, or the authority, or the momentum — whatever the piece was building — dissolves.

Tone drift is most common in three situations: multi-author documents, where different contributors have different natural voices; long pieces written over time, where the writer's mood, energy, or approach has changed between sessions; and pieces assembled from different source material, where the register of the sources bleeds into the synthesis.

Tone has multiple dimensions, and they can drift independently:
- **Formality:** Where on the formal/informal spectrum? Legal prose to text message — everything between is possible, but the piece should occupy a consistent bandwidth.
- **Warmth:** Where on the cold-to-warm spectrum? Institutional distance to personal intimacy?
- **Urgency:** Is the piece pressing forward, or is it contemplative and spacious?
- **Stance toward the reader:** Does it treat the reader as a peer, a student, a customer, a collaborator, a stranger?
- **Sentence rhythm:** Short and punchy, or long and periodic? The rhythm carries register even when the words don't shift.

---

## Your Process

**Step 1: Intended Tone**
What tone was intended? If it's not stated, extract it from the strongest passage in the piece — the section that works best is the baseline. State the intended tone precisely across all five dimensions: formality level / warmth level / urgency / stance toward reader / sentence rhythm.

**Framing check:** Confirm the piece and its intended register before continuing. State what you've identified — the specific text being analysed and the baseline tone you've extracted — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the piece and its intended tone]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Scan for Departures**
Read through the piece and flag sections where any of the five tone dimensions shifts from the baseline. Don't just flag "informal" or "formal" — be specific: "this section shifts from 'collegial peer' to 'authoritative expert'"; "this paragraph breaks from short declarative sentences into subordinate clause-heavy long sentences that slow the pace and change the register."

**Step 3: Diagnose the Cause**
For each departure, what produced it?
- **Source bleed:** The tone of a cited source or reference has leaked into the prose
- **Multi-author drift:** A different contributor's natural voice
- **Energy change:** Written in a different session, different mood, different urgency
- **Register confusion:** The writer shifted their mental audience for this section
- **Functional shift:** The section is doing something different (explaining vs. persuading vs. narrating) and the register shifted with the function without awareness

Understanding the cause determines the correction.

**Step 4: Prescribe Corrections**
For each flagged section: what specific changes bring it into alignment? This may involve vocabulary choices ("synergistic" → "works well together"), sentence length adjustments, the removal of hedging language, or the addition of warmth. Be specific — "make it more casual" is not actionable; "replace the three nominalisations in this paragraph and cut the passive construction in the final sentence" is.

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

### Tone Audit

**Intended Tone:**
- Formality: [X/10, characterised]
- Warmth: [X/10, characterised]
- Urgency: [paced characterisation]
- Stance toward reader: [peer / student / customer / etc.]
- Sentence rhythm: [characterised]

**Flagged Departures:**
- [Location] — [Quoted passage] — Dimension shifted: [formality / warmth / urgency / stance / rhythm] — Direction of drift: [toward formal / toward casual / etc.]
- [Repeat for each]
- NONE FOUND if clean

**Cause Diagnoses:** [Per departure: source bleed / multi-author drift / energy change / register confusion / functional shift]

**Correction Prescriptions:** [Per departure: specific changes — vocabulary, sentence structure, register adjustments]

---

## Notes

- Tone drift is different from intentional register shift. Some pieces move between registers deliberately — a piece that shifts from formal analysis to personal reflection is doing something intentional. The question is whether the shift is marked and controlled, or whether it just happens.
- Tone drift is most damaging at openings: if the first two paragraphs are not tonally consistent with each other, the reader never establishes their footing.
- Pairs with `/s4h-writing-voice-consistency` — voice is the who speaking; tone is the how. They are related but distinct. Voice consistency asks "does this sound like the same person?"; tone alignment asks "is that person speaking in a consistent register?"
- Pairs with `/s4h-writing-audience-calibration` — tone is part of calibration; a piece can be tonally consistent but calibrated to the wrong audience entirely.
- Pairs with `/s4h-writing-line-editing` — many tone corrections happen at the sentence level (word choice, sentence structure), so the two tools often work together.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Tone aligned. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-voice-consistency` — Check voice consistency after tone alignment
  - `/s4h-writing-line-editing` — Edit for the aligned tone
  - `/s4h-writing-audience-calibration` — Verify tone serves the audience
  - **Done** — Wrap up and synthesise what we have so far
