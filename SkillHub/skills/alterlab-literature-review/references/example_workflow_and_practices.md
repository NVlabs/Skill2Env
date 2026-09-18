# Example Workflow, Best Practices, and Integration

## Example Workflow

Complete workflow for a biomedical literature review:

```bash
# 1. Create review document from template
cp assets/review_template.md crispr_sickle_cell_review.md

# 2. Search multiple databases using appropriate APIs
# - Use NCBI E-utilities (Entrez) for PubMed/PMC
# - Use the bioRxiv API (api.biorxiv.org) or Europe PMC for preprints
# - Use direct API access for arXiv, Semantic Scholar
# - Export results in JSON format

# 3. Aggregate and process results
python scripts/search_databases.py combined_results.json \
  --deduplicate \
  --rank citations \
  --year-start 2015 \
  --year-end 2024 \
  --format markdown \
  --output search_results.md \
  --summary

# 4. Screen results and extract data
# - Manually screen titles, abstracts, full texts
# - Extract key data into the review document
# - Organize by themes

# 5. Write the review following template structure
# - Introduction with clear objectives
# - Detailed methodology section
# - Results organized thematically
# - Critical discussion
# - Clear conclusions

# 6. Verify all citations
python scripts/verify_citations.py crispr_sickle_cell_review.md

# Review the citation report
cat crispr_sickle_cell_review_citation_report.json

# Fix any failed citations and re-verify
python scripts/verify_citations.py crispr_sickle_cell_review.md

# 7. Generate professional PDF
python scripts/generate_pdf.py crispr_sickle_cell_review.md \
  --citation-style nature \
  --output crispr_sickle_cell_review.pdf

# 8. Review final PDF and markdown outputs
```

## Best Practices

### Search Strategy
1. **Use multiple databases** (minimum 3): ensures comprehensive coverage.
2. **Include preprint servers**: captures the latest unpublished findings.
3. **Document everything**: search strings, dates, result counts for reproducibility.
4. **Test and refine**: run pilot searches, review results, adjust search terms.
5. **Sort by citations**: when available, sort search results by citation count to surface influential work first.

### Screening and Selection
1. **Use clear criteria**: document inclusion/exclusion criteria before screening.
2. **Screen systematically**: Title → Abstract → Full text.
3. **Document exclusions**: record reasons for excluding studies.
4. **Consider dual screening**: for systematic reviews, have two reviewers screen independently.

### Synthesis
1. **Organize thematically**: group by themes, NOT by individual studies.
2. **Synthesize across studies**: compare, contrast, identify patterns.
3. **Be critical**: evaluate quality and consistency of evidence.
4. **Identify gaps**: note what is missing or understudied.

### Quality and Reproducibility
1. **Assess study quality**: use appropriate quality assessment tools.
2. **Verify all citations**: run `verify_citations.py`.
3. **Document methodology**: provide enough detail for others to reproduce.
4. **Follow guidelines**: use PRISMA for systematic reviews.

### Writing
1. **Be objective**: present evidence fairly, acknowledge limitations.
2. **Be systematic**: follow the structured template.
3. **Be specific**: include numbers, statistics, effect sizes where available.
4. **Be clear**: use clear headings, logical flow, thematic organization.

## Common Pitfalls to Avoid

1. **Single database search**: misses relevant papers; always search multiple databases.
2. **No search documentation**: makes the review irreproducible; document all searches.
3. **Study-by-study summary**: lacks synthesis; organize thematically instead.
4. **Unverified citations**: leads to errors; always run `verify_citations.py`.
5. **Too broad search**: yields thousands of irrelevant results; refine with specific terms.
6. **Too narrow search**: misses relevant papers; include synonyms and related terms.
7. **Ignoring preprints**: misses the latest findings; include bioRxiv, medRxiv, arXiv.
8. **No quality assessment**: treats all evidence equally; assess and report quality.
9. **Publication bias**: only positive results published; note potential bias.
10. **Outdated search**: the field evolves rapidly; clearly state the search date.

## Integration with Other Skills

### Database Access Skills
- **NCBI E-utilities (Entrez)**: PubMed/PMC search and retrieval
- **bioRxiv API / Europe PMC**: bioRxiv and medRxiv preprints
- **gget**: COSMIC, AlphaFold, Ensembl, UniProt
- **bioservices**: ChEMBL, KEGG, Reactome, UniProt, PubChem
- **datacommons-client**: Demographics, economics, health statistics

### Analysis Skills
- **pydeseq2**: RNA-seq differential expression (for methods sections)
- **scanpy**: Single-cell analysis (for methods sections)
- **anndata**: Single-cell data (for methods sections)
- **biopython**: Sequence analysis (for background sections)

### Visualization Skills
- **matplotlib**: Generate figures and plots for the review
- **seaborn**: Statistical visualizations

### Writing Skills
- **alterlab-scientific-writing**: Turn the structured synthesis into flowing manuscript prose (Introduction/Discussion sections).
- **alterlab-citation-mgmt**: Convert DOIs to BibTeX and build the bibliography.
- **alterlab-citation-verifier**: Audit that every reference actually exists and is not retracted.

## Dependencies

### Required Python Packages
```bash
pip install requests  # For citation verification
```

### Required System Tools
```bash
# For PDF generation
brew install pandoc  # macOS
apt-get install pandoc  # Linux

# For LaTeX (PDF generation)
brew install --cask mactex  # macOS
apt-get install texlive-xetex  # Linux
```

Check dependencies:
```bash
python scripts/generate_pdf.py --check-deps
```

## External Resources

**Guidelines:**
- PRISMA (Systematic Reviews): http://www.prisma-statement.org/
- Cochrane Handbook: https://training.cochrane.org/handbook
- AMSTAR 2 (Review Quality): https://amstar.ca/

**Tools:**
- MeSH Browser: https://meshb.nlm.nih.gov/search
- PubMed Advanced Search: https://pubmed.ncbi.nlm.nih.gov/advanced/
- Boolean Search Guide: https://www.ncbi.nlm.nih.gov/books/NBK3827/

**Citation Styles:**
- APA Style: https://apastyle.apa.org/
- Nature Portfolio: https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards
- NLM/Vancouver: https://www.nlm.nih.gov/bsd/uniform_requirements.html
