# Open Targets Platform API Reference

## API Endpoint

```
https://api.platform.opentargets.org/api/v4/graphql
```

Interactive GraphQL playground with documentation:
```
https://api.platform.opentargets.org/api/v4/graphql/browser
```

## Access Methods

The Open Targets Platform provides multiple access methods:

1. **GraphQL API** - Best for single entity queries and flexible data retrieval
2. **Web Interface** - Interactive platform at https://platform.opentargets.org
3. **Data Downloads** - FTP at https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/
4. **Google BigQuery** - For large-scale systematic queries

## Authentication

No authentication is required for the GraphQL API. All data is freely accessible.

## Schema Versioning

The GraphQL schema changes between quarterly releases — field and argument names
move. The queries below were verified against data version **26.03**. Confirm the
running version and introspect when a field errors:

```graphql
query { meta { name apiVersion { x y z } dataVersion { year month iteration } } }
```

Notable recent changes reflected below: `Pagination` requires both `index` and
`size`; disease/target `knownDrugs` was replaced by `drugAndClinicalCandidates`;
`datatypeScores`/`ScoredComponent` uses `id` (not `componentId`); the `evidences`
query filters by `datasourceIds` (not `datatypes`); `Drug.maximumClinicalTrialPhase`
became `maximumClinicalStage` (enum string), and `Drug.indications`/`mechanismsOfAction`
are now paginated (`rows`).

## Rate Limits

For systematic queries involving multiple targets or diseases, use dataset downloads or BigQuery instead of repeated API calls. The API is optimized for single-entity and exploratory queries.

## GraphQL Query Structure

GraphQL queries consist of:
1. Query operation with optional variables
2. Field selection (request only needed fields)
3. Nested entity traversal

### Basic Python Example

```python
import requests
import json

# Define the query
query_string = """
  query target($ensemblId: String!){
    target(ensemblId: $ensemblId){
      id
      approvedSymbol
      biotype
      geneticConstraint {
        constraintType
        exp
        obs
        score
      }
    }
  }
"""

# Define variables
variables = {"ensemblId": "ENSG00000169083"}

# Make the request
base_url = "https://api.platform.opentargets.org/api/v4/graphql"
response = requests.post(base_url, json={"query": query_string, "variables": variables})
data = json.loads(response.text)
print(data)
```

## Available Query Endpoints

### /target
Retrieve gene annotations, tractability assessments, and disease associations.

**Common fields:**
- `id` - Ensembl gene ID
- `approvedSymbol` - HGNC gene symbol
- `approvedName` - Full gene name
- `biotype` - Gene type (protein_coding, etc.)
- `tractability` - Druggability assessment
- `safetyLiabilities` - Safety information
- `expressions` - Baseline expression data
- `drugAndClinicalCandidates` - Approved/clinical drugs (replaces the former `knownDrugs`)
- `associatedDiseases` - Disease associations with evidence

### /disease
Retrieve disease/phenotype data, known drugs, and clinical information.

**Common fields:**
- `id` - Disease identifier (EFO, MONDO, HP, Orphanet)
- `name` - Disease name
- `description` - Disease description
- `therapeuticAreas` - High-level disease categories
- `synonyms` - Alternative names
- `drugAndClinicalCandidates` - Drugs indicated for disease (replaces the former `knownDrugs`)
- `associatedTargets` - Target associations with evidence

### /drug
Retrieve compound details, mechanisms of action, and pharmacovigilance data.

**Common fields:**
- `id` - ChEMBL identifier
- `name` - Drug name
- `drugType` - Small molecule, antibody, etc.
- `maximumClinicalStage` - Development stage (enum string, e.g. "APPROVAL", "PHASE_3")
- `indications` - Disease indications (paginated: `indications { rows { ... } }`)
- `mechanismsOfAction` - Target mechanisms (paginated: `mechanismsOfAction { rows { ... } }`)
- `drugWarnings` - Withdrawal/toxicity warnings
- `adverseEvents` - Pharmacovigilance data

### /search
Search across all entities (targets, diseases, drugs).

**Parameters:**
- `queryString` - Search term
- `entityNames` - Filter by entity type(s)
- `page` - Pagination

### Indirect associations
There is no separate endpoint for indirect associations. To include evidence
propagated from disease descendants in the ontology, pass `enableIndirect: true`
to `associatedTargets`, `associatedDiseases`, or `evidences`, e.g.
`associatedTargets(enableIndirect: true, page: {index: 0, size: 50})`.

Other root query fields include `targets`/`diseases`/`drugs` (batch by ID list),
`facets`, `mapIds`, and `variant`/`study`/`credibleSet` (genetics).

## Example Queries

### Query 1: Get target information with disease associations

```python
query = """
  query targetInfo($ensemblId: String!) {
    target(ensemblId: $ensemblId) {
      approvedSymbol
      approvedName
      tractability {
        label
        modality
        value
      }
      associatedDiseases(page: {index: 0, size: 10}) {
        rows {
          disease {
            name
          }
          score
          datatypeScores {
            id
            score
          }
        }
      }
    }
  }
"""
variables = {"ensemblId": "ENSG00000157764"}
```

### Query 2: Search for diseases

```python
query = """
  query searchDiseases($queryString: String!) {
    search(queryString: $queryString, entityNames: ["disease"], page: {index: 0, size: 10}) {
      hits {
        id
        entity
        name
        description
      }
    }
  }
"""
variables = {"queryString": "alzheimer"}
# Returns e.g. {"id": "MONDO_0004975", "name": "Alzheimer disease", ...}
```

### Query 3: Get evidence for target-disease pair

```python
query = """
  query evidences($ensemblId: String!, $efoId: String!) {
    disease(efoId: $efoId) {
      evidences(ensemblIds: [$ensemblId], size: 100) {
        rows {
          datasourceId
          datatypeId
          score
          studyId
          literature
        }
      }
    }
  }
"""
# To narrow at the API, add `datasourceIds: ["gwas_catalog", ...]` (filters by
# data source, not data type). Otherwise filter rows client-side on datatypeId.
variables = {"ensemblId": "ENSG00000157764", "efoId": "MONDO_0004975"}
```

### Query 4: Get known drugs / clinical candidates for a disease

```python
query = """
  query drugCandidates($efoId: String!) {
    disease(efoId: $efoId) {
      drugAndClinicalCandidates {
        count
        rows {
          maxClinicalStage
          drug {
            id
            name
            mechanismsOfAction {
              rows {
                mechanismOfAction
                targets { approvedSymbol }
              }
            }
          }
          clinicalReports {
            trialPhase
            trialOverallStatus
          }
        }
      }
    }
  }
"""
variables = {"efoId": "MONDO_0004975"}
```

## Error Handling

GraphQL returns status code 200 even for errors. Check the response structure:

```python
if 'errors' in response_data:
    print(f"GraphQL errors: {response_data['errors']}")
else:
    print(f"Data: {response_data['data']}")
```

## Best Practices

1. **Request only needed fields** - Minimize data transfer and improve response time
2. **Use variables** - Make queries reusable and safer
3. **Handle pagination** - Most list fields support pagination with `page: {size: N, index: M}`
4. **Explore the schema** - Use the GraphQL browser to discover available fields
5. **Batch related queries** - Combine multiple entity fetches in a single query when possible
6. **Cache results** - Store frequently accessed data locally to reduce API calls
7. **Use BigQuery for bulk** - Switch to BigQuery/downloads for systematic analyses

## Data Licensing

All Open Targets Platform data is freely available. When using the data in research or commercial products, cite the latest publication:

Ochoa, D. et al. (2025) Open Targets Platform: facilitating therapeutic hypotheses building in drug discovery. Nucleic Acids Research, 53(D1):D1467-D1477.
