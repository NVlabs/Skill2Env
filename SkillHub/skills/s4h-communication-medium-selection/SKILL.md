---
name: s4h-communication-medium-selection
description: "Matches the message to the right channel and format — the same content in the wrong medium loses most of its effect. Triggers: 'which channel', 'email vs meeting', 'should this be async or sync', 'medium fit', 'how should I deliver this'."
---

# Communication Medium Selection

The same content delivered through the wrong medium loses most of its effect. Bad news in
Slack destroys trust. A complex decision in an email generates confusion. A routine update
in a meeting wastes an hour. Medium selection is not a logistics question — it is a
communication design decision that determines whether the message can land at all.

---

## Your Process

**Step 1: Message Goal**
What must the receiver do, feel, or understand as a result of this communication? Be
specific. "Understand the situation" is not a goal. "Approve the budget by Friday" is.
"Feel heard about the reorg" is.

**Framing check:** Confirm the message, the audience, and the goal before continuing. State what you've identified — the actual communication being designed and its key parameters — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the message, audience, and goal]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Urgency**
How quickly must they act or respond? Hours, days, weeks? Urgency drives the sync vs
async question more than any other factor.

**Step 3: Emotional Weight**
Is this message carrying emotional content? Difficult news, a sensitive correction, a
celebration, a request that requires trust, a change that affects someone's identity or
security? Emotional weight requires channels that allow nuance and reaction.

**Step 4: Complexity**
Does this require back-and-forth to resolve, or can it land cleanly in a single read?
Complex decisions with multiple unknowns require synchronous dialogue. Clear information
transfers can be async.

**Step 5: Match to Medium**
Apply the selection logic:
- Difficult news / sensitive topic → sync verbal (in person or video)
- Complex decision requiring buy-in → meeting with written pre-read
- Simple update, no action required → async written (email or doc)
- Permanent record needed → written
- Emotional connection is the goal → video or in person
- Fast coordination, low stakes → messaging (Slack, etc.)
- Formal commitment → written with signature or named acknowledgment

**Step 6: Choose Primary and Secondary Medium**

**Before narrowing:** Show the complete set of candidate media that matched in Step 5 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified these candidate media: [list each matching channel from Step 5]. Before I select the best fit, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific channel to include
  - **Add a missing one** — user will describe it

Select the primary channel. If the message needs reinforcement (complex, high-stakes,
or high emotional weight), add a secondary: e.g., meeting followed by written summary.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Channel recommendation only** — Which medium and why, skip the full analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Message assessment:**

| Dimension | Assessment |
|-----------|------------|
| Goal | [What must receiver do/feel/understand] |
| Urgency | [Timeline] |
| Emotional weight | [None / Low / Medium / High — why] |
| Complexity | [One-way or requires dialogue] |

**Recommended medium:** [Primary channel]
**Secondary medium (if needed):** [Reinforcement channel + why]

**Rationale:**
> [2-3 sentences on why this medium fits this message — and what would go wrong in
> the next-most-obvious alternative]

---

## Notes

The most common error is defaulting to async written (Slack, email) for messages with
high emotional weight, because it feels faster and less confrontational. The short-term
comfort always costs more in trust and rework than the difficult conversation would have.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Medium selected. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-communication-audience-modeling` — Model the audience for the selected medium
  - `/s4h-writing-audience-calibration` — Calibrate the writing for the chosen medium
  - `/s4h-communication-clarity-audit` — Audit clarity for the selected medium
  - **Done** — Wrap up and synthesise what we have so far
