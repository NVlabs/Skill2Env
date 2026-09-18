---
name: alterlab-kvkk-dmp
description: "Produces KVKK-compliant (Law 6698, as amended by Law 7499 — published in the Official Gazette 12 Mar 2024, KVKK provisions effective 1 Jun 2024) data management plans for Turkish research, encoding the açık rıza (explicit consent) default basis, the Art. 28(1)(b) anonymization exemption as the primary compliance lever, the Art. 6 special-category regime for health/genetic/biometric data, Art. 7 deletion/destruction/anonymization at purpose-end, the Art. 13 thirty-day data-subject response window, Art. 9 cross-border adequacy-decision rules for cloud/overseas data, and Art. 16 VERBIS pre-processing registration, with a KVKK-vs-GDPR crosswalk. Use when the user needs a KVKK data management plan, to anonymize a research dataset under Turkish law, a VERBIS check, or to fix EU DMP boilerplate for Turkey; for pure GDPR/HIPAA use alterlab-research-ethics. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key required — generates KVKK data management plans from primary mevzuat (Law 6698) encoded in references/; the optional scaffold runs via `uv run python` on the standard library only
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-tr-research-ethics (etik kurul routing), alterlab-aperta (TÜBİTAK open-science / VYP)"
---

# KVKK Data Management Plan — Compliance Scaffolding for Turkish Research Data

Generates a **KVKK** (Kişisel Verilerin Korunması Kanunu — Turkey's Personal
Data Protection Law, No. 6698) data management plan for empirical research, and
audits EU/GDPR DMP boilerplate for the points where Turkish law **diverges**.
KVKK applies to essentially all Turkish empirical research that touches
personal data, yet it is not GDPR: the lawful-basis menu is narrower, the
research exemption works differently, and registration (**VERBIS**) and
cross-border rules are Turkey-specific. This skill encodes those divergences so
a researcher does not silently reuse an EU plan that is non-compliant in Türkiye.

All article references trace to the primary text of Law 6698
(mevzuat.gov.tr) and the official KVKK English translation; the substantive
divergences are tabulated in `references/kvkk_vs_gdpr.md`. Anonymization
techniques and the re-identification trap are in
`references/anonymization_methods.md`. Article-level detail with the exact
exemption wording is in `references/kvkk_articles.md`.

## When to Use This Skill

Use this skill when the request is about **Turkish data-protection compliance
for research data** — producing or fixing a data management plan under KVKK,
deciding whether a dataset can ride the anonymization exemption, choosing a
lawful basis (açık rıza — explicit consent — vs. an Art. 5/6 alternative),
planning retention and deletion at purpose-end, checking whether **VERBIS**
registration is required, or assessing a cloud/overseas transfer under Art. 9.

Typical triggers:

- "KVKK uyumlu veri yönetim planı hazırla" (prepare a KVKK-compliant DMP)
- "Anonymize this research dataset so it falls under the KVKK research exemption"
- "VERBIS kaydı gerekli mi?" (is VERBIS registration required?)
- "I have an EU Horizon DMP — make it KVKK-compliant for my Türkiye site"
- "Can I store this survey data on a US cloud under KVKK?"
- "We collect health/biometric data — what does Art. 6 require?"

### Does NOT Trigger

Route adjacent requests to the correct sibling skill instead of forcing this one:

| The user actually wants… | Route to | Why not this skill |
|---|---|---|
| GDPR / HIPAA / non-Turkish data-protection compliance | `alterlab-research-ethics` | This skill is KVKK-only; the international ethics/privacy skill owns GDPR/HIPAA |
| An **etik kurul** (ethics committee) application or which committee is needed (anket/TİTCK) | `alterlab-tr-research-ethics` | That skill scaffolds the Turkish ethics-board submission; KVKK-DMP covers data protection, not ethics review |
| Depositing accepted manuscripts / data in **Aperta** or a TÜBİTAK open-science **VYP** (veri yönetim planı / data-management plan) for the funder | `alterlab-aperta` | Aperta owns the TÜBİTAK open-science mandate and funder-facing VYP; KVKK-DMP only supplies the Principle-6 "why data is closed" justification |
| Building a TÜBİTAK ARDEB 1001/1002-A proposal | `alterlab-tubitak-proposal` | That skill scaffolds the proposal form; KVKK-DMP only fills the data-protection annex |
| Building a data-capture instrument / survey (Qualtrics, REDCap) or questionnaire | `alterlab-survey-design` | That owns instrument design; KVKK-DMP governs the legal-basis/retention layer over the data they collect |
| Turkish APA-7 / TR Dizin citation style or academic-writing conventions | `alterlab-tr-academic-style` | Style, not data protection |

If a workflow needs both a **funder VYP** (Aperta) and a **KVKK DMP** (here),
produce the KVKK plan first and hand its lawful-basis / anonymization decision
to `alterlab-aperta` to populate the open-science Principle-6 justification.

## The Six Decisions a KVKK DMP Must Resolve

A compliant plan answers these in order. Each maps to a specific article of Law
6698 (full wording in `references/kvkk_articles.md`).

1. **Lawful basis (Art. 5 / Art. 6).** The default is **açık rıza** (explicit
   consent). Unlike GDPR Art. 6, KVKK Art. 5 has **no standalone "scientific
   research" lawful basis** — if consent is not used, the processing must fit one
   of the enumerated Art. 5(2) alternatives (e.g. legal obligation, a contract,
   data made public by the subject, legitimate interest). Special-category data
   (sağlık/health, genetic, biometric, religious belief, etc.) falls under
   **Art. 6**, where processing is prohibited except in enumerated cases and the
   Board can mandate **adequate measures** (yeterli önlemler).

2. **Anonymization exemption (Art. 28(1)(b)) — the primary compliance lever.**
   Personal data that are **anonymized** for research, planning and statistics
   fall **outside the scope of the Law** under Art. 28(1)(b). Art. 28(1)(c)
   similarly exempts processing for scientific/artistic/literary purposes within
   limits. This is the single most powerful move in a research DMP: a genuinely
   anonymized dataset escapes consent, VERBIS, and transfer constraints.
   **Caveat:** data that remain re-identifiable are *not* anonymized and do **not**
   qualify — see `references/anonymization_methods.md`. Pseudonymized data are
   still personal data.

3. **Retention & destruction at purpose-end (Art. 7).** When the reasons for
   processing no longer exist, data must be **erased, destroyed, or anonymized**
   (silme / yok etme / anonim hale getirme) ex officio or on the data subject's
   request, per the KVKK By-Law on Erasure, Destruction or Anonymization. The DMP
   states a retention period and the destruction method for each data category.

4. **Data-subject rights & the response window (Art. 13).** A controller must
   answer a data-subject application **within thirty days** (otuz gün) at the
   latest. The DMP names the contact point and the procedure.

5. **Cross-border transfer (Art. 9, as amended by Law 7499 — published in the
   Official Gazette 12 Mar 2024, RG No. 32487; KVKK provisions effective 1 Jun
   2024).** Overseas/cloud storage needs either an **adequacy decision** by the
   Board or one of the enumerated safeguards (standard contracts, binding
   corporate rules, written undertakings, etc.). The Law 7499 amendment
   restructured Art. 9 around adequacy decisions and standard contracts — do not
   reuse pre-2024 "explicit consent for every transfer" boilerplate. Flag any
   non-Türkiye cloud.

6. **VERBIS registration (Art. 16).** Controllers must register with the **Veri
   Sorumluları Sicili** (VERBIS — Data Controllers' Registry) **before**
   processing, though the Board exempts categories by objective criteria. The DMP
   records VERBIS status (registered / exempt-by-criterion / pending) with the
   reason.

A worked walkthrough of all six on a sample survey + health-data project is in
`references/dmp_walkthrough.md`.

## How to Produce the Plan

1. **Classify the data.** For each data category, decide: personal vs.
   special-category (Art. 6), and identifiable vs. (intended-)anonymized.
2. **Pick the lever.** If the research questions can be answered on anonymized
   data, plan for Art. 28(1)(b) anonymization at the earliest point and document
   the technique and the re-identification-risk assessment. Otherwise select an
   Art. 5/6 lawful basis (default açık rıza) and justify it.
3. **Fill the six decisions** above into the DMP sections.
4. **Run the scaffold** (optional, deterministic) to emit a structured TR+EN DMP
   skeleton you then complete and review:

   ```bash
   uv run python skills/turkish-academia/alterlab-kvkk-dmp/scripts/kvkk_dmp_scaffold.py \
       --title "Project title" \
       --basis explicit-consent \
       --special-category health \
       --retention "5 years post-publication" \
       --cross-border none \
       --verbis registered \
       --lang both \
       --out kvkk_dmp.md
   ```

   The scaffold writes only a template grounded in the encoded article map; it
   makes **no legal determination** and reaches no network. Run
   `--help` for all flags, or `--self-check` to validate the article encoding.
5. **Audit reused EU/GDPR boilerplate** against `references/kvkk_vs_gdpr.md` and
   rewrite each divergent clause (no research basis; anonymization exemption;
   VERBIS; 2024 transfer rules).

## Hard Rules (do not violate)

- **Never claim a dataset is anonymized if it is re-identifiable.** Re-identifiable
  "anonymized" data does not qualify for the Art. 28 exemption and remains fully
  in scope. Pseudonymization is not anonymization.
- **Do not invent an Art. 5 "research" basis.** KVKK has none; use consent or a
  real enumerated alternative, or anonymize.
- **Cite base figures and mechanisms, not stale amounts.** KVKK Art. 18
  administrative fines are revalued every January under the Tax Procedure Law
  (Vergi Usul Kanunu) revaluation rate — cite the mechanism and direct the user to
  verify the current-year figure; do not hard-code a TRY amount.
- **Verify against the current law before relying on an output.** Flag the Law
  7499 amendments (Art. 6, 9, 18) — adopted 2 Mar 2024, published in the Official
  Gazette 12 Mar 2024 (RG No. 32487), KVKK provisions effective 1 Jun 2024 — as
  the most recent substantive change.
- This skill produces compliance **scaffolding**, not legal advice; recommend a
  Veri Sorumlusu / KVKK officer (or counsel) sign-off for high-risk processing.

## References

- `references/kvkk_articles.md` — article-by-article map (Art. 5, 6, 7, 9, 13, 16,
  28) with the exact exemption wording, sourced to Law 6698.
- `references/kvkk_vs_gdpr.md` — KVKK↔GDPR crosswalk: the four divergences that
  break EU DMP boilerplate (no research basis, anonymization exemption, VERBIS,
  2024 transfer reform).
- `references/anonymization_methods.md` — masking, aggregation, generalization
  (k-anonymity-style), and the re-identification trap that voids Art. 28.
- `references/dmp_walkthrough.md` — the six decisions worked end-to-end on a
  sample survey + health-data study, with a fill-in DMP outline.

### Primary sources

- Law 6698 (KVKK) full text — https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6698.pdf
- KVKK official English translation — https://www.kvkk.gov.tr/Icerik/6649/Personal-Data-Protection-Law
- By-Law on Erasure, Destruction or Anonymization of Personal Data — https://www.kvkk.gov.tr/Icerik/6636/By-Law-on-Erasure-Destruction-or-Anonymization-of-Personal-Data
- VERBIS (Data Controllers' Registry) — https://www.kvkk.gov.tr/Icerik/2043/
- Law 7499 — amendments to Art. 6, 9, 18 (adopted 2 Mar 2024; published in the Official Gazette 12 Mar 2024, RG No. 32487 — https://www.resmigazete.gov.tr/eskiler/2024/03/20240312-1.htm; KVKK provisions effective 1 Jun 2024)

Part of the AlterLab Academic Skills suite.
