# PDF Explore — Usage Reference

Deeper detail for `alterlab-pdf-explore`. Pick a parser that fits the document; verify pins
against your environment (`TODO(verify)`).

## Parser choice

- **`pymupdf` (fitz)** — fast text + layout + image extraction; good default.
- **`pdfplumber`** — strong table extraction and word/character bounding boxes.
- **OCR** (e.g. Tesseract via `pytesseract`) — needed for scanned/image-only PDFs; run it once
  during parsing and cache the text.

Parse once into an index (page text + coordinates, detected headings, figure/table regions),
then answer questions against the index rather than re-reading the file.

## Section / figure index

Detect section headings (font-size / style heuristics or a table-of-contents) to segment the
document, and record figure/table bounding regions per page. Every answer should carry a
**page + section** citation so it is verifiable.

## Extract-every-instance

For "find all X", scan the full parsed text (not just the first match) and return a located
list — page, section, surrounding context — for each hit. Common patterns: p-values, sample
sizes (n=…), effect sizes/CIs, gene/protein mentions, dataset identifiers.

## Reading figures and tables

- **Tables**: extract with `pdfplumber`'s table finder; verify column alignment.
- **Charts**: reading values off a rendered chart is approximate — report axis ranges and
  estimated series values and flag that they should be confirmed against underlying data if
  available. Do not present chart-read numbers as exact.

## Choosing the document skill

| Goal | Skill |
|------|-------|
| Deep Q&A within ONE PDF (sections/figures/appendix) | `alterlab-pdf-explore` |
| Structured comparison table across MANY papers | `alterlab-pdf-extract` |
| Convert a document to clean Markdown | `alterlab-markitdown` |
| References / DOIs / BibTeX | `alterlab-pyzotero` |

## Pipeline

Located extractions feed `alterlab-paper-reviewer` and literature-review workflows; escalate to
`alterlab-pdf-extract` when the task becomes a multi-paper corpus table.
