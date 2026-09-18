# Network, Bibliometric, Review, and Evaluation Methods

Detailed concepts, tool comparisons, worked examples, and templates for the relational
and applied-policy methods. See also `references/social-science-frameworks.md` for the
SNA measures quick reference, ERGM guide, full bibliometric study protocol, Theory of
Change / RE-AIM templates, and Delphi reporting checklist.

## Social Network Analysis (SNA)

Social network analysis examines the structure and implications of relationships between
actors (individuals, organizations, nations). It shifts the analytical focus from
attributes of individual cases to patterns of connections.

**Key SNA concepts:**

| Concept | Definition | Measure |
|---------|-----------|---------|
| Degree centrality | Number of direct connections | Count of ties |
| Betweenness centrality | How often a node lies on shortest paths between others | Freeman betweenness |
| Closeness centrality | Average distance to all other nodes | Inverse of average path length |
| Eigenvector centrality | Connections to well-connected nodes | Eigenvector score |
| Density | Proportion of possible ties that are present | Actual ties / possible ties |
| Clustering coefficient | Extent to which a node's neighbors are connected to each other | Proportion of closed triads |
| Homophily | Tendency for similar nodes to be connected | E-I index, assortivity |
| Structural holes | Gaps between clusters that a node can bridge | Burt's constraint measure |

**SNA software:**

| Software | Strengths | Cost |
|----------|----------|------|
| Gephi | Visualization, large networks | Free |
| UCINET | Classic SNA measures, ERGM | Paid |
| igraph (R/Python) | Programmable, scalable | Free |
| NetworkX (Python) | Programmable, well-documented | Free |
| Pajek | Very large networks | Free |
| NodeXL | Excel integration, social media | Paid |
| statnet (R) | Statistical models (ERGM, STERGM) | Free |

**Example: research question to SNA measure mapping**

```
Question: Who are the most influential researchers in the field?
  --> Eigenvector centrality (connected to other influential nodes)

Question: Who bridges different research communities?
  --> Betweenness centrality (lies on paths between clusters)

Question: How cohesive is this policy network?
  --> Density, average path length, clustering coefficient

Question: Do researchers collaborate within or across institutions?
  --> Homophily (E-I index by institutional affiliation)

Question: How has the collaboration network evolved?
  --> Longitudinal SNA (STERGM, RSIENA)
```

## Bibliometrics and Scientometrics

Bibliometrics uses quantitative analysis of scholarly publications to map research fields,
identify trends, and evaluate impact. Scientometrics is the broader study of the scientific
enterprise using quantitative methods.

**Core bibliometric techniques:**

1. **Citation analysis** -- Who cites whom? Identifies intellectual influence and knowledge flows
2. **Co-citation analysis** -- Which works are cited together? Reveals intellectual structure
3. **Bibliographic coupling** -- Which works share references? Identifies research fronts
4. **Co-authorship analysis** -- Who collaborates with whom? Maps collaboration networks
5. **Keyword co-occurrence** -- Which concepts appear together? Maps thematic structure
6. **Science mapping** -- Visual representation of field structure and evolution

**Bibliometric tools:**

| Tool | Type | Best For |
|------|------|----------|
| VOSviewer | Visualization | Network visualization, co-citation maps |
| Bibliometrix (R) | Analysis package | Comprehensive bibliometric analysis |
| CiteSpace | Visualization + analysis | Burst detection, timeline visualization |
| Publish or Perish | Citation metrics | Individual-level citation analysis |
| Dimensions | Database + analytics | AI-powered literature analytics |
| Lens.org | Database | Patent + scholarly literature integration |
| Scopus/WoS | Database | Authoritative citation data |

## Systematic Mapping Reviews

Systematic mapping reviews (also called scoping reviews or evidence maps) provide a broad
overview of a research area, identifying the volume and nature of available evidence without
synthesizing effect sizes. They differ from systematic reviews in scope and depth.

**Mapping review vs. systematic review:**

| Feature | Systematic Review | Mapping Review |
|---------|------------------|----------------|
| Question | Focused, specific | Broad, exploratory |
| Search | Comprehensive | Comprehensive |
| Quality appraisal | Formal, required | Optional |
| Data extraction | Detailed outcomes | Descriptive categorization |
| Synthesis | Meta-analysis or narrative | Visual maps, frequency tables |
| Purpose | Answer specific question | Map the territory |

**PRISMA-ScR (Scoping Reviews) checklist items:**

1. Title identifying the report as a scoping review
2. Structured abstract
3. Rationale and objectives
4. Eligibility criteria
5. Information sources and search strategy
6. Selection of evidence
7. Data charting process
8. Critical appraisal (if conducted)
9. Results with flow diagram
10. Discussion of findings in context

## Program Evaluation

Program evaluation systematically assesses the design, implementation, and outcomes of
interventions, programs, or policies. It serves both accountability and learning functions.

**Major evaluation frameworks:**

| Framework | Focus | Key Feature |
|-----------|-------|-------------|
| Logic Model | Program theory | Inputs -> Activities -> Outputs -> Outcomes |
| Theory of Change | Causal pathways | Maps assumptions and mechanisms |
| RE-AIM | Implementation | Reach, Effectiveness, Adoption, Implementation, Maintenance |
| CIPP (Stufflebeam) | Decision-making | Context, Input, Process, Product evaluation |
| Utilization-Focused (Patton) | Use | Designed for intended users |
| Developmental Evaluation | Innovation | Real-time evaluation for adaptive programs |
| Empowerment Evaluation | Equity | Community ownership of evaluation process |

**Logic model template:**

```
INPUTS          ACTIVITIES         OUTPUTS           OUTCOMES
                                                Short-term | Long-term
-----------     -------------      ----------    --------   ----------
Funding         Training           # trained     Knowledge  Policy change
Staff           Workshops          # sessions    Attitudes  Health improvement
Materials       Counseling         # served      Skills     Reduced inequality
Partnerships    Outreach           # materials   Behaviors  Systems change
Technology      Data collection    # referrals   Access     Sustainability
```

## Policy Analysis Methods

Policy analysis provides structured approaches to evaluating public policies and generating
alternatives.

**Bardach's Eightfold Path:**

1. Define the problem
2. Assemble some evidence
3. Construct the alternatives
4. Select the criteria (efficiency, equity, feasibility, political acceptability)
5. Project the outcomes
6. Confront the trade-offs
7. Decide
8. Tell your story

**Cost-benefit analysis (CBA) and cost-effectiveness analysis (CEA):**

| Feature | CBA | CEA |
|---------|-----|-----|
| Outcome measure | Monetized | Natural units (lives saved, cases prevented) |
| Comparison | Net benefits | Cost per unit of outcome |
| When to use | When outcomes can be monetized | When monetization is inappropriate |
| Result | Benefit-cost ratio or net present value | Incremental cost-effectiveness ratio (ICER) |
