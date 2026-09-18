---
name: s4h-linguistics
description: "Entry point for the linguistics toolkit. Routes to the right linguistics skill based on your situation. Use when you say 'linguistics', 'how is this framed', 'what does this word really mean', 'what is implied here', 'what does this word carry', 'how has this term changed', or want language analysis applied without knowing which specific tool fits."
---

# Linguistics

Examines language as a system of meaning — not just what words say, but what they frame, imply, carry, and do over time. Diagnoses what kind of linguistic analysis is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Identify how the frame shapes what options are visible | framing |
| Map the emotional and political freight a word carries | connotation |
| Analyze what is implied rather than said | pragmatics |
| Track how a word's meaning has shifted — or is shifting | semantic-drift |

## Routing Decision

**Framing check:** Confirm the language situation in focus before routing. State what you've identified — the text, term, or communication at stake and the linguistic dimension you're examining — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the language situation and the specific dimension to analyze]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **The way an issue is described is shaping what solutions feel possible** → framing
- **A specific word or phrase carries freight beyond its dictionary definition** → connotation
- **What someone said is less important than what they meant or implied** → pragmatics
- **A word's meaning is shifting, contested, or has changed over time** → semantic-drift
- **Unclear** → framing; understanding the frame usually reveals which other tools are needed

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

## Framing

*Identifies how the frame shapes what options are visible and what conclusions feel natural.*

Every description of a situation is also a frame — it makes certain options thinkable and others invisible, certain conclusions feel natural and others require effort. George Lakoff showed that frames operate below conscious argumentation: you cannot refute a frame by accepting its terms. This skill surfaces the current frame, maps its invisible boundaries, and generates alternative frames that reveal different solution spaces.

**Output:** The active frame named and its implications mapped; what the frame makes visible and invisible; three to five alternative frames with their distinct implications; a reframe recommendation.

---

## Connotation

*Maps the emotional and political freight that words carry beyond their literal meaning.*

Words have denotations (dictionary definitions) and connotations (what they evoke, who uses them, what politics they carry). "Investment" and "spending" denote the same action; their connotations produce entirely different policy debates. This skill audits word choices for their connotative freight, identifies where that freight is helping or undermining a message, and finds better alternatives when needed.

**Output:** Connotation audit of key terms — denotation vs. connotation, freight (positive, negative, neutral), audience sensitivity, and replacement candidates.

---

## Pragmatics

*Analyzes what is implied rather than said — the gap between literal content and communicative meaning.*

Following H.P. Grice's maxims of conversation, speakers routinely communicate far more than they literally say. Pragmatics examines what is implicated, presupposed, or performed by an utterance — what the context and speaker intentions supply beyond the explicit words. This skill surfaces hidden implications, identifies speech acts (promises, threats, commands in disguise), and makes visible what a communication is really doing.

**Output:** Pragmatic analysis — literal meaning vs. communicated meaning; implicatures identified; speech acts named; presuppositions surfaced; what the listener will likely infer.

---

## Semantic Drift

*Tracks how meanings shift over time or across groups — and what it costs when words change.*

Words do not hold still. "Literally" now means "figuratively" in common use. "Woke" shifted from an internal community descriptor to a political pejorative. "Investment" expanded to cover what was once called "spending." Semantic drift is sometimes natural evolution, sometimes deliberate capture, sometimes concept creep that changes what a term permits. This skill traces the drift, identifies whether it is organic or engineered, and assesses the consequences.

**Output:** Semantic trajectory — original meaning, current meaning(s), mechanism of drift, who benefits from the drift, and what the shift costs or enables.
