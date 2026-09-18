# Bilgilendirilmiş Gönüllü Olur Formu — Minimum Content (TİTCK, 29 Mar 2023)

The participant-facing informed-consent form (*Bilgilendirilmiş Gönüllü Olur
Formu*; also called *onam formu* / *olur formu*) must carry, at minimum, the
elements below. This checklist is the source of truth for the linter in
`scripts/consent_form_check.py`, which scans a draft for each element (Turkish or
English wording) and reports PASS / MISSING per element.

Glossary: *gönüllü* = volunteer / participant; *onam* = assent/consent; *olur* =
consent; *parafe* = initials.

> A linter PASS means the **checklist elements are present**, not that the wording
> satisfies the committee. The institution's own template and the committee's
> decision are authoritative.

---

## Required Elements

| # | Element (TR) | Element (EN) | What it requires |
|---|--------------|--------------|------------------|
| 1 | Tarih, versiyon ve sayfa numarası | Date, version, page numbers | Every page carries a date, a version, and page numbering. |
| 2 | Gönüllü parafe alanı | Volunteer initials per page | (Clinical track) the participant initials each page. |
| 3 | Çalışmanın amacı (sade dil) | Purpose, in plain language | Why the study is done, stated without jargon. |
| 4 | İşlemler ve süre | Procedures and duration | What the participant will do and how long it takes. |
| 5 | Öngörülen riskler / rahatsızlıklar | Foreseeable risks / discomforts | Honest statement of risks and burdens. |
| 6 | Beklenen yararlar | Expected benefits | Benefits to the participant and/or to science. |
| 7 | 24 saat ulaşılabilir iletişim | 24-hour contact | A contact reachable for problems/questions. |
| 8 | Gönüllülük beyanı | Voluntary-participation statement | Participation is voluntary. |
| 9 | İstediği zaman ayrılma hakkı | Right to withdraw at any time | May withdraw anytime without penalty. |
| 10 | Baskı/zorlama olmadığı beyanı | No-coercion statement | No pressure or inducement to participate. |
| 11 | Gizlilik / veri kullanımı | Confidentiality / data use | How data are kept confidential and used (link to the KVKK plan). |

### Clinical-track additions (Door 2 studies)

For TİTCK clinical-track studies, the form additionally addresses, as the
regulation requires:

- **Sigorta** — insurance coverage for the participant.
- **Alternatif tedaviler** — available alternative treatments.
- **Sponsor / sorumlu araştırmacı** — sponsor and responsible-investigator
  contact chain.

---

## Notes for Drafting

- Keep Turkish as the primary language; add an English gloss only where a
  bilingual form is needed (e.g. non-Turkish-speaking participants).
- Write at a **plain-language** reading level — avoid clinical and legal jargon.
- The **confidentiality / data-use** element (11) is the bridge to KVKK: describe
  it here briefly, and produce the full KVKK-compliant data plan with
  `alterlab-kvkk-dmp`.
- Vulnerable groups: pair the consent with guardian consent + age-appropriate
  assent (çocuk rızası) for minors, and document any additional safeguards.

---

## Source

- TİTCK informed-consent minimum contents, updated **29 March 2023**.
- *Beşeri Tıbbi Ürünlerin Klinik Araştırmaları Hakkında Yönetmelik* —
  mevzuat.gov.tr MevzuatNo 40207 (R.G. 27/5/2023, No. 32203) for the clinical-track
  consent requirements.

_Last verified: 2026-06-06. The minimum-content list is periodically updated by
TİTCK — re-verify against the current TİTCK document before finalizing a form._
