# GWAS Catalog Query Workflows

Step-by-step workflows for disease-, variant-, and gene-centric queries, systematic reviews, and summary-statistics analysis. Web-interface search modes are listed at the end.

## Workflow 1: Exploring Genetic Associations for a Disease

1. **Identify the trait** using ontology terms or free text:
   - Search web interface or `/efoTraits/search/findByTrait?trait=...` for the disease name
   - Note the current short-form (e.g., MONDO_0005148 for type 2 diabetes on the main REST API). Legacy EFO ids like EFO_0001360 may 404 on the main API but are still used by the Summary Statistics API — see the trait-ID gotcha in SKILL.md.

2. **Query associations via API:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/efoTraits/{efo_id}/associations"
   ```

3. **Filter by significance and population:**
   - Check p-values (genome-wide significant: p ≤ 5×10⁻⁸)
   - Review ancestry information in study metadata
   - Filter by sample size or discovery/replication status

4. **Extract variant details:** rs IDs, effect alleles and directions, effect sizes (odds ratios, beta coefficients), population allele frequencies.

5. **Cross-reference with other databases:** variant consequences in Ensembl, population frequencies in gnomAD, gene function and pathways.

## Workflow 2: Investigating a Specific Genetic Variant

1. **Query the variant:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}"
   ```

2. **Retrieve all trait associations:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}/associations"
   ```

3. **Analyze pleiotropy:** identify all traits associated with this variant, review effect directions across traits, look for shared biological pathways.

4. **Check genomic context:** nearby genes, coding/regulatory regions, linkage disequilibrium with other variants.

## Workflow 3: Gene-Centric Association Analysis

1. **Search by gene symbol** in web interface or:
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/search/findByGene"
   params = {"geneName": gene_symbol}
   ```

2. **Retrieve variants in gene region:** get chromosomal coordinates for the gene, query variants in region, include promoter and regulatory regions (extend boundaries).

3. **Analyze association patterns:** identify traits associated with variants in this gene, look for consistent associations across studies, review effect sizes and directions.

4. **Functional interpretation:** determine variant consequences (missense, regulatory, etc.), check expression QTL (eQTL) data, review pathway and network context.

## Workflow 4: Systematic Review of Genetic Evidence

1. **Define research question:** specific trait/disease, population considerations, study design requirements.

2. **Comprehensive variant extraction:** query all associations for the trait, set significance threshold, note discovery and replication studies.

3. **Quality assessment:** review study sample sizes, check population diversity, assess heterogeneity across studies, identify potential biases.

4. **Data synthesis:** aggregate associations across studies, perform meta-analysis if applicable, create summary tables, generate Manhattan or forest plots.

5. **Export and documentation:** download full association data, export summary statistics if needed, document search strategy and date, create reproducible analysis scripts.

## Workflow 5: Accessing and Analyzing Summary Statistics

1. **Identify studies with summary statistics:** browse summary statistics portal, check FTP directory listings, query API for available studies.

2. **Download summary statistics:**
   ```bash
   # Via FTP
   wget ftp://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCSTXXXXXX/harmonised/GCSTXXXXXX-harmonised.tsv.gz
   ```

3. **Query via API for specific variants:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/summary-statistics/api/chromosomes/{chrom}/associations"
   params = {"start": start_pos, "end": end_pos}
   ```

4. **Process and analyze:** filter by p-value thresholds, extract effect sizes and confidence intervals, perform downstream analyses (fine-mapping, colocalization, etc.).

## Web Interface Search Modes

The web interface at https://www.ebi.ac.uk/gwas/ supports multiple search modes:

**By Variant (rs ID):** `rs7903146` — returns all trait associations for this SNP.

**By Disease/Trait:** `type 2 diabetes`, `Parkinson disease`, `body mass index` — returns all associated genetic variants.

**By Gene:** `APOE`, `TCF7L2` — returns variants in or near the gene region.

**By Chromosomal Region:** `10:114000000-115000000` — returns variants in the specified genomic interval.

**By Publication:** `PMID:20581827`, `Author: McCarthy MI`, `GCST001234` — returns study details and all reported associations.
