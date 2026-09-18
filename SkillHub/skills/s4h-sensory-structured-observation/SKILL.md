---
name: s4h-sensory-structured-observation
description: "Applies disciplined observation to a situation — suspending interpretation to see what's actually there before deciding what it means. Triggers: 'observe this carefully', 'structured observation', 'what do you actually see', 'suspend interpretation', 'look more carefully'."
---

# Structured Observation

Most observation is interpretation in disguise. We perceive a situation and instantly explain it — but the explanation overwrites the raw data. Structured observation forces a separation between what can be directly seen and what we conclude from it.

---

## Your Process

**Step 1: Define the Target and Time Boundary**
Name the exact thing being observed and the scope. What counts as inside this observation, and what is out of scope?

**Framing check:** Confirm the specific subject before continuing. State what you've identified — the actual object being observed and its boundaries — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific subject and scope]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Separate Observation from Interpretation**
Write only what can be directly observed — no inferences, no attributions of intent or cause. "User clicked back immediately" not "user was confused." Flag every sentence that is actually an inference and set it aside.

**Step 3: Observe at Three Levels**
- **Events** — what is happening? Discrete, specific occurrences.
- **Patterns** — how is it happening? Recurring structure across events.
- **Absences** — what is not happening that might be expected?

**Step 4: Flag Surprising or Incongruent Observations**
What doesn't fit? Where does something contradict expectations?

**Before narrowing:** Show the complete set of observations from Steps 2–3 to the user first. Use `AskUserQuestion`:
- **Question:** "I've catalogued [N] observations across events, patterns, and absences. Before I select the most surprising or incongruent, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific observation to include
  - **Add a missing one** — user will describe it

These are the most information-rich observations — prioritise them.

**Step 5: Generate Interpretations**
Only after completing Steps 2–4: generate multiple possible interpretations for each key observation. Aim for at least two competing explanations.

**Step 6: Identify the Most Testable Interpretation**
Which interpretation makes the most specific, falsifiable prediction? That is the one to act on first.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Initial observations only** — What's actually there before any interpretation is applied
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Observations
| Level | Observation (no interpretation) |
|-------|----------------------------------|
| Event | ... |
| Pattern | ... |
| Absence | ... |

### Surprising or Incongruent Observations
- List each, with a note on why it is surprising.

### Interpretations per Key Observation
| Observation | Interpretation A | Interpretation B |
|-------------|-----------------|-----------------|
| ... | ... | ... |

### Most Testable Interpretation
State it as a prediction: "If [interpretation] is correct, then [specific observable consequence]."

---

## Notes

Run this before diagnosis, analysis, or decision. The discipline has most value when you feel you already understand the situation — that feeling is usually a sign that interpretation has already overtaken observation.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Observation complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-sensory-detail-mining` — Mine details from what structured observation revealed
  - `/s4h-sensory-signal-detection` — Detect signals in the observed
  - `/s4h-aesthetic-coherence-check` — Check coherence of what was observed
  - **Done** — Wrap up and synthesise what we have so far
