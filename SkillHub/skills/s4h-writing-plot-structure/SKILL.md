---
name: s4h-writing-plot-structure
description: "Diagnoses structural failures in a story using the five-beat dramatic framework — inciting incident, first turning point, midpoint, dark night, climax. Use when a plot isn't working, the middle drags, momentum is lost, or the story feels loose. Triggers: 'the story isn't working', 'plot structure', 'my middle drags', 'the plot feels loose', 'story structure', 'momentum problem', 'the structure is off'."
---

# Writing: Plot Structure

Most plot problems are structural. When readers say "it loses momentum," "the middle drags," or "the ending felt rushed," they are usually reporting structural failures, not prose failures. The sentences may be excellent. The problem is in the architecture.

The five-beat structure is not a formula — it is a description of how dramatic tension works. Each beat is defined by what it does to the story's central question, not by where it falls in the word count. A thriller and a literary novel obey the same structural logic: the reader holds a question, the beats escalate the stakes of that question, and the climax answers it. The internal and external arcs must mirror each other: the external plot generates the conditions that force the internal change.

The most common structural failures: a missing first turning point (so the protagonist never truly commits, meaning there are no real stakes); a flat midpoint (so the story runs in a straight line rather than shifting direction); and a dark night that is too short (so the climax feels unearned).

---

## Your Process

**Step 1: Inciting Incident**
What disrupts the equilibrium? Identify the event that breaks the story's opening state and raises the central question. Diagnostic: does this event happen *to* the protagonist, or merely *near* them? An inciting incident that the protagonist can ignore is not functioning — it must demand response. Does it raise a specific, answerable question that will carry the story?

**Framing check:** Confirm the specific story and its structural situation before continuing. State what you've identified — the title or subject of the work, its genre, and the structural symptom the user is reporting — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the story, its genre, and the structural problem being diagnosed]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: First Turning Point**
Where does the protagonist commit to the central struggle? This is the point of no return — after this, they cannot go back to the opening state even if they wanted to. It is often marked by an active choice, not just an event that happens to them. Diagnostic: is there a real cost to this commitment? If there's no cost, there are no stakes.

**Step 3: Midpoint**
False victory or false defeat — identify it. The midpoint should shift the story's direction: if the first half was a rising pursuit, the midpoint brings a reversal that changes what the story is really about. Diagnostic: does the story's central question *change shape* at the midpoint, or does the story simply continue? A midpoint that doesn't shift direction is doing nothing structural — it is merely an event.

**Step 4: Dark Night / Lowest Point**
The protagonist confronts the central struggle with everything they have and appears to lose. This is not a setback — it is the apparent defeat. Diagnostic: is the protagonist active here (trying and failing) or passive (simply having bad things happen to them)? Passive dark nights feel melodramatic rather than earned. Does this moment force the internal confrontation that the arc requires?

**Step 5: Climax and Resolution**
The internal change enabled by the dark night allows the external problem to resolve. The key diagnostic: does the climax require the protagonist's change, or could any competent person have resolved it? If the resolution doesn't require the protagonist's specific internal transformation, the plot and character arc are running on parallel tracks that never truly connect.

**For each beat:** Does it exist? Is it caused by the beat before it (cause-and-effect chain)? Does it raise the stakes rather than maintain them?

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

### Structural Map

**Inciting Incident:** [Event + central question it raises / diagnosis of whether it is functioning]

**First Turning Point:** [Commitment moment + stakes diagnosis / missing or weak?]

**Midpoint:** [False victory or false defeat + direction shift / diagnosis]

**Dark Night:** [Apparent defeat + active vs. passive diagnosis / earned or melodramatic?]

**Climax and Resolution:** [How internal change enables external resolution / does the plot require this specific character?]

**Cause-and-Effect Chain:** [Does each beat cause the next? Gaps or breaks identified]

**Diagnosis:** [Primary structural problem(s) — which beats are missing, weak, or disconnected]

**Recommended Fixes:** [Specific interventions for each problem beat]

---

## Notes

- Structural problems cannot be fixed at the prose level. If a beat is missing or broken, adding better sentences will not repair it.
- A common false fix: adding subplots to fill structural gaps. Subplots that don't connect to the central question create weight without tension.
- Pairs with `/s4h-writing-arc-design` — the internal arc must mirror the external structure; structural diagnosis and arc design must happen together for the fix to hold.
- Pairs with `/s4h-writing-restructure` when the beats exist but are in the wrong sequence or proportion — restructure addresses arrangement, not the beats themselves.
- Pairs with `/s4h-writing-scene-construction` when the structural beats are present but individual scenes within them are not delivering what the structure requires.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Plot structured. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-arc-design` — Design the arc within the plot structure
  - `/s4h-writing-character-development` — Develop characters in service of the plot
  - `/s4h-narrative-tension-mapping` — Map tension across the plot structure
  - **Done** — Wrap up and synthesise what we have so far
