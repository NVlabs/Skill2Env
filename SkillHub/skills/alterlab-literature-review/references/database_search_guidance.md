# Database-Specific Search Guidance

How to access and query each literature database. Pairs with `references/database_strategies.md` (broader strategy). Use NCBI E-utilities (Entrez) for PubMed/PMC — not screen-scraping.

## PubMed / PubMed Central

Access via NCBI E-utilities (Entrez esearch/efetch). Use Biopython's `Bio.Entrez`
or query the eutils.ncbi.nlm.nih.gov endpoints directly:
```python
# Search PubMed via Entrez (Biopython)
from Bio import Entrez
Entrez.email = "you@example.com"  # required by NCBI
handle = Entrez.esearch(db="pubmed", term="CRISPR gene editing", retmax=100)
ids = Entrez.read(handle)["IdList"]
records = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")

# Build complex queries with the PubMed Advanced Search Builder,
# then pass the resulting query string as the `term` argument above.
```

**Search tips**:
- Use MeSH terms: `"sickle cell disease"[MeSH]`
- Field tags: `[Title]`, `[Title/Abstract]`, `[Author]`
- Date filters: `2020:2024[Publication Date]`
- Boolean operators: AND, OR, NOT
- See MeSH browser: https://meshb.nlm.nih.gov/search

## bioRxiv / medRxiv

Access via the bioRxiv API (api.biorxiv.org) or Europe PMC:
```bash
# bioRxiv/medRxiv content API (returns metadata for a date/DOI range)
curl "https://api.biorxiv.org/details/biorxiv/2024-01-01/2024-12-31/0"

# Or keyword-search preprints via Europe PMC (covers bioRxiv + medRxiv)
curl "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=CRISPR%20sickle%20cell%20AND%20SRC:PPR&format=json"
```

**Important considerations**:
- Preprints are not peer-reviewed
- Verify findings with caution
- Check if the preprint has been published (CrossRef)
- Note preprint version and date

## arXiv

Access via direct API or WebFetch:
```python
# Example search categories:
# q-bio.QM (Quantitative Methods)
# q-bio.GN (Genomics)
# q-bio.MN (Molecular Networks)
# cs.LG (Machine Learning)
# stat.ML (Machine Learning Statistics)

# Search format: category AND terms
search_query = "cat:q-bio.QM AND ti:\"single cell sequencing\""
```

## Semantic Scholar

Access via direct API (requires API key, or use the free tier):
- 200M+ papers across all fields
- Excellent for cross-disciplinary searches
- Provides citation graphs and paper recommendations
- Use for finding highly influential papers

## Specialized Biomedical Databases

Use the appropriate skills:
- **ChEMBL**: `bioservices` skill for chemical bioactivity
- **UniProt**: `gget` or `bioservices` skill for protein information
- **KEGG**: `bioservices` skill for pathways and genes
- **COSMIC**: `gget` skill for cancer mutations
- **AlphaFold**: `gget alphafold` for protein structures
- **PDB**: `gget` or direct API for experimental structures

## Citation Chaining

Expand the search via citation networks:

1. **Forward citations** (papers citing key papers):
   - Use Google Scholar "Cited by"
   - Use Semantic Scholar or OpenAlex APIs
   - Identifies newer research building on seminal work
2. **Backward citations** (references from key papers):
   - Extract references from included papers
   - Identify highly cited foundational work
   - Find papers cited by multiple included studies
