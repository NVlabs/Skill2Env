---
name: s4h-systems-emergence-detection
description: "Identifies system-level properties that exist nowhere in any individual component. Use when asked about 'emergent behavior', 'components are fine but the system isn't', 'why does the whole behave like this', or 'what creates this property'."
---

# Systems Emergence Detection

Emergent properties are the most important features of complex systems and the least designed for. They arise from interactions between components, not from the components themselves — which is why fixing individual parts often fails to fix system-level problems. Identifying emergence requires asking not what each component does, but what arises when they interact.

---

## Your Process

**Step 1: State the System-Level Property**
Name the property to explain or design for. Be precise: "the platform feels trustworthy", "the team produces poor decisions", "the market self-corrects". Vague properties produce vague analysis.

**Framing check:** Confirm the specific system and emergent property before continuing. State what you've identified — the actual system being analyzed and the property you are tracing — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system and the emergent property in focus]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: List Components**
Enumerate the system's components — people, subsystems, rules, technologies, incentives. These are the parts whose interactions you will examine.

**Step 3: Test Each Component**
For each component: does the property exist in it alone? If trust cannot exist in a single user, the property is emergent. This step confirms emergence and rules out simple aggregation.

**Step 4: Trace the Producing Interactions**
Identify the specific interactions between components that generate the property. Show the full set of candidate interactions before narrowing.

**Before narrowing:** Show the complete set of interactions identified to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] candidate interactions. Before I select the ones most necessary and sufficient for producing the property, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific interaction to include
  - **Add a missing one** — user will describe it

Not all interactions contribute equally — find the ones that are necessary and sufficient.

**Step 5: Assess Desirability**
Is this emergent property desirable? If yes: which interactions need protection from being disrupted? If no: which specific interactions need changing — not which components need replacing.

**Step 6: Identify Intervention Points**
If the emergence is undesirable, locate where in the interaction chain the property can be interrupted or redirected with minimum disruption to desirable emergent properties.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Emergence sources only** — Where unexpected behavior is coming from, skip implications
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**System-Level Property:** [precise statement]

**Emergence Table**

| Property | Present in Components Alone? | Producing Interactions | Desirable? |
|----------|------------------------------|----------------------|-----------|
| | | | |

**Key Producing Interactions:** [the 2–3 interactions most responsible for the property]

**Intervention Points (if undesirable):** [where to change interactions, not components]

---

## Notes

Removing a component to fix an emergent property rarely works — the interaction pattern will reproduce the property with whatever components remain. Target the interaction, not the part.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Emergent properties detected. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-systems-leverage-analysis` — Find leverage in the emergent properties
  - `/s4h-systems-feedback-mapping` — Map feedback loops creating the emergence
  - `/s4h-strategy-positioning` — Position relative to the emergent dynamics
  - **Done** — Wrap up and synthesise what we have so far
