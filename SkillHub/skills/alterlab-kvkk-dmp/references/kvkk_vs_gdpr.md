# KVKK ↔ GDPR Crosswalk — Fixing EU DMP Boilerplate for Türkiye

KVKK (Law 6698) was modelled on the pre-GDPR EU Directive 95/46/EC, so much of
the structure looks familiar — but the divergences below are exactly the places
a reused EU/Horizon-Europe data management plan becomes **non-compliant** in
Türkiye. Audit each clause of an inherited DMP against this table.

Sourced to Law 6698 (mevzuat.gov.tr) and the official KVKK English translation;
GDPR articles are cited for orientation only. Last verified 2026-06-06.

## The four divergences that break EU boilerplate

| Topic | GDPR | KVKK (Law 6698) | What to change in the DMP |
|---|---|---|---|
| **Research lawful basis** | Art. 6 + Art. 9(2)(j) + Art. 89 give scientific research dedicated standing; consent is one option among several | **No standalone research basis.** Art. 5 default is **açık rıza** (explicit consent); otherwise an enumerated Art. 5(2) alternative must fit | Remove any "processing for scientific research (Art. 89 GDPR)" basis. Use explicit consent or a real Art. 5(2) alternative — or anonymize under Art. 28 |
| **Research exemption mechanism** | Research benefits from *derogations* (Art. 89 safeguards) but data stays in scope | **Art. 28(1)(b)** puts **anonymized** research/planning/statistics data **fully outside the scope** of the Law (likewise 28(1)(c) for scientific/artistic) | Make anonymization the lead strategy where the science allows; document the technique and re-identification-risk assessment |
| **Registration** | No general "register before processing" duty (GDPR dropped notification; Art. 30 records are internal) | **Art. 16 VERBIS** — controllers must register with the Data Controllers' Registry **before processing** unless Board-exempted by objective criteria | Add a VERBIS-status section (registered / exempt-by-criterion / pending). An EU DMP will not have one |
| **Cross-border transfer** | Art. 44–49: adequacy, SCCs, BCRs, derogations | **Art. 9, restructured by Law 7499 (Official Gazette 12 Mar 2024; in force 1 Jun 2024)** around **adequacy decisions** + **standard contracts (standart sözleşme)** + safeguards | Replace pre-2024 "consent for each transfer" text; name the Art. 9 mechanism for every non-Türkiye cloud/host |

## Terminology map (use the canonical Turkish term, gloss once)

| English | KVKK term |
|---|---|
| Explicit consent | açık rıza |
| Special-category personal data | özel nitelikli kişisel veri |
| Data controller | veri sorumlusu |
| Data processor | veri işleyen |
| Data subject | ilgili kişi |
| Erasure / destruction / anonymization | silme / yok etme / anonim hale getirme |
| Data Controllers' Registry | VERBIS — Veri Sorumluları Sicili |
| Adequate measures (special category) | yeterli önlemler |
| Adequacy decision (transfer) | yeterlilik kararı |
| Standard contract (transfer) | standart sözleşme |
| Data management plan | veri yönetim planı (VYP) |

## Things that look the same and roughly are

- **Data-subject rights** (access, rectification, erasure, objection) exist under
  both; KVKK Art. 11 enumerates them and Art. 13 sets the **30-day** response
  window (vs GDPR's "without undue delay / one month").
- **Purpose limitation, data minimisation, storage limitation** principles
  appear in KVKK Art. 4 and mirror GDPR Art. 5(1).
- **Special categories** overlap heavily (health, genetic, biometric, religion,
  etc.) but KVKK's list and processing conditions (Art. 6) are **not identical** —
  re-check, do not assume GDPR Art. 9 conditions transfer.

## Bottom line

An EU DMP is a **starting point**, not a compliant Türkiye plan. The minimum
edits are: (1) drop the Art. 89 research basis, (2) foreground Art. 28
anonymization, (3) add VERBIS, (4) rewrite transfers for the 2024 Art. 9 regime.
For non-Turkish processing or pure GDPR/HIPAA questions, use
`alterlab-research-ethics` instead of this skill.
