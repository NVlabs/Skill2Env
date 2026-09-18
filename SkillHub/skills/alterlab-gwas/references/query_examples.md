# GWAS Catalog Query Examples

Code patterns for REST API access, the four canonical query examples, summary-statistics access, cross-referencing, and a complete paginated Python integration.

## REST API Access

The GWAS Catalog provides two REST APIs for programmatic access.

**Base URLs:**
- GWAS Catalog API: `https://www.ebi.ac.uk/gwas/rest/api`
- Summary Statistics API: `https://www.ebi.ac.uk/gwas/summary-statistics/api`

**API Documentation:**
- Main API docs: https://www.ebi.ac.uk/gwas/rest/docs/api
- Summary stats docs: https://www.ebi.ac.uk/gwas/summary-statistics/docs/

**Core Endpoints:**

1. **Studies endpoint** - `/studies/{accessionID}`
   ```python
   import requests

   # Get a specific study
   url = "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   study = response.json()
   ```

2. **Associations endpoint** - `/associations`
   ```python
   # Find associations for a variant
   variant = "rs7903146"
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{variant}/associations"
   params = {"projection": "associationBySnp"}
   response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
   associations = response.json()
   ```

3. **Variants endpoint** - `/singleNucleotidePolymorphisms/{rsID}`
   ```python
   # Get variant details
   url = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/rs7903146"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   variant_info = response.json()
   ```

4. **Traits endpoint** - `/efoTraits/{shortForm}`
   ```python
   # Get trait information (main REST API uses current short-forms, e.g. MONDO_0005148)
   url = "https://www.ebi.ac.uk/gwas/rest/api/efoTraits/MONDO_0005148"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   trait_info = response.json()
   ```

## Query Examples and Patterns

**Example 1: Find all associations for a disease**
```python
import requests

trait = "MONDO_0005148"  # Type 2 diabetes (main REST API short-form; legacy EFO_0001360 404s here)
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# Query associations for this trait
url = f"{base_url}/efoTraits/{trait}/associations"
response = requests.get(url, headers={"Content-Type": "application/json"})
associations = response.json()

# Process results — rsID and risk allele are nested, not top-level
for assoc in associations.get('_embedded', {}).get('associations', []):
    variant = (assoc.get('snps') or [{}])[0].get('rsId')
    pvalue = assoc.get('pvalue')
    risk_allele = ((assoc.get('loci') or [{}])[0]
                   .get('strongestRiskAlleles') or [{}])[0].get('riskAlleleName')
    print(f"{variant}: p={pvalue}, risk allele={risk_allele}")
```

**Example 2: Get variant information and all trait associations**
```python
import requests

variant = "rs7903146"
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# Get variant details
url = f"{base_url}/singleNucleotidePolymorphisms/{variant}"
response = requests.get(url, headers={"Content-Type": "application/json"})
variant_data = response.json()

# Get all associations for this variant
url = f"{base_url}/singleNucleotidePolymorphisms/{variant}/associations"
params = {"projection": "associationBySnp"}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
associations = response.json()

# Extract trait names and p-values — trait name is nested under efoTraits[]
for assoc in associations.get('_embedded', {}).get('associations', []):
    trait = (assoc.get('efoTraits') or [{}])[0].get('trait')
    pvalue = assoc.get('pvalue')
    print(f"Trait: {trait}, p-value: {pvalue}")
```

**Example 3: Access summary statistics**
```python
import requests

# Query summary statistics API
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"

# Find associations by trait with p-value threshold.
# Summary Statistics API keys on the legacy EFO id (the main REST API uses MONDO_0005148).
trait = "EFO_0001360"  # Type 2 diabetes
p_upper = "0.000000001"  # p < 1e-9
url = f"{base_url}/traits/{trait}/associations"
params = {
    "p_upper": p_upper,
    "size": 100  # Number of results
}
response = requests.get(url, params=params)
results = response.json()

# Process genome-wide significant hits
for hit in results.get('_embedded', {}).get('associations', []):
    variant_id = hit.get('variant_id')
    chromosome = hit.get('chromosome')
    position = hit.get('base_pair_location')
    pvalue = hit.get('p_value')
    print(f"{chromosome}:{position} ({variant_id}): p={pvalue}")
```

**Example 4: Query by chromosomal region**
```python
import requests

# Find variants in a specific genomic region
chromosome = "10"
start_pos = 114000000
end_pos = 115000000

base_url = "https://www.ebi.ac.uk/gwas/rest/api"
url = f"{base_url}/singleNucleotidePolymorphisms/search/findByChromBpLocationRange"
params = {
    "chrom": chromosome,
    "bpStart": start_pos,
    "bpEnd": end_pos
}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
variants_in_region = response.json()
```

## Working with Summary Statistics

The GWAS Catalog hosts full summary statistics for many studies, providing access to all tested variants (not just genome-wide significant hits).

**Access Methods:**
1. **FTP download**: http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/
2. **REST API**: Query-based access to summary statistics
3. **Web interface**: Browse and download via the website

**Summary Statistics API Features:**
- Filter by chromosome, position, p-value
- Query specific variants across studies
- Retrieve effect sizes and allele frequencies
- Access harmonized and standardized data

**Example: Download summary statistics for a study**
```python
import requests
import gzip

# Get available summary statistics
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"
url = f"{base_url}/studies/GCST001234"
response = requests.get(url)
study_info = response.json()

# Download link is provided in the response
# Alternatively, use FTP:
# ftp://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCSTXXXXXX/
```

## Data Integration and Cross-referencing

The GWAS Catalog provides links to external resources:

**Genomic Databases:** Ensembl (gene annotations, variant consequences), dbSNP (variant IDs, population frequencies), gnomAD (population allele frequencies).

**Functional Resources:** Open Targets (target-disease associations), PGS Catalog (polygenic risk scores), UCSC Genome Browser (genomic context).

**Phenotype Resources:** EFO (standardized trait terms), OMIM (disease gene relationships), Disease Ontology (disease hierarchies).

**Following Links in API Responses:**
```python
import requests

# API responses include _links for related resources
response = requests.get("https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001234")
study = response.json()

# Follow link to associations
associations_url = study['_links']['associations']['href']
associations_response = requests.get(associations_url)
```

## Complete Python Integration

Paginated query and analysis of GWAS data into a DataFrame:

```python
import requests
import pandas as pd
from time import sleep

def query_gwas_catalog(trait_id, p_threshold=5e-8):
    """
    Query GWAS Catalog for trait associations

    Args:
        trait_id: trait short-form for the main REST API (e.g. 'MONDO_0005148');
                  legacy EFO ids such as EFO_0001360 404 on this API
        p_threshold: P-value threshold for filtering

    Returns:
        pandas DataFrame with association results
    """
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    url = f"{base_url}/efoTraits/{trait_id}/associations"

    headers = {"Content-Type": "application/json"}
    results = []
    page = 0

    while True:
        params = {"page": page, "size": 100}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            break

        data = response.json()
        associations = data.get('_embedded', {}).get('associations', [])

        if not associations:
            break

        for assoc in associations:
            pvalue = assoc.get('pvalue')
            if pvalue and float(pvalue) <= p_threshold:
                # rsID / allele / trait are nested, not top-level
                rs = (assoc.get('snps') or [{}])[0].get('rsId')
                allele = ((assoc.get('loci') or [{}])[0]
                          .get('strongestRiskAlleles') or [{}])[0].get('riskAlleleName')
                trait = (assoc.get('efoTraits') or [{}])[0].get('trait')
                results.append({
                    'variant': rs,
                    'pvalue': pvalue,
                    'risk_allele': allele,
                    'or_beta': assoc.get('orPerCopyNum') or assoc.get('betaNum'),
                    'trait': trait,
                    # follow _links.study.href for accession + PubMed ID
                    'study_href': assoc.get('_links', {}).get('study', {}).get('href'),
                })

        page += 1
        sleep(0.1)  # Rate limiting

    return pd.DataFrame(results)

# Example usage
df = query_gwas_catalog('MONDO_0005148')  # Type 2 diabetes (main REST API short-form)
print(df.head())
print(f"\nTotal associations: {len(df)}")
print(f"Unique variants: {df['variant'].nunique()}")
```
