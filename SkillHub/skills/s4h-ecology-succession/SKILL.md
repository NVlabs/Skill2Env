---
name: s4h-ecology-succession
description: "Applies ecological succession to understand how systems evolve through stages — pioneer, consolidation, climax, and disturbance. Use when asked 'what stage are we at', 'where are we in the cycle', 'what comes next', 'the old model isn't working anymore', 'we're in transition', or 'what does disruption mean for us'."
---

# Ecology: Succession

Ecological succession describes the predictable sequence by which communities change over time. A bare rock is colonised by pioneer species — fast-growing, opportunistic, tolerant of harsh conditions. They modify the environment, creating conditions for the next wave: consolidators that are slower-growing but more efficient, gradually outcompeting the pioneers. Over time, the community reaches a climax state — diverse, stable, highly interconnected, highly efficient in resource use, but also highly dependent on stability. Then disturbance arrives — fire, flood, predator collapse — and the cycle resets.

C.S. Holling formalised this into the adaptive cycle model, a framework that applies far beyond ecology. The four phases — rapid growth (r), conservation (K), release (Ω), and reorganisation (α) — describe the developmental trajectory of any complex adaptive system: ecosystems, organisations, industries, civilisations, technologies, and social movements. Each phase has its own logic, its own vulnerabilities, and its own strategic imperatives. Mistaking which phase you are in — or assuming the system is static when it is in transition — is one of the most common causes of strategic failure.

The adaptive cycle is not deterministic. Disturbance does not guarantee successful reorganisation. Systems can get stuck in the release phase (chronic crisis), fail to exit the reorganisation phase (perpetual restart), or be locked into the conservation phase by accumulated rigidity (unable to adapt until catastrophic release). Understanding which phase a system is in, and why, is the starting point for intelligent navigation of change.

---

## Your Process

**Step 1: Characterise the System**
Name the system being analysed, its current state, and the timeframe in view. Succession operates at different speeds in different systems — a product market might cycle in years, an ecosystem in decades, an organisation in quarters. Establish the relevant scale.

**Framing check:** Confirm the system and the succession question in focus before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system, its current state, and the timeframe]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Read the Phase Signals**
Apply the adaptive cycle diagnostic. Each phase has characteristic signals:

- **Rapid growth (r) — Pioneer phase:** Resources abundant relative to demand; fast growth rewarded; diversity of forms competing; experimentation cheap; little accumulated structure or overhead. Risk: growing into constraints that are not yet visible.

- **Conservation (K) — Climax phase:** Growth slowing; efficiency and specialisation premium; accumulated complexity and interconnection; high resource efficiency; high resilience to normal fluctuations. Risk: accumulated rigidity; loss of adaptability; high connectivity means disturbance propagates further.

- **Release (Ω) — Disturbance phase:** Accumulated structure breaks down; energy and resources stored in the previous phase are released; diversity of viable forms collapses; uncertainty and volatility high. Risk: catastrophic if release happens faster than actors can adapt; also risk of over-response (destroying viable structure in panic).

- **Reorganisation (α) — Pioneer phase restart:** Resources freed up; new forms competing for the available space; high experimentation; low overhead; tight new communities forming around new organising principles. Risk: premature consolidation around the wrong model; failure to fully release legacy constraints.

**Step 3: Identify Where in the Cycle the System Sits**
Map the phase signals against the system's actual current state. Note: systems can have sub-systems at different phases simultaneously (a mature organisation with a startup division; an industry undergoing disturbance with some incumbents still in K phase). Identify the dominant phase for the system as a whole, and flag sub-systems that are out of phase.

**Before narrowing:** Show the phase signal assessment to the user. Use `AskUserQuestion`:
- **Question:** "Based on the signals, I'm reading this as [phase] phase. Does that match your read of the current state?"
- **Header:** "Phase Check"
- **Options:**
  - **Yes — that's right** — proceed with this phase diagnosis
  - **Between phases** — system is transitioning; user will describe the transition
  - **Different read** — user will correct the phase assessment

**Step 4: Map the Next Transition**
What does the transition into the next phase look like? What signals would indicate it has begun? What are the trigger conditions — what accumulation, disturbance, or threshold-crossing would initiate the shift? Map two scenarios: managed transition (the system navigates the next phase shift with awareness) and unmanaged transition (the phase shift happens faster or more severely than anticipated).

**Step 5: Identify Phase-Appropriate Strategy**
Each phase requires a different strategic posture:

- **r phase:** Prioritise speed and experimentation; invest in options not optimisation; don't over-structure what doesn't need structure yet
- **K phase:** Invest in efficiency and depth; build resilience buffers; monitor for rigidity accumulation; prepare for inevitable release
- **Ω phase:** Protect the most valuable accumulated capital (knowledge, relationships, culture) while releasing the inefficient structure; avoid panic over-destruction; create space for reorganisation
- **α phase:** Invest in experimentation; resist premature convergence on new models; identify which elements from the previous cycle should carry forward

**Step 6: Assess Panarchy**
Holling's panarchy concept: systems are nested within larger systems, and succession at one scale is shaped by what is happening at adjacent scales. A team in reorganisation is operating within a division that may be in K phase; a startup in r phase is operating in an industry that may be in Ω. Identify the cross-scale interactions that constrain or enable the system's current trajectory.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — which phase the system appears to be in and what the strategic question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Next transition focus** — What the next phase shift looks like and how to navigate it
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**System:** [name and scope]

**Phase Diagnosis**

| Phase Signal | Present? | Evidence |
|--------------|----------|----------|
| Abundant resources / fast growth | | |
| Efficiency premium / specialisation | | |
| Accumulated rigidity / high interconnection | | |
| Breakdown of accumulated structure | | |
| Experimentation / new forms competing | | |

**Current Phase:** [r / K / Ω / α] — [one-sentence characterisation of what this means for the system right now]

**Sub-Systems Out of Phase:** [any parts of the system in a different phase from the whole]

**Next Transition**

| Scenario | Trigger Conditions | Timeline | First Signals | Strategic Implication |
|----------|-------------------|----------|--------------|----------------------|
| Managed | | | | |
| Unmanaged | | | | |

**Phase-Appropriate Strategic Posture:** [what the current phase requires and what it warns against]

**Panarchy Context:** [how adjacent-scale systems are shaping this system's trajectory]

---

## Notes

Succession analysis pairs naturally with `/s4h-temporal-futures-mapping` when the goal is to project forward through phase transitions, and with `/s4h-historical-cycle-detection` when the goal is to recognise that the current trajectory matches a known historical pattern. The distinction: succession maps the structural logic of the cycle; historical analysis names the precedent.

The nearest neighbor is `/s4h-systems-archetype-matching` — specifically the "Limits to Growth" archetype describes a system in K phase approaching its carrying capacity. If that is the precise dynamic, archetype matching provides a tighter structural model. Succession is the right tool when the question is about phase and trajectory, not about a specific dynamic within a phase.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Succession stage mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-ecology-carrying-capacity` — Assess the constraints that will shape or trigger the next phase transition
  - `/s4h-temporal-futures-mapping` — Project forward through multiple succession scenarios
  - `/s4h-historical-cycle-detection` — Find historical precedents for this succession pattern
  - **Done** — Wrap up and synthesise what we have so far
