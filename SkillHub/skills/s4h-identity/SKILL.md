---
name: s4h-identity
description: "Entry point for the identity toolkit. Routes to the right identity skill based on your situation. Use when you say 'identity', 'who are we', 'values check', 'is this on mission', 'what do we actually stand for', 'gut check', 'are we drifting', or want identity/values reasoning applied without knowing which specific tool fits."
---

# Identity

Applies identity and values reasoning to decisions and directions. Diagnoses what kind of identity work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Ask what a person or organization of genuine integrity would do | character-testing |
| Test whether a decision is genuinely aligned with stated mission | mission-alignment |
| Surface the actual operative values revealed by decisions | values-clarification |

## Routing Decision

**Framing check:** Confirm the specific identity situation before routing. State what you've identified — the person or organization in question, the decision or situation triggering the identity question, and whether the concern is about integrity, mission drift, or revealed values — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the identity situation and what's at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Gut says something is wrong but can't articulate it** → character-testing
- **Worried a direction is drifting from core purpose** → mission-alignment
- **Want to know what your decisions actually reveal about your values** → values-clarification
- **Unclear** → values-clarification; understanding actual values informs both mission alignment and character testing

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

## Character Testing

*Asks what a person or organization of genuine integrity would do.*

Describe the decision or situation. Now ask: what would someone you deeply respect — someone with genuine integrity and good judgment — do here? Not someone who optimizes outcomes, but someone whose character is beyond question. Where does that answer differ from your current direction? The gap between "what I'm doing" and "what a person of integrity would do" is the information.

**Output:** The integrity-baseline answer, the gap from the current direction, and what specifically would need to change to close it.

---

## Mission Alignment

*Tests whether a proposed decision is genuinely aligned with stated mission.*

State the mission clearly. Now test the decision against it: (1) Does this serve the people/outcomes the mission is for? (2) Does this use the methods or principles the mission commits to? (3) Is the argument for doing this primarily mission-driven, or does it rationalize a departure for other reasons (revenue, convenience, opportunity)? Organizations drift from mission through a thousand individually defensible decisions.

**Output:** Mission statement tested against the decision. Alignment score. Whether the decision is genuinely on-mission, a legitimate expansion, or a rationalized departure.

---

## Values Clarification

*Surfaces the actual operative values revealed by decisions.*

Stated values are aspirational; operative values are revealed by decisions under pressure. Look at recent decisions — especially hard ones where something was sacrificed. What was traded? What was protected? What would never be compromised, and what has been compromised? The pattern reveals the actual hierarchy of values, which often differs from the posted list.

**Output:** Stated values vs. operative values comparison. The decisions that reveal the gap. The actual value hierarchy as demonstrated by behavior.
