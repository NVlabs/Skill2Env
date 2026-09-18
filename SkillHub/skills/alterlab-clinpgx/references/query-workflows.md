# ClinPGx Query Workflows

End-to-end workflows and common use cases for ClinPGx. All queries respect the
2 req/sec rate limit — see `rate-limiting-and-error-handling.md`.

**Verified API conventions used throughout**: responses are wrapped as
`{"status", "data"}` (read results from `response.json()["data"]`, never a bare
list); filter genes with `relatedGenes.symbol` and drugs with
`relatedChemicals.name` (`relatedChemicals.symbol` returns `status: "fail"`). The
snippets below show `response.json()` for brevity — unwrap `["data"]` in real
use, or call the helpers in `scripts/query_clinpgx.py`, which unwrap it for you.

## Workflow 1: Clinical Decision Support for Drug Prescription

1. **Identify patient genotype** for relevant pharmacogenes:
   ```python
   # Example: Patient is CYP2C19 *1/*2 (intermediate metabolizer)
   # Star-allele function/definitions come from PharmVar (no /allele resource in the API):
   # https://www.pharmvar.org/gene/CYP2C19
   ```

2. **Find guideline annotations** for the medication of interest:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                          params={"relatedChemicals.name": "clopidogrel"})
   guideline_annotations = response.json()
   # Recommendation: Alternative antiplatelet therapy for IM/PM
   ```

3. **Check drug label** for regulatory guidance:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/data/label",
                          params={"relatedChemicals.name": "clopidogrel"})
   label = response.json()
   ```

## Workflow 2: Gene Panel Analysis

1. **Get list of pharmacogenes** in clinical panel:
   ```python
   pgx_panel = ["CYP2C19", "CYP2D6", "CYP2C9", "TPMT", "DPYD", "SLCO1B1"]
   ```

2. **For each gene, retrieve its guideline annotations**:
   ```python
   all_interactions = {}
   for gene in pgx_panel:
       response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                              params={"relatedGenes.symbol": gene})
       all_interactions[gene] = response.json()
   ```

3. **Review the guideline annotations** returned for each gene:
   ```python
   for gene, annotations in all_interactions.items():
       for ann in annotations:
           print(f"{gene}: {ann.get('name')}")
   ```

4. **Generate patient report** with actionable pharmacogenomic findings.

## Workflow 3: Drug Safety Assessment

1. **Query drug for PGx associations**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/data/chemical",
                          params={"name": "abacavir"})
   drug_id = response.json()["data"][0]['id']
   ```

2. **Get summary annotations**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/data/summaryAnnotation",
                          params={"relatedChemicals.name": "abacavir"})
   annotations = response.json()
   ```

3. **Check for HLA associations** and toxicity risk:
   ```python
   for annotation in annotations:
       if 'HLA' in annotation.get('genes', []):
           print(f"Toxicity risk: {annotation.get('phenotype')}")
   ```

4. **Retrieve screening recommendations** from guidelines and labels.

## Workflow 4: Research Analysis — Population Pharmacogenomics

1. **Get allele frequencies** for population comparison. The ClinPGx API has no
   `/allele` resource; allele definitions and population frequencies are obtained
   from **PharmVar** (https://www.pharmvar.org/), which offers its own
   download/API:
   ```python
   # e.g. PharmVar gene page / downloads for CYP2D6 star-allele frequencies
   # https://www.pharmvar.org/gene/CYP2D6
   alleles = []  # populate from PharmVar data
   ```

2. **Extract population-specific frequencies** from the PharmVar records:
   ```python
   populations = ['European', 'African', 'East Asian', 'Latino']
   frequency_data = {}
   for allele in alleles:
       allele_name = allele['name']
       frequency_data[allele_name] = {
           pop: allele.get(f'{pop}_frequency', 'N/A')
           for pop in populations
       }
   ```

3. **Calculate phenotype distributions** by population:
   ```python
   # Combine allele frequencies with function to predict phenotypes
   phenotype_dist = calculate_phenotype_frequencies(frequency_data)
   ```

4. **Analyze implications** for drug dosing in diverse populations.

## Workflow 5: Literature Evidence Review

1. **Find guideline annotations for the gene-drug relationship**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                          params={"relatedGenes.symbol": "TPMT"})
   guideline_annotations = response.json()
   ```

2. **Retrieve all summary annotations**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/data/summaryAnnotation",
                          params={"relatedGenes.symbol": "TPMT"})
   annotations = response.json()
   ```

3. **Filter by the annotation's level-of-evidence field** (confirm field name
   against the OpenAPI spec):
   ```python
   high_quality = [a for a in annotations
                   if a.get('levelOfEvidence') in ['1A', '1B', '2A']]
   ```

4. **Extract PMIDs** and retrieve full references:
   ```python
   pmids = [a['pmid'] for a in high_quality if 'pmid' in a]
   # Use PubMed skill to retrieve full citations
   ```

## Common Use Cases

### Pre-emptive Pharmacogenomic Testing

Query all clinically actionable gene-drug pairs to guide panel selection:

```python
# List CPIC guideline annotations and derive the actionable gene-drug pairs from them
response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                       params={"source": "CPIC"})
guideline_annotations = response.json()
```

### Medication Therapy Management

Review patient medications against known genotypes:

```python
patient_genes = {"CYP2C19": "*1/*2", "CYP2D6": "*1/*1", "SLCO1B1": "*1/*5"}
medications = ["clopidogrel", "simvastatin", "escitalopram"]

for med in medications:
    response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                           params={"relatedChemicals.name": med})
    guideline_annotations = response.json()
    # Cross-reference returned annotations against patient_genes for dosing guidance
```

### Clinical Trial Eligibility

Screen for pharmacogenomic contraindications:

```python
# Check for HLA-B*57:01 guidance before abacavir trial
response = requests.get("https://api.clinpgx.org/v1/data/guidelineAnnotation",
                       params={"relatedChemicals.name": "abacavir"})
guideline_annotations = response.json()
# CPIC: Do not use if HLA-B*57:01 positive
```
