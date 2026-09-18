# TÜBİTAK Açık Bilim Politikası — Binding Mandates

> **Last verified: 2026-06-06.** TÜBİTAK revises this policy. Re-confirm every
> figure and rule against the current policy PDF before a researcher relies on it.

## Source documents

- **TÜBİTAK Açık Bilim Politikası** (Open Science Policy) PDF —
  `https://tubitak.gov.tr/sites/default/files/tubitak_acik_bilim_politikasi_190316.pdf`
  (in force **14 March 2019**).
- **ULAKBİM — Türkiye Açık Arşivi / Aperta** —
  `https://ulakbim.tubitak.gov.tr/en/turkey-open-archive-aperta/`
- Aperta repository: `https://aperta.ulakbim.gov.tr/`

The mandates below are the binding rules verified from the Open Science Policy.
Anything not stated here is intentionally omitted — do not fabricate principle
numbers, exact embargo start-points, or monetary figures.

## Mandate 1 — Green-road deposit of the accepted manuscript, on acceptance

TÜBİTAK-funded research outputs must be deposited via the **green road** (self-
archiving). The object to deposit is the **kabul edilmiş makale** (accepted
manuscript / author-accepted version), and the trigger is **acceptance**, not
publication. Deposit goes to **Aperta** (or another compliant open archive).

Glossary: *yeşil yol* = green road / self-archiving; *kabul edilmiş makale* =
author-accepted manuscript (post-peer-review, pre-typesetting version).

## Mandate 2 — Open-access embargo ceilings (field-dependent)

The deposited output must become **openly accessible** within a maximum embargo
period that depends on the discipline:

| Field bucket (Turkish) | English | Embargo ceiling |
|------------------------|---------|-----------------|
| Fen ve mühendislik bilimleri | STEM (science & engineering) | **≤ 6 months** |
| Sosyal ve beşeri bilimler | SSH (social sciences & humanities) | **≤ 12 months** |

These are **upper bounds**. Immediate open access on deposit is always permitted
and is the preferred outcome. The embargo is the *latest* the work may become
open, not a required waiting period.

> The exact clock start (acceptance date vs publication date) is governed by the
> policy text and any publisher agreement. If a user needs the precise start
> point, direct them to the policy PDF and the publisher's self-archiving terms;
> do not assert it from memory.

## Mandate 3 — Veri Yönetim Planı (VYP) at application time

A **Veri Yönetim Planı / VYP** (data management plan) covering the **full data
lifecycle** is prepared **at grant-application time**. It describes what data the
project will create/collect, formats and standards, storage and preservation,
sharing/access, and the legal/ethical constraints on the data.

The VYP is the funder-facing data plan. For projects handling personal data it
should be developed alongside the **KVKK** compliance analysis — see
`alterlab-kvkk-dmp` for the lawful-basis and anonymisation decision that feeds the
"why is data open/closed" part of the VYP.

## Mandate 4 — İlke-6: documenting closed data

Where research data **cannot be opened**, the reason must be **documented**. Valid
grounds include:

- **KVKK** (Law 6698) — personal data or special-category (health/genetic/
  biometric) data that cannot be shared even after the project ends, where
  anonymisation is not achievable without destroying research value;
- **commercial/IP confidentiality**;
- **security/national-interest** restrictions;
- an **etik kurul** (ethics committee) restriction on data sharing.

The compliant pattern in Aperta is a **restricted (embargoed) record with open
metadata**: the dataset stays discoverable and citable (DOI + metadata) while
access to the files is gated. The documented justification (the "İlke-6
justification") is carried into both the VYP and the project's final report.

Bridge to KVKK: a dataset claimed as "anonymised" only qualifies for open release
if it is **genuinely non-re-identifiable**. Re-identifiable pseudonymised data is
still personal data under KVKK and must be treated as closed/restricted. Get this
determination from `alterlab-kvkk-dmp`, not from this skill.

## Mandate 5 — Report compliance in the final report

Open-access and data-deposition compliance is **reported in the project sonuç
raporu** (final report). The report should, per output, state the Aperta DOI, the
access mode (open/restricted), the open-access date, and — for any closed data —
reference the İlke-6 justification.

## What is deliberately NOT encoded here

To avoid fabrication, this file does **not** assert:

- specific numbered principle labels beyond "İlke-6 = closed-data documentation"
  as named in the project plan;
- any TRY budget cap, application deadline, or program-specific rule (those belong
  to `alterlab-tubitak-proposal`);
- a fixed maximum embargo for data (the 6/12-month ceilings above apply to the
  publication open-access requirement);
- exact clause numbers of the policy PDF.

If a researcher needs any of the above, instruct them to read the current policy
PDF directly and confirm before submission.
