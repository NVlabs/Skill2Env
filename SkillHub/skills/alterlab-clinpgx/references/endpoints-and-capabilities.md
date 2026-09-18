# ClinPGx Endpoints and Core Capabilities

Worked code for each of the nine ClinPGx capability areas. See
`api_reference.md` for the complete endpoint/parameter listing.

**Resource addressing reminder**: ClinPGx resources are addressed by ClinPGx
accession IDs in the path (e.g. gene CYP2D6 = `PA128`, CYP2C9 = `PA126`), not by
gene symbols or rsIDs. To resolve a symbol or rsID, query the collection
endpoint with parameters (e.g. `GET /v1/data/gene?symbol=CYP2D6`,
`GET /v1/data/variant?symbol=rs4244285`) and read the accession ID from the
response.

**Response/param reminder** (verified): every response is wrapped as
`{"status": "success"|"fail", "data": [...]}`, so read records from
`response.json()["data"]` — it is never a bare list. Filter genes with
`relatedGenes.symbol` but drugs with `relatedChemicals.name`
(`relatedChemicals.symbol` returns `status: "fail"`). The snippets below call
`response.json()` for brevity; unwrap `["data"]` in real use (the helpers in
`scripts/query_clinpgx.py` do this for you).

Base URL: `https://api.clinpgx.org/v1/data/`

## 1. Gene Queries

Retrieve gene function, clinical annotations, and pharmacogenomic significance:

```python
import requests

# Resolve a gene symbol to its ClinPGx record (accession ID is in the response)
response = requests.get("https://api.clinpgx.org/v1/data/gene",
                       params={"symbol": "CYP2D6"})
genes = response.json()

# Get gene details directly by accession ID (CYP2D6 = PA128)
response = requests.get("https://api.clinpgx.org/v1/data/gene/PA128")
gene_data = response.json()
```

**Key pharmacogenes:**
- **CYP450 enzymes**: CYP2D6, CYP2C19, CYP2C9, CYP3A4, CYP3A5
- **Transporters**: SLCO1B1, ABCB1, ABCG2
- **Other metabolizers**: TPMT, DPYD, NUDT15, UGT1A1
- **Receptors**: OPRM1, HTR2A, ADRB1
- **HLA genes**: HLA-B, HLA-A

## 2. Drug and Chemical Queries

Retrieve drug information including pharmacogenomic annotations and mechanisms:

```python
# Get drug details by ClinPGx accession ID (response is {"status","data"})
response = requests.get("https://api.clinpgx.org/v1/data/chemical/PA451906")  # Warfarin
drug_data = response.json()["data"]

# Search drugs by name (filter chemicals by .name, not .symbol)
response = requests.get("https://api.clinpgx.org/v1/data/chemical",
                       params={"name": "warfarin"})
drugs = response.json()["data"]
```

**Drug categories with pharmacogenomic significance:**
- Anticoagulants (warfarin, clopidogrel)
- Antidepressants (SSRIs, TCAs)
- Immunosuppressants (tacrolimus, azathioprine)
- Oncology drugs (5-fluorouracil, irinotecan, tamoxifen)
- Cardiovascular drugs (statins, beta-blockers)
- Pain medications (codeine, tramadol)
- Antivirals (abacavir)

## 3. Gene-Drug Pair Queries

There is no single gene-drug-pair endpoint in the public API; derive pairs from
guideline annotations, or use the pair report endpoint when you have both object
accession IDs:

```python
# Derive gene-drug relationships from guideline annotations
response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                       params={"relatedChemicals.name": "codeine"})
guideline_annotations = response.json()

# Pair report endpoint (requires accession IDs for both objects)
# /report/pair/{firstObjId}/{secondObjId}/{resultType}
response = requests.get(
    "https://api.clinpgx.org/v1/report/pair/PA128/PA449088/guidelineAnnotation"
)
pair_report = response.json()
```

**Clinical annotation sources:**
- CPIC (Clinical Pharmacogenetics Implementation Consortium)
- DPWG (Dutch Pharmacogenetics Working Group)
- FDA (Food and Drug Administration) labels
- Peer-reviewed literature summary annotations

## 4. CPIC Guidelines

Access evidence-based clinical practice guidelines:

```python
# Get a guideline annotation by accession ID
response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation/PA166104939")
guideline = response.json()

# List guideline annotations from a given source
response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                       params={"source": "CPIC"})
guidelines = response.json()
```

**CPIC guideline components:** gene-drug pairs covered, clinical recommendations
by phenotype, evidence levels and strength ratings, supporting literature,
downloadable PDFs and supplementary materials, and implementation considerations.

**Example guidelines:**
- CYP2D6-codeine (avoid in ultra-rapid metabolizers)
- CYP2C19-clopidogrel (alternative therapy for poor metabolizers)
- TPMT-azathioprine (dose reduction for intermediate/poor metabolizers)
- DPYD-fluoropyrimidines (dose adjustment based on activity)
- HLA-B*57:01-abacavir (avoid if positive)

## 5. Allele and Variant Information

The public ClinPGx API does **not** expose a dedicated `/allele` resource.
Star-allele definitions, functional status, and population frequencies are
maintained by **PharmVar** (https://www.pharmvar.org/); allele-level clinical
implications are surfaced through guideline annotations:

```python
# Allele function / phenotype implications come through guideline annotations
response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                       params={"relatedGenes.symbol": "CYP2D6"})
guideline_annotations = response.json()

# For canonical star-allele definitions and frequencies, use PharmVar:
# https://www.pharmvar.org/gene/CYP2D6
```

**Allele information (via PharmVar / guideline annotations) includes:**
functional status (normal, decreased, no function, increased, uncertain),
population frequencies across ethnic groups, defining variants (SNPs, indels,
CNVs), phenotype assignment, and references to PharmVar and other nomenclature
systems.

**Phenotype categories:**
- **Ultra-rapid metabolizer** (UM): Increased enzyme activity
- **Normal metabolizer** (NM): Normal enzyme activity
- **Intermediate metabolizer** (IM): Reduced enzyme activity
- **Poor metabolizer** (PM): Little to no enzyme activity

## 6. Variant Annotations

Access clinical annotations for specific genetic variants:

```python
# Resolve an rsID to its ClinPGx variant record (accession ID is in the response)
response = requests.get("https://api.clinpgx.org/v1/data/variant",
                       params={"symbol": "rs4244285"})
variants = response.json()

# Then fetch the full record directly by its accession ID, e.g.:
#   requests.get(f"https://api.clinpgx.org/v1/data/variant/{variants[0]['id']}")
```

**Variant data includes:** rsID and genomic coordinates, gene and functional
consequence, allele associations, clinical significance, population frequencies,
and literature references.

## 7. Clinical Annotations

Curated literature annotations (formerly PharmGKB clinical annotations) are
served by the annotation collections `summaryAnnotation`, `variantAnnotation`,
and `dataAnnotation` depending on annotation type:

```python
# Get summary (clinical) annotations related to a gene
response = requests.get("https://api.clinpgx.org/v1/data/summaryAnnotation",
                       params={"relatedGenes.symbol": "CYP2D6"})
annotations = response.json()

# Variant-level annotations
response = requests.get("https://api.clinpgx.org/v1/data/variantAnnotation",
                       params={"relatedGenes.symbol": "CYP2D6"})
variant_annotations = response.json()
```

Confirm the exact query parameter names and any evidence-level filters against
the live OpenAPI spec before relying on them in production.

**Evidence levels** (highest to lowest):
- **Level 1A**: High-quality evidence, CPIC/FDA/DPWG guidelines
- **Level 1B**: High-quality evidence, not yet guideline
- **Level 2A**: Moderate evidence from well-designed studies
- **Level 2B**: Moderate evidence with some limitations
- **Level 3**: Limited or conflicting evidence
- **Level 4**: Case reports or weak evidence

## 8. Drug Labels

Access pharmacogenomic information from drug labels:

```python
# Get drug labels with PGx information
response = requests.get("https://api.clinpgx.org/v1/data/label",
                       params={"relatedChemicals.name": "warfarin"})
labels = response.json()

# Filter by regulatory source
response = requests.get("https://api.clinpgx.org/v1/data/label",
                       params={"source": "FDA"})
fda_labels = response.json()
```

**Label information includes:** testing recommendations, dosing guidance by
genotype, warnings and precautions, biomarker information, and regulatory source
(FDA, EMA, PMDA, etc.).

## 9. Pathways

Explore pharmacokinetic and pharmacodynamic pathways:

```python
# Get pathway information by accession ID
response = requests.get("https://api.clinpgx.org/v1/data/pathway/PA146123006")  # Warfarin pathway
pathway_data = response.json()

# Search pathways related to a drug
response = requests.get("https://api.clinpgx.org/v1/data/pathway",
                       params={"relatedChemicals.name": "warfarin"})
pathways = response.json()
```

**Pathway diagrams** show: drug metabolism steps, enzymes and transporters
involved, gene variants affecting each step, downstream effects on
efficacy/toxicity, and interactions with other pathways.
