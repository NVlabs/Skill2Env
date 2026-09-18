---
name: s4h-writing-prose-elevation
description: "Raises the quality of competent but flat prose by targeting abstraction, weak verbs, and sensory absence. Use when writing is error-free but doesn't sing — when it reads as competent but not compelling. Triggers: 'the writing is flat', 'prose elevation', 'competent but not compelling', 'lift this writing', 'the prose needs work but isn't broken', 'make this sing', 'the prose is fine but forgettable'."
---

# Writing: Prose Elevation

Prose elevation is not about imposing a style — it's about realising the latent quality already present. Flat prose usually fails in three specific ways, and fixing these three things is enough to significantly raise the quality without overwriting or artificially inflating the voice.

**Abstraction without grounding:** The writer reaches for the general statement — "she felt profound grief" — when a specific image would land harder and trust the reader more. "She kept finding his reading glasses in places she hadn't thought to look." Abstraction summarises experience; specific images recreate it. The reader feels what the abstract statement tries to tell them.

**Weak verbs:** Was, had, got, made, felt, seemed, looked, walked, went. These verbs are not wrong — they are just underloaded. "The room was cold" tells us almost nothing. "The cold crept in under the door and settled at floor level" gives us a room. Precise verbs do the work that adverbs are often asked to do — and do it better.

**Sensory absence:** Prose that lives entirely in dialogue and action, with no texture of the physical world — no temperature, smell, sound, surface — feels disembodied. The reader floats above the scene rather than inhabiting it. Sensory detail is not decoration; it is the mechanism by which the reader is placed inside the experience.

These three failures are addressable without changing a writer's voice. The elevation preserves what is already working and deepens it.

---

## Your Process

**Step 1: Identify Existing Strengths**
Before anything else: what is already working? Strong rhythm, distinctive voice, sharp observation, effective structural choice — whatever the piece is doing well. These are the anchors. The elevation must stay consistent with them; it cannot override them. A prose elevation that erases the writer's idiosyncrasies in favour of "better" prose has failed.

**Framing check:** Confirm the specific prose piece before continuing. State what you've identified — the actual text being elevated and its key characteristics (form, length, apparent purpose or genre) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific prose — e.g. 'a short story opening of roughly 400 words with a quiet, interior voice']. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Abstraction Audit**
Flag abstract statements — places where the prose summarises or tells rather than shows or evokes. For each:
- Quote the abstract statement
- Identify what specific image, action, or detail could carry the same meaning
- Write the grounded alternative

The test: does the replacement trust the reader to make the connection, or does it explain it? If it explains it, it has not moved from abstract to concrete — it has just added a concrete example that summarises the abstract statement. The concrete image should stand alone.

**Step 3: Verb Audit**
Scan for weak verbs in every sentence. The most common offenders: forms of *to be* (was, were, is, are), *to have* (had, has), *to get*, *to make*, *to seem*, *to look*, *to go*, *to feel*. For each:
- Quote the sentence with the weak verb
- Identify what the sentence is actually trying to say about action, quality, or state
- Write a more precise verb that carries that meaning directly

Note: not every weak verb needs replacing. Sometimes "was" is correct. The audit is about identifying instances where a stronger verb would do more work.

**Step 4: Sensory Audit**
Identify scenes, descriptions, or passages with no sensory grounding — where the prose operates only at the level of action, dialogue, and emotion without any texture of the physical world. For each:
- Identify which senses are absent (almost always smell and touch; sometimes sound)
- Suggest specific sensory details that are both accurate to the scene and meaningful — connected to what the scene is doing thematically or emotionally
- The detail should not be arbitrary. The smell of antiseptic in a hospital scene about loss serves the scene; the smell of coffee in the same scene may not.

**Step 5: One-Sentence Diagnosis**
What is the prose's single main weakness across all three categories? Name it precisely. This shapes the recommendation: if the biggest issue is abstraction, the rewrite priority is grounding. If it's weak verbs, the priority is verb replacement. If it's sensory absence, the priority is texture.

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

### Prose Elevation Report

**Existing Strengths:** [What is working — preserve this]

**Abstraction Instances:**
- [Quoted abstract statement → Grounded replacement]
- [Repeat]

**Verb Replacements:**
- [Quoted sentence with weak verb → Rewritten with precise verb]
- [Repeat]

**Sensory Additions:**
- [Location / description of absent sense / Specific suggested detail + why it serves the scene]
- [Repeat]

**Single Main Weakness:** [The prose's primary elevation opportunity in one sentence]

**Rewritten Sample Passage:** [A passage from the submitted text, rewritten applying all three categories of changes — at least one paragraph, showing the cumulative elevation effect]

---

## Notes

- Prose elevation is not the same as rewriting. The goal is to realise the prose's potential, not replace it. A rewritten passage that no longer sounds like the writer has failed.
- Elevation should happen after line editing: a clean, tight passage elevated to a higher quality is the goal. An elevated but verbose passage is worse than where it started.
- The hardest part of abstraction replacement: finding the specific image that captures the abstract truth exactly — neither overstating nor understating it. "She felt alone" is abstract; "no one texted back" is specific; "she checked her phone and put it face-down on the table" is specific and also says something about the character.
- Pairs with `/s4h-writing-line-editing` — these two tools work in sequence. Line editing first (remove problems), then prose elevation (raise quality).
- Pairs with `/s4h-writing-voice-consistency` — elevation must stay in the voice. If the elevated passages sound like a different writer, the elevation has overshot.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Prose elevated. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-voice-consistency` — Check voice after elevation
  - `/s4h-writing-line-editing` — Refine the elevated prose further
  - `/s4h-aesthetic-elegance-testing` — Test the elegance of the elevated prose
  - **Done** — Wrap up and synthesise what we have so far
