---
name: s4h-writing-restructure
description: "Diagnoses and repairs structural problems in non-fiction, essays, and documents — wrong order, buried lead, wrong ending, proportion errors. Use when a piece is in the wrong order, starts too late, or spends space on the wrong things. Triggers: 'the piece is in the wrong order', 'restructure', 'buries the lede', 'the structure is off', 'reorganise this', 'the ending is in the wrong place', 'takes too long to get to the point'."
---

# Writing: Restructure

Structural problems are the hardest to see from inside the piece — because from inside, structure is invisible. The writer always knows where they're going; they know the context, the backstory, why the claim matters. The reader only knows where they've been. The result: pieces that are perfectly clear to the writer and impenetrable to the reader, because the reader doesn't have the context that makes the opening make sense, doesn't know that the important claim is on page four, and has no way to distinguish the load-bearing material from the scaffolding.

Three structural failures account for the majority of structurally broken pieces:

**Burying the lead:** The piece starts with context, background, or setup rather than the claim or finding. The writer needed to write the setup to arrive at the claim. The reader doesn't need it — or needs a fraction of it, after the claim has been stated.

**Wrong ending:** The piece stops before it resolves. The real insight is in the second-to-last paragraph. The final paragraph is a softening or a retreat. Or the piece stops at the conclusion of the argument but before its implications — leaving the reader with the logic but not the meaning.

**Wrong proportion:** The piece spends three pages on the least important point and half a page on the most important one. The proportion reflects the order in which the writer discovered things, not the order of their importance.

All three failures have the same cause: the structure was not designed for the reader — it was inherited from the process of writing.

---

## Your Process

**Step 1: Central Argument or Effect**
What is the piece trying to do? State it in one sentence. If this can't be done in one sentence, the piece may not have a clear central claim — which is itself a structural problem. A piece that doesn't know what it's arguing cannot be structured around its argument.

**Framing check:** Confirm the specific piece and its structural situation before continuing. State what you've identified — the actual document being analyzed, its apparent central claim (if one exists), and the structural failure type most visible — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the piece, its central claim, and the primary structural problem]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map the Actual Structure**
What comes first, second, third? Summarise each major section in one sentence. Note: not what the writer intended each section to do — what it actually does, from a reader's perspective. Often these are different.

**Step 3: Find the Real Beginning**
What is the first sentence or section that actually matters — where the piece's energy starts, where the reader genuinely needs to be to follow what follows? Everything before this point is either context that could be cut, setup that could be condensed to a sentence, or warming-up that the writer needed but the reader doesn't.

**Step 4: Find the Right Ending**
Where does the piece's energy actually resolve? This is often not the last paragraph. Look for the sentence or paragraph where the piece's central claim gets its fullest, most resonant expression. Everything after that point may be retreating from the claim, adding caveats, or continuing past the natural stopping point.

**Step 5: Proportion Audit**
List each major section with an approximate word count or proportional weight. Ask: is the heaviest section the most important one? Is the lightest section actually the load-bearing claim? Proportion that doesn't match importance sends the reader false signals about what matters.

**Step 6: Reorder Recommendation**
Given the above, what is the optimal sequence? State the new structure as a sequence of sections with rationale for the order.

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

### Structural Diagnosis

**Central Argument:** [One sentence — what the piece is trying to do]

**Actual Structure Map:**
1. [Section: what it does + approximate weight]
2. [Section: what it does + approximate weight]
3. [And so on]

**Real Beginning:** [The sentence/section where the piece actually starts / Note on what precedes it and whether it should be cut or condensed]

**Right Ending:** [Where the piece's energy resolves / Note on what follows it and whether it can be cut]

**Proportion Audit:** [Most important sections vs. most space given / Mismatch between importance and weight]

**Reorder Recommendation:** [New sequence with rationale for each position change]

---

## Notes

- The most useful diagnostic question: if you deleted the first third of the piece and sent the reader straight to what is currently the middle, would they be lost? If no, the first third is probably setup that the writer needed but the reader doesn't.
- Restructuring should happen before line editing. Rewriting sentences in a section that will be cut or moved is wasted effort.
- Pairs with `/s4h-writing-executive-summary` when the restructured piece needs a front-loaded brief for an audience that won't read the full document.
- Pairs with `/s4h-writing-argument` when the structural problem is an argument-structure problem — the claim, warrant, and evidence are in the wrong order or the warrant is missing.
- Pairs with `/s4h-writing-line-editing` after restructuring is complete — once the order is right, the sentences can be cleaned.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Restructuring complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-line-editing` — Edit after restructuring
  - `/s4h-writing-tone-alignment` — Realign tone after the restructure
  - `/s4h-writing-voice-consistency` — Check voice is consistent after restructure
  - **Done** — Wrap up and synthesise what we have so far
