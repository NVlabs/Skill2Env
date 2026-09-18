---
name: s4h-sensory-signal-detection
description: "Separates meaningful signal from background noise — finding what actually matters among everything present. Triggers: 'what actually matters here', 'separate signal from noise', 'too much information', 'find the signal', 'what should I focus on', 'what's relevant'."
---

# Signal Detection

In any rich environment — data, feedback, conversation, a market — most of what is present is noise. Signal is what varies with the thing you're trying to understand; noise varies independently. The challenge is not finding more information, it's knowing which information is doing real work.

---

## Your Process

**Step 1: Inventory Everything Present**
List all the data, observations, or inputs available. Don't filter yet — complete the inventory first.

**Framing check:** Confirm the specific subject before continuing. State what you've identified — the actual environment or dataset being analyzed and what outcome or phenomenon the user is trying to understand — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific environment/dataset and the outcome you're testing against]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Variance Test**
For each item: does it vary with the outcome or phenomenon you're trying to understand? Signal co-varies with what you care about. Noise varies on its own schedule.

**Step 3: Persistence Test**
Is this item consistently present across time and contexts, or did it appear once? Persistent patterns are more likely to be signal. One-off observations may be noise, anomaly, or coincidence.

**Step 4: Specificity Test**
Is this item unique to this situation, or is it always present? Always-present background conditions are usually noise. What is specific to the case is more likely signal.

**Step 5: Counterfactual Test**
If this item changed or disappeared, would the outcome change? If yes: probable signal. If the outcome would be the same regardless: probable noise.

**Step 6: Classify and Summarise**
Assign a classification to each item and present the full classified inventory to the user.

**Before narrowing:** Show the complete classified set to the user first. Use `AskUserQuestion`:
- **Question:** "I've classified [N] elements. Before I select the top signals to act on, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific element to include in the top signals
  - **Add a missing one** — user will describe an element not yet in the inventory

Then identify the top signals to act on.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Noise sources only** — What's obscuring the real signal
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Element Inventory and Classification
| Element | Varies with Outcome? | Persistent? | Specific? | Counterfactual? | Classification |
|---------|---------------------|-------------|-----------|-----------------|----------------|
| ... | ... | ... | ... | ... | Signal / Noise / Unclear |

**Classifications:** Clear Signal / Probable Signal / Unclear / Probable Noise / Clear Noise

### Top 3 Signals to Focus On
1. [Signal] — rationale for prioritisation.
2. [Signal] — rationale.
3. [Signal] — rationale.

### Notable Noise to Stop Tracking
- Elements consuming attention without signal value.

---

## Notes

When in doubt, classify as "unclear" rather than forcing a label — the act of flagging uncertainty is itself useful. Run this when a situation feels overwhelming or when a team is arguing about what matters.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Signals detected. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-sensory-structured-observation` — Observe in depth around the detected signals
  - `/s4h-aesthetic-pattern-detection` — Find patterns in the signals
  - `/s4h-systems-feedback-mapping` — Map feedback systems the signals reveal
  - **Done** — Wrap up and synthesise what we have so far
