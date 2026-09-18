---
name: s4h-writing-dialogue
description: "Diagnoses and repairs dialogue for subtext, voice differentiation, exposition, and forward momentum. Use when dialogue sounds wrong, on-the-nose, or when characters all sound the same. Triggers: 'the dialogue sounds wrong', 'dialogue feels on the nose', 'dialogue review', 'characters sound the same', 'dialogue fix', 'dialogue is too direct', 'the dialogue explains too much'."
---

# Writing: Dialogue

Dialogue fails in two primary ways: it says exactly what it means (no subtext), or it explains things the characters already know (exposition dressed as conversation). Both failures produce the same effect on the reader — a sense of flatness, of the author's hand visible, of characters becoming mouthpieces rather than people.

Real conversation is oblique. People in conflict rarely say "I'm angry with you." They talk about something else. The anger is present in what they say about the dishes, the schedule, the way someone looks. The subtext *is* the scene — the surface conversation is the vehicle for it. When dialogue is on the nose, the subtext and the surface are the same thing, which means there is no scene — only information delivery.

Voice differentiation is the second major failure point. Every character has a distinct rhythm of thought, a vocabulary range shaped by their history, evasion patterns specific to their wound, and a relationship to silence. When characters sound interchangeable, the dialogue's only differentiator is the attribution ("he said / she said") — which means the characters, on the page, don't exist yet.

---

## Your Process

**Step 1: Speaker Goals — Surface vs. Subtext**
For each speaker in the exchange, identify:

**Framing check:** Confirm the specific dialogue before continuing. State what you've identified — the exchange being analysed, the speakers involved, and the apparent dramatic situation — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the dialogue, its speakers, and the situation it takes place in]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding
- **Surface goal:** What they appear to be talking about
- **Subtext goal:** What they actually want from this exchange (what they won't say directly)

These should be different. If surface goal and subtext goal are identical, the speaker is saying exactly what they mean — the subtext has collapsed into the text, and the scene has lost its tension.

**Step 2: Voice Differentiation**
Analyse each speaker's distinct voice characteristics:
- **Rhythm:** Long periodic sentences or short declarative ones? Interrupted speech or complete thoughts?
- **Vocabulary range:** Formal/educated diction, colloquial speech, domain-specific language?
- **Evasion pattern:** How does this character deflect, dodge, or redirect when pressed?
- **Relationship to silence:** Does this character fill silences, create them, use them as weapons?

If the voices are interchangeable — if you could swap the speakers' lines without the scene changing — the characters have not yet been individualised.

**Step 3: Exposition Check**
Flag any lines where characters explain things they both already know, solely for the reader's benefit. This is the "As you know, Bob" problem: "As you know, we've been married for fifteen years and your father never approved of me." Neither character needs to be told this. It's only there for the reader — and the reader knows it.

Exposition that is genuinely needed can be delivered through conflict (characters who have different versions of the same event), curiosity (a character who genuinely doesn't know something), or revelation (information emerging under pressure, not volunteered).

**Step 4: Scene Function**
What is the dialogue doing? Mark all that apply:
- **Conflict:** Two opposing wants in direct tension
- **Revelation:** Something new emerges for a character or reader
- **Bonding:** Intimacy or connection established or tested
- **Negotiation:** Characters working toward an arrangement
- **Deflection:** A character managing a threat through misdirection

If the dialogue serves no discernible function — if it is simply exchange — it should be cut or redirected.

**Step 5: Forward Momentum**
Does the dialogue advance the scene, or does it stall it? Diagnose the rate at which the scene's situation changes through the dialogue. If the first and last lines of the dialogue exchange are in the same state as each other, the dialogue is stalling.

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

### Dialogue Analysis

**Speaker Goals:**
- [Speaker A]: Surface goal / Subtext goal
- [Speaker B]: Surface goal / Subtext goal
- FLAGGED: [any speaker whose surface and subtext goals are identical]

**Voice Differentiation:**
- [Speaker A]: Rhythm / Vocabulary / Evasion pattern / Silence relationship
- [Speaker B]: Same
- FLAGGED: [any voices that are interchangeable]

**Exposition Flags:** [Quoted lines + why they're exposition + how to deliver the information legitimately]

**Scene Function:** [Conflict / Revelation / Bonding / Negotiation / Deflection — mark all present / FLAG if none]

**Forward Momentum:** [Does the scene advance through dialogue? Where does it stall?]

**Line-by-Line Notes:** [Specific notes on strongest exchanges and weakest — quote and diagnose]

**Rewrites for Flagged Lines:** [Specific rewrites that restore subtext, differentiate voice, or remove exposition]

---

## Notes

- Subtext does not mean obscure. The reader should be able to feel what's underneath even if the characters don't say it. Clarity and subtext are not in tension.
- The best dialogue rewrites keep the surface plausible while loading the subtext — the characters are still talking about something real, but the real thing is not what they say.
- Pairs with `/s4h-writing-scene-construction` for diagnosing the dialogue within its scene context — dialogue problems are often scene-construction problems.
- Pairs with `/s4h-writing-character-development` because voice flows from character: the wound and defence determine how a character speaks, evades, and what they're incapable of saying directly.
- Pairs with `/s4h-writing-voice-consistency` when the issue is that a character's voice is inconsistent across the manuscript rather than within a single scene.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Dialogue written. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-voice-consistency` — Ensure dialogue is voice-consistent throughout
  - `/s4h-writing-character-development` — Use dialogue to deepen character
  - `/s4h-writing-scene-construction` — Embed the dialogue in its scene
  - **Done** — Wrap up and synthesise what we have so far
