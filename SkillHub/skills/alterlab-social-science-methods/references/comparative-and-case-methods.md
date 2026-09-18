# Comparative and Case-Based Methods

## Qualitative Comparative Analysis (QCA)

QCA, developed by Charles Ragin, bridges the qualitative-quantitative divide by using Boolean algebra and set theory to analyze causal complexity across cases. It is designed for medium-N research (10-50 cases) where statistical methods lack power but individual case studies cannot establish generality.

**QCA variants:**

| Variant | Data Type | Best For |
|---------|----------|----------|
| crisp-set QCA (csQCA) | Binary (0/1) | Clear-cut conditions |
| fuzzy-set QCA (fsQCA) | Continuous (0.0-1.0) | Degree of membership |
| multi-value QCA (mvQCA) | Categorical (0, 1, 2...) | Non-binary categories |

**Steps in fsQCA:**

1. **Identify conditions and outcome** -- Select theoretically grounded conditions (typically 4-7)
2. **Calibrate sets** -- Convert raw data into fuzzy-set membership scores (0.0 to 1.0) using three anchor points: fully in (0.95), crossover (0.50), fully out (0.05)
3. **Construct truth table** -- List all logically possible combinations of conditions
4. **Analyze necessary conditions** -- Test whether any single condition is necessary for the outcome (consistency > 0.90)
5. **Analyze sufficient conditions** -- Use Boolean minimization to identify combinations of conditions sufficient for the outcome
6. **Interpret solutions** -- Distinguish between parsimonious, intermediate, and complex solutions
7. **Return to cases** -- Validate the solutions against within-case knowledge

**Example: QCA truth table row**

```
Conditions: HIGH_FUNDING * STRONG_LEADERSHIP * COMMUNITY_SUPPORT * ~POLITICAL_OPPOSITION
Outcome: PROGRAM_SUCCESS
Cases: Portland, Austin, Minneapolis
Consistency: 0.92
Coverage: 0.45

Interpretation: The combination of high funding AND strong leadership
AND community support AND the absence of political opposition is
sufficient for program success, as observed in three cases.
```

**Software:** fsQCA (free), QCA package in R, TOSMANA

## Mill's Methods

John Stuart Mill's methods of agreement and difference remain foundational for comparative case selection:

- **Method of Agreement** -- If two or more cases share the outcome and one common condition while differing on others, that condition may be causal
- **Method of Difference** -- If two cases differ on the outcome and one condition while being similar on others, that condition may be causal
- **Method of Concomitant Variation** -- If a condition and outcome vary together across cases, they may be causally related
- **Joint Method** -- Combining agreement and difference for stronger inference

## Process Tracing

Process tracing is a within-case method for identifying causal mechanisms. Developed in political science (George & Bennett, 2005; Beach & Pedersen, 2019), it examines the causal chain between an independent variable and outcome by identifying observable evidence of theorized mechanisms.

**Process tracing variants:**

1. **Theory-testing** -- Evaluates whether a hypothesized causal mechanism operated in a specific case
2. **Theory-building** -- Inductively identifies causal mechanisms from detailed case evidence
3. **Explaining-outcome** -- Iteratively constructs a case-specific explanation

**Bayesian process tracing (Beach & Pedersen):**

For each piece of evidence, assess:
- **Prior probability** -- How likely is the hypothesis before seeing this evidence?
- **Likelihood of evidence if hypothesis is true** -- Would we expect this evidence if the mechanism operated?
- **Likelihood of evidence if hypothesis is false** -- Could this evidence exist without the mechanism?

**Four types of process tracing tests:**

| Test | High uniqueness | Low uniqueness |
|------|----------------|----------------|
| **High certainty** | Doubly decisive | Hoop test |
| **Low certainty** | Smoking gun | Straw-in-the-wind |

- **Hoop test** -- Evidence the hypothesis must pass to remain viable (necessary but not sufficient)
- **Smoking gun** -- Evidence that strongly confirms if found (sufficient but not necessary)
- **Doubly decisive** -- Evidence that is both necessary and sufficient (rare)
- **Straw-in-the-wind** -- Slightly shifts the probability but is neither necessary nor sufficient

## Archival Research

Archival research involves systematic analysis of primary source documents stored in archives, libraries, government records offices, organizational files, and digital repositories. It is a core method in history, political science, sociology, and area studies.

**Types of archival sources:**

- Government records (legislation, policy memos, diplomatic cables, census data)
- Organizational records (meeting minutes, correspondence, financial records)
- Personal papers (diaries, letters, memoirs)
- Legal documents (court records, contracts, charters)
- Media archives (newspapers, broadcasts, advertisements)
- Visual materials (photographs, maps, architectural plans)
- Digital archives (email collections, web archives, social media datasets)

**Evaluating archival sources -- the four questions:**

1. **Authenticity** -- Is this document what it purports to be? (forgery detection, provenance chain)
2. **Reliability** -- How accurate is the information? (proximity to events, author bias, corroboration)
3. **Representativeness** -- What has survived and what has been lost? (selection bias in archives)
4. **Meaning** -- What did this document mean in its original context? (historical semantics, cultural context)

**Practical archival research workflow:**

1. Identify relevant archives through finding aids, archival catalogs, and secondary literature
2. Contact archivists in advance -- they are invaluable guides to collection organization
3. Review finding aids to identify relevant boxes, folders, and series
4. Develop a systematic note-taking protocol (metadata, transcription, analysis notes)
5. Photograph or scan documents when permitted (check institutional policies)
6. Cross-reference documents across collections to corroborate claims
7. Maintain a chain of custody for all evidence cited in publications
