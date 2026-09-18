---
name: s4h-communication-objection-mapping
description: "Maps likely objections before delivering a proposal — objections that are anticipated feel addressed; objections that land as surprises derail. Triggers: 'anticipate objections', 'what will they push back on', 'steelman the opposition', 'prepare for resistance', 'objection mapping'."
---

# Communication Objection Mapping

Anticipated objections feel handled. Unanticipated objections derail. The difference is
not the content of the objection — it is whether the receiver senses that the sender
has thought it through. A proposal that addresses likely objections before they are
raised signals rigor and respect. One that doesn't signals that the sender only thought
from their own perspective.

---

## Your Process

**Step 1: State the Proposal**
Write the proposal clearly — what is being asked, what it proposes to do, and what it
asks of the audience (approval, resources, behaviour change, belief change).

**Framing check:** Confirm the message, the audience, and the goal before continuing. State what you've identified — the actual proposal being analyzed, who it is directed at, and what it is asking them to do — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the proposal, its audience, and the outcome being sought]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: List Audience Segments**
Who will receive this? Different roles and individuals will have different objections.
A finance stakeholder's objection to a proposal is structurally different from an
engineering lead's, even if both say "this is risky."

**Step 3: Generate Objections per Segment**
For each segment: given what they care about and what they fear, what is their most
likely objection? Be specific — "they might push back on cost" is too vague. "They will
argue the ROI model assumes usage patterns that contradict last quarter's data" is useful.

**Step 4: Classify Each Objection**
- **Legitimate**: the objection raises a real concern the proposal should genuinely engage
  with. Dismissing it will damage credibility.
- **Unfounded**: the objection reflects a misunderstanding, missing information, or
  an assumption the proposal already addresses. Requires clarification, not capitulation.

**Step 5: Respond to Legitimate Objections**
For each legitimate objection: what is the honest, direct response? Acknowledge the
concern genuinely. Address it specifically. Do not pretend it doesn't exist or soften
it into irrelevance — that will be noticed.

**Step 6: Pre-emptive Move**
For each significant objection: is there something in the message itself that could reduce
the objection's force without capitulating to it? Pre-empting an objection by raising it
yourself is more credible than responding to it when challenged.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Top 3 objections only** — Most likely showstoppers, skip the full map
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Proposal:** [Summary — what is being asked and what is being proposed]

**Objection map:**

| Audience segment | Likely objection | Legitimate / Unfounded | Response | Pre-emptive move |
|-----------------|-----------------|----------------------|----------|------------------|
| | | | | |
| | | | | |

**Objections to address in the message itself:**
> [Which objections should be pre-empted in the proposal, not left for Q&A — and why]

**Objections to prepare for but not address upfront:**
> [Which are better handled in dialogue than in the message]

---

## Notes

The classification in Step 4 requires honesty. The temptation is to classify all
objections as unfounded — that they reflect misunderstanding rather than legitimate
concern. If an objection is legitimate and you dismiss it, you lose credibility on
everything else.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Objections mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-argument` — Build arguments that directly address each mapped objection
  - `/s4h-communication-clarity-audit` — Check that responses to objections are clear
  - `/s4h-logic-argument-validation` — Validate the arguments you'll use to address key objections
  - **Done** — Wrap up and synthesise what we have so far
