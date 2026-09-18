---
name: s4h-ecology
description: "Entry point for the ecology thinking toolkit. Routes to the right ecology skill based on your situation. Use when you say 'ecology', 'carrying capacity', 'keystone', 'interdependence', 'succession', 'what holds this system together', 'who depends on whom', 'what happens if we remove X', or want ecological thinking applied without knowing which specific tool fits."
---

# Ecology

Applies ecological thinking to any system with interdependencies, limits, and change over time. Diagnoses what kind of ecological analysis is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Identify limits and what happens when they are exceeded | carrying-capacity |
| Find which entities hold the system together disproportionately | keystone-species |
| Map who depends on whom and what cascades when something changes | interdependence |
| Understand how a system evolves through stages over time | succession |

## Routing Decision

**Framing check:** Confirm the system and the ecological question in focus before routing. State what you've identified — the actual system being analysed and the dynamic at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system and the ecological dynamic in focus]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **System is approaching a ceiling or showing overshoot signs** → carrying-capacity
- **Need to identify critical, non-replaceable actors or nodes** → keystone-species
- **A change has happened or is planned and you need to trace the ripples** → interdependence
- **System is at a transition point or undergoing a phase shift** → succession
- **Unclear** → interdependence; mapping who depends on whom reveals limits, keystones, and developmental stage together

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

## Carrying Capacity

*Identifies the ceiling and what happens when the system crosses it.*

Every system has limits — not always visible, often crossed before they are named. Arthur Tansley's ecosystem concept and Howard Odum's energy flow work showed that populations, communities, and organisations grow until they hit structural constraints. Carrying capacity analysis maps that ceiling: what resources or conditions bound the system, which of them is tightest, how far from the limit the system currently sits, and what overshoot looks like. Applied to teams, markets, platforms, and communities, it surfaces the constraint before the crash.

**Output:** Ceiling identified, current load relative to the limit, overshoot risk assessment, and options for raising or respecting the carrying capacity.

---

## Keystone Species

*Identifies the entities whose removal would collapse the system.*

Robert Paine's 1966 sea star experiments showed that some species have effects wildly disproportionate to their biomass — remove them and the system restructures. Keystone species analysis finds those entities in any system: the people, platforms, institutions, or capabilities that hold structure in place and whose loss would trigger cascade. The question is not who contributes the most, but who is structurally irreplaceable.

**Output:** Keystones identified with evidence of structural disproportionality, collapse scenarios if removed, and substitutability assessment.

---

## Interdependence

*Maps dependency webs and the cascades that follow when a node changes.*

Complex systems are not collections of independent parts — they are webs of mutual dependency, often invisible until something breaks. Interdependence analysis traces who relies on whom, which dependencies are tight and which are loose, and what propagates through the web when any node is added, removed, or stressed. Joseph Connell's work on competition and facilitation shows that dependencies are not always harmful — mutualism and facilitation create structural strength. The map reveals both the brittleness and the resilience.

**Output:** Dependency map with directionality and tightness, cascade pathways, structural bottlenecks, and resilience assessment.

---

## Succession

*Applies ecological succession to understand how systems evolve through stages.*

Ecological communities don't stay static — they move through pioneer, consolidation, climax, and disturbance-reset stages. C.S. Holling's adaptive cycle formalised this into a four-phase model: rapid growth (r), conservation (K), release (Ω), and reorganisation (α). Each phase has different vulnerabilities and opportunities. Succession analysis identifies where a system sits in its cycle, what the next phase transition looks like, and how to read disturbances as reorganisation rather than failure.

**Output:** Stage identification, phase transition signals, vulnerability and opportunity assessment for current stage, and strategic posture for each scenario.
