---
name: s4h-network
description: "Entry point for the network analysis toolkit. Routes to the right network skill based on your situation. Use when you say 'network', 'who's connected to whom', 'how does this spread', 'who are the key players', 'why did this go viral', 'network effects', 'tipping point', 'weak ties', 'bridges between groups', or want network thinking applied without knowing which specific tool fits."
---

# Network

Applies network analysis to situations where structure — not just individual attributes — determines outcomes. Diagnoses what kind of network thinking is needed and routes to the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Identify the most influential, well-connected, or critical nodes | centrality |
| Model how something spreads — or fails to spread — through a network | contagion |
| Find the bridging connections that link otherwise-disconnected groups | weak-ties |
| Understand how value scales with participation and where tipping points lie | network-effects |

## Routing Decision

**Framing check:** Confirm the network and the question before routing. State what you've identified — the actual network being analyzed and the core question or decision at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the network and the key question]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Need to identify key people, hubs, or critical points in a network** → centrality
- **Something is (or needs to) spread through a network — adoption, behavior, disease, failure** → contagion
- **Surprised by where information, opportunities, or influence came from** → weak-ties
- **Value of a product or platform depends on how many others use it** → network-effects
- **Unclear** → centrality; mapping who matters usually reveals how things spread, where bridges are, and what drives value

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

## Centrality

*Identifies which nodes in a network have the most influence, reach, or control.*

Not all nodes are equal. Centrality analysis measures which nodes are most connected (degree centrality), which are best positioned to reach the rest of the network quickly (closeness centrality), which sit on the most paths between others and can broker or bottleneck (betweenness centrality), and which are connected to other highly-connected nodes (eigenvector/PageRank centrality). Albert-László Barabási's work on scale-free networks showed that real-world networks are dominated by hubs — and understanding those hubs explains why some people, websites, cities, and companies exert disproportionate influence.

**Output:** Centrality rankings by type, identification of hubs and brokers, structural vulnerabilities, and the highest-leverage targets for intervention.

---

## Contagion

*Models how things spread through networks — ideas, behaviors, viruses, failures.*

Contagion depends on network structure as much as on the thing spreading. Duncan Watts' research showed that large cascades are not caused by exceptional "influencers" — they're caused by a susceptible network. Whether something spreads turns on: the reproduction number (how many nodes each infected node infects on average), the threshold structure of the population (what fraction of neighbours must adopt before you adopt), and the presence of structural bridges that let spread jump between clusters. Understanding contagion means understanding the network, not just the pathogen.

**Output:** Spread model with reproduction number estimate, threshold analysis, cascade risk, bottlenecks, and intervention points.

---

## Weak Ties

*Maps bridging connections across structural holes — the counterintuitive power of loose connections.*

Mark Granovetter's 1973 finding remains one of sociology's most durable results: the information and opportunities that change your life almost always come through weak ties — acquaintances, not close friends. Strong ties share the same information you already have; weak ties bridge different clusters. Structural holes — gaps in the network where no bridge currently exists — represent untapped arbitrage: the person who bridges them gains information advantage, influence, and access. This skill identifies where the structural holes are and who currently spans them.

**Output:** Strong-tie clusters identified, structural holes mapped, current bridges and their leverage, and recommendations for where to build or strengthen bridging connections.

---

## Network Effects

*Analyzes how value scales with participation — tipping points, lock-in, and winner-take-all dynamics.*

Robert Metcalfe's law states that the value of a network scales with the square of its connected users. But the mechanics vary: direct network effects (each user adds value to all others), indirect network effects (more users on one side attract complementary participants on the other), data network effects (more usage generates better intelligence that attracts more usage), and local network effects (value is driven by connections within a cluster, not the whole network). Understanding which type is operating tells you where the tipping point is, how defensible the position is, and whether this is a winner-take-all or winner-take-most market.

**Output:** Network effect type identified, tipping point analysis, current position relative to critical mass, defensibility assessment, and strategic implications.
