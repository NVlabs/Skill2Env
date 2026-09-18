---
name: s4h-sensory
description: "Entry point for the sensory observation toolkit. Routes to the right observational skill based on your situation. Use when you say 'sensory', 'what are we missing', 'look more carefully', 'separate signal from noise', 'too much information', 'what actually matters here', 'observe this carefully', or want observational precision applied without knowing which specific tool fits."
---

# Sensory

Applies disciplined observation and attention to any situation. Diagnoses what kind of observational work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Find specific details that are being overlooked | detail-mining |
| Separate what actually matters from background noise | signal-detection |
| Apply disciplined observation before interpreting | structured-observation |

## Routing Decision

- **Have a situation and suspect important details are being missed** → detail-mining
- **Overwhelmed with information and need to find what matters** → signal-detection
- **Rushing to interpret before fully observing** → structured-observation
- **Unclear** → structured-observation first; disciplined observation before mining or filtering

---

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

## Detail Mining

*Finds specific details being overlooked.*

Slow down. The most important information is often present but not being registered. Go back to primary sources — the actual data, the actual words, the actual behavior. For each element: what specific, concrete, observable detail is present? What exactly is being said, not what it means? Generate a dense inventory of specifics before drawing conclusions. Vague observations produce vague conclusions.

**Output:** Dense inventory of specific, concrete details. The details most likely to be overlooked and their implications.

---

## Signal Detection

*Separates meaningful signal from background noise.*

Not all information is equally relevant. Classify each piece of information: (1) Strong signal — directly relevant to the question, (2) Weak signal — potentially relevant, worth watching, (3) Noise — present but irrelevant. For each strong signal: what does it indicate? For each weak signal: what would make it stronger or weaker? The goal is attention management — what should be acted on, watched, and ignored.

**Output:** Signal/noise classification for all inputs. Strong signals and their implications. Weak signals to monitor.

---

## Structured Observation

*Applies disciplined observation by suspending interpretation.*

Most people observe and interpret simultaneously — which means interpretation shapes what they see. Suspend interpretation: for this exercise, describe only what you observe, not what it means. What is actually present? What is actually happening? What are the exact words, behaviors, or outputs? After observation is complete, interpretation can begin — but it starts from a richer, more accurate base.

**Output:** Pure observation record (no interpretation). Then: interpretation layer applied to the observation record, now clearly separated from what was actually seen.
