---
name: s4h-network-centrality
description: "Identifies which nodes in a network have the most influence, reach, or control. Use when asked 'who are the key players', 'who should we target', 'where is the bottleneck', 'who connects everyone', 'who would we lose most if they left', or when mapping influence in an organisation, market, or social network."
---

# Network: Centrality

In almost every network — social, organizational, digital, biological — a small number of nodes exert disproportionate influence. They are not necessarily the most visible or the most senior. They are the most structurally positioned. Albert-László Barabási's research on scale-free networks established that real-world networks follow power-law degree distributions: a few hubs have vastly more connections than average, while most nodes have very few. These hubs emerge through preferential attachment — new nodes connect to already-well-connected nodes — which means structural inequality in networks is self-reinforcing.

Centrality analysis unpacks what "important" means in a specific network. There are four distinct types of centrality, and they identify different kinds of importance. A node can be a hub (high degree), a broker (high betweenness), an efficient spreader (high closeness), or influential because it is connected to other influential nodes (high eigenvector). These often coincide — but when they diverge, the divergence is analytically rich.

The key implication: targeting or protecting the most central nodes has outsized effect. Removing a high-betweenness broker can fragment a network; reaching a high-eigenvector hub can cascade influence throughout it.

---

## Your Process

**Step 1: Define the Network**
Name the nodes (what entities?) and the edges (what relationship?). Be precise about direction — is the relationship directional (A influences B but not vice versa) or undirected (mutual connection)? Name the time horizon and state what question you are trying to answer with centrality analysis.

**Framing check:** Confirm the network definition and the question before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence description of the nodes, the relationship, and the question to answer]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Enumerate the Nodes and Edges**
List all known nodes. For each pair, identify whether an edge exists and its weight or frequency if relevant. If working from description rather than data, reason from available information — who interacts with whom, who reports to whom, who collaborates, who is referenced.

**Step 3: Calculate Centrality by Type**

For each node, assess across four dimensions:

- **Degree centrality:** How many direct connections does this node have? (Raw count or normalised as a fraction of all possible connections.) High degree = a hub.
- **Betweenness centrality:** How often does this node sit on the shortest path between two other nodes? High betweenness = a broker or bottleneck — removing them disrupts information or resource flow.
- **Closeness centrality:** How short are this node's average distances to all other nodes? High closeness = fastest to reach everyone; efficient at spreading or receiving information.
- **Eigenvector / prestige centrality:** Is this node connected to other highly-connected nodes? High eigenvector = influence through association; the node's power is amplified by the power of its neighbours.

**Before narrowing:** Show the full centrality picture first. Use `AskUserQuestion`:
- **Question:** "I've mapped [N] nodes across all four centrality types. Before I identify the top-priority nodes, is there a specific type of centrality — hubs, brokers, spreaders, or prestige — you most care about for this question?"
- **Header:** "Priority"
- **Options:**
  - **Rank all four** — give a complete picture across all centrality types
  - **Focus on brokers** — betweenness centrality; who controls flow?
  - **Focus on hubs** — degree centrality; who is most connected?
  - **Focus on prestige** — eigenvector; who matters because of who they know?

**Step 4: Identify Structural Features**
Flag nodes with unusual profiles:
- **High betweenness, low degree:** A narrow broker — few connections but sits on critical paths. High leverage, high vulnerability.
- **High eigenvector, low degree:** Connected to powerful nodes but not widely. A "backdoor" to influence.
- **Isolates:** Nodes with no connections. Excluded from the network — may be by design or a gap.
- **Cut points / articulation nodes:** Nodes whose removal would disconnect parts of the network.

**Step 5: Apply to the Question**
Translate structural findings into actionable answers for the original question. Different questions call for different centrality types: targeting for influence → eigenvector and degree; identifying single points of failure → betweenness; seeding information efficiently → closeness.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the network and the question in 1–2 sentences, then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output: top nodes by type and the structural implications
  - **Specific focus** — Zoom in on one centrality type or one subset of nodes
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Network Definition**
[Nodes, edges, direction, time horizon, question being answered]

**Centrality Rankings**

| Node | Degree | Betweenness | Closeness | Eigenvector | Overall Assessment |
|------|--------|-------------|-----------|-------------|-------------------|
| | | | | | |

**Structural Features**
[Cut points, isolates, anomalous profiles, and what each means]

**Answer to the Original Question**
[Direct application of centrality findings to the specific question — who to target, protect, connect, or disconnect]

**Caveats**
[Where the analysis is limited by missing edges, assumed relationships, or a changing network structure]

---

## Notes

Centrality analysis assumes the network is reasonably stable and that the edges you've mapped reflect real relationships. In dynamic networks — where ties form and dissolve quickly — centrality scores can be misleading snapshots. Pair with `/s4h-network-contagion` when the goal is to model spread, since centrality tells you *who* matters but not *how* something moves through the network. Pair with `/s4h-social-power-mapping` when the network is organizational and the edges are influence or authority rather than communication.

The most important structural insight is often not the top-ranked node — it is the node with surprisingly high betweenness relative to its degree. These "hidden brokers" are frequently invisible to conventional analysis because they are not the loudest, most senior, or most connected — they just happen to sit on the only path between two otherwise-disconnected parts of the network.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Centrality mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-network-contagion` — Model how something spreads through this network, using the identified hubs and brokers as seed points or bottlenecks
  - `/s4h-network-weak-ties` — Identify the structural holes in this network and the bridging connections that span them
  - `/s4h-social-power-mapping` — Translate the structural centrality findings into an organizational power map
  - **Done** — Wrap up and synthesise what we have so far
