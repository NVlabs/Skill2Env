---
name: s4h-writing-rhetoric
description: "Analyses what a piece of writing is doing rhetorically — its rhetorical situation, explicit argument vs. buried frame, appeals map, and loaded language. Use to surface assumptions, examine persuasion techniques, or understand how a piece is working. Triggers: 'rhetorical analysis', 'what is this piece doing rhetorically', 'rhetoric', 'analyze this argument', 'how is this persuasive', 'what assumptions is this making', 'loaded language', 'hidden assumptions', 'what is this piece really arguing'."
---

# Writing: Rhetoric

Rhetoric analysis asks not "what does this say" but "what is this doing." Every piece of writing has a rhetorical situation — a speaker, an audience, a purpose, a context — and makes rhetorical moves that are often invisible to both writer and reader. The analysis surfaces what is operating below the explicit argument.

The most important distinction: **the explicit argument vs. the rhetorical frame**. The explicit argument is what the text claims. The rhetorical frame is what the text assumes without stating — the premises, values, and world-views that must be accepted for the argument to work, and which are never examined because they are presented as neutral common ground. The frame often does more work than the argument, and it is almost never examined.

Example: a piece arguing for stricter immigration policy may frame "the nation" as a coherent entity with interests that can be defended, may frame immigration as a *flow* rather than people making decisions, and may frame the relevant question as "how many" rather than "who benefits and who bears costs." None of these framing choices are acknowledged as choices — they are presented as the natural way to think about the issue. But they are doing enormous rhetorical work.

The classical appeals — logos (reason), ethos (authority/credibility), pathos (emotion) — describe the rhetorical resources available to any writer. Understanding which appeals dominate a piece, and whether they are being used proportionately and honestly, is central to rhetorical analysis.

---

## Your Process

**Step 1: Rhetorical Situation**
Identify the four elements of the rhetorical situation:
- **Speaker/Author:** Who is presenting? What is their apparent identity, authority, and relationship to the subject?
- **Audience:** Who is the intended reader? What assumptions does the text make about what the reader already believes?
- **Purpose:** What is the text trying to do? (Persuade? Inform? Legitimise? Mobilise? Reassure?)
- **Context:** What is the occasion and institutional setting of this text? What situation does it respond to?

**Framing check:** Confirm the specific text and its rhetorical context before continuing. State what you've identified — the actual piece being analysed, its apparent genre/form, and the core question the analysis will answer — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific text, its form, and the rhetorical question at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Explicit Argument vs. Rhetorical Frame**
State the explicit argument: what does the text claim?
Then map the rhetorical frame: what does the text assume without claiming?
- What categories does the text use, and are those categories neutral or loaded?
- What is presented as natural or obvious that is actually a contested choice?
- What is not said — what counterframes, alternative categories, or competing values are absent?

**Step 3: Appeals Map**
Identify the proportion and quality of each appeal:
- **Logos:** Reasoning, evidence, data, logical structure. Is the logical structure valid? Is the evidence sufficient and credible?
- **Ethos:** Authority, credibility, shared values. Is authority earned or asserted? Is the ethos appeal based on genuine expertise or on status?
- **Pathos:** Emotional resonance, story, imagery, language that activates feeling. Is the emotional appeal calibrated to the argument, or disproportionate? Is it being used honestly or to bypass reasoning?

**Step 4: Loaded Language**
Flag specific words or phrases that carry ideological weight without acknowledgment. These are words that encode a position within their seemingly neutral meaning:
- "Common sense" (implies disagreement is unreasonable)
- "Our values" (constructs a unified "we" that may not exist)
- "Simply" / "obviously" (dismisses complexity)
- Terms that are contested being used as if settled
- Metaphors that encode a frame (immigration as "flood"; policy as "battle")

For each: quote the term, identify what frame it encodes, and note what alternative language would make the choice visible.

**Step 5: Verdict**
Is the rhetoric honest and proportionate to the argument? This is the key evaluative question. Rhetoric is not inherently manipulative — all writing makes rhetorical choices. The question is whether the rhetorical moves are serving the argument or substituting for it; whether the loaded language is doing work the logic doesn't; whether the frame is being deployed honestly or invisibly.

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

### Rhetorical Analysis

**Rhetorical Situation:**
- Speaker: [Identity, authority, relationship to subject]
- Audience: [Intended reader + assumed prior beliefs]
- Purpose: [What the text is trying to do]
- Context: [Occasion and institutional setting]

**Explicit Argument vs. Rhetorical Frame:**
- Explicit argument: [What the text claims]
- Buried frame: [What the text assumes — specific categories, naturalisations, absences]

**Appeals Map:**
- Logos: [Quality and proportion of reasoning and evidence]
- Ethos: [Authority appeal — earned or asserted]
- Pathos: [Emotional appeals — calibrated or disproportionate]
- Dominant appeal: [Which dominates — appropriate or not?]

**Loaded Language:**
- [Quoted term] — Frame encoded: [what position it carries] — Alternative: [language that makes the choice visible]
- [Repeat]
- NONE FOUND if language is neutral

**Verdict:** [Is the rhetoric honest and proportionate? Where does it serve the argument? Where does it substitute for it?]

---

## Notes

- Rhetoric analysis is not the same as saying a piece is wrong. A rhetorically sophisticated piece may also be logically sound. Rhetoric analysis describes what it is doing — the evaluation of whether that is appropriate or misleading is a separate judgment.
- The most common rhetoric problem in ostensibly neutral writing: the frame is doing the persuasion while the explicit content maintains the appearance of objectivity. News articles, policy briefs, and corporate communications are particularly susceptible to this.
- Pairs with `/s4h-writing-argument` — argument analysis evaluates whether the logic is sound; rhetoric analysis evaluates how it is being made. They are complementary, not redundant.
- Pairs with `logic-argument-validation` (in the logic category) — for formal logical structure analysis when the rhetoric analysis reveals argument problems that need rigorous logical audit.
- Pairs with `/s4h-writing-audience-calibration` when the rhetorical analysis reveals that the text is calibrated not for its stated audience but for a different one — a common finding in political and institutional writing.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Rhetoric applied. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-argument` — Strengthen the underlying argument with the rhetoric
  - `/s4h-communication-objection-mapping` — Map objections the rhetoric must address
  - `/s4h-writing-line-editing` — Polish the rhetorical prose
  - **Done** — Wrap up and synthesise what we have so far
