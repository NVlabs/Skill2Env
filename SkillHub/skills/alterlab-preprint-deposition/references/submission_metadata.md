# Submission Metadata Checklist

The fields each server asks for at deposit time. Assemble these *before*
starting the web submission so the upload is one pass. To **reuse an existing
record's** metadata (e.g. copy categories from a related arXiv paper), defer to
`alterlab-arxiv` / `alterlab-biorxiv` for the lookup — this skill prepares the
*new* submission, it does not search.

## Contents

- [Universal fields](#universal-fields-all-servers)
- [arXiv specifics](#arxiv-specifics)
- [bioRxiv / medRxiv specifics](#biorxiv--medrxiv-specifics)
- [SSRN / OSF specifics](#ssrn--osf-specifics)
- [Pre-submission file checklist](#pre-submission-file-checklist)

## Universal fields (all servers)

- **Title** — final, matches the manuscript.
- **Authors** — full names, order, **ORCID iDs**, affiliations, the
  corresponding author and contact email.
- **Abstract** — plain text; check the server's length/format limits.
- **License** — chosen per `licensing.md`.
- **Declarations** — competing interests, funding/grant numbers, data & code
  availability statement.
- **Manuscript file** — typically **PDF**; arXiv also accepts (La)TeX source.

## arXiv specifics

- **Primary category** — one required (e.g. `cs.CL`, `q-bio.GN`, `stat.ML`,
  `eess.IV`). Drives moderation routing and discovery.
- **Cross-list categories** — optional secondary categories for reach.
- **Endorsement** — first-time submitters in some archives need an endorser.
- **Comments field** — page/figure counts, "submitted to <venue>", or version
  notes (do not put the license here).
- **MSC / ACM class** — optional subject codes for math/CS.
- Source vs PDF: submitting LaTeX source lets arXiv build the PDF and enables
  some features; a PDF-only submission is also accepted.

## bioRxiv / medRxiv specifics

- **Subject collection / category** — one required from the server's controlled
  list (e.g. Genomics, Neuroscience for bioRxiv; Infectious Diseases, Public &
  Global Health for medRxiv).
- **Manuscript type** — new results / confirmatory / contradictory, etc.
- **medRxiv only:** trial registration number (if applicable), ethics/IRB
  statement, and confirmation there are no identifiable patient data.
- **Author-supplied DOI link** — leave for post-publication linking (the server
  also auto-detects many links).

## SSRN / OSF specifics

- **SSRN:** classification codes (e.g. JEL for economics), keywords, abstract;
  network/series selection.
- **OSF Preprints:** choose the **provider** (general OSF or a community server),
  subjects/tags, and a license from the provider's allowed set.

## Pre-submission file checklist

- [ ] Final PDF (and LaTeX source for arXiv if desired).
- [ ] Figures/tables embedded or in the server's required form.
- [ ] Supplementary files within size limits.
- [ ] ORCID confirmed for the submitting author.
- [ ] Funding/grant IDs and data/code availability statement written.
- [ ] License decided and reconciled with funder + journal (`licensing.md`,
      `journal_policy.md`).
- [ ] No embedded identifiable personal data (especially medRxiv).
