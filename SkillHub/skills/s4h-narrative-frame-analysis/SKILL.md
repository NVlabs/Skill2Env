---
name: s4h-narrative-frame-analysis
description: "Identifies the current frame around a situation and generates alternative frames that reveal different truths. Use when asked to 'reframe this', 'the framing is wrong', 'change the narrative', 'different angle', or 'why won't they see it'."
---

# Narrative Frame Analysis

Frames are invisible until named. The same facts support radically different conclusions depending on who is the protagonist, what counts as the problem, and what counts as success. Most communication failures are framing failures — not evidence failures. Reframing does not change the facts; it changes which facts are salient and which conclusions they support.

---

## Your Process

**Step 1: Name the Current Frame**
Make the implicit explicit. Who is the protagonist in the current frame? What is the problem being solved? What counts as a successful outcome? What is the frame's implicit villain or antagonist?

**Framing check:** Confirm the specific situation and its dominant frame before continuing. State what you've identified — the actual narrative or discourse being analysed, who the current protagonist is, and what the core tension appears to be — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation and its current frame]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify What the Current Frame Hides**
Every frame foregrounds some things and backgrounds others. What does the current frame make invisible, irrelevant, or unthinkable? Who loses standing in this frame? What solutions become impossible to see?

**Step 3: Generate 3–4 Alternative Frames**
For each alternative, change at least one of: protagonist, problem definition, success criteria, or time horizon. Assign each alternative a short name.

**Step 4: Assess Each Alternative**
What does each alternative frame reveal that the current frame hides? Who gains standing? What solutions become visible? What previously central concerns become peripheral?

**Step 5: Select the Most Useful Frame**
**Before narrowing:** Show the complete set of alternative frames generated in Step 3 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] alternative frames. Before I select the most useful one, are there any you'd flag as especially promising, or any framing I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific frame to prioritise
  - **Add a missing one** — user will describe an alternative frame to include

The best frame is not the most flattering — it is the one that most accurately surfaces what matters and opens the most productive path forward. State the rationale.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Reframe options only** — Alternative frames, skip analysis of the current frame
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Current Frame**
- Protagonist: [who]
- Problem: [what]
- Success: [what counts]
- What it hides: [what becomes invisible]

**Alternative Frames**

| Frame Name | Protagonist | Problem Definition | Success Criteria | What It Reveals |
|-----------|-------------|-------------------|-----------------|----------------|
| | | | | |

**Recommended Frame:** [name] — [rationale in 2 sentences]

**Message Implications:** [how communication changes under the recommended frame]

---

## Notes

Reframing surfaces different truths, not false ones. If an alternative frame requires ignoring real evidence, it is spin — a useful frame must be defensible against the facts.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Frame analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-narrative-structure-mapping` — Map the structure of the dominant frame
  - `/s4h-communication-objection-mapping` — Map objections rooted in alternative frames
  - `/s4h-writing-argument` — Build an argument that works within the frame
  - **Done** — Wrap up and synthesise what we have so far
