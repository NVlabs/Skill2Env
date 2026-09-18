---
name: s4h-sensory-detail-mining
description: "Finds specific details being overlooked — the most important information is often present but not being registered. Triggers: 'what are we missing', 'go deeper on this', 'find the details', 'be more specific', 'what exactly is happening', 'ground this in specifics'."
---

# Detail Mining

Abstractions are useful — but they lose the specific detail that often contains the real insight. "Users are frustrated" is an abstraction that conceals which users, in which moment, doing what, saying what exactly. Detail mining forces that concealment back into the open.

---

## Your Process

**Step 1: Take the Current Description**
Work with whatever account, analysis, or summary exists. This is the starting material — it contains the abstractions to excavate.

**Framing check:** Confirm the specific subject before continuing. State what you've identified — the actual material being excavated and what kind of abstraction it primarily deals in — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific content — e.g. 'a session-recording summary describing user behaviour at a checkout flow']. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify Where It's Abstract**
Mark every place the description uses categories, summaries, or generalisations instead of specific observed instances. Words like "often," "users," "usually," "issues," "problems," and "feedback" are abstraction signals.

**Step 3: Force Specificity on Each Abstraction**
For each abstraction: what are the actual, specific instances behind it? Name them. Quote them if possible. Specify who, when, what exactly.
- Instead of: "Users are frustrated."
- Write: "3 users in session recordings said 'I don't understand this button' and clicked it twice before abandoning the flow."

**Step 4: Recover Ignored Background Details**
What is present in the situation but not described — treated as taken-for-granted background? List these. They are often invisible because everyone assumes they are known.

**Step 5: Surface Absences as Details**
What should be there but isn't? Absence is a detail. A missing response, a skipped step, a field left blank — these are observations, not gaps in data.

**Step 6: Read What the Specifics Reveal**
Now that you have the specifics: what do they show that the abstractions concealed? What changes about your understanding?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **One overlooked detail** — The single most important thing being missed
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Abstractions Identified
| Abstraction | Specific Instances Behind It |
|-------------|------------------------------|
| "users are frustrated" | [exact quote / behaviour / timestamp] |
| ... | ... |

### Ignored Background Details
- [Detail treated as given, not described]

### Notable Absences
- [What should be present but isn't]

### What the Specifics Reveal
Paragraph summary: how does the specific picture differ from the abstract one? What new questions or insights emerge?

---

## Notes

This skill is most useful immediately before a decision, a diagnosis, or a design choice — the moment when abstractions are about to drive action. Getting specific at that point can prevent expensive errors.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Details mined. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-sensory-signal-detection` — Detect signals in the mined details
  - `/s4h-writing-scene-construction` — Use the mined details in scene construction
  - `/s4h-aesthetic-pattern-detection` — Detect aesthetic patterns in the details
  - **Done** — Wrap up and synthesise what we have so far
