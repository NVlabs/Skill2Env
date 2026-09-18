---
name: alterlab-pdf-explore
description: Explore a single PDF in depth — parse it once, then answer questions across its sections, figures, tables, and appendices — comparing methods across sections, extracting every instance of a pattern within the document, and reading values off its charts and tables. Use when interrogating one paper or report end-to-end, pulling every occurrence of something inside a document, or reading data from a figure/table in a PDF, serving the literature-review and paper-review pipeline. To build a comparison table across MANY papers prefer alterlab-pdf-extract; to simply convert a PDF to Markdown prefer alterlab-markitdown; for reference/citation management prefer alterlab-pyzotero. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs under `uv run python` with a PDF parser (e.g. `pymupdf`/`pdfplumber` — TODO(verify) preferred pin) plus, for scanned pages, an OCR pass. No GPU or account required. Parses the PDF once into a section/figure/table index that later questions reuse; large scanned PDFs are slower due to OCR."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PDF Explore (deep single-document Q&A)

## Overview

Reading one paper or report *thoroughly* means jumping between the methods, a results figure,
a supplementary table, and an appendix — repeatedly. This skill **parses a PDF once** into a
reusable index of sections, figures, and tables, then answers **many questions across the
whole document** without re-parsing: compare what two sections say, extract *every* instance
of a pattern, and read values off charts/tables.

It is the **single-document deep-dive** counterpart to the corpus-level tools: to build a
comparison table across **many** papers use `alterlab-pdf-extract`; to just **convert** a PDF
to Markdown use `alterlab-markitdown`.

## When to Use This Skill

Use this skill when the user wants to:
- **Interrogate one paper/report end-to-end** (methods vs. results vs. appendix).
- **Extract every occurrence** of a pattern within a document (all p-values, all sample sizes,
  every mention of a gene).
- **Read data off a figure or table** inside the PDF.
- Feed precise, located answers into the **literature-review** or **paper-review** pipeline.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Build a comparison table across **many** papers (one row per paper) | `alterlab-pdf-extract` |
| **Convert** a PDF/DOCX to clean Markdown | `alterlab-markitdown` |
| Manage references / DOIs / BibTeX | `alterlab-pyzotero` |
| Work with a Jupyter notebook | `alterlab-open-notebook` |

## Core Capabilities

### 1. Parse-once, ask-many

Parse the PDF a single time into a structured index — page text with layout, detected section
headings, figure/table regions, and (for scans) OCR'd text — then answer subsequent questions
against that index instead of re-reading the file each time.

### 2. Cross-section questions

Answer questions that span the document: "does the discussion's claim match the methods'
design?", "which limitations does the appendix add beyond the main text?". Cite the **page and
section** for every answer so it is verifiable.

### 3. Extract-every-instance

Pull *all* occurrences of a pattern (every reported p-value, every cohort size, every figure
that mentions a variable), returning a located list rather than a single hit — the reliable
way to avoid missing one.

### 4. Read values off figures/tables

Extract tabular data from table regions, and read approximate values from a chart (axis
ranges, series values) with an explicit note that chart-read values are approximate and should
be confirmed against any underlying data.

### 5. Pipeline role

Provides the per-document evidence that `alterlab-paper-reviewer` and literature-review
workflows build on; hand its located extractions to `alterlab-pdf-extract` when the task grows
from one paper to a whole corpus table.

## Resources

- `references/pdf_explore_usage.md` — parser choice, the section/figure index, OCR handling,
  extract-every-instance patterns, and figure/table reading caveats. Loaded on demand.

Part of the AlterLab Academic Skills suite.
