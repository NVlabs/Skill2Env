---
name: s4h-writing-audience-calibration
description: "Calibrates writing for a specific reader by profiling their knowledge, concerns, and relationship to the topic — then rewriting for that reader without changing the substance. Use when content is too technical, too basic, or framed for the wrong audience. Triggers: 'write for a specific audience', 'audience calibration', 'this needs to work for non-technical readers', 'the audience isn't the right fit', 'calibrate this for', 'it's too technical / not technical enough', 'recalibrate this for'."
---

# Writing: Audience Calibration

Calibration failures come in two forms: over-explanation and under-explanation. Over-explanation treats experts as novices — it defines terms they know, explains concepts they've mastered, and adds context they don't need. This reads as condescending, and the expert reader disengages. Under-explanation treats novices as experts — it uses jargon without definition, assumes mental models the reader doesn't have, and skips the connections that make the logic followable. This reads as inaccessible, and the novice reader gives up.

The critical insight: calibration does not require changing the substance of what is being communicated. The same analysis can serve a technical expert and a non-technical decision-maker if it is correctly calibrated for each. The facts don't change; the entry point, assumed knowledge, vocabulary, framing, and emphasis all do.

The three dimensions of calibration:
- **Knowledge calibration:** What does this reader already know? What can be assumed, what needs brief context, what needs explanation?
- **Stakes calibration:** What does this reader care about? The engineer cares about implementation; the product manager cares about user impact; the executive cares about business consequences. Same finding, different emphasis.
- **Relationship calibration:** Is the reader expert or novice, friendly or skeptical, time-pressed or engaged? Each requires different structural choices.

---

## Your Process

**Step 1: Reader Profile**
Build a specific reader profile:
- **Knowledge:** What domain knowledge, terminology, and conceptual background can be assumed?
- **Role:** What is their function — technical, managerial, strategic? What decisions do they make?
- **Stakes:** What do they care about most? What is the highest-value question they bring to this content?
- **Relationship:** Friendly, skeptical, or neutral? Expert, novice, or intermediate?
- **Time:** How much attention do they have? Will they read carefully or scan?

**Framing check:** Confirm the specific content and target audience before continuing. State what you've identified — the actual piece being calibrated and the reader it is being calibrated for — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the content and target audience]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Calibration Failures — Identify**
Read the content as the profiled reader. Flag:
- **Jargon without definition:** Technical terms the reader won't know
- **Over-explanation:** Concepts or terms the reader already knows being explained to them
- **Wrong prior assumed:** The content frames itself around a conceptual model the reader doesn't have
- **Wrong emphasis:** The most important thing for *this reader* is buried; the most important thing for the *author* is prominent
- **Wrong entry point:** The content starts in the middle of a context the reader is not inside

**Step 3: Reader's Highest-Value Question**
What is the single question this reader most needs answered? Is it answered prominently and early? If the reader has to read to the end to find the answer to their most pressing question, the calibration has failed regardless of other qualities.

**Step 4: Framing Adjustment**
Same substance, different framing. For technical content going to a non-technical reader: replace mechanism with outcome ("this algorithm sorts results by frequency" → "the most relevant results appear first"). For strategic content going to a technical reader: replace policy with specification ("improve response times" → "p95 response time under 200ms"). The framing makes the content land in the register the reader occupies.

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

### Calibration Report

**Reader Profile:** [Knowledge / Role / Stakes / Relationship / Time-attention]

**Calibration Failures:**
- [Jargon: quoted term + plain language alternative]
- [Over-explanation: quoted passage + note on what the reader already knows]
- [Wrong prior: identified assumption + what needs to be established instead]
- [Wrong emphasis: what's prominent vs. what this reader needs prominent]
- NONE FOUND if well-calibrated

**Highest-Value Question:** [What this reader most needs answered] — Answered prominently / Buried / Not answered

**Framing Adjustments:** [Specific reframings for this reader — mechanism → outcome, policy → specification, etc.]

**Rewritten Opening Paragraph:** [The opening paragraph rewritten for the target reader — calibrated vocabulary, assumed knowledge, entry point, emphasis]

---

## Notes

- Calibration is not simplification. A well-calibrated piece for a non-technical reader is not a dumbed-down version of the technical piece — it is the same substance approached from a different entry point. Simplification removes content; calibration changes the door.
- The hardest calibration: from expert to novice, when the expert has forgotten what it's like not to know. The test: can a reader with the stated knowledge profile understand this without asking a clarifying question?
- Pairs with `/s4h-writing-executive-summary` for executive calibration — the executive summary format is a specific calibration for senior decision-makers.
- Pairs with `/s4h-writing-technical` for technical audience calibration — when the content is documentation and the calibration question is which technical level to write for.
- Pairs with `/s4h-writing-voice-consistency` — calibration adjustments must stay within the established voice; a recalibrated piece that sounds like a different writer has traded one problem for another.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Writing calibrated for audience. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-tone-alignment` — Align tone to the calibrated audience
  - `/s4h-communication-audience-modeling` — Deepen the audience model further
  - `/s4h-writing-voice-consistency` — Ensure voice serves the audience throughout
  - **Done** — Wrap up and synthesise what we have so far
