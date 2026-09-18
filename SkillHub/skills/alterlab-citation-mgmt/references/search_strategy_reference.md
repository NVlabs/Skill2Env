# Search Strategy Reference

High-impact-paper heuristics, Google Scholar operators, and PubMed/MeSH query
construction, extracted from the skill body. Complete database guides are in
`google_scholar_search.md` and `pubmed_search.md`.

## Finding Seminal and High-Impact Papers (CRITICAL)

Prioritize papers by citation count, venue quality, and author reputation.

**Citation Count Thresholds:**

| Paper Age | Citations | Classification |
|-----------|-----------|----------------|
| 0-3 years | 20+ | Noteworthy |
| 0-3 years | 100+ | Highly Influential |
| 3-7 years | 100+ | Significant |
| 3-7 years | 500+ | Landmark Paper |
| 7+ years | 500+ | Seminal Work |
| 7+ years | 1000+ | Foundational |

**Venue Quality Tiers:**
- **Tier 1 (Prefer):** Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS
- **Tier 2 (High Priority):** Impact Factor >10, top conferences (NeurIPS, ICML, ICLR)
- **Tier 3 (Good):** Specialized journals (IF 5-10)
- **Tier 4 (Sparingly):** Lower-impact peer-reviewed venues

**Author Reputation Indicators:**
- Senior researchers with h-index >40
- Multiple publications in Tier-1 venues
- Leadership at recognized institutions
- Awards and editorial positions

**Search strategies for high-impact papers:**
- Sort by citation count (most cited first)
- Look for review articles from Tier-1 journals for an overview
- Check "Cited by" for impact assessment and recent follow-up work
- Use citation alerts for tracking new citations to key papers
- Filter by top venues using `source:Nature` or `source:Science`
- Search for papers by known field leaders using `author:LastName`

## Google Scholar Operators

```
"exact phrase"           # Exact phrase matching
author:lastname          # Search by author
intitle:keyword          # Search in title only
source:journal           # Search specific journal
-exclude                 # Exclude terms
OR                       # Alternative terms
2020..2024               # Year range
```

**Example searches:**
```
# Find recent reviews on a topic
"CRISPR" intitle:review 2023..2024

# Find papers by specific author on topic
author:Church "synthetic biology"

# Find highly cited foundational work
"deep learning" 2012..2015 sort:citations

# Exclude surveys and focus on methods
"protein folding" -survey -review intitle:method
```

## PubMed: MeSH and Field Tags

**Using MeSH terms** (controlled vocabulary for precise searching):
1. Find MeSH terms at https://meshb.nlm.nih.gov/search
2. Use in queries: `"Diabetes Mellitus, Type 2"[MeSH]`
3. Combine with keywords for comprehensive coverage

**Field tags:**
```
[Title]              # Search in title only
[Title/Abstract]     # Search in title or abstract
[Author]             # Search by author name
[Journal]            # Search specific journal
[Publication Date]   # Date range
[Publication Type]   # Article type
[MeSH]               # MeSH term
```

**Building complex queries:**
```bash
# Clinical trials on diabetes treatment published recently
"Diabetes Mellitus, Type 2"[MeSH] AND "Drug Therapy"[MeSH]
AND "Clinical Trial"[Publication Type] AND 2020:2024[Publication Date]

# Reviews on CRISPR in specific journal
"CRISPR-Cas Systems"[MeSH] AND "Nature"[Journal] AND "Review"[Publication Type]

# Specific author's recent work
"Smith AB"[Author] AND cancer[Title/Abstract] AND 2022:2024[Publication Date]
```

**E-utilities for automation** (the scripts use the NCBI E-utilities API):
- **ESearch**: Search and retrieve PMIDs
- **EFetch**: Retrieve full metadata
- **ESummary**: Get summary information
- **ELink**: Find related articles

See `pubmed_search.md` for complete API documentation.

## Metadata Sources

1. **CrossRef API**: primary source for DOIs; comprehensive journal-article metadata;
   free, no API key required.
2. **PubMed E-utilities**: biomedical literature; official NCBI metadata incl. MeSH
   terms and abstracts; PMID/PMCID; free, API key recommended for high volume.
3. **arXiv API**: preprints in physics, math, CS, q-bio; version tracking; free.
4. **DataCite API**: datasets, software, other scholarly outputs; free.

**What gets extracted:** required fields (author, title, year); journal-article fields
(journal, volume, number, pages, DOI); book fields (publisher, ISBN, edition);
conference fields (booktitle, location, pages); preprint fields (repository, ID); plus
abstract, keywords, URL. See `metadata_extraction.md`.

## Validation Checks (summary)

DOI verification (resolves via doi.org, metadata matches CrossRef); required-field
presence; data consistency (valid year, numeric volume/number, page format `123--145`);
duplicate detection; format compliance (valid BibTeX syntax, unique keys, proper
escaping). Full criteria: `citation_validation.md`. Example JSON validation report
structure includes `total_entries`, `valid_entries`, `errors[]`, and `warnings[]`.
