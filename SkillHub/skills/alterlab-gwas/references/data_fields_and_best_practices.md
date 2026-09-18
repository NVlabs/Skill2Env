# GWAS Catalog Data Fields and Best Practices

Response record fields, pagination, query/interpretation best practices, and data-quality considerations.

## Data Structure Overview

The GWAS Catalog is organized around four core entities:

- **Studies**: GWAS publications with metadata (PMID, author, cohort details)
- **Associations**: SNP-trait associations with statistical evidence (p ≤ 5×10⁻⁸)
- **Variants**: Genetic markers (SNPs) with genomic coordinates and alleles
- **Traits**: Phenotypes and diseases (mapped to EFO ontology terms)

**Key Identifiers:**
- Study accessions: `GCST` IDs (e.g., GCST001234)
- Variant IDs: `rs` numbers (e.g., rs7903146) or `variant_id` format
- Trait IDs: EFO terms (e.g., EFO_0001360 for type 2 diabetes)
- Gene symbols: HGNC approved names (e.g., TCF7L2)

## Response Formats and Data Fields

**Key Fields in Association Records (verified against the live v2 API):**

The rsID, allele, and trait are **nested**, not top-level — a frequent extraction bug. On an association object:
- `pvalue`: Association p-value (top-level, present)
- `pvalueMantissa` / `pvalueExponent`: p-value split form (top-level)
- `orPerCopyNum`: Odds ratio per allele copy (top-level; `null` for quantitative traits)
- `betaNum`: Effect size for quantitative traits (top-level; `null` for case-control)
- `betaUnit`, `betaDirection`: Unit / direction of beta
- `range`, `standardError`: Confidence interval and SE
- `riskFrequency`: Reported risk-allele frequency
- `snps[]`: array; the rsID is `snps[i].rsId` (there is **no** top-level `rsId`)
- `loci[].strongestRiskAlleles[].riskAlleleName`: the risk allele, e.g. `rs7903146-T` (there is **no** top-level `strongestAllele`)
- `efoTraits[]`: array of `{trait, uri, shortForm}`; the trait name is `efoTraits[i].trait` (there is **no** top-level `efoTrait` or `mappedLabel`)
- `_links.study.href`: follow this for the study/accession and PubMed ID — these are **not** inline on the association

To list rsID/trait/p-value for an association `a`:
```python
rs   = (a.get("snps") or [{}])[0].get("rsId")
trait = (a.get("efoTraits") or [{}])[0].get("trait")
allele = ((a.get("loci") or [{}])[0].get("strongestRiskAlleles") or [{}])[0].get("riskAlleleName")
pval = a.get("pvalue")
```

**Study Metadata Fields:**
- `accessionId`: GCST study identifier
- `pubmedId`: PubMed ID
- `author`: First author
- `publicationDate`: Publication date
- `ancestryInitial`: Discovery population ancestry
- `ancestryReplication`: Replication population ancestry
- `sampleSize`: Total sample size

**Pagination:**
Results are paginated (default 20 items per page). Navigate using:
- `size` parameter: Number of results per page
- `page` parameter: Page number (0-indexed)
- `_links` in response: URLs for next/previous pages

## Best Practices

### Query Strategy
- Start with web interface to identify relevant EFO terms and study accessions
- Use API for bulk data extraction and automated analyses
- Implement pagination handling for large result sets
- Cache API responses to minimize redundant requests

### Data Interpretation
- Always check p-value thresholds (genome-wide: 5×10⁻⁸)
- Review ancestry information for population applicability
- Consider sample size when assessing evidence strength
- Check for replication across independent studies
- Be aware of winner's curse in effect size estimates

### Rate Limiting and Ethics
- Respect API usage guidelines (no excessive requests)
- Use summary statistics downloads for genome-wide analyses
- Implement appropriate delays between API calls
- Cache results locally when performing iterative analyses
- Cite the GWAS Catalog in publications

### Data Quality Considerations
- GWAS Catalog curates published associations (may contain inconsistencies)
- Effect sizes reported as published (may need harmonization)
- Some studies report conditional or joint associations
- Check for study overlap when combining results
- Be aware of ascertainment and selection biases

## Important Notes

### Data Updates
- The GWAS Catalog is updated regularly with new publications
- Re-run queries periodically for comprehensive coverage
- Summary statistics are added as studies release data
- EFO mappings may be updated over time

### Limitations
- Not all GWAS publications are included (curation criteria apply)
- Full summary statistics available for subset of studies
- Effect sizes may require harmonization across studies
- Population diversity is growing but historically limited
- Some associations represent conditional or joint effects

### Data Access
- Web interface: Free, no registration required
- REST APIs: Free, no API key needed
- FTP downloads: Open access
- Rate limiting applies to API (be respectful)
