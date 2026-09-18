---
name: s4h-ecology-interdependence
description: "Maps dependency webs and the cascading effects of removing or changing a node in the web. Use when asked 'who depends on whom', 'what cascades if we change X', 'downstream effects', 'what holds this together', 'ripple effects', or 'what breaks if we remove this'."
---

# Ecology: Interdependence

Systems are not collections of independent parts. They are webs of mutual dependency — some tight, some loose, some visible, many invisible until they are broken. The ecologist Joseph Connell's foundational work on community ecology demonstrated that interactions between species — competition, predation, mutualism, commensalism — shape community structure as powerfully as the individual traits of each species. You cannot understand a system by studying its components in isolation; you understand it through its relationships.

The same principle governs organisations, supply chains, technology stacks, and social ecosystems. A team's performance is a function not just of individual capability but of the dependency structure between people. A product's reliability is determined not just by its architecture but by the dependency web between components, teams, vendors, and infrastructure. When you change a node in such a web — add it, remove it, degrade it, accelerate it — effects propagate. Sometimes the propagation is local and contained. Sometimes it reaches parts of the system that seem entirely unrelated to the original change.

Interdependence analysis makes the invisible web visible. It maps who relies on whom, distinguishes tight dependencies (cascades propagate fast and fully) from loose ones (dampened or delayed effects), identifies the structural bottlenecks, and traces what happens in the system when something changes. The goal is not to eliminate dependency — which is usually impossible and often counterproductive, since tight interdependence is also a source of coordination strength — but to understand the web well enough to anticipate what will happen and to act with awareness of the propagation paths.

---

## Your Process

**Step 1: Define the System and the Change Event**
Name the system being mapped and, if there is a specific change being considered or that has already happened, name it. If this is a general mapping exercise (no specific change in focus), note that too — the map will be built to reveal structural features rather than to model a specific event.

**Framing check:** Confirm the system and the question driving the analysis before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system and what's being asked — general mapping or specific change modelling]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Enumerate the Nodes**
List the distinct entities (people, roles, teams, systems, vendors, resources, institutions) that operate in this system. Aim for completeness at this stage — it is easier to prune than to recover a missing node later. Group related nodes into clusters if the system is large.

**Step 3: Map the Dependencies**
For each pair of nodes where a dependency exists, characterise it:
- **Direction** — A depends on B, B depends on A, or mutual (bidirectional)
- **Type** — resource dependency (A needs B's output), information dependency (A needs B's knowledge), trust dependency (A's users accept A only because B endorses or underpins it), infrastructure dependency (A operates on B's platform)
- **Tightness** — tight (failure in B immediately degrades A) or loose (B's degradation takes time to affect A, or has a buffer)
- **Substitutability** — if B were removed, could A find an equivalent? How quickly?

**Before narrowing:** Show the dependency inventory to the user. Use `AskUserQuestion`:
- **Question:** "I've mapped [N] dependencies. Before I analyse which are structurally critical, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Dependencies"
- **Options:**
  - **Proceed with your selection** — the map looks right
  - **Flag one** — user will name a specific dependency to highlight
  - **Add a missing one** — user will describe it

**Step 4: Identify Structural Features**
From the dependency map, identify:
- **Hubs** — nodes with many dependencies flowing through them; potential bottlenecks and keystones
- **Bridges** — single connections between otherwise disconnected clusters; removing a bridge splits the system
- **Cycles** — mutual dependencies that create tight coupling and propagation loops
- **Orphans** — nodes with few connections; potentially underutilised or structurally redundant

**Step 5: Trace Cascade Pathways**
For the change event specified in Step 1 (or for the top-two most structurally interesting changes if doing general mapping): trace the cascade. First-order effects: what is directly affected? Second-order: what does the first-order wave affect? Third-order: where does it reach? Note where tight dependencies amplify propagation and where loose dependencies or redundancy absorbs it.

**Step 6: Assess Resilience and Brittleness**
Which parts of the system are resilient — capable of absorbing disruption without propagating it? Which are brittle — where a single failure propagates broadly? Map the ratio of tight to loose dependencies: heavily tight-coupled systems are efficient in stable conditions but fragile under disturbance.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what system is being mapped and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Cascade focus** — Trace what propagates from the specified change, skip structural feature mapping
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**System:** [name and scope]

**Dependency Map**

| Dependency | Direction | Type | Tightness | Substitutability |
|------------|-----------|------|-----------|-----------------|
| | | | | |

**Structural Features**
- **Hubs:** [nodes with high dependency concentration]
- **Bridges:** [single-connection links between clusters]
- **Cycles:** [mutual dependency loops]
- **Orphans:** [low-connectivity nodes]

**Cascade Analysis** (for specified change or top structural scenarios)

| Stage | Affected Nodes | Mechanism | Lag | Amplified or Absorbed? |
|-------|---------------|-----------|-----|------------------------|
| First-order | | | | |
| Second-order | | | | |
| Third-order | | | | |

**Resilience Assessment:** [where the system absorbs disruption — and where it propagates]

**Critical Vulnerabilities:** [the highest-risk structural features with recommended actions]

---

## Notes

Interdependence analysis is the foundational map that other ecology tools build on. Before running `/s4h-ecology-keystone-species`, it helps to have the dependency web — keystones show up as the hubs and bridges in the map. Before running `/s4h-ecology-succession`, the interdependence map reveals which relationships are stable across stages and which are disrupted by transitions.

The nearest neighbor is `/s4h-systems-feedback-mapping` — feedback loops are a special class of interdependency (circular, time-delayed, amplifying or dampening). If the core question is about why the system keeps producing a particular behavior over time, `/s4h-systems-feedback-mapping` is the right entry point. If the core question is about structural dependency and what propagates when something changes, interdependence analysis is the right tool.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Dependency web mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-ecology-keystone-species` — Identify which nodes in the dependency web are structurally irreplaceable
  - `/s4h-ecology-carrying-capacity` — Assess whether the system's dependency structure is sustainable at current load
  - `/s4h-systems-feedback-mapping` — Map the reinforcing and balancing loops embedded in the dependency web
  - **Done** — Wrap up and synthesise what we have so far
