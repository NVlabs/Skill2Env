# Aperta — Repository Facts & Deposit Checklist

> **Last verified: 2026-06-06.** Confirm the live submission form before depositing.

## What Aperta is

| Property | Value | Source |
|----------|-------|--------|
| Name | Aperta — Türkiye Açık Arşivi (Turkey Open Archive) | ULAKBİM page |
| Operator | TÜBİTAK ULAKBİM | ULAKBİM page |
| URL | `https://aperta.ulakbim.gov.tr/` | ULAKBİM page |
| Purpose | Archive that stores, preserves, manages, indexes and gives free access to articles from TÜBİTAK academic journals and their research data, plus TÜBİTAK-funded and UBYT-incentivised outputs | ULAKBİM page |
| Platform | **InvenioRDM**-based research-data repository | project key_resources (pre-verified) |
| Persistent ID | Assigns a **DOI** per record | project key_resources (pre-verified) |
| Access modes | Open, **restricted/embargoed**, **versioned** records | project key_resources (pre-verified) |

The operator, URL and purpose are confirmed on ULAKBİM's own page
(`ulakbim.tubitak.gov.tr/en/turkey-open-archive-aperta/`). The platform
(InvenioRDM), per-record DOI minting, restricted-access support and versioning
are taken from the project's pre-verified resource list. **Do not assert other
repository features** (e.g. specific metadata schemas, API routes, file-size
limits) — they are not verified here; check the live site if a user needs them.

## Why InvenioRDM matters for compliance

InvenioRDM separates **metadata** (always public) from **files** (which can be
open, embargoed, or restricted). That is exactly the shape İlke-6 needs: a closed
clinical/KVKK dataset can have a public, citable record (title, authors, abstract,
DOI) while the data files sit behind restricted access. Versioning lets a later,
opened or anonymised version supersede an embargoed one without losing the DOI
lineage.

## Deposit checklist (per record)

Walk these for each manuscript or dataset. Field names mirror a generic
InvenioRDM deposit form; confirm exact labels on the live Aperta form.

1. **Resource type** — publication (accepted manuscript) vs dataset vs both.
2. **Object/version** — for a publication, upload the **kabul edilmiş makale**
   (author-accepted version), unless the publisher permits the version of record.
3. **Core metadata** — title, creators (with affiliations/ORCID if available),
   publication/issue date, language, abstract, keywords.
4. **Funding** — record the TÜBİTAK project (program + grant number) so the
   deposit is linked to the funded project for final-report reporting.
5. **Licence** — choose an open licence for openly-released outputs (the policy
   favours open access; the specific licence is the author's/publisher's call).
6. **Access mode** —
   - *Open* → set the open-access date to satisfy the field embargo ceiling
     (≤ 6 mo STEM / ≤ 12 mo SSH; see `policy_mandates.md`).
   - *Restricted/embargoed* → keep metadata public; gate the files; attach the
     İlke-6 justification. Set the embargo lift date if the closure is temporary.
7. **DOI** — let Aperta mint the DOI; capture it for the final report.
8. **Version** — if replacing an earlier embargoed/preprint version, add a new
   version rather than a new record to preserve citation lineage.

## After deposit

- Record the **DOI**, the **access mode**, and the **open-access date** for the
  project's *sonuç raporu* (final report) compliance statement.
- If anything is restricted, ensure the İlke-6 justification is on file and
  referenced from the VYP.

## Not Aperta's job (route elsewhere)

- International deposit (Zenodo/Dryad/Figshare/OSF), open-access routes, or
  preprint posting to arXiv/bioRxiv/SSRN → `alterlab-open-science`.
- The KVKK lawful-basis/anonymisation determination → `alterlab-kvkk-dmp`.
