---
name: s4h-systems
description: "Entry point for the systems thinking toolkit. Routes to the right systems skill based on your situation. Use when you say 'systems', 'feedback loops', 'how does this system work', 'where should we intervene', 'unexpected behavior', 'what archetype is this', 'find the leverage', or want systems thinking applied without knowing which specific tool fits."
---

# Systems

Applies systems thinking to complex, dynamic situations. Diagnoses what kind of systems analysis is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Recognize what recurring system pattern this is | archetype-matching |
| Understand unexpected or counterintuitive system behavior | emergence-detection |
| Map the feedback loops driving behavior | feedback-mapping |
| Find where small interventions produce large change | leverage-analysis |

## Routing Decision

**Framing check:** Confirm the system and the feedback relationship in focus before routing. State what you've identified — the actual system being analyzed and the behavior or dynamic at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system and the dynamic in focus]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Situation has a familiar-feeling dynamic — want to name the archetype** → archetype-matching
- **System is producing results no one intended or expected** → emergence-detection
- **Need to understand what's reinforcing the current behavior** → feedback-mapping
- **Need to know where to intervene for maximum effect** → leverage-analysis
- **Unclear** → feedback-mapping; mapping the loops reveals archetypes, emergence, and leverage points together

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

## Archetype Matching

*Identifies what recurring system pattern this is.*

Systems behave in recurring patterns. The common archetypes: Limits to Growth (growth stalls as it approaches an unseen constraint), Shifting the Burden (quick fixes address symptoms while the underlying problem grows), Fixes that Fail (interventions create delayed side effects that make things worse), Escalation (each side responds to the other's moves, spiraling), Tragedy of the Commons (individual rational behavior depletes a shared resource). Name the candidates. Test each against the current situation.

**Output:** Archetype identified with structural evidence, what the archetype predicts will happen next, and the leverage point specific to this archetype.

---

## Emergence Detection

*Understands unexpected behavior that no single part of the system intended.*

Emergent behavior arises from interactions, not components. When the system produces a result that surprises everyone: map the interactions that generate it. Which feedback loop is amplifying the behavior? Which constraint is the system bumping against? Emergence is often counterintuitive — pushing harder in the obvious direction makes things worse. Find the non-obvious intervention.

**Output:** The emergent behavior described structurally, the interactions generating it, why intuitive interventions fail, and the non-obvious leverage point.

---

## Feedback Mapping

*Maps the feedback loops driving behavior in a system.*

Identify reinforcing loops (R): A increases B, B increases A — creates exponential growth or collapse. Identify balancing loops (B): A increases, B responds to reduce A — creates stability or oscillation. For the current situation: which loops are active? Which are dominant? What is the time delay between cause and effect — where delays exist, oscillation is likely. The behavior of any system is the behavior of its feedback loops.

**Output:** Feedback map — reinforcing and balancing loops, dominant loops, time delays, and the behavior each loop generates.

---

## Leverage Analysis

*Finds where small interventions produce large, lasting change.*

Apply Donella Meadows' leverage point hierarchy. Low-leverage interventions: adjusting numbers, parameters, flow rates. Medium-leverage: changing feedback loop strength, information availability, rules. High-leverage: changing system goals, system structure, the paradigm the system operates within. Map current interventions by leverage level. Find the higher-leverage points being avoided — they're usually avoided for a reason (political resistance, long time horizon, requires belief change). That reason is worth examining.

**Output:** Intervention map by leverage level, identification of high-leverage points being avoided and why, and the most feasible high-leverage intervention.
