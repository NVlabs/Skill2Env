# Social Science Methods Frameworks -- Reference Guide

## Discourse Analysis Frameworks Comparison

### Framework Selection Guide

| Framework | Epistemology | Data Types | Focus | Best For |
|-----------|-------------|-----------|-------|----------|
| Fairclough CDA | Critical realism | Texts, speeches, media | Power and ideology in language | Policy documents, media, institutional texts |
| Gee discourse analysis | Social constructionism | Talk, texts, multimodal | Identity and social language | Education, identity, interaction |
| Foucauldian DA | Poststructuralism | Historical texts, policy | Discourse as constitutive of knowledge | Genealogies of knowledge, governance |
| Discursive psychology | Social constructionism | Naturalistic talk | Psychological concepts as discursive actions | Everyday talk, accounts, descriptions |
| Multimodal CDA | Critical realism | Texts + images + layout | Semiotic resources and power | Advertising, websites, textbooks |
| Corpus-assisted DA | Various | Large text collections | Patterns across large datasets | Media discourse, political language |

### CDA Analytical Checklist

```
TEXT LEVEL (Linguistic Analysis)
  Vocabulary:
  [ ] Ideologically contested words identified
  [ ] Overwording/underlexicalization noted
  [ ] Metaphor systems mapped
  [ ] Euphemism and dysphemism identified
  
  Grammar:
  [ ] Transitivity analysis (who does what to whom)
  [ ] Agency and passivization
  [ ] Modality (certainty, obligation, permission)
  [ ] Nominalization (processes turned into nouns)
  
  Textual structure:
  [ ] Given vs. new information
  [ ] Thematic structure
  [ ] Cohesion devices
  
DISCURSIVE PRACTICE LEVEL
  [ ] Conditions of production identified
  [ ] Distribution channels analyzed
  [ ] Consumption/reception contexts considered
  [ ] Intertextual chains traced
  [ ] Genre mixing (interdiscursivity) identified
  
SOCIAL PRACTICE LEVEL
  [ ] Institutional context described
  [ ] Power relations mapped
  [ ] Ideological effects assessed
  [ ] Historical context provided
  [ ] Connection to broader social structures made
```

## QCA Calibration Guide

### Fuzzy Set Calibration Methods

**Direct calibration (Ragin, 2008):**

Define three qualitative anchors:
- Full membership (e.g., 0.95)
- Crossover point (0.50) -- the point of maximum ambiguity
- Full non-membership (e.g., 0.05)

**Example calibration for "high GDP per capita":**

```
Anchor           Value          Fuzzy Score
Fully in         $50,000+       0.95
Crossover        $25,000        0.50
Fully out        $5,000-        0.05

Country examples:
  Norway ($82,000)     --> 0.99
  Spain ($30,000)      --> 0.73
  Brazil ($8,900)      --> 0.12
  Niger ($560)         --> 0.01
```

**Calibration best practices:**
- Anchors should be based on theoretical or substantive knowledge, not data distribution
- Document and justify every calibration decision
- Sensitivity analysis: test whether results change with different anchor points
- Avoid mechanical calibration (e.g., using percentiles) without theoretical justification

### Truth Table Analysis Steps

```
Step 1: Construct truth table
  - List all 2^k rows (k = number of conditions)
  - Assign cases to rows based on fuzzy membership
  - Calculate consistency for each row

Step 2: Set frequency threshold
  - Minimum number of cases per row (typically 1-3)
  - Higher thresholds for larger datasets

Step 3: Set consistency threshold
  - Typically 0.80 for sufficiency
  - Typically 0.90 for necessity

Step 4: Boolean minimization
  - Reduce complex expressions using logical minimization
  - Report parsimonious, intermediate, and complex solutions

Step 5: Assess solution quality
  - Solution consistency (> 0.80)
  - Solution coverage (how much of the outcome is explained)
  - Unique coverage (each path's unique contribution)
```

### QCA Reporting Standards

Based on Schneider and Wagemann (2010) transparency standards:

```
Required elements in QCA publications:
[ ] Raw data matrix (conditions x cases)
[ ] Calibration decisions with justifications
[ ] Truth table with consistency and frequency values
[ ] Necessity analysis results
[ ] All three solutions (parsimonious, intermediate, complex)
[ ] Directional expectations for intermediate solution
[ ] Solution consistency and coverage
[ ] Within-case evidence for key configurations
[ ] Robustness checks (sensitivity to calibration, thresholds)
```

## Process Tracing Templates

### Causal Mechanism Template

```
Mechanism Name: [descriptive label]

Theoretical Origin: [which theory predicts this mechanism]

Scope Conditions: [when/where this mechanism operates]

Mechanism Steps:
  Step 1: [Trigger/cause] -->
  Step 2: [Entity + activity] -->
  Step 3: [Entity + activity] -->
  Step 4: [Outcome]

Observable Manifestations:
  For Step 1: [What evidence would we observe?]
  For Step 2: [What evidence would we observe?]
  For Step 3: [What evidence would we observe?]
  For Step 4: [What evidence would we observe?]

Evidence Assessment:
  Evidence piece 1: [description]
    Type of test: [hoop / smoking gun / straw-in-the-wind / doubly decisive]
    If found: [what it means for the hypothesis]
    If not found: [what it means for the hypothesis]
    
  Evidence piece 2: [description]
    Type of test: [hoop / smoking gun / straw-in-the-wind / doubly decisive]
    ...
```

### Evidence Evaluation Matrix

| Evidence | Source | Test Type | Expected if H1 True | Expected if H1 False | Found? | Inference |
|----------|--------|-----------|---------------------|---------------------|--------|-----------|
| Budget allocation memo | Archive | Smoking gun | Specific allocation to program | No such memo | Yes | Strongly confirms |
| Timeline matches | Documents | Hoop | Policy change follows lobbying | Timeline mismatch | Yes | Passes necessary test |
| Actor testimony | Interview | Straw-in-the-wind | Claims causal role | Denies or is silent | Yes | Slightly supports |
| Alternative explanation evidence | Multiple | Hoop (for H2) | H2-specific evidence present | H2-specific evidence absent | No | Weakens H2 |

## Social Network Analysis Reference

### Network Measures Quick Reference

**Node-level measures:**

| Measure | Formula Concept | Interpretation |
|---------|----------------|----------------|
| Degree | Count of ties | Popularity / activity |
| In-degree | Incoming ties | Prestige / popularity |
| Out-degree | Outgoing ties | Activity / expansiveness |
| Betweenness | Shortest paths through node | Brokerage potential |
| Closeness | Inverse avg. distance to all | Efficiency of information access |
| Eigenvector | Connections to well-connected | Influence through connections |
| PageRank | Weighted eigenvector variant | Web influence (Google algorithm) |
| Constraint (Burt) | Redundancy of contacts | High = embedded, Low = bridging |

**Network-level measures:**

| Measure | Interpretation | Range |
|---------|---------------|-------|
| Density | Proportion of possible ties present | 0-1 |
| Reciprocity | Proportion of mutual ties | 0-1 |
| Transitivity | Proportion of closed triads | 0-1 |
| Average path length | Typical distance between nodes | 1+ |
| Diameter | Longest shortest path | 1+ |
| Centralization | Inequality of centrality distribution | 0-1 |
| Modularity | Strength of community structure | -0.5 to 1 |
| E-I Index | External vs. internal group ties | -1 to 1 |

### ERGM (Exponential Random Graph Model) Guide

ERGMs model the probability of observing a network as a function of structural features:

```
Common ERGM terms:
  edges          -- Baseline density (like intercept)
  mutual         -- Reciprocity tendency
  gwesp          -- Transitivity (friends of friends become friends)
  gwdegree       -- Degree distribution shape
  nodematch      -- Homophily on categorical attribute
  nodecov        -- Effect of continuous node attribute
  edgecov        -- Effect of dyad-level covariate
  nodefactor     -- Differential activity by group
```

**ERGM workflow in R (statnet):**

```r
library(statnet)

# Fit model
model <- ergm(network ~ edges + mutual + gwesp(0.5, fixed=TRUE) +
              nodematch("department") + nodecov("seniority"))

# Check convergence
mcmc.diagnostics(model)

# Goodness of fit
gof_results <- gof(model)
plot(gof_results)

# Interpret coefficients (log-odds)
summary(model)
```

## Bibliometric Analysis Workflow

### Complete Bibliometric Study Protocol

```
1. DEFINE SCOPE
   - Research question(s) for the bibliometric analysis
   - Time period
   - Disciplines/fields to include
   - Inclusion/exclusion criteria

2. DATA COLLECTION
   - Select database(s): Scopus, Web of Science, Dimensions, OpenAlex
   - Develop search query (Boolean operators, field codes)
   - Test and refine query
   - Download records (include abstracts, references, author info)
   - Document: date of search, query string, number of results

3. DATA CLEANING
   - Remove duplicates
   - Standardize author names (disambiguation)
   - Standardize journal names
   - Standardize institutional affiliations
   - Verify keyword consistency

4. DESCRIPTIVE ANALYSIS
   - Publication trends over time
   - Top journals, authors, institutions, countries
   - Most cited publications
   - Keyword frequency analysis

5. NETWORK ANALYSIS
   - Co-authorship network (collaboration patterns)
   - Co-citation network (intellectual base)
   - Bibliographic coupling (research fronts)
   - Keyword co-occurrence network (thematic structure)

6. ADVANCED ANALYSIS
   - Burst detection (emerging topics)
   - Thematic evolution (topic changes over time)
   - Science mapping (field structure visualization)
   - Three-field plots (connections between categories)

7. INTERPRETATION AND REPORTING
   - Identify research gaps
   - Map intellectual structure of the field
   - Describe emerging trends
   - Provide recommendations for future research
```

## Program Evaluation Frameworks Detailed

### Theory of Change Template

```
LONG-TERM GOAL:
[Ultimate change you want to see in the world]

PRECONDITIONS (working backward):

Level 4 - Long-term outcomes:
  [What must be true for the long-term goal?]
  Assumptions: [What must hold?]
  Evidence: [What supports this link?]

Level 3 - Medium-term outcomes:
  [What must be true for Level 4?]
  Assumptions: [What must hold?]
  Interventions: [What activities produce these outcomes?]

Level 2 - Short-term outcomes:
  [What must be true for Level 3?]
  Assumptions: [What must hold?]
  Interventions: [What activities produce these outcomes?]

Level 1 - Outputs and activities:
  [What does the program actually do?]
  Resources needed: [Inputs required]

CONTEXT:
  [External factors that affect the theory]
  [Enabling conditions required]
  [Potential disruptions]
```

### RE-AIM Evaluation Checklist

```
REACH
  [ ] What proportion of the target population participated?
  [ ] Are participants representative of the target population?
  [ ] What are characteristics of participants vs. non-participants?
  
EFFECTIVENESS
  [ ] What was the impact on primary outcomes?
  [ ] Were there negative outcomes or unintended consequences?
  [ ] What was the impact on quality of life / broader outcomes?
  [ ] Were there differential effects by subgroup?

ADOPTION
  [ ] What proportion of settings/organizations adopted the program?
  [ ] Are adopting settings representative?
  [ ] What are barriers and facilitators to adoption?

IMPLEMENTATION
  [ ] Was the program delivered as intended (fidelity)?
  [ ] What adaptations were made and why?
  [ ] What were the costs of implementation?
  [ ] What was the consistency of delivery across settings?

MAINTENANCE
  [ ] Were individual-level outcomes maintained over time?
  [ ] Was the program institutionalized (sustained at setting level)?
  [ ] What modifications were made for sustainability?
```

## Delphi Method Reporting Checklist

Based on CREDES guidelines (Junger et al., 2017):

```
PLANNING
  [ ] Rationale for using Delphi method stated
  [ ] Type of Delphi specified (classical, modified, real-time, policy)
  [ ] Consensus definition pre-specified
  [ ] Number of rounds pre-specified or stopping rule defined

PARTICIPANTS
  [ ] Expert selection criteria defined
  [ ] Recruitment strategy described
  [ ] Panel size justified
  [ ] Response rates per round reported
  [ ] Participant characteristics described

PROCEDURE
  [ ] Round 1 instrument described
  [ ] Scale types and anchors specified
  [ ] Feedback content and format described
  [ ] Anonymity maintained between panelists
  [ ] Time between rounds reported

ANALYSIS
  [ ] Statistical measures reported per item per round
  [ ] Consensus criteria applied consistently
  [ ] Stability between rounds assessed
  [ ] Attrition analysis conducted

RESULTS
  [ ] Items meeting consensus listed
  [ ] Items not meeting consensus listed
  [ ] Changes between rounds documented
  [ ] Minority opinions reported
```

## Key Methodological Texts by Method

### Essential Reading List

**Discourse Analysis:**
- Fairclough, N. (2003). *Analysing Discourse*. Routledge.
- Gee, J. P. (2014). *An Introduction to Discourse Analysis* (4th ed.). Routledge.
- Wodak, R., & Meyer, M. (Eds.). (2015). *Methods of Critical Discourse Studies* (3rd ed.). SAGE.

**Conversation Analysis:**
- Sidnell, J., & Stivers, T. (Eds.). (2013). *The Handbook of Conversation Analysis*. Wiley-Blackwell.
- ten Have, P. (2007). *Doing Conversation Analysis* (2nd ed.). SAGE.

**QCA:**
- Ragin, C. C. (2008). *Redesigning Social Inquiry*. University of Chicago Press.
- Schneider, C. Q., & Wagemann, C. (2012). *Set-Theoretic Methods for the Social Sciences*. Cambridge University Press.

**Process Tracing:**
- Beach, D., & Pedersen, R. B. (2019). *Process-Tracing Methods* (2nd ed.). University of Michigan Press.
- Bennett, A., & Checkel, J. T. (Eds.). (2015). *Process Tracing*. Cambridge University Press.

**Social Network Analysis:**
- Wasserman, S., & Faust, K. (1994). *Social Network Analysis*. Cambridge University Press.
- Scott, J. (2017). *Social Network Analysis* (4th ed.). SAGE.
- Lusher, D., Koskinen, J., & Robins, G. (Eds.). (2013). *Exponential Random Graph Models for Social Networks*. Cambridge University Press.

**Bibliometrics:**
- Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping. *Journal of Informetrics*, 11(4), 959-975.
- Zupic, I., & Cater, T. (2015). Bibliometric methods in management and organization. *Organizational Research Methods*, 18(3), 429-472.

**Program Evaluation:**
- Patton, M. Q. (2008). *Utilization-Focused Evaluation* (4th ed.). SAGE.
- Rossi, P. H., Lipsey, M. W., & Henry, G. T. (2019). *Evaluation* (8th ed.). SAGE.
- Stufflebeam, D. L., & Coryn, C. L. S. (2014). *Evaluation Theory, Models, and Applications* (2nd ed.). Jossey-Bass.

**Policy Analysis:**
- Bardach, E., & Patashnik, E. M. (2019). *A Practical Guide for Policy Analysis* (6th ed.). CQ Press.
- Weimer, D. L., & Vining, A. R. (2017). *Policy Analysis* (6th ed.). Routledge.
