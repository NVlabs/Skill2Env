---
name: alterlab-clinpgx
description: Access ClinPGx pharmacogenomics data (the successor to PharmGKB) to query gene-drug interactions, CPIC/DPWG dosing guidelines, drug labels, and pharmacogene records. Use when interpreting pharmacogenes (CYP2D6, CYP2C19, TPMT, DPYD, SLCO1B1), looking up genotype-guided drug dosing, checking PGx drug-safety associations (e.g. HLA-B*57:01 and abacavir), or supporting precision medicine and clinical pharmacogenomics decisions. For star-allele definitions/frequencies see PharmVar; for germline/somatic variant pathogenicity see alterlab-clinvar. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Keyless ClinPGx (PharmGKB) API for basic access (no authentication required)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# ClinPGx Database

## Overview

ClinPGx (Clinical Pharmacogenomics Database) is a comprehensive resource for
clinical pharmacogenomics, the successor to PharmGKB. It consolidates data from
PharmGKB, CPIC, and PharmCAT, providing curated information on how genetic
variation affects medication response. Access gene-drug pairs, clinical
guidelines, allele functions, and drug labels for precision medicine.

## When to Use This Skill

Use this skill for:

- **Gene-drug interactions** — how variants affect drug metabolism, efficacy, or toxicity
- **CPIC guidelines** — evidence-based clinical practice guidelines for pharmacogenetics
- **Allele information** — allele function, frequency, and phenotype data
- **Drug labels** — FDA and other regulatory pharmacogenomic labeling
- **Pharmacogenomic annotations** — curated literature on gene-drug-disease relationships
- **Clinical decision support** — PharmDOG for phenoconversion and custom genotype interpretation
- **Precision medicine / personalized dosing** — genotype-guided dosing recommendations
- **Drug metabolism** — CYP450 and other pharmacogene functions
- **Adverse drug reactions** — genetic risk factors for drug toxicity

## Setup and Access Essentials

Only `requests` is needed. Run the helper script (or any snippet) with an
ephemeral dependency — no venv to manage:

```bash
uv run --with requests python scripts/query_clinpgx.py
# or, inside an existing project venv: uv pip install requests
```

Base URL: `https://api.clinpgx.org/v1/data/`

- **Resource addressing**: ClinPGx resources are addressed by ClinPGx accession
  IDs in the path (e.g. gene CYP2D6 = `PA128`, CYP2C9 = `PA126`), **not** by gene
  symbols or rsIDs. To resolve a symbol or rsID, query the collection endpoint
  with parameters (e.g. `GET /v1/data/gene?symbol=CYP2D6`,
  `GET /v1/data/variant?symbol=rs4244285`) and read the accession ID from the
  response.
- **Response envelope** (verified): every response is a JSON object
  `{"status": "success"|"fail", "data": [...]}` — the payload is **never** a bare
  list. Read results from `response.json()["data"]`; on `status == "fail"`,
  `data` is `{"errors": [...]}` (e.g. "No results matching criteria").
- **Query-param convention** (verified): genes filter on `relatedGenes.symbol`
  (the `.name` form fails), while chemicals/drugs filter on
  `relatedChemicals.name` — `relatedChemicals.symbol` silently returns
  `status: "fail"` with zero results. The `gene` collection takes `?symbol=`, the
  `chemical` collection takes `?name=`, and `variant` accepts `?symbol=`/`?name=`.
- **Rate limits**: 2 requests per second maximum; excessive requests return HTTP
  429. Implement a ~500ms delay between requests.
- **Authentication**: Not required for basic access.
- **Data license**: Creative Commons Attribution-ShareAlike 4.0 International.
- For substantial API use, notify the ClinPGx team at **api@clinpgx.org**.

## Core Workflow

1. **Resolve identifiers** — Convert gene symbols / rsIDs to ClinPGx accession
   IDs via collection endpoints with `symbol=` parameters.
2. **Query the relevant resource** — `gene`, `chemical`, `guidelineAnnotation`,
   `summaryAnnotation`, `variantAnnotation`, `variant`, `label`, or `pathway`.
   There is no `/allele` resource — use **PharmVar** (https://www.pharmvar.org/)
   for star-allele definitions and population frequencies.
3. **Derive gene-drug relationships** — From guideline annotations
   (`relatedGenes.symbol` for genes, `relatedChemicals.name` for drugs), or the
   `/report/pair/{firstObjId}/{secondObjId}/{resultType}` endpoint.
4. **Filter by evidence level** — Prefer levels 1A/1B/2A for clinical use;
   confirm field names against the live OpenAPI spec.
5. **Respect rate limits** — Throttle, retry on 429 with backoff, and cache.

For ready-made functions with rate limiting and error handling, see
`scripts/query_clinpgx.py`.

## Routing Guidance

- **Need the exact code for a resource (gene, chemical, gene-drug pair, CPIC
  guideline, allele/PharmVar, variant, clinical annotation, label, pathway)?**
  Read `references/endpoints-and-capabilities.md`.
- **Doing an end-to-end task (clinical decision support, gene-panel analysis,
  drug-safety assessment, population pharmacogenomics, literature review) or a
  common use case?** Read `references/query-workflows.md`.
- **Need robust API plumbing (rate limiting, retries, caching)?** Read
  `references/rate-limiting-and-error-handling.md`.
- **Need full endpoint/parameter/schema details?** Read
  `references/api_reference.md`.

## References

- `references/api_reference.md` — Complete endpoint listing, request/response
  formats, filter operators, data schemas, rate-limit details, and
  troubleshooting.
- `references/endpoints-and-capabilities.md` — Worked code for all nine
  capability areas (gene, drug/chemical, gene-drug pair, CPIC guidelines,
  allele/PharmVar, variant, clinical annotations, drug labels, pathways),
  including key pharmacogenes and evidence-level definitions.
- `references/query-workflows.md` — Five end-to-end workflows (decision support,
  gene panel, drug safety, population pharmacogenomics, literature review) plus
  common use cases (pre-emptive testing, medication therapy management, trial
  eligibility).
- `references/rate-limiting-and-error-handling.md` — Reusable helpers for rate
  limiting, retries with exponential backoff, and result caching.

## PharmDOG Tool

PharmDOG (formerly DDRx) is ClinPGx's clinical decision support tool for
interpreting pharmacogenomic test results. Features: phenoconversion calculator
(adjusts phenotype for drug-drug interactions affecting CYP2D6), custom genotype
input, QR-code report sharing, selectable guidance sources (CPIC, DPWG, FDA), and
multi-drug analysis. Access:
https://www.clinpgx.org/pharmacogenomic-decision-support

## Important Notes

**Data sources** — ClinPGx consolidates PharmGKB (now part of ClinPGx), CPIC,
PharmCAT, DPWG, and FDA/EMA labels. As of July 2025, all PharmGKB URLs redirect
to corresponding ClinPGx pages.

**Clinical considerations** — Always check evidence strength before clinical
application; allele frequencies vary significantly across populations; account
for phenoconversion (drug-drug interactions) and multi-gene effects; non-genetic
factors (age, organ function) also affect response; not all clinically relevant
alleles are detected by all assays.

**Data updates / API stability** — ClinPGx updates continuously; check
publication dates and the ClinPGx Blog (https://blog.clinpgx.org/). API endpoints
are relatively stable but may change during development — pin versions and test
in development before production.

## Additional Resources

- **ClinPGx website**: https://www.clinpgx.org/
- **ClinPGx Blog**: https://blog.clinpgx.org/
- **API documentation**: https://api.clinpgx.org/
- **CPIC website**: https://cpicpgx.org/
- **PharmCAT**: https://pharmcat.clinpgx.org/
- **PharmVar** (star alleles): https://www.pharmvar.org/
- **ClinGen**: https://clinicalgenome.org/
- **Contact**: api@clinpgx.org (for substantial API use)
