# NCBI Gene API Reference

This document provides detailed API documentation for accessing NCBI Gene database programmatically.

## Table of Contents

1. [E-utilities API](#e-utilities-api)
2. [NCBI Datasets API](#ncbi-datasets-api)
3. [Authentication and Rate Limits](#authentication-and-rate-limits)
4. [Error Handling](#error-handling)

---

## E-utilities API

E-utilities (Entrez Programming Utilities) provide a stable interface to NCBI's Entrez databases.

### Base URL

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

### Common Parameters

- `db` - Database name (use `gene` for Gene database)
- `api_key` - API key for higher rate limits
- `retmode` - Return format (json, xml, text)
- `retmax` - Maximum number of records to return

### ESearch - Search Database

Search for genes matching a text query.

**Endpoint:** `esearch.fcgi`

**Parameters:**
- `db=gene` (required) - Database to search
- `term` (required) - Search query
- `retmax` - Maximum results (default: 20)
- `retmode` - json or xml (default: xml)
- `usehistory=y` - Store results on history server for large result sets

**Query Syntax:**
- Gene symbol: `BRCA1[gene]` or `BRCA1[gene name]`
- Organism: `human[organism]` or `9606[taxid]`
- Combine terms: `BRCA1[gene] AND human[organism]`
- Disease: `muscular dystrophy[disease]`
- Chromosome: `17q21[chromosome]`
- GO terms: `GO:0006915[biological process]`

**Example Request:**

```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=BRCA1[gene]+AND+human[organism]&retmode=json"
```

**Response Format (JSON):**

```json
{
  "esearchresult": {
    "count": "1",
    "retmax": "1",
    "retstart": "0",
    "idlist": ["672"],
    "translationset": [],
    "querytranslation": "BRCA1[Gene Name] AND human[Organism]"
  }
}
```

### ESummary - Document Summaries

Retrieve document summaries for Gene IDs.

**Endpoint:** `esummary.fcgi`

**Parameters:**
- `db=gene` (required) - Database
- `id` (required) - Comma-separated Gene IDs (up to 500)
- `retmode` - json or xml (default: xml)

**Example Request:**

```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=672&retmode=json"
```

**Response Format (JSON):**

```json
{
  "result": {
    "672": {
      "uid": "672",
      "name": "BRCA1",
      "description": "BRCA1 DNA repair associated",
      "organism": {
        "scientificname": "Homo sapiens",
        "commonname": "human",
        "taxid": 9606
      },
      "chromosome": "17",
      "geneticsource": "genomic",
      "maplocation": "17q21.31",
      "nomenclaturesymbol": "BRCA1",
      "nomenclaturename": "BRCA1 DNA repair associated"
    }
  }
}
```

### EFetch - Full Records

Fetch detailed gene records in various formats.

**Endpoint:** `efetch.fcgi`

**Parameters:**
- `db=gene` (required) - Database
- `id` (required) - Comma-separated Gene IDs
- `retmode` - xml, text, asn.1 (default: xml)
- `rettype` - gene_table, docsum

**Example Request:**

```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id=672&retmode=xml"
```

**XML Response:** Contains detailed gene information including:
- Gene nomenclature
- Sequence locations
- Transcript variants
- Protein products
- Gene Ontology annotations
- Cross-references
- Publications

### ELink - Related Records

Find related records in Gene or other databases.

**Endpoint:** `elink.fcgi`

**Parameters:**
- `dbfrom=gene` (required) - Source database
- `db` (required) - Target database (gene, nuccore, protein, pubmed, etc.)
- `id` (required) - Gene ID(s)

**Example Request:**

```bash
# Get related PubMed articles
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=pubmed&id=672&retmode=json"
```

### EInfo - Database Information

Get information about the Gene database.

**Endpoint:** `einfo.fcgi`

**Parameters:**
- `db=gene` - Database to query

**Example Request:**

```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=gene&retmode=json"
```

---

## NCBI Datasets API

The Datasets API provides streamlined access to gene data with metadata and sequences.

### Base URL

```
https://api.ncbi.nlm.nih.gov/datasets/v2/gene
```

> Note: the older `v2alpha` path still resolves but is superseded by `v2`; use `v2`. Every gene response wraps results under a top-level `reports` array (each item has a `gene` object), plus a `total_count` field — there is no top-level `genes` key.

### Authentication

Include API key in request headers:

```
api-key: YOUR_API_KEY
```

### Get Gene by ID

Retrieve gene data by Gene ID.

**Endpoint:** `GET /gene/id/{gene_id}`

**Example Request:**

```bash
curl "https://api.ncbi.nlm.nih.gov/datasets/v2/gene/id/672"
```

**Response Format (JSON):**

```json
{
  "reports": [
    {
      "gene": {
        "gene_id": "672",
        "symbol": "BRCA1",
        "description": "BRCA1 DNA repair associated",
        "tax_id": "9606",
        "taxname": "Homo sapiens",
        "common_name": "human",
        "type": "PROTEIN_CODING",
        "orientation": "minus",
        "chromosomes": ["17"],
        "synonyms": ["BRCC1", "FANCS", "PNCA4", "RNF53"],
        "nomenclature_authority": { "authority": "HGNC", "identifier": "HGNC:1100" },
        "swiss_prot_accessions": ["P38398"],
        "ensembl_gene_ids": ["ENSG00000012048"],
        "map_locations": [{ "map_type": "Cytogenetic", "map_value": "17q21.31" }],
        "annotations": [
          {
            "assembly_name": "GRCh38.p14",
            "genomic_locations": [
              {
                "genomic_accession_version": "NC_000017.11",
                "genomic_range": { "begin": "43044295", "end": "43170327", "orientation": "minus" }
              }
            ]
          }
        ],
        "transcript_count": 368,
        "protein_count": 368,
        "gene_ontology": { "molecular_functions": [], "biological_processes": [], "cellular_components": [] }
      }
    }
  ],
  "total_count": 1
}
```

> Field notes (verified against the live v2 API): numeric coordinates are returned as **strings**; `type` is upper-case (e.g. `PROTEIN_CODING`); the genomic location lives at `annotations[].genomic_locations[].genomic_range`, not a top-level `genomic_ranges`; the base report carries `transcript_count`/`protein_count` and GO terms but **not** the individual transcript/protein RefSeq accessions — fetch `GET /gene/id/{id}/product_report` for those.

### Get Gene by Symbol

Retrieve gene data by symbol and organism.

**Endpoint:** `GET /gene/symbol/{symbol}/taxon/{taxon}`

**Parameters:**
- `{symbol}` - Gene symbol (e.g., BRCA1)
- `{taxon}` - Taxon ID (e.g., 9606 for human)

**Example Request:**

```bash
curl "https://api.ncbi.nlm.nih.gov/datasets/v2/gene/symbol/BRCA1/taxon/9606"
```

### Get Multiple Genes

Retrieve data for multiple genes by passing comma-separated Gene IDs on the
GET path. (There is no working `POST /gene/id` body endpoint on v2.)

**Endpoint:** `GET /gene/id/{id1,id2,...}`

**Example Request:**

```bash
curl "https://api.ncbi.nlm.nih.gov/datasets/v2/gene/id/672,7157,5594"
```

The response is the same `reports`/`total_count` envelope, with one `reports[]`
entry per gene.

---

## Authentication and Rate Limits

### Obtaining an API Key

1. Create an NCBI account at https://www.ncbi.nlm.nih.gov/account/
2. Navigate to Settings → API Key Management
3. Generate a new API key
4. Include the key in requests

### Rate Limits

**E-utilities:**
- Without API key: 3 requests/second
- With API key: 10 requests/second

**Datasets API:**
- Without API key: 5 requests/second
- With API key: 10 requests/second

### Usage Guidelines

1. **Include email in requests:** Add `&email=your@email.com` to E-utilities requests
2. **Implement rate limiting:** Use delays between requests
3. **Use POST for large queries:** When working with many IDs
4. **Cache results:** Store frequently accessed data locally
5. **Handle errors gracefully:** Implement retry logic with exponential backoff

---

## Error Handling

### HTTP Status Codes

- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters or malformed query
- `404 Not Found` - Gene ID or symbol not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error (retry with backoff)

### E-utilities Error Messages

E-utilities return errors in the response body:

**XML format:**
```xml
<ERROR>Empty id list - nothing to do</ERROR>
```

**JSON format:**
```json
{
  "error": "Invalid db name"
}
```

### Common Errors

1. **Empty Result Set**
   - Cause: Gene symbol or ID not found
   - Solution: Verify spelling, check organism filter

2. **Rate Limit Exceeded**
   - Cause: Too many requests
   - Solution: Add delays, use API key

3. **Invalid Query Syntax**
   - Cause: Malformed search term
   - Solution: Use proper field tags (e.g., `[gene]`, `[organism]`)

4. **Timeout**
   - Cause: Large result set or slow connection
   - Solution: Use History Server, reduce result size

### Retry Strategy

Implement exponential backoff for failed requests:

```python
import time

def retry_request(func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt < max_attempts - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                time.sleep(wait_time)
            else:
                raise
```

---

## Common Taxon IDs

| Organism | Scientific Name | Taxon ID |
|----------|----------------|----------|
| Human | Homo sapiens | 9606 |
| Mouse | Mus musculus | 10090 |
| Rat | Rattus norvegicus | 10116 |
| Zebrafish | Danio rerio | 7955 |
| Fruit fly | Drosophila melanogaster | 7227 |
| C. elegans | Caenorhabditis elegans | 6239 |
| Yeast | Saccharomyces cerevisiae | 4932 |
| Arabidopsis | Arabidopsis thaliana | 3702 |
| E. coli | Escherichia coli | 562 |

---

## Additional Resources

- **E-utilities Documentation:** https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **Datasets API Documentation:** https://www.ncbi.nlm.nih.gov/datasets/docs/v2/
- **Gene Database Help:** https://www.ncbi.nlm.nih.gov/gene/
- **API Key Registration:** https://www.ncbi.nlm.nih.gov/account/
