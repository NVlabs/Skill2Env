# Script CLI Reference

Per-script features and command-line usage for the `scripts/` in this skill,
extracted from the skill body.

## search_google_scholar.py

Search Google Scholar and export results.

**Features**: automated searching with rate limiting; pagination; year-range
filtering; export to JSON or BibTeX; citation-count information.

```bash
# Basic search
python scripts/search_google_scholar.py "quantum computing"

# Advanced search with filters
python scripts/search_google_scholar.py "quantum computing" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --sort-by citations \
  --output quantum_papers.json

# Export directly to BibTeX
python scripts/search_google_scholar.py "machine learning" \
  --limit 50 \
  --format bibtex \
  --output ml_papers.bib
```

## search_pubmed.py

Search PubMed using the E-utilities API.

**Features**: complex query support (MeSH, field tags, Boolean); date-range
filtering; publication-type filtering; batch retrieval with metadata; export to
JSON or BibTeX.

```bash
# Simple keyword search
python scripts/search_pubmed.py "CRISPR gene editing"

# Complex query with filters
python scripts/search_pubmed.py \
  --query '"CRISPR-Cas Systems"[MeSH] AND "therapeutic"[Title/Abstract]' \
  --date-start 2020-01-01 \
  --date-end 2024-12-31 \
  --publication-types "Clinical Trial,Review" \
  --limit 200 \
  --output crispr_therapeutic.json

# Export to BibTeX
python scripts/search_pubmed.py "Alzheimer's disease" \
  --limit 100 \
  --format bibtex \
  --output alzheimers.bib
```

## extract_metadata.py

Extract complete metadata from paper identifiers.

**Features**: supports DOI, PMID, arXiv ID, URL; queries CrossRef, PubMed, arXiv
APIs; handles multiple identifier types; batch processing; multiple output formats.

```bash
# Single DOI
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# Single PMID
python scripts/extract_metadata.py --pmid 34265844

# Single arXiv ID
python scripts/extract_metadata.py --arxiv 2103.14030

# From URL
python scripts/extract_metadata.py \
  --url "https://www.nature.com/articles/s41586-021-03819-2"

# Batch processing (file with one identifier per line)
python scripts/extract_metadata.py \
  --input paper_ids.txt \
  --output references.bib

# Different output formats
python scripts/extract_metadata.py \
  --doi 10.1038/nature12345 \
  --format json  # bibtex (default) or json
```

## validate_citations.py

Validate BibTeX entries for accuracy and completeness.

**Features**: required-field checking (per entry type); duplicate detection (DOI,
key, identical title); format validation (year, DOI pattern, page dashes, author
separators); optional DOI resolution via doi.org/CrossRef; JSON report.

This tool reports only — it does not rewrite the `.bib`. Run `format_bibtex.py` to
apply fixes. DOI resolution is off by default; pass `--check-dois` to enable it.

```bash
# Offline validation (fields, format, duplicates) — fast
python scripts/validate_citations.py references.bib --verbose

# Also resolve every DOI against doi.org/CrossRef — slow, network-bound
python scripts/validate_citations.py references.bib --check-dois

# Save a machine-readable JSON report
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose
```

Flags: `--check-dois`, `--report FILE`, `--verbose`. (`--auto-fix` is accepted but
currently a no-op; use `format_bibtex.py` for fixes.)

## format_bibtex.py

Format and clean BibTeX files.

**Features**: standardize formatting; sort entries (by key, year, author); remove
duplicates; validate syntax; fix common errors; enforce citation-key conventions.

```bash
# Basic formatting
python scripts/format_bibtex.py references.bib

# Sort by year (newest first)
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_refs.bib

# Remove duplicates
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_refs.bib

# Complete cleanup (dedup + sort newest-first; common fixes run by default)
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output final_refs.bib
```

Common fixes (page-range dashes, `pp.` stripping, DOI URL prefixes, author
separators) are applied automatically; pass `--no-fix` to disable them.

## doi_to_bibtex.py

Quick DOI to BibTeX conversion.

**Features**: fast single-DOI conversion via DOI content negotiation; batch
processing with rate limiting; `bibtex` (default) or `json` output. Unlike
`extract_metadata.py`, this returns the publisher's raw BibTeX verbatim (no field
reordering or title-brace protection) — use `format_bibtex.py` afterward to clean it.

```bash
# Single DOI
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# Multiple DOIs (rate-limited; tune with --delay)
python scripts/doi_to_bibtex.py \
  10.1038/nature12345 \
  10.1126/science.abc1234 \
  10.1016/j.cell.2023.01.001

# From file (one DOI per line)
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib
```
