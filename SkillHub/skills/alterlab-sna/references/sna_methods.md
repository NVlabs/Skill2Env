# SNA Methods — Selection, Community Detection, and Inference

Loaded on demand from the sna SKILL.md. Verified against networkx (v3.6), python-igraph (v1.0),
and R `ergm` (v4.12) current docs.

## Centrality selection (match to the claim)

| Centrality | Captures | Use when the claim is… | networkx call |
|-----------|----------|------------------------|---------------|
| Degree | volume of direct ties | "most active / most connected" | `nx.degree_centrality(G)` |
| Betweenness | lying on shortest paths | "broker / gatekeeper between groups" | `nx.betweenness_centrality(G)` |
| Closeness | short distance to all others | "can diffuse information fastest" | `nx.closeness_centrality(G)` |
| Eigenvector | ties to well-connected others | "influential via influential contacts" | `nx.eigenvector_centrality(G, max_iter=1000)` |
| PageRank | eigenvector variant, directed | "importance in a directed flow" | `nx.pagerank(G, alpha=0.85)` |

For directed/weighted networks pass the directed graph and `weight=` where supported; eigenvector
centrality can fail to converge on some graphs — raise `max_iter` or use `pagerank`.

## Community detection: Louvain vs Leiden

- **Louvain** (`nx.community.louvain_communities(G, weight=..., resolution=1.0)`) — native in
  networkx 3.x, fast, greedy modularity optimization. Can produce badly-connected (even
  disconnected) communities.
- **Leiden** — fixes Louvain's connectivity flaw and is generally preferred; not in networkx, use
  `python-igraph` `ig.Graph.community_leiden(objective_function="modularity")` or the `leidenalg`
  package (supports CPM/Surprise/Significance quality functions).
- Score any partition with `nx.community.modularity(G, communities)`; resolution controls
  community size (higher → more, smaller communities).
- For large graphs (10^5+ nodes) prefer igraph/graph-tool; export from networkx with
  `nx.write_gexf(G, "graph.gexf")` for Gephi.

## Inference — ERGM (R statnet)

ERGMs model the probability of the observed network as a function of structural terms. Common terms:

| Term | Models |
|------|--------|
| `edges` | baseline density (like an intercept) |
| `mutual` | reciprocity (directed) |
| `nodematch("attr")` | homophily on a nodal attribute |
| `nodecov("x")` | activity by a continuous attribute |
| `gwesp(alpha, fixed=TRUE)` | triadic closure (geometrically-weighted shared partners) |
| `gwdegree(...)` | degree distribution |

```r
library(ergm)
m <- ergm(net ~ edges + mutual + nodematch("dept") + gwesp(0.5, fixed = TRUE),
          control = control.ergm(MCMC.samplesize = 4096))
summary(m)
mcmc.diagnostics(m)   # check MCMC convergence and model degeneracy
```

Watch for **model degeneracy** (the MCMC wanders to empty/complete graphs) — geometrically-weighted
terms mitigate it. There is no mature Python ERGM; `pyERGM` exists but is young. Latent-space models
(R `latentnet`) are an alternative for tie-level inference.

## The dependence problem (why not plain regression)

Ties share nodes, so observations are not independent. For dyadic hypotheses (e.g. "do same-department
pairs tie more?") use **QAP / MRQAP** permutation tests (permute node labels, recompute) rather than
OLS SEs. For node-level outcomes correlated with network position, use network-autocorrelation models
or ERGM-derived quantities — never read naive regression SEs on centrality as if nodes were iid.

## References

- Wasserman & Faust (1994), *Social Network Analysis: Methods and Applications.*
- Traag, Waltman & van Eck (2019), From Louvain to Leiden.
- Lusher, Koskinen & Robins (2013), *Exponential Random Graph Models for Social Networks.*
- Hunter, Handcock, Butts, Goodreau & Morris (2008), ergm (statnet).
