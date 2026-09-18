# ÜAK Doçentlik Criteria — Bundled Table (Sağlık Bilimleri)

> **last_verified: 2026-06-08** — Sağlık Bilimleri (Health Sciences) TABLO 10,
> re-verified against the primary ÜAK source and multiple corroborating
> summaries of the **2025 Mart dönemi** criteria on this date.
>
> **These numbers change every application term (başvuru dönemi).** Always
> re-confirm the live criteria for the candidate's own field and term before
> relying on any output — see *Primary sources* below.

## Contents

- What "doçentlik" is
- Mandatory minimums — MODELLED by the scorer
- Mandatory minimums — NOT modelled (verify by hand)
- Per-index point table — Sağlık Bilimleri TABLO 10
- Why this skill is a PARTIAL pre-screen
- Other fields
- Primary sources (re-verify here)

## What "doçentlik" is

**Doçentlik** is the Turkish associate-professorship title, awarded through a
national procedure run by **ÜAK** (Üniversitelerarası Kurul / the Inter-University
Council). Eligibility to *apply* is gated by an objective, points-based
publication threshold plus several category-specific mandatory minimums; the
bundled table and minimums below encode that gate for the **Sağlık Bilimleri
(Health Sciences)** field only. Applications open twice a year (15 March and
15 October per the Doçentlik Yönetmeliği).

## Mandatory minimums — MODELLED by the scorer

`score_docentlik.py` computes these four from a publication list and pass/fail
checks each. **All four must pass** before the scorer returns its non-green
`PRESCREEN_PASS_VERIFY_REMAINING` status (it never returns "ELIGIBLE").

| Check | Threshold | Notes |
|---|---|---|
| Total points | **≥ 100** | Sum of all scored work (pre- and post-doctorate). |
| Post-doctorate points | **≥ 90** | Points from work after the doctorate / uzmanlık (doktora/uzmanlık sonrası). |
| International SCIE/SSCI article points | **≥ 40** | Points from SCIE/SSCI **Q1–Q4** articles, post-doctorate. |
| Lead-author Q-indexed articles | **≥ 3** | Q1–Q4 (SCIE/SSCI) articles where the candidate is **başlıca yazar**; **Q4 counts** ("Q4'ler dahil"). |

## Mandatory minimums — NOT modelled (verify by hand)

The live TABLO 10 also imposes the following mandatory minimums (asgari
koşullar). The scorer **does not** compute these because a bare publication list
does not carry the needed inputs (citation counts, congress papers, teaching,
sub-category tags). They are **verified to exist** in the criteria and are
emitted in every report under `summary.unmodelled_minimums` so the output can
never be mistaken for a complete eligibility decision. Confirm the exact
thresholds and wording against the live source for the candidate's term.

| Requirement | Threshold (as captured) | Why not modelled |
|---|---|---|
| National / TR Dizin articles | ≥ 3 ulusal makale, ≥ 2 in TR Dizin, candidate başlıca yazar in ≥ 2 (post-doctorate) | Needs ulusal-vs-TR-Dizin status + a per-article lead-author count; resolve TR Dizin status with `alterlab-trdizin` first. |
| Citation (atıf) | ≥ 5 points (post-doctorate) | Citation counts are not in the publication list. |
| Scientific meeting (bilimsel toplantı / bildiri) | ≥ 5 points | Congress papers are a separate category, not in the article list. |
| Education / teaching (eğitim-öğretim) | ≥ 2 points | Teaching activity is not a publication. |
| Per-category point caps | thesis-derived ≤ 20, books ≤ 20, citation ≤ 10, project ≤ 20, thesis supervision ≤ 10, patent ≤ 20, award ≤ 25 (verify) | Caps need each item tagged with its TABLO 10 sub-category, which the input does not carry; an uncapped raw total can therefore overstate the usable total. |

> The cap values above come from a single secondary summary and are **not**
> independently primary-source-confirmed at the value level. Treat them as a
> checklist of caps that EXIST, not as authoritative numbers — verify each
> against the live TABLO 10 PDF.

## Per-index point table — Sağlık Bilimleri TABLO 10

| Index tier | Code | Points |
|---|---|---|
| SCI-E / SSCI, 1st quartile | `Q1` | 30 |
| 2nd quartile | `Q2` | 20 |
| 3rd quartile | `Q3` | 15 |
| 4th quartile | `Q4` | 10 |
| Arts & Humanities Citation Index | `AHCI` | 20 |
| Emerging Sources Citation Index | `ESCI` | 10 |
| TR Dizin (ULAKBİM national index) | `TRDizin` | 10 |

**Index tier glossary**

- **Q1–Q4** — journal quartile within its Web of Science subject category
  (Q1 = top 25%). Resolve from the candidate's own JCR/index records. For Sağlık,
  Q1–Q4 all count toward both the ≥40 international-points floor and the ≥3
  lead-author minimum.
- **AHCI / ESCI** — Web of Science indexes without quartile ranking; they score a
  flat value and do **not** count toward the SCIE/SSCI ≥40 floor or the
  lead-author *Q-article* minimum.
- **TR Dizin** — TÜBİTAK ULAKBİM's national citation index. Whether a journal is
  *currently* TR Dizin-indexed is a live status — confirm with `alterlab-trdizin`
  before scoring; DergiPark hosting does **not** imply TR Dizin indexing.

## Why this skill is a PARTIAL pre-screen

The scorer models 4 of the TABLO 10 mandatory minimums but not the national /
citation / congress / education minimums or the per-category caps (above).
Clearing the modelled checks is **necessary but not sufficient** for
eligibility. Accordingly the scorer's verdict vocabulary is deliberately
**FAIL_MODELLED_CHECK** / **PRESCREEN_PASS_VERIFY_REMAINING** — it has **no
"ELIGIBLE" state** and structurally cannot emit a green eligibility verdict. The
official decision is the doçentlik jury's.

## Other fields

Other ÜAK fields (Fen ve Mühendislik / Sciences & Engineering, Sosyal ve Beşeri /
Social Sciences & Humanities, Güzel Sanatlar / Fine Arts, Hukuk / Law, İlahiyat /
Theology, …) each have their **own** point table with **different** values and
different category-specific minimums (each is a separate TABLO). The bundled
table here is Sağlık only. To score another field, supply that field's table
from the live ÜAK source — never reuse the Sağlık numbers.

## Primary sources (re-verify here)

- **ÜAK** — Doçentlik başvuru şartları and the per-field criteria tables:
  <https://www.uak.gov.tr/page/docentlik-basvuru-sartlari-kLPHX>
  (Sağlık Bilimleri TABLO 10 PDF: `uak.gov.tr/documents/documents/688340614375c.pdf`).
- **Doçentlik Yönetmeliği** — the binding regulation (Resmî Gazete 15/4/2018,
  No. 30392), on the official legislation portal:
  `mevzuat.gov.tr/mevzuat?MevzuatNo=24519&MevzuatTur=7&MevzuatTertip=5`
  (Resmî Gazete copy: `resmigazete.gov.tr/eskiler/2018/04/20180415-3.htm`).
  Note: `mevzuat.gov.tr/MevzuatMetin/21.5.201811834.pdf` is a *different*
  regulation — the **Akademik Teşvik Ödeneği Yönetmeliği** (see
  `alterlab-akademik-tesvik`), not the doçentlik binding regulation.

> The point values and the existence of each mandatory minimum above were
> re-verified on the `last_verified` date against the ÜAK TABLO 10 source and
> corroborating summaries of the 2025 Mart term. ÜAK can revise them between
> terms without notice in this file; the primary ÜAK PDF is authoritative.
> Where a value is single-source (the per-category caps), it is flagged as such
> above — do not present it as confirmed.
