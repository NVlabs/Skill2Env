---
name: alterlab-sna
description: "Applies social-network-analysis method discipline to relational data — degree/betweenness/closeness/eigenvector centrality and PageRank, community detection (Louvain and greedy-modularity native in networkx, Leiden via igraph), and inferential network models (ERGM) — choosing the measure that matches the substantive question and the right dependence assumptions, then routing computation to the existing networkx (and igraph/R) tooling. Use when the request mentions social network analysis, centrality, key players/brokerage, community or cluster detection in a network, ERGM, or modeling ties between nodes. For general graph algorithms and plotting prefer alterlab-networkx; for graph neural networks prefer alterlab-torch-geometric. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Computation routes to networkx>=3.4 (centrality, native Louvain/greedy-modularity). Leiden and very large graphs -> python-igraph>=0.11. ERGM has no mature Python package -> R statnet/ergm via an R bridge (declare it). No API key; runs locally via `uv run python`."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-networkx (computation), alterlab-ssci-design-gate; audited by alterlab-ssci-inference-gate"
---

# Social Network Analysis — Match the Measure to the Question

**Skill type: ANALYSIS MODULE.** SNA treats the **ties** as the data. The discipline is not
running a centrality function — it is choosing the centrality that answers the substantive
question, respecting network dependence (ties are not independent observations), and using an
inferential model (ERGM) when you want to *explain* tie formation rather than describe it.
Computation is handed to `alterlab-networkx`.

## Core Mission

```
THE TIE IS THE UNIT. PICK THE CENTRALITY THAT MATCHES THE QUESTION; TIES ARE NOT IID.
```

## When to Use This Skill

- "Run a social network analysis / compute centrality on my network."
- "Who are the key players / brokers in this network?"
- "Detect communities / clusters in my network."
- "Fit an ERGM to explain why ties form."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| General graph algorithms / plotting / I/O | `alterlab-networkx` | This skill adds SNA method choice; networkx executes. |
| Graph neural networks / node embeddings for prediction | `alterlab-torch-geometric` | Deep learning on graphs, not SNA description/inference. |
| Whether a relational design is appropriate | `alterlab-ssci-design-gate` | Design routing, upstream. |
| Plain tabular statistics | `alterlab-statistical-analysis` | No network structure. |

## Centrality — pick by the substantive claim (verified networkx 3.x)

| Question | Centrality | Call |
|----------|-----------|------|
| Who has the most direct ties? | degree | `nx.degree_centrality(G)` |
| Who bridges otherwise-separate groups? | betweenness (brokerage) | `nx.betweenness_centrality(G)` |
| Who can reach everyone fastest? | closeness | `nx.closeness_centrality(G)` |
| Who is connected to well-connected others? | eigenvector / PageRank | `nx.eigenvector_centrality(G)` / `nx.pagerank(G)` |

Do not report "centrality" generically — name which one and why it matches the claim (a broker
argument needs betweenness, not degree).

## Community detection (verified)

- `nx.community.louvain_communities(G)` — **native** in networkx 3.x (no `python-louvain` needed).
- `nx.community.greedy_modularity_communities(G)` — Clauset-Newman-Moore.
- `nx.community.modularity(G, communities)` — score a partition.
- **Leiden** (Traag et al.) is not in networkx; it guarantees well-connected communities and is the
  recommended improvement over Louvain — route to `python-igraph`
  (`ig.Graph.community_leiden(...)`) or `leidenalg`. Use igraph for large graphs generally.

## Inference: ERGM (no mature Python — use R statnet)

To *explain* tie formation (reciprocity, homophily, triadic closure) rather than describe it, use
an **exponential random graph model**. There is no mature Python ERGM package (pyERGM exists but is
young); the standard is R **`statnet`/`ergm`** via an R bridge:

```r
library(ergm)
model <- ergm(net ~ edges + mutual + nodematch("group") + gwesp(0.5, fixed = TRUE))
summary(model)
```

Declare the R dependency; do not fabricate a Python ERGM API. Full algorithm-selection guidance,
the ERGM term glossary, and the dependence caveat: `references/sna_methods.md`.

## The dependence caveat

Network ties violate the independence assumption of ordinary regression: you cannot regress an
outcome on centrality and read the SE naively, because nodes are linked. Use permutation/QAP tests
for dyadic hypotheses, or ERGM/latent-space models for tie-level inference. Flag this whenever a
network measure is fed into a downstream test.

## Output Template

```
NETWORK:      <directed? weighted? n nodes, m edges; how ties were defined>
MEASURE:      <named centrality/community algorithm + why it matches the question>
RESULT:       <top nodes / partition + modularity; not just a number>
INFERENCE:    <ERGM terms + fit, OR permutation/QAP test> — respect tie dependence
CLAIM SCOPE:  descriptive (structure) vs inferential (tie-formation) — do not conflate
```

## References

- `references/sna_methods.md` — centrality selection, Louvain vs Leiden, ERGM terms + R bridge, QAP/permutation, large-graph tooling.

Part of the AlterLab Academic Skills suite.
