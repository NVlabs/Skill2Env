---
name: alterlab-opentargets
description: Query the Open Targets Platform GraphQL API for target-disease associations, tractability and safety data, genetics/omics evidence, and known drugs. Use when identifying or prioritizing therapeutic drug targets, assessing target druggability/safety, or gathering target-disease evidence for drug discovery. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Keyless Open Targets GraphQL API (no authentication required)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Open Targets Database

## Overview

The Open Targets Platform is a comprehensive resource for systematic identification and prioritization of potential therapeutic drug targets. It integrates publicly available datasets including human genetics, omics, literature, and chemical data to build and score target-disease associations.

**Key capabilities:**
- Query target (gene) annotations including tractability, safety, expression
- Search for disease-target associations with evidence scores
- Retrieve evidence from multiple data types (genetics, pathways, literature, etc.)
- Find known drugs for diseases and their mechanisms
- Access drug information including clinical trial phases and adverse events
- Evaluate target druggability and therapeutic potential

**Data access:** The platform provides a GraphQL API, web interface, data downloads, and Google BigQuery access. This skill focuses on the GraphQL API for programmatic access.

## When to Use This Skill

This skill should be used when:

- **Target discovery:** Finding potential therapeutic targets for a disease
- **Target assessment:** Evaluating tractability, safety, and druggability of genes
- **Evidence gathering:** Retrieving supporting evidence for target-disease associations
- **Drug repurposing:** Identifying existing drugs that could be repurposed for new indications
- **Competitive intelligence:** Understanding clinical precedence and drug development landscape
- **Target prioritization:** Ranking targets based on genetic evidence and other data types
- **Mechanism research:** Investigating biological pathways and gene functions
- **Biomarker discovery:** Finding genes differentially expressed in disease
- **Safety assessment:** Identifying potential toxicity concerns for drug targets

## Core Workflow

### 1. Search for Entities

Start by finding the identifiers for targets, diseases, or drugs of interest.

**For targets (genes):**
```python
from scripts.query_opentargets import search_entities

# Search by gene symbol or name
results = search_entities("BRCA1", entity_types=["target"])
# Returns: [{"id": "ENSG00000012048", "name": "BRCA1", ...}]
```

**For diseases:**
```python
# Search by disease name
results = search_entities("alzheimer", entity_types=["disease"])
# Returns: [{"id": "MONDO_0004975", "name": "Alzheimer disease", ...}]
```
Always resolve the ID via search rather than hardcoding it — Open Targets has
migrated many diseases from EFO to MONDO IDs (e.g. Alzheimer disease is now
`MONDO_0004975`, not the older `EFO_0000249`).

**For drugs:**
```python
# Search by drug name
results = search_entities("aspirin", entity_types=["drug"])
# Returns: [{"id": "CHEMBL25", "name": "ASPIRIN", ...}]
```

**Identifiers used:**
- Targets: Ensembl gene IDs (e.g., `ENSG00000157764` = BRAF, `ENSG00000012048` = BRCA1)
- Diseases: ontology IDs — EFO, **MONDO** (now common), HP, Orphanet (e.g., `MONDO_0004975` = Alzheimer disease). The `disease(efoId:)` argument accepts any of these.
- Drugs: ChEMBL IDs (e.g., `CHEMBL25` = aspirin)

### 2. Query Target Information

Retrieve comprehensive target annotations to assess druggability and biology.

```python
from scripts.query_opentargets import get_target_info

target_info = get_target_info("ENSG00000157764", include_diseases=True)

# Access key fields:
# - approvedSymbol: HGNC gene symbol
# - approvedName: Full gene name
# - tractability: Druggability assessments across modalities
# - safetyLiabilities: Known safety concerns
# - geneticConstraint: Constraint scores from gnomAD
# - associatedDiseases: Top disease associations with scores
```

**Key annotations to review:**
- **Tractability:** Small molecule, antibody, PROTAC druggability predictions
- **Safety:** Known toxicity concerns from multiple databases
- **Genetic constraint:** pLI and LOEUF scores indicating essentiality
- **Disease associations:** Diseases linked to the target with evidence scores

Refer to `references/target_annotations.md` for detailed information about all target features.

### 3. Query Disease Information

Get disease details and associated targets/drugs.

```python
from scripts.query_opentargets import get_disease_info

disease_info = get_disease_info("MONDO_0004975", include_targets=True)

# Access fields:
# - name: Disease name
# - description: Disease description
# - therapeuticAreas: High-level disease categories
# - associatedTargets: Top targets with association scores
```

### 4. Retrieve Target-Disease Evidence

Get detailed evidence supporting a target-disease association.

```python
from scripts.query_opentargets import get_target_disease_evidence

# Get all evidence
evidence = get_target_disease_evidence(
    ensembl_id="ENSG00000157764",
    efo_id="MONDO_0004975"
)

# The API filters by data SOURCE, not broad data type. To narrow to genetic
# evidence, pass its sources (or fetch all rows and filter on datatypeId).
genetic_evidence = get_target_disease_evidence(
    ensembl_id="ENSG00000157764",
    efo_id="MONDO_0004975",
    datasource_ids=["gwas_catalog", "clinvar", "gene_burden"]
)

# Each evidence record contains:
# - datasourceId: Specific data source (e.g., "gwas_catalog", "chembl")
# - datatypeId: Evidence category (e.g., "genetic_association", "known_drug")
# - score: Evidence strength (0-1)
# - studyId: Original study identifier
# - literature: Associated publications
```

**Major evidence types:**
1. **genetic_association:** GWAS, rare variants, ClinVar, gene burden
2. **somatic_mutation:** Cancer Gene Census, IntOGen, cancer biomarkers
3. **known_drug:** Clinical precedence from approved/clinical drugs
4. **affected_pathway:** CRISPR screens, pathway analyses, gene signatures
5. **rna_expression:** Differential expression from Expression Atlas
6. **animal_model:** Mouse phenotypes from IMPC
7. **literature:** Text-mining from Europe PMC

Refer to `references/evidence_types.md` for detailed descriptions of all evidence types and interpretation guidelines.

### 5. Find Known Drugs

Identify drugs used for a disease and their targets.

```python
from scripts.query_opentargets import get_known_drugs_for_disease

drugs = get_known_drugs_for_disease("MONDO_0004975")

# Helper queries the `drugAndClinicalCandidates` field (the former `knownDrugs`
# field was removed). It returns:
# - count: Total number of drug-indication records
# - rows: List of records, each with:
#   - maxClinicalStage: Max stage reached for this disease (enum string)
#   - drug: {id, name, drugType, maximumClinicalStage, mechanismsOfAction{rows{actionType, mechanismOfAction, targets}}}
#   - clinicalReports: [{trialPhase, clinicalStage, trialOverallStatus}]
```

**Clinical stage** is an enum string (not an integer):
- `APPROVAL`: Approved drug (the former Phase 4)
- `PHASE_3`: Late-stage clinical trials
- `PHASE_2`: Mid-stage trials
- `PHASE_1`: Early safety trials
- `UNKNOWN`: Stage not recorded

### 6. Get Drug Information

Retrieve detailed drug information including mechanisms and indications.

```python
from scripts.query_opentargets import get_drug_info

drug_info = get_drug_info("CHEMBL25")

# Access:
# - name, synonyms: Drug identifiers
# - drugType: Small molecule, antibody, etc.
# - maximumClinicalStage: Development stage (enum string, e.g. "APPROVAL")
# - mechanismsOfAction.rows: Target(s) and action type
# - indications.rows: Diseases with maxClinicalStage per indication
# - drugWarnings: Toxicity/withdrawal warnings (toxicityClass, description, country, year)
```

### 7. Get All Associations for a Target

Find all diseases associated with a target, optionally filtering by score.

```python
from scripts.query_opentargets import get_target_associations

# Get associations with score >= 0.5
associations = get_target_associations(
    ensembl_id="ENSG00000157764",
    min_score=0.5
)

# Each association contains:
# - disease: {id, name}
# - score: Overall association score (0-1)
# - datatypeScores: Breakdown by evidence type
```

**Association scores:**
- Range: 0-1 (higher = stronger evidence)
- Aggregate evidence across all data types using harmonic sum
- NOT confidence scores but relative ranking metrics
- Under-studied diseases may have lower scores despite good evidence

## GraphQL API Details

**For custom queries beyond the provided helper functions**, use the GraphQL API directly or modify `scripts/query_opentargets.py`.

Key information:
- **Endpoint:** `https://api.platform.opentargets.org/api/v4/graphql`
- **Interactive browser:** `https://api.platform.opentargets.org/api/v4/graphql/browser`
- **No authentication required**
- **Request only needed fields** to minimize response size
- **Use pagination** for large result sets: `page: {index: M, size: N}` — both `index` and `size` are required (non-null)

Refer to `references/api_reference.md` for:
- Complete endpoint documentation
- Example queries for all entity types
- Error handling patterns
- Best practices for API usage

## Best Practices

### Target Prioritization Strategy

When prioritizing drug targets:

1. **Start with genetic evidence:** Human genetics (GWAS, rare variants) provides strongest disease relevance
2. **Check tractability:** Prefer targets with clinical or discovery precedence
3. **Assess safety:** Review safety liabilities, expression patterns, and genetic constraint
4. **Evaluate clinical precedence:** Known drugs indicate druggability and therapeutic window
5. **Consider multiple evidence types:** Convergent evidence from different sources increases confidence
6. **Validate mechanistically:** Pathway evidence and biological plausibility
7. **Review literature manually:** For critical decisions, examine primary publications

### Evidence Interpretation

**Strong evidence indicators:**
- Multiple independent evidence sources
- High genetic association scores (especially GWAS with L2G > 0.5)
- Clinical precedence from approved drugs
- ClinVar pathogenic variants with disease match
- Mouse models with relevant phenotypes

**Caution flags:**
- Single evidence source only
- Text-mining as sole evidence (requires manual validation)
- Conflicting evidence across sources
- High essentiality + ubiquitous expression (poor therapeutic window)
- Multiple safety liabilities

**Score interpretation:**
- Scores rank relative strength, not absolute confidence
- Under-studied diseases have lower scores despite potentially valid targets
- Weight expert-curated sources higher than computational predictions
- Check evidence breakdown, not just overall score

### Common Workflows

**Workflow 1: Target Discovery for a Disease**
1. Search for disease → get EFO ID
2. Query disease info with `include_targets=True`
3. Review top targets sorted by association score
4. For promising targets, get detailed target info
5. Examine evidence types supporting each association
6. Assess tractability and safety for prioritized targets

**Workflow 2: Target Validation**
1. Search for target → get Ensembl ID
2. Get comprehensive target info
3. Check tractability (especially clinical precedence)
4. Review safety liabilities and genetic constraint
5. Examine disease associations to understand biology
6. Look for chemical probes or tool compounds
7. Check known drugs targeting gene for mechanism insights

**Workflow 3: Drug Repurposing**
1. Search for disease → get EFO ID
2. Get known drugs for disease
3. For each drug, get detailed drug info
4. Examine mechanisms of action and targets
5. Look for related disease indications
6. Assess clinical trial phases and status
7. Identify repurposing opportunities based on mechanism

**Workflow 4: Competitive Intelligence**
1. Search for target of interest
2. Get associated diseases with evidence
3. For each disease, get known drugs
4. Review clinical phases and development status
5. Identify competitors and their mechanisms
6. Assess clinical precedence and market landscape

## Resources

### Scripts

**scripts/query_opentargets.py**
Helper functions for common API operations:
- `search_entities()` - Search for targets, diseases, or drugs
- `get_target_info()` - Retrieve target annotations
- `get_disease_info()` - Retrieve disease information
- `get_target_disease_evidence()` - Get supporting evidence
- `get_known_drugs_for_disease()` - Find drugs for a disease
- `get_drug_info()` - Retrieve drug details
- `get_target_associations()` - Get all associations for a target
- `execute_query()` - Execute custom GraphQL queries

### References

**references/api_reference.md**
Complete GraphQL API documentation including:
- Endpoint details and authentication
- Available query types (target, disease, drug, search)
- Example queries for all common operations
- Error handling and best practices
- Data licensing and citation requirements

**references/evidence_types.md**
Comprehensive guide to evidence types and data sources:
- Detailed descriptions of all 7 major evidence types
- Scoring methodologies for each source
- Evidence interpretation guidelines
- Strengths and limitations of each evidence type
- Quality assessment recommendations

**references/target_annotations.md**
Complete target annotation reference:
- 12 major annotation categories explained
- Tractability assessment details
- Safety liability sources
- Expression, essentiality, and constraint data
- Interpretation guidelines for target prioritization
- Red flags and green flags for target assessment

## Data Updates and Versioning

The Open Targets Platform is updated periodically with new data releases. The
GraphQL schema changes between releases — field names and argument names move
(this skill's queries were verified against data version 26.03). If a field
errors, introspect the live schema via the GraphQL browser. Confirm the running
version with the `meta { apiVersion { x y z } dataVersion { year month } }` query.

**Release information:** Check https://platform-docs.opentargets.org/release-notes for the latest updates.

**Citation:** When using Open Targets data, cite:
Ochoa, D. et al. (2025) Open Targets Platform: facilitating therapeutic hypotheses building in drug discovery. Nucleic Acids Research, 53(D1):D1467-D1477.

## Limitations and Considerations

1. **API is for exploratory queries:** For systematic analyses of many targets/diseases, use data downloads or BigQuery
2. **Scores are relative, not absolute:** Association scores rank evidence strength but don't predict clinical success
3. **Under-studied diseases score lower:** Novel or rare diseases may have strong evidence but lower aggregate scores
4. **Evidence quality varies:** Weight expert-curated sources higher than computational predictions
5. **Requires biological interpretation:** Scores and evidence must be interpreted in biological and clinical context
6. **No authentication required:** All data is freely accessible, but cite appropriately

