---
name: s4h-network-contagion
description: "Models how things spread through networks — ideas, behaviors, viruses, product adoption, financial contagion, cascading failures. Use when asked 'why did this go viral', 'why isn't this spreading', 'how do we accelerate adoption', 'what's the tipping point', 'could this cascade', or when modeling any spread or diffusion process through a connected system."
---

# Network: Contagion

The intuitive explanation for why something spreads is usually wrong. We attribute viral spread to exceptional content, charismatic spreaders, or luck. Duncan Watts' research on complex contagion demolished this story: large cascades are not caused by extraordinary seed nodes. They are caused by a network that is structurally ready to propagate — a susceptible population in the right configuration. The seed is almost irrelevant; the structure is everything.

Two distinct contagion mechanisms operate differently and require different interventions. Simple contagion (like a biological virus) spreads on single exposure — one infected contact is enough to infect you. Complex contagion (like a social norm, a behavior change, or a product that requires social proof) requires multiple exposures from different parts of your network before you adopt. Simple contagion spreads fast through hubs; complex contagion requires local density and reinforcement. Most real-world spread processes — technology adoption, organizational change, political movements — are complex contagion, not simple.

The foundational framework is the SIR model (Susceptible, Infected, Recovered), extended through threshold models and network topology. The reproduction number R₀ — how many nodes each infectious node infects — determines whether spread occurs at all. But R₀ varies with network structure: the same pathogen spreads very differently through a random network versus a scale-free network versus a clustered community network.

---

## Your Process

**Step 1: Define What Is Spreading and What Is the Network**
Name the contagion (what is spreading) and the network (what nodes, what edges). Is this simple or complex contagion? Simple: one exposure is enough. Complex: requires social proof, multiple exposures, or threshold crossing. Name the current state: what fraction of nodes are currently infected/adopted?

**Framing check:** Confirm the contagion type and the question before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence description of what's spreading, through what network, and whether this is simple or complex contagion]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Estimate the Reproduction Number (R₀)**
For each currently infected/adopting node: on average, how many others does it infect or influence toward adoption? If R₀ > 1, spread accelerates. If R₀ < 1, spread dies out. If R₀ ≈ 1, spread is endemic but not explosive. Note that R₀ is not fixed — it changes as the pool of susceptibles depletes, as behavior changes, and as the network structure shifts.

**Step 3: Map the Threshold Structure**
For complex contagion: what fraction of a node's neighbours must have adopted before that node adopts? Threshold distributions matter enormously. A population with heterogeneous thresholds (most need 10% but a few need only 5%) can cascade from a small seed to near-total adoption. A population with uniformly high thresholds (everyone needs 40%) will never cascade regardless of seed size. Identify: are there threshold concentrations that, once breached, unlock the next wave?

**Step 4: Identify Structural Bottlenecks and Bridges**
Where does spread currently stall? Network clusters that are internally well-connected but weakly bridged to other clusters create firebreaks for spread. Identify: which bridges are currently carrying spread between clusters, and which structural holes are preventing spread from reaching certain populations? For complex contagion specifically: find the dense subgraphs where local reinforcement can accumulate until the threshold is crossed for bridge nodes.

**Before narrowing:** Show the full spread map before recommending interventions. Use `AskUserQuestion`:
- **Question:** "I've mapped the spread dynamic with [R₀ estimate] and identified [N] key bottlenecks or bridges. Before I recommend interventions, are you primarily trying to accelerate spread, contain it, or understand why it has or hasn't spread?"
- **Header:** "Goal"
- **Options:**
  - **Accelerate spread** — identify seed points, bridge targets, and threshold-crossing strategies
  - **Contain or slow spread** — identify cut points, firebreaks, and quarantine strategies
  - **Diagnose why it stopped** — understand the structural barriers and threshold failures
  - **Model both directions** — show both the spread path and the containment options

**Step 5: Model the Cascade**
Trace the likely spread path given current R₀, threshold structure, and network topology. Identify: the tipping point (at what adoption rate does spread become self-sustaining?), the saturation ceiling (what fraction of nodes is structurally reachable?), the speed (how many time steps to reach X% adoption?), and the dead zones (which clusters or nodes are structurally isolated from the contagion?).

**Step 6: Design Interventions**
For acceleration: seed high-closeness nodes for simple contagion; seed dense clusters for complex contagion. For containment: remove high-betweenness bridges; reduce transmission probability through the critical path. For threshold-breaking: cluster early adopters in the same neighborhood to create local reinforcement density before bridging out.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the contagion, the network, and the goal in 1–2 sentences, then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete spread model with R₀, threshold analysis, cascade trace, and interventions
  - **Key findings only** — Will this spread? Where will it stall? What is the highest-leverage intervention?
  - **Specific focus** — Zoom in on one aspect: seed strategy, bottlenecks, threshold analysis, or containment
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Spread Definition**
[What is spreading, through what network, simple or complex contagion]

**Current State**
[Estimated adoption/infection rate, seed nodes, active spreading edges]

**Reproduction Number (R₀)**
[Estimate with reasoning. Trajectory: accelerating / stable / dying out]

**Threshold Analysis** *(for complex contagion)*
[Distribution of adoption thresholds; where critical mass concentrations exist]

**Cascade Map**

| Stage | Trigger Condition | Expected Reach | Key Nodes / Bridges |
|-------|------------------|---------------|---------------------|
| | | | |

**Tipping Point**
[The adoption rate at which spread becomes self-sustaining — and how far away it currently is]

**Structural Bottlenecks**
[Where spread stalls and why — structural holes, threshold barriers, isolated clusters]

**Interventions**
[Ranked by leverage — seed strategy, bridge targeting, threshold reduction, or containment]

---

## Notes

The most common contagion error is treating complex contagion as simple contagion and targeting hubs. For behavior change, product adoption, and social norms — all complex contagion — targeting the most connected node rarely works. The node's many weak ties mean it sees the innovation from many independent directions simultaneously, diluting the social proof signal. Better targets are dense clusters where local reinforcement can accumulate. Pair with `/s4h-network-weak-ties` to understand the bridges that must be crossed for spread to jump between clusters. Pair with `/s4h-systems-feedback-mapping` when the spread process has feedback loops (adoption breeds more adoption, resistance breeds more resistance).

For organizational change initiatives specifically: the spread problem is almost always complex contagion. People need to see multiple trusted peers adopt before they will. The intervention implication is to seed the change in a dense, visible sub-cluster — not to announce it to the whole network at once.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Contagion model built. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-network-centrality` — Identify the specific high-value nodes to target as seeds or cut points
  - `/s4h-network-weak-ties` — Map the structural bridges that spread must cross to reach new clusters
  - `/s4h-systems-feedback-mapping` — Model the feedback loops that amplify or dampen spread over time
  - **Done** — Wrap up and synthesise what we have so far
