# ClinPGx API Reference

Complete reference documentation for the ClinPGx REST API.

## Base URL

```
https://api.clinpgx.org/v1/data/
```

**Resource addressing**: ClinPGx objects are addressed by ClinPGx accession IDs in the path (e.g. gene CYP2D6 = `PA128`, CYP2C9 = `PA126`), not by gene symbols or rsIDs. Resolve a symbol or rsID by querying the collection endpoint with parameters (e.g. `GET /v1/data/gene?symbol=CYP2D6`, `GET /v1/data/variant?symbol=rs4244285`) and reading the accession ID from the response.

## Response Envelope (verified)

Every response is a JSON object, never a bare array:

```json
{ "status": "success", "data": [ /* ...records... */ ] }
```

Read results from `response.json()["data"]`. On failure the envelope is
`{"status": "fail", "data": {"errors": [{"message": "No results matching criteria."}]}}`.
A single-object GET (e.g. `/gene/PA128`) returns the object inside `data` as well.

## Filter-Parameter Convention (verified)

- **Genes** filter on `relatedGenes.symbol` (e.g. `CYP2C19`). The `relatedGenes.name` form fails.
- **Chemicals/drugs** filter on `relatedChemicals.name` (e.g. `clopidogrel`). The `relatedChemicals.symbol` form returns `status: "fail"` ("No results matching criteria") — do **not** use it.
- Collection lookups: `gene?symbol=`, `chemical?name=`, `variant?symbol=` or `variant?name=`.

The illustrative `Example Response` blocks below predate this verification and are schematic — trust the envelope/param rules above and the live OpenAPI spec (`https://api.clinpgx.org/`) over the exact field names shown.

## Rate Limiting

- **Maximum rate**: 2 requests per second
- **Enforcement**: Requests exceeding the limit will receive HTTP 429 (Too Many Requests)
- **Best practice**: Implement 500ms delay between requests (0.5 seconds)
- **Recommendation**: For substantial API use, contact api@clinpgx.org

## Authentication

No authentication is required for basic API access. All endpoints are publicly accessible.

## Data License

All data accessed through the API is subject to:
- Creative Commons Attribution-ShareAlike 4.0 International License
- ClinPGx Data Usage Policy

## Response Format

All successful responses return JSON with appropriate HTTP status codes:
- `200 OK`: Successful request
- `404 Not Found`: Resource does not exist
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Core Endpoints

### 1. Gene Endpoint

Retrieve pharmacogene information including function, variants, and clinical significance.

#### Get Gene by Accession ID

```http
GET /v1/data/gene/{gene_id}
```

**Parameters:**
- `gene_id` (path, required): ClinPGx gene accession ID (e.g., PA128 for CYP2D6, PA126 for CYP2C9)

**Example Request:**
```bash
curl "https://api.clinpgx.org/v1/data/gene/PA128"
```

**Example Response:**
```json
{
  "id": "PA128",
  "symbol": "CYP2D6",
  "name": "cytochrome P450 family 2 subfamily D member 6",
  "chromosome": "22",
  "chromosomeLocation": "22q13.2",
  "function": "Drug metabolism",
  "description": "Highly polymorphic gene encoding enzyme...",
  "clinicalAnnotations": [...],
  "relatedDrugs": [...]
}
```

#### Resolve / Search Genes by Symbol

```http
GET /v1/data/gene?symbol={gene_symbol}
```

**Parameters:**
- `symbol` (query): Gene symbol to resolve to its accession ID (e.g., CYP2D6)

**Example:**
```bash
curl "https://api.clinpgx.org/v1/data/gene?symbol=CYP2D6"
```

### 2. Chemical/Drug Endpoint

Access drug and chemical compound information including pharmacogenomic annotations.

#### Get Drug by ID

```http
GET /v1/data/chemical/{drug_id}
```

**Parameters:**
- `drug_id` (path, required): ClinPGx drug accession ID (e.g., PA451906 for warfarin)

**Example Request:**
```bash
curl "https://api.clinpgx.org/v1/data/chemical/PA451906"
```

#### Search Drugs by Name

```http
GET /v1/data/chemical?name={drug_name}
```

**Parameters:**
- `name` (query, optional): Drug name or synonym

**Example:**
```bash
curl "https://api.clinpgx.org/v1/data/chemical?name=warfarin"
```

**Example Response:**
```json
[
  {
    "id": "PA451906",
    "name": "warfarin",
    "genericNames": ["warfarin sodium"],
    "tradeNames": ["Coumadin", "Jantoven"],
    "drugClasses": ["Anticoagulants"],
    "indication": "Prevention of thrombosis",
    "relatedGenes": ["CYP2C9", "VKORC1", "CYP4F2"]
  }
]
```

### 3. Gene-Drug Relationships (no single pair endpoint)

The public ClinPGx API does **not** provide a `geneDrugPair` endpoint. Gene-drug relationships are derived from guideline annotations, or fetched via the pair report endpoint when both object accession IDs are known.

#### Derive from Guideline Annotations

```http
GET /v1/data/guidelineAnnotation?relatedGenes.symbol={gene}
GET /v1/data/guidelineAnnotation?relatedChemicals.name={drug}
```

**Example Requests:**
```bash
# Guideline annotations related to a gene
curl "https://api.clinpgx.org/v1/data/guidelineAnnotation?relatedGenes.symbol=CYP2D6"

# Guideline annotations related to a drug
curl "https://api.clinpgx.org/v1/data/guidelineAnnotation?relatedChemicals.name=codeine"
```

#### Pair Report Endpoint

```http
GET /report/pair/{firstObjId}/{secondObjId}/{resultType}
```

**Parameters:**
- `firstObjId` (path): Accession ID of the first object (e.g., gene PA128)
- `secondObjId` (path): Accession ID of the second object (e.g., chemical PA449088)
- `resultType` (path): Report type (e.g., `guidelineAnnotation`)

**Example:**
```bash
curl "https://api.clinpgx.org/v1/report/pair/PA128/PA449088/guidelineAnnotation"
```

### 4. Guideline Annotation Endpoint

Access clinical practice guideline annotations from CPIC, DPWG, and other sources.

#### Get Guideline Annotations

```http
GET /v1/data/guidelineAnnotation?source={source}&relatedGenes.symbol={gene}&relatedChemicals.name={drug}
```

**Parameters:**
- `source` (query, optional): Guideline source (CPIC, DPWG, FDA)
- `relatedGenes.symbol` (query, optional): Gene symbol
- `relatedChemicals.name` (query, optional): Drug name/symbol

**Example Requests:**
```bash
# Get all CPIC guideline annotations
curl "https://api.clinpgx.org/v1/data/guidelineAnnotation?source=CPIC"

# Get guideline annotations for a specific gene
curl "https://api.clinpgx.org/v1/data/guidelineAnnotation?relatedGenes.symbol=CYP2C19"
```

#### Get Guideline Annotation by ID

```http
GET /v1/data/guidelineAnnotation/{guideline_id}
```

**Example:**
```bash
curl "https://api.clinpgx.org/v1/data/guidelineAnnotation/PA166104939"
```

**Example Response:**
```json
{
  "id": "PA166104939",
  "name": "CPIC Guideline for CYP2C19 and Clopidogrel",
  "source": "CPIC",
  "genes": ["CYP2C19"],
  "drugs": ["clopidogrel"],
  "recommendationLevel": "A",
  "lastUpdated": "2023-08-01",
  "summary": "Alternative antiplatelet therapy recommended for...",
  "recommendations": [...],
  "pdfUrl": "https://www.clinpgx.org/...",
  "pmid": "23400754"
}
```

### 5. Alleles (no /allele resource in the public API)

The public ClinPGx API does **not** expose an `/allele` resource. Canonical star-allele definitions, functional status, activity scores, and population frequencies are maintained by **PharmVar** (https://www.pharmvar.org/), which provides its own gene pages, downloads, and API. Allele-level clinical implications are surfaced through ClinPGx guideline annotations.

**For star-allele data**, use PharmVar:
```bash
# e.g. CYP2D6 star-allele definitions and frequencies
# https://www.pharmvar.org/gene/CYP2D6
```

**For allele-related clinical guidance**, use the guideline annotation endpoint:
```bash
curl "https://api.clinpgx.org/v1/data/guidelineAnnotation?relatedGenes.symbol=CYP2D6"
```

### 6. Variant Endpoint

Search for genetic variants and their pharmacogenomic annotations.

#### Resolve Variant by rsID

The path form `/variant/{id}` expects a ClinPGx accession ID, so resolve an rsID via the collection endpoint and read the accession ID from the response.

```http
GET /v1/data/variant?symbol={rsid}
```

**Parameters:**
- `symbol` (query): dbSNP reference SNP ID (e.g., rs4244285)

**Example Request:**
```bash
curl "https://api.clinpgx.org/v1/data/variant?symbol=rs4244285"
```

#### Get Variant by Accession ID

```http
GET /v1/data/variant/{variant_id}
```

**Parameters:**
- `variant_id` (path, required): ClinPGx variant accession ID

**Example:**
```bash
curl "https://api.clinpgx.org/v1/data/variant/{variant_id}"
```

### 7. Annotation Endpoints

Access curated literature annotations for gene-drug-phenotype relationships. ClinPGx serves these through the `summaryAnnotation`, `variantAnnotation`, and `dataAnnotation` collections depending on annotation type. Query parameter names (including any level-of-evidence filter) should be confirmed against the live OpenAPI spec.

#### Get Summary Annotations

```http
GET /v1/data/summaryAnnotation?relatedGenes.symbol={gene}&relatedChemicals.name={drug}
```

**Parameters:**
- `relatedGenes.symbol` (query, optional): Gene symbol
- `relatedChemicals.name` (query, optional): Drug name/symbol

**Example Requests:**
```bash
# Summary annotations related to a gene
curl "https://api.clinpgx.org/v1/data/summaryAnnotation?relatedGenes.symbol=CYP2D6"

# Variant-level annotations related to a gene
curl "https://api.clinpgx.org/v1/data/variantAnnotation?relatedGenes.symbol=TPMT"
```

**Example Response:**
```json
[
  {
    "id": "PA166153683",
    "gene": "CYP2D6",
    "drug": "codeine",
    "phenotype": "Reduced analgesic effect",
    "evidenceLevel": "1A",
    "annotation": "Poor metabolizers have reduced conversion...",
    "pmid": "24618998",
    "studyType": "Clinical trial",
    "population": "European",
    "sources": ["CPIC"]
  }
]
```

**Evidence Levels:**
- **1A**: High-quality evidence from guidelines (CPIC, FDA, DPWG)
- **1B**: High-quality evidence not yet guideline
- **2A**: Moderate evidence from well-designed studies
- **2B**: Moderate evidence with some limitations
- **3**: Limited or conflicting evidence
- **4**: Case reports or weak evidence

### 8. Label Endpoint

Retrieve regulatory drug label information with pharmacogenomic content.

#### Get Labels

```http
GET /v1/data/label?relatedChemicals.name={drug_name}&source={source}
```

**Parameters:**
- `relatedChemicals.name` (query): Drug name/symbol
- `source` (query, optional): Regulatory source (FDA, EMA, PMDA, Health Canada)

**Example Requests:**
```bash
# Get all labels for warfarin
curl "https://api.clinpgx.org/v1/data/label?relatedChemicals.name=warfarin"

# Get only FDA labels
curl "https://api.clinpgx.org/v1/data/label?relatedChemicals.name=warfarin&source=FDA"
```

**Example Response:**
```json
[
  {
    "id": "DL001234",
    "drug": "warfarin",
    "source": "FDA",
    "sections": {
      "testing": "Consider CYP2C9 and VKORC1 genotyping...",
      "dosing": "Dose adjustment based on genotype...",
      "warnings": "Risk of bleeding in certain genotypes"
    },
    "biomarkers": ["CYP2C9", "VKORC1"],
    "testingRecommended": true,
    "labelUrl": "https://dailymed.nlm.nih.gov/...",
    "lastUpdated": "2024-01-15"
  }
]
```

### 9. Pathway Endpoint

Access pharmacokinetic and pharmacodynamic pathway diagrams and information.

#### Get Pathway by ID

```http
GET /v1/data/pathway/{pathway_id}
```

**Parameters:**
- `pathway_id` (path, required): ClinPGx pathway accession ID

**Example:**
```bash
curl "https://api.clinpgx.org/v1/data/pathway/PA146123006"
```

#### Search Pathways

```http
GET /v1/data/pathway?relatedChemicals.name={drug_name}&relatedGenes.symbol={gene}
```

**Parameters:**
- `relatedChemicals.name` (query, optional): Drug name/symbol
- `relatedGenes.symbol` (query, optional): Gene symbol

**Example:**
```bash
curl "https://api.clinpgx.org/v1/data/pathway?relatedChemicals.name=warfarin"
```

**Example Response:**
```json
{
  "id": "PA146123006",
  "name": "Warfarin Pharmacokinetics and Pharmacodynamics",
  "drugs": ["warfarin"],
  "genes": ["CYP2C9", "VKORC1", "CYP4F2", "GGCX"],
  "description": "Warfarin is metabolized primarily by CYP2C9...",
  "diagramUrl": "https://www.clinpgx.org/pathway/...",
  "steps": [
    {
      "step": 1,
      "process": "Absorption",
      "genes": []
    },
    {
      "step": 2,
      "process": "Metabolism",
      "genes": ["CYP2C9", "CYP2C19"]
    },
    {
      "step": 3,
      "process": "Target interaction",
      "genes": ["VKORC1"]
    }
  ]
}
```

## Query Patterns and Examples

### Common Query Patterns

#### 1. Patient Medication Review

Find guideline annotations for a patient's medications:

```python
import requests

patient_meds = ["clopidogrel", "simvastatin", "codeine"]
patient_genes = {"CYP2C19": "*1/*2", "CYP2D6": "*1/*1", "SLCO1B1": "*1/*5"}

for med in patient_meds:
    response = requests.get(
        "https://api.clinpgx.org/v1/data/guidelineAnnotation",
        params={"relatedChemicals.name": med}
    )
    guideline_annotations = response.json()
    # Cross-reference returned annotations against patient_genes
```

#### 2. Actionable Gene Panel

Find genes with CPIC guideline annotations:

```python
response = requests.get(
    "https://api.clinpgx.org/v1/data/guidelineAnnotation",
    params={"source": "CPIC"}
)
guideline_annotations = response.json()

# Enumerate genes from each annotation's relatedGenes
genes = set()
for ann in guideline_annotations:
    for g in ann.get("relatedGenes", []):
        genes.add(g.get("symbol"))
print(f"Panel should include: {sorted(genes)}")
```

#### 3. Population Frequency Analysis

Compare allele frequencies across populations. The ClinPGx API has no `/allele` resource; obtain star-allele definitions and frequencies from **PharmVar** (https://www.pharmvar.org/):

```python
# Populate from PharmVar gene data, e.g. https://www.pharmvar.org/gene/CYP2D6
alleles = []  # list of allele records from PharmVar

# Calculate phenotype frequencies
pm_freq = {}  # Poor metabolizer frequencies
for allele in alleles:
    if allele['function'] == 'No function':
        for pop, freq in allele['frequencies'].items():
            pm_freq[pop] = pm_freq.get(pop, 0) + freq
```

#### 4. Drug Safety Screen

Check for high-risk gene-drug associations via guideline annotations:

```python
# Screen for HLA-B*57:01 guidance before abacavir
response = requests.get(
    "https://api.clinpgx.org/v1/data/guidelineAnnotation",
    params={"relatedChemicals.name": "abacavir"}
)
guideline_annotations = response.json()
# CPIC: Do not use if HLA-B*57:01 positive
```

## Error Handling

### Common Error Responses

#### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "Gene 'INVALID' does not exist"
}
```

#### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 2 requests per second allowed"
}
```

### Recommended Error Handling Pattern

```python
import requests
import time

def safe_query(url, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                time.sleep(0.5)  # Rate limiting
                return response.json()
            elif response.status_code == 429:
                wait = 2 ** attempt
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif response.status_code == 404:
                print("Resource not found")
                return None
            else:
                response.raise_for_status()

        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise

    return None
```

## Best Practices

### Rate Limiting
- Implement 500ms delay between requests (2 requests/second maximum)
- Use exponential backoff for rate limit errors
- Consider caching results for frequently accessed data
- For bulk operations, contact api@clinpgx.org

### Caching Strategy
```python
import json
from pathlib import Path

def cached_query(cache_file, query_func, *args, **kwargs):
    cache_path = Path(cache_file)

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    result = query_func(*args, **kwargs)

    if result:
        with open(cache_path, 'w') as f:
            json.dump(result, f)

    return result
```

### Batch Processing
```python
import time

def batch_gene_query(genes, delay=0.5):
    results = {}
    for gene in genes:
        # Resolve each symbol via the collection endpoint (path takes an accession ID)
        response = requests.get(
            "https://api.clinpgx.org/v1/data/gene", params={"symbol": gene}
        )
        if response.status_code == 200:
            results[gene] = response.json()
        time.sleep(delay)
    return results
```

## Data Schema Definitions

### Gene Object
```typescript
{
  id: string;              // ClinPGx gene ID
  symbol: string;          // HGNC gene symbol
  name: string;            // Full gene name
  chromosome: string;      // Chromosome location
  function: string;        // Pharmacogenomic function
  clinicalAnnotations: number;  // Count of annotations
  relatedDrugs: string[];  // Associated drugs
}
```

### Drug Object
```typescript
{
  id: string;              // ClinPGx drug ID
  name: string;            // Generic name
  tradeNames: string[];    // Brand names
  drugClasses: string[];   // Therapeutic classes
  indication: string;      // Primary indication
  relatedGenes: string[];  // Pharmacogenes
}
```

### Gene-Drug Relationship (derived, not a single endpoint object)

There is no `geneDrugPair` resource. Relationships are derived from guideline
annotations; inspect each annotation's `relatedGenes` and `relatedChemicals`
fields together with its source and level-of-evidence fields (confirm exact
field names against the live OpenAPI spec).

### Allele Object (PharmVar, not the ClinPGx API)

Star-allele records are served by PharmVar (https://www.pharmvar.org/), not by
the ClinPGx API. Refer to the PharmVar schema for the authoritative shape of
allele name, function, activity score, population frequencies, and defining
variants.

## API Stability and Versioning

### Current Status
- API version: v1
- Stability: Beta - endpoints stable, parameters may change
- Monitor: https://blog.clinpgx.org/ for updates

### Migration from PharmGKB
As of July 2025, PharmGKB URLs redirect to ClinPGx. Update references:
- Old: `https://api.pharmgkb.org/`
- New: `https://api.clinpgx.org/`

### Future Changes
- Watch for API v2 announcements
- Breaking changes will be announced on ClinPGx Blog
- Consider version pinning for production applications

## Support and Contact

- **API Issues**: api@clinpgx.org
- **Documentation**: https://api.clinpgx.org/
- **General Questions**: https://www.clinpgx.org/page/faqs
- **Blog**: https://blog.clinpgx.org/
- **CPIC Guidelines**: https://cpicpgx.org/

## Related Resources

- **PharmCAT**: Pharmacogenomic variant calling and annotation tool
- **PharmVar**: Pharmacogene allele nomenclature database
- **CPIC**: Clinical Pharmacogenetics Implementation Consortium
- **DPWG**: Dutch Pharmacogenetics Working Group
- **ClinGen**: Clinical Genome Resource
