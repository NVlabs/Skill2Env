---
name: s4h-writing-executive-summary
description: "Produces executive summaries, 1-page briefs, and board-level documents by extracting the situation, key findings, implications, and recommendation — answer-first, one page maximum. Use when a lengthy document needs a senior-audience brief that enables a decision. Triggers: 'executive summary', 'summarise this for a senior audience', '1-page brief', 'TL;DR for leadership', 'distil this', 'board summary', 'write a brief'."
---

# Writing: Executive Summary

Executive summaries fail when they summarise the document rather than answering the reader's question. A summary of a 40-page analysis is not what an executive needs. They need: what is the situation, what are the three things most important to know, what does it mean for their decision, and what should happen next. In that order. In one page.

The fundamental principle: the executive is not the end reader of your analysis — they are a decision-maker who needs the *output* of your analysis in a form that enables action. The detail, the methodology, the full data — that stays in the main document. The executive summary gives them what they need to act without reading the full document.

Four common failures:
- **Summarising the process, not the answer:** "We conducted a comprehensive analysis of three market segments, reviewing 47 data sources over 8 weeks." The executive doesn't need to know how long it took — they need to know what it found.
- **Findings without implications:** Stating what happened without stating what it means for the decision at hand.
- **False balance:** Including minor findings to be thorough, diluting the signal with noise. Three things that matter are better than twelve things that range from critical to marginal.
- **Passive language on the recommendation:** "It may be worth considering..." — the executive summary is where the recommendation is made, not hedged.

---

## Your Process

**Step 1: Reader's Role and Actual Decision**
Who exactly is reading this? What is the specific decision they need to make? Not "the board should be informed" but "the board is deciding whether to approve the $2M market expansion budget." This decision frames everything: what gets included, what gets cut, and how the recommendation is framed.

**Framing check:** Confirm the reader and their decision before continuing. State what you've identified — the specific audience, their role, and the exact decision they are making — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of who the reader is and what decision they need to make]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify the Three Most Important Things**
From the full document: what are the three findings, facts, or insights that most directly bear on the reader's decision? Not the most interesting to you — the most important to them.

**Before narrowing:** Show the complete set of candidate findings to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] candidate findings. Before I select the three most critical to the reader's decision, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific finding to include
  - **Add a missing one** — user will describe it

These become the three bullets in the Key Findings section. If there are more than three, you are either including noise or you have not prioritised.

**Step 3: Implications Not Findings**
Translate findings into implications: not "our Q3 customer acquisition cost rose 40%" but "our current acquisition strategy is unsustainable at scale — at Q3 rates, the expansion budget funds half the projected customer growth." Implications answer "so what?" They are what the executive needs in order to act.

**Step 4: Cut Context That Serves the Writer**
Anything that explains how the analysis was done, why you looked at what you looked at, or what you ruled out — this serves the writer's need for credit and completeness, not the reader's need for decision support. Cut it. If it is genuinely important context, it can be one sentence.

**Step 5: Draft to One Page / 300 Words**
Every sentence must earn its place. The test for each sentence: does a reader without this sentence make a worse decision? If no, cut it. The executive summary is not a place for comprehensive coverage — it is a place for decisive clarity.

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

### Executive Summary

**Situation:** [One sentence. What is the context or problem that prompted this analysis?]

**Key Findings:**
- [Finding 1 — most important to the reader's decision]
- [Finding 2]
- [Finding 3 — maximum]

**Implications:** [2–3 sentences. What do these findings mean for the decision? What is at stake if action is taken, or not taken?]

**Recommendation:** [One clear sentence. What should happen? Active voice, no hedging.]

**Next Steps:**
- [Specific action, owner if relevant, timeline]
- [Second action]
- [Third action if needed]

---

## Notes

- Max one page / 300 words. This is not a guideline — it is the requirement. An executive summary that requires two pages has failed.
- The Situation sentence must be answer-first: it should be the one sentence that, if the executive reads nothing else, leaves them with the most important thing to know.
- Passive language on recommendations ("it may be worth considering") signals that the writer is not confident in the recommendation. If you have done the analysis, make the recommendation. The executive can disagree — but they need a recommendation to react to.
- Pairs with `/s4h-writing-report` — the executive summary sits above the full report. The report is for the reader who needs the detail; the summary is for the reader who needs the decision.
- Pairs with `/s4h-writing-audience-calibration` — the executive's specific role, decision context, and prior knowledge shape every word of the summary; what an investor needs is different from what a CEO needs.
- Pairs with `/s4h-writing-restructure` — if the source document is poorly structured, finding the three most important findings requires first identifying what the document actually says (which may require restructuring it).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Executive summary written. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-clarity-audit` — Audit summary clarity for the executive audience
  - `/s4h-writing-audience-calibration` — Calibrate further for the executive reader
  - `/s4h-writing-restructure` — Restructure if the summary doesn't flow
  - **Done** — Wrap up and synthesise what we have so far
