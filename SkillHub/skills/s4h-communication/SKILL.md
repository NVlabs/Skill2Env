---
name: s4h-communication
description: "Entry point for the communication toolkit. Routes to the right communication skill based on your situation. Use when you say 'communication', 'how do I say this', 'will this land', 'which channel', 'what will they push back on', 'does this make sense', or want communication help without knowing which specific tool fits."
---

# Communication

Applies communication thinking to any message, proposal, or delivery decision. Diagnoses what kind of communication problem this is and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Understand what your audience actually believes and cares about | audience-modeling |
| Find where a message will be misread or lost before sending | clarity-audit |
| Choose the right channel and format for the message | medium-selection |
| Anticipate and pre-address likely objections | objection-mapping |

## Routing Decision

**Framing check:** Confirm the message, the audience, and the goal before continuing. State what you've identified — the actual communication situation being addressed — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the message, who it's going to, and what success looks like]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Don't know your audience well or why they're not getting it** → audience-modeling
- **Have a draft and want to find where it breaks** → clarity-audit
- **Unsure whether to email, meet, async, sync, document** → medium-selection
- **About to present something contentious and need to prepare** → objection-mapping
- **Unclear** → audience-modeling first; communication fails at the receiver, not the sender

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Audience Modeling

*Maps what the audience currently believes, actually cares about, and fears.*

Build a model of the audience before communicating. What do they already believe about this topic? What are their real goals (often different from their stated role)? What do they fear — about the message, the change, the consequences? What would need to be true for them to change their mind or take action? Communication fails not because the message is unclear, but because the sender doesn't model the receiver.

**Output:** Audience belief map, real goals, fears, and the threshold conditions for a positive response.

---

## Clarity Audit

*Finds where a message will be lost, misread, or misunderstood.*

Read the message as if you have no prior context. Where does it assume knowledge the reader may not have? Where could a word or phrase be interpreted differently? Where does structure obscure the point? Where is the ask buried or implicit? For each problem: classify as ambiguity (multiple valid interpretations), assumption (missing context), or structure (the architecture hides the message).

**Output:** Annotated list of clarity problems, classified by type, with specific rewrites for each.

---

## Medium Selection

*Matches the message to the right channel and format.*

Assess the message against four dimensions: (1) complexity — does understanding require dialogue, or is the content self-contained? (2) tone — does this carry emotional weight requiring presence? (3) record — does this need to be findable later? (4) urgency — how time-sensitive is the response? Map these against available channels. The same content in the wrong medium loses most of its effect — an async message that needed presence, or a meeting that needed a document.

**Output:** Recommended channel with reasoning, format within that channel, and what to avoid.

---

## Objection Mapping

*Maps likely objections before delivering a proposal.*

List all stakeholders who will encounter this proposal. For each: what is their likely first objection? What's the deeper concern beneath it? Now assess each objection: is it addressable by changing the proposal, addressable by framing, or genuinely unresolvable? Objections anticipated feel addressed; objections that arrive as surprises derail.

**Output:** Objection map — stakeholder, surface objection, underlying concern, and how to address it. Flags unresolvable objections the presenter must prepare for.
