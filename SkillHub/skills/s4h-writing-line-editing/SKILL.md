---
name: s4h-writing-line-editing
description: "Applies five-category line-editing passes to identify and repair redundancy, nominalisations, passive voice, rhythmic monotony, and throat-clearing. Use when prose is clunky, wordy, or mechanically flawed. Triggers: 'the sentences are clunky', 'line editing', 'the prose is wordy', 'tighten this up', 'sentence-level editing', 'too many passive constructions', 'the writing is verbose'."
---

# Writing: Line Editing

Line editing addresses mechanical failures at the sentence level — the problems that make competent writing feel clunky, slow, or airless. These are distinct from prose quality problems (which `/s4h-writing-prose-elevation` addresses): line editing is about removing what is broken, not elevating what is merely flat.

Five failures account for the majority of sentence-level problems:

**Redundancy:** Saying the same thing twice, either in the same sentence or in adjacent sentences. Often invisible to the writer because the repetition feels like emphasis or clarity.

**Nominalisation (zombie nouns):** Converting verbs and adjectives into noun forms, burying the action inside the noun. "Made a decision" instead of "decided." "Had a realisation" instead of "realised." "Conducted an investigation" instead of "investigated." Every nominalisation costs one verb, reduces clarity, and adds bureaucratic weight.

**Agency-obscuring passive voice:** Not all passive voice is wrong — "Mistakes were made" is passive, but sometimes the subject genuinely isn't known or relevant. The problem is passive voice that obscures *who did what*, when the agent matters: "The decision was made to cut the programme" when the sentence needs to say who cut it.

**Rhythmic monotony:** All sentences the same length. All sentences starting the same way. A page that reads like a manual because every sentence is a main clause, subject-verb-object, approximately fifteen words, followed by another exactly like it. Rhythm variation creates pace, emphasis, and the sense of a living mind behind the prose.

**Throat-clearing:** Opening sentences or paragraphs that warm up before landing. "It is worth noting that the situation has certain characteristics that make it worth considering." The sentence starts before the writer has found the point. The actual sentence starts at "the situation."

---

## Your Process

**Pass 1: Redundancy**

**Framing check:** Confirm the specific text before continuing. State what you've identified — the actual piece being edited and its key parameters (length, register, genre) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific text — e.g. 'a 400-word professional report introduction with academic register']. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

Flag any sentence or passage that says what has already been said. This includes: direct repetition (same information twice in close proximity), circular sentences (restating the subject in the predicate), and summary after explanation (explaining something then immediately summarising it). For each: quote both instances, recommend cutting or combining.

**Pass 2: Zombie Nouns (Nominalisations)**
Scan for the most common nominalisation patterns:
- "Made a [noun]" → [verb]: made a decision → decided; made a recommendation → recommended
- "Had a [noun]" → [verb]: had a realisation → realised; had a discussion → discussed
- "Conducted a [noun]" → [verb]: conducted an investigation → investigated
- Abstract nouns with -tion, -ment, -ance, -ence endings that are hiding a more precise verb

For each: quote the nominalised form + suggest the active verb replacement.

**Pass 3: Passive Voice**
Flag passive constructions. For each:
- Is the agent unknown or genuinely irrelevant? → Passive is acceptable.
- Is the agent known and relevant? → Reconstruct as active with agent as subject.
- Is the passive obscuring accountability or responsibility? → Flag specifically.

**Pass 4: Sentence Rhythm**
Read a sample passage aloud. Note:
- Are all sentences approximately the same length?
- Are all sentences the same syntactic pattern (subject-verb-object)?
- Are there no short sentences? (A single short declarative sentence after a long passage creates emphasis. Without them, everything is the same weight.)
- Is there no sentence variety — compound sentences, complex sentences, fragments for effect?

Prescribe: where to add short sentences; where to vary opening patterns; where a sentence can be broken or combined.

**Pass 5: Throat-Clearing**
Identify opening sentences in paragraphs and in the piece itself where the writer is warming up rather than landing. Signs: "It is worth noting that...", "It is important to understand that...", "One of the interesting aspects of this is...", sentences where the subject is "it" or "there" followed by a linking verb.

For each: quote the throat-clearing opener + write the sentence as it should start.

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

### Line-Edit Report

**Redundancies:** [Quoted instances + cut/combine recommendation]

**Zombie Nouns:** [Quoted form → Active verb replacement]

**Passive Voice:**
- Acceptable: [Quoted + reason passive is fine]
- Should be active: [Quoted → Active reconstruction]
- Accountability-obscuring: [Quoted + FLAG]

**Rhythm Notes:** [Diagnosis of monotony type + prescription: where to add short sentences, vary openings, etc.]

**Throat-Clearing:** [Quoted opener → Lean reconstruction]

**Rewritten Sample Paragraph:** [One complete paragraph from the submitted text with all five categories of changes applied, showing the cumulative effect]

---

## Notes

- Run `/s4h-writing-restructure` before line editing. Rewriting sentences in a section that will be cut or moved is wasted effort. Structure first, sentences second.
- Line editing removes problems; it does not create quality. After a clean line edit, flat prose is still flat — just more efficient. For prose quality, see `/s4h-writing-prose-elevation`.
- The zombie noun pattern is the single highest-return edit pass: nominalisations are extremely common in professional and academic writing, and every conversion strengthens the sentence.
- Pairs with `/s4h-writing-prose-elevation` — these two skills work in sequence: line editing removes the clutter, prose elevation raises the quality.
- Pairs with `/s4h-writing-tone-alignment` — many tone corrections are sentence-level changes; the two passes can often be combined.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Line editing complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-voice-consistency` — Check voice is consistent after editing
  - `/s4h-writing-tone-alignment` — Check tone after editing
  - `/s4h-writing-prose-elevation` — Elevate the edited prose
  - **Done** — Wrap up and synthesise what we have so far
