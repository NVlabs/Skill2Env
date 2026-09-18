---
name: s4h-linguistics-pragmatics
description: "Analyzes what is implied rather than said — the gap between literal content and communicative meaning. Use when you say 'what does this really mean', 'what is this message actually doing', 'is this a threat', 'what is being implied here', 'what does this leave unsaid', 'why does this feel off even though it seems polite', or when a communication seems fine on the surface but something is wrong underneath."
---

# Linguistics: Pragmatics

What people say and what they mean are rarely the same thing.

H.P. Grice's theory of conversational implicature — developed in his 1975 "Logic and Conversation" — is one of the most powerful tools in the analysis of communication. Grice observed that speakers routinely communicate far more than they literally say, and that listeners routinely infer far more than they are told. This works because communication operates against a background assumption of cooperation: speakers are expected to be relevant, truthful, informative, and clear. When they violate one of these maxims — saying less than is relevant, using indirect language when direct would do — listeners do not take the violation at face value. They infer that the speaker is communicating something the literal words do not state.

This is how "could you pass the salt?" functions as a polite request rather than a question about physical capacity. It is how "some of our guests have enjoyed the new policy" implies that others have not. It is how "we need to talk" implies something serious even before any content is delivered. J.L. Austin and John Searle extended this analysis to speech acts — the recognition that utterances do not just describe the world but perform actions: they promise, warn, threaten, command, apologise, and commit. "I'll get to it" is not just a prediction; in context, it can be a promise, a deflection, or a passive refusal.

This skill surfaces what a communication is actually doing below its literal content.

---

## Your Process

**Step 1: Establish Literal Content**
Read the communication exactly as written or spoken. State the literal propositional content — what the words denote, with no inference added. This is the baseline from which all implicature is measured. Be precise: strip out any reading of intent and state only what the words explicitly assert.

**Framing check:** Confirm the communication and the pragmatic analysis task before continuing. State what you've identified — the utterance or text being analyzed and the implied communication concern — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence description of what is being analyzed and what pragmatic question is at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify Gricean Maxim Violations**
Apply Grice's maxims to the text. For each maxim, ask: is the speaker operating within it, or flouting it? A flout — a visible, deliberate violation — generates implicature. A violation that cannot be detected does not.

- **Quantity:** Is the speaker saying too little or too much? "Some of the team agreed" says too little if we expect the speaker to know how many — implying fewer than we'd want.
- **Quality:** Is the speaker saying something they cannot be sure of? Hedges like "I imagine" and "it's possible that" can implicate low confidence or deliberate distancing.
- **Relation:** Is the contribution relevant? An apparently irrelevant response often implicates an evasion or a change of subject.
- **Manner:** Is the speaker being indirect, vague, or ambiguous when clarity is expected? Indirect speech acts, euphemisms, and circumlocutions usually implicate something about the speaker's relationship to the content.

**Step 3: Identify Speech Acts**
Following Austin and Searle, identify what speech acts the communication is performing. The illocutionary force — what the utterance is doing — is often different from its grammatical form:
- A question may be a rhetorical assertion, a polite command, or an accusation
- A statement may be a threat, a warning, or a promise
- A compliment may be a status move or an indirect request
- An expression of concern may be a form of control

Name the illocutionary act explicitly: "this utterance is functioning as a [threat / promise / rebuke / deflection / implicit demand / soft refusal]."

**Step 4: Surface Presuppositions**
Every sentence presupposes a set of background assumptions. "Have you stopped taking shortcuts?" presupposes you were taking shortcuts. "Our new initiative builds on the progress we've made" presupposes there has been progress. Accepting a question or responding to a statement without challenging its presuppositions means implicitly endorsing them. Surface the presuppositions embedded in the communication.

**Step 5: Reconstruct the Full Communicative Meaning**
Synthesize the gap between literal content and full communicative meaning. What will a competent listener actually hear — not just the words, but the implications, the speech acts, the presuppositions, and the things left strategically unsaid? State this reconstruction explicitly as a single paragraph: "A listener reading this communication in context will understand that..."

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences, then ask:

- **Question:** "My read: [your 1–2 sentence interpretation of what's being analyzed and what pragmatic question you're investigating]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps: implicatures, speech acts, presuppositions, and full reconstruction
  - **Key findings only** — The bottom-line gap between what was said and what was communicated
  - **Speech acts only** — What is this communication actually doing?
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Literal Content**
What the words actually say, stripped of inference.

**Gricean Analysis**

| Maxim | Status | Implicature generated |
|---|---|---|
| Quantity | Operating within / Flouting | |
| Quality | Operating within / Flouting | |
| Relation | Operating within / Flouting | |
| Manner | Operating within / Flouting | |

**Speech Acts**
List of illocutionary acts identified, with the specific phrase or passage that performs each act.

**Presuppositions**
List of background assumptions the communication takes for granted. For each: state the presupposition and note whether accepting the communication without challenge implicitly endorses it.

**Full Communicative Meaning**
A paragraph reconstructing what a competent listener will actually understand from this communication in context — the sum of literal content, implicature, speech acts, and presuppositions.

**Strategic Assessment**
What this communication is doing — what it achieves or attempts to achieve at the pragmatic level, and whether the strategy is likely to work.

---

## Notes

Pragmatics analysis is useful both for understanding what others are communicating and for auditing what your own communications imply. Most unintended communications are pragmatic failures: the literal content was fine, but the implicatures, speech acts, or presuppositions did unintended work.

The nearest-neighbor trap: confusing pragmatics with subtext hunting. Pragmatics is disciplined — it works from the specific mechanisms of implicature, speech acts, and presupposition, not from free association about intent. Not every indirect phrase is a hidden message; the analysis stays grounded in what a reasonable listener would infer in context.

Pair with `/s4h-linguistics-framing` when the presuppositions reveal a deeper framing problem. Pair with `/s4h-communication-objection-mapping` when you need to anticipate how listeners will respond to the implied content rather than just identify it.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Pragmatic analysis complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-linguistics-framing` — Examine the frame the presuppositions reveal
  - `/s4h-communication-objection-mapping` — Map how listeners will respond to the implied meaning
  - `/s4h-psychology-persuasion` — Understand the persuasion mechanisms operating in the implied content
  - **Done** — Wrap up and synthesise what we have so far
