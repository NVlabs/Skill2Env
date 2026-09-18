---
name: s4h-writing-report
description: "Writes and audits business reports, briefing documents, and information reports for answer-first structure, precision, hierarchy, and navigability. Use when a report buries its findings, is written for the writer rather than the reader, or lacks clear structure. Triggers: 'write a report', 'report writing', 'business report', 'briefing document', 'information report', 'research summary', 'the report isn't clear', 'buries the findings'."
---

# Writing: Report

Reports fail when they are written for the writer rather than the reader. The writer knows the context, did the work, and wants to show the rigour of the process. The reader needs to know the answer, understand its implications, and decide what to do — usually in less time than the writer spent writing. These are incompatible objectives, and when the report serves the writer's needs, it fails the reader.

The most common report failures:

**Context before answer:** The report explains how the analysis was done before stating what it found. The reader who needs to act has to mine through methodology to find the claim.

**Findings without implications:** The report states what happened but not what it means. "Revenue declined 12% in Q3" is a finding. "Revenue declined 12% in Q3, driven primarily by a 31% drop in enterprise segment that is likely to continue unless the pricing model is revised" is an implication. Readers who need to decide need implications, not just findings.

**Vague quantification:** "Significant growth," "substantial decline," "many customers." These phrases communicate nothing. If a number exists, use it. If it doesn't, acknowledge the absence explicitly.

**Non-navigability:** A report that can only be understood by reading it from beginning to end has failed. The reader who needs the answer to one specific question should be able to find it. Section headers, a clear hierarchy, and an executive summary are not optional niceties — they are the delivery mechanism.

---

## Your Process

**Step 1: Reader's Question**
Who is reading this report, and what do they need to know and decide? State it specifically: not "the board needs to understand performance" but "the board needs to decide whether to approve the Q4 investment increase given Q3 performance." The reader's specific decision shapes every structural choice.

**Framing check:** Confirm the specific report and its reader before continuing. State what you've identified — the actual document being analyzed, its intended audience, and the core decision it must serve — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the report, its audience, and the decision it needs to serve]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Answer-First Check**
Does the opening section answer the main question before developing it? The first section of a well-structured report should contain the key finding and its primary implication, in plain language, before any methodology, context, or detail. Check: can a reader who only reads the first section make an informed decision?

**Step 3: Hierarchy**
Are sections ordered by importance? Does each section have a clear, functional header that tells the reader what the section will say (not just what topic it covers)? "Q3 Performance" is a topic header. "Q3 Revenue Down 12% — Enterprise Segment Driving Decline" is an answer header. Answer headers allow navigation; topic headers don't.

**Step 4: Precision**
Flag every instance of vague quantification or hedging language: significant, substantial, many, some, often, rarely, most. For each: is there a specific number available? If yes, use it. If no, state the absence: "data not available" or "estimate pending" rather than a vague word that implies precision.

**Step 5: Navigability**
Can a time-pressed reader find what they need without reading everything? Check: is there an executive summary? Are section headers navigable? If there is a key recommendation, is it labelled clearly? Is there a table of contents for documents over 10 pages?

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

### Report Audit

**Reader's Question:** [Specific decision the reader needs to make]

**Answer-First Assessment:** [Does the opening answer the question? / What is the first section actually doing?]

**Hierarchy Map:** [Current section order + assessment of whether importance matches position / Answer headers vs. topic headers]

**Precision Flags:** [Quoted vague language + specific alternative if number is available / "Data absent" note if not]

**Navigability Assessment:** [Executive summary present? / Headers navigable? / Time-pressed reader path]

**Recommended Structural Changes:** [Specific reorderings, reframings, and section header rewrites]

---

## Notes

- Answer-first is not optional for executive audiences. The more senior the reader, the less time they will spend looking for the point. The point must be first.
- The most common resistance to answer-first structure: "but the reader needs the context to understand the finding." Test this assumption. Usually the reader needs a fraction of the context they're given, and they need it after the finding, not before.
- Pairs with `/s4h-writing-executive-summary` — for reports requiring a one-page brief above the full document.
- Pairs with `/s4h-writing-audience-calibration` — the reader profile shapes every structural decision; the report format for a technical team and for a board are different documents.
- Pairs with `/s4h-writing-restructure` when the report's problems are primarily structural — the findings are buried not in the prose but in the architecture.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Report written. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-executive-summary` — Add an executive summary to the report
  - `/s4h-writing-audience-calibration` — Calibrate the report for its specific audience
  - `/s4h-communication-clarity-audit` — Audit report clarity throughout
  - **Done** — Wrap up and synthesise what we have so far
