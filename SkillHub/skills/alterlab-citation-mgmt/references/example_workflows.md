# Example Workflows

End-to-end worked examples for citation management, extracted from the skill body.

## Example 1: Building a Bibliography for a Paper

```bash
# Step 1: Find key papers on your topic
python scripts/search_google_scholar.py "transformer neural networks" \
  --year-start 2017 \
  --limit 50 \
  --output transformers_gs.json

python scripts/search_pubmed.py "deep learning medical imaging" \
  --date-start 2020 \
  --limit 50 \
  --output medical_dl_pm.json

# Step 2: Extract metadata from search results
python scripts/extract_metadata.py \
  --input transformers_gs.json \
  --output transformers.bib

python scripts/extract_metadata.py \
  --input medical_dl_pm.json \
  --output medical.bib

# Step 3: Add specific papers you already know
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2 >> specific.bib
python scripts/doi_to_bibtex.py 10.1126/science.aam9317 >> specific.bib

# Step 4: Combine all BibTeX files
cat transformers.bib medical.bib specific.bib > combined.bib

# Step 5: Format and deduplicate
python scripts/format_bibtex.py combined.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output formatted.bib

# Step 6: Apply fixes (format_bibtex.py), then validate (report-only)
cp formatted.bib final_references.bib
python scripts/validate_citations.py final_references.bib \
  --check-dois \
  --report validation.json \
  --verbose

# Step 7: Review any issues
cat validation.json | grep -A 3 '"errors"'

# Step 8: Use in LaTeX
# \bibliography{final_references}
```

## Example 2: Converting a List of DOIs

```bash
# You have a text file with DOIs (one per line)
# dois.txt contains:
# 10.1038/s41586-021-03819-2
# 10.1126/science.aam9317
# 10.1016/j.cell.2023.01.001

# Convert all to BibTeX
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# Validate the result
python scripts/validate_citations.py references.bib --verbose
```

## Example 3: Cleaning an Existing BibTeX File

```bash
# You have a messy BibTeX file from various sources; clean it up systematically

# Step 1: Format and standardize
python scripts/format_bibtex.py messy_references.bib \
  --output step1_formatted.bib

# Step 2: Remove duplicates
python scripts/format_bibtex.py step1_formatted.bib \
  --deduplicate \
  --output step2_deduplicated.bib

# Step 3: Validate (report-only); fixes already applied by format_bibtex above
python scripts/validate_citations.py step2_deduplicated.bib \
  --report step3_validation.json \
  --verbose
cp step2_deduplicated.bib step3_validated.bib

# Step 4: Sort by year
python scripts/format_bibtex.py step3_validated.bib \
  --sort year \
  --descending \
  --output clean_references.bib

# Step 5: Final validation report
python scripts/validate_citations.py clean_references.bib \
  --report final_validation.json \
  --verbose

# Review report
cat final_validation.json
```

## Example 4: Finding and Citing Seminal Papers

```bash
# Find highly cited papers on a topic
python scripts/search_google_scholar.py "AlphaFold protein structure" \
  --year-start 2020 \
  --year-end 2024 \
  --sort-by citations \
  --limit 20 \
  --output alphafold_seminal.json

# Extract the top results by citation count
# (script will have included citation counts in JSON)

# Convert to BibTeX
python scripts/extract_metadata.py \
  --input alphafold_seminal.json \
  --output alphafold_refs.bib

# The BibTeX file now contains the most influential papers
```

## Combined Workflow: Building References for Manuscripts

```bash
# 1. Search for papers on your topic
python scripts/search_pubmed.py \
  '"CRISPR-Cas Systems"[MeSH] AND "Gene Editing"[MeSH]' \
  --date-start 2020 \
  --limit 200 \
  --output crispr_papers.json

# 2. Extract DOIs from search results and convert to BibTeX
python scripts/extract_metadata.py \
  --input crispr_papers.json \
  --output crispr_refs.bib

# 3. Add specific papers by DOI
python scripts/doi_to_bibtex.py 10.1038/nature12345 >> crispr_refs.bib
python scripts/doi_to_bibtex.py 10.1126/science.abcd1234 >> crispr_refs.bib

# 4. Format and clean the BibTeX file
python scripts/format_bibtex.py crispr_refs.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output references.bib

# 5. Validate all citations (report-only; resolve DOIs with --check-dois)
cp references.bib final_references.bib
python scripts/validate_citations.py final_references.bib \
  --check-dois \
  --report validation.json \
  --verbose

# 6. Review validation report and fix any remaining issues
cat validation.json

# 7. Use in your LaTeX document
# \bibliography{final_references}
```
