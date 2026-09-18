# Etik Kurul Routing — Which Committee Does Your Study Need?

Turkish human-subjects ethics review has **two doors**. Route by what the study
*does to or with participants*, not by discipline. Sending a study to the wrong
committee wastes a review cycle and, for clinical work, can invalidate the
approval entirely.

Glossary: *etik kurul* = ethics committee; *girişimsel olmayan* = non-interventional;
*klinik araştırma* = clinical research; *TİTCK* = Türkiye İlaç ve Tıbbi Cihaz Kurumu
(Turkish Medicines and Medical Devices Agency); *BA/BE* = biyoyararlanım /
biyoeşdeğerlik (bioavailability / bioequivalence); *izin* = permit.

---

## Door 1 — Üniversite Girişimsel Olmayan Etik Kurulu (non-interventional committee)

**Trigger (the TR Dizin / ULAKBİM rule, mandatory for publications from 2020):**
any study that collects data **from participants** by one of these methods needs
ethics-committee approval before data collection:

- **Anket** — survey / questionnaire
- **Görüşme / mülakat** — interview
- **Odak grup** — focus group
- **Gözlem** — observation
- **Deney** — experiment (non-clinical, e.g. behavioral/educational tasks)

For social, behavioral, educational, and other **non-clinical** human-subjects
research, this is the researcher's **own university's non-interventional ethics
committee** (Girişimsel Olmayan Klinik Araştırmalar / Sosyal ve Beşeri Bilimler
Etik Kurulu, depending on the institution's naming).

What this committee reviews: study aim, design, sampling, instruments,
risk/benefit to participants, the informed-consent procedure, and data-handling
(at a high level — the detailed KVKK data plan is a separate track; route to
`alterlab-kvkk-dmp`).

---

## Door 2 — TİTCK-onaylı Klinik Araştırmalar Etik Kurulu + ayrı TİTCK izni

**Trigger:** the study involves any of —

- **Beşeri tıbbi ürün** — human medicinal product (drug) research
- **Tıbbi cihaz** — medical device research
- **Kozmetik** — cosmetic product research
- **Kök hücre** — stem-cell research
- **BA/BE** — bioavailability / bioequivalence studies

These require **two** things, not one:

1. Approval from an ethics committee that is **approved by TİTCK** (a Klinik
   Araştırmalar Etik Kurulu), **and**
2. A **separate TİTCK start permit** (and Ministry of Health permission).

Per TİTCK: clinical research is conducted "TİTCK tarafından onay verilen Etik
Kurulların onayı ve Sağlık Bakanlığının izni ile gerçekleştirilmektedir."

> **Legal-validity gate.** A decision issued by a committee that is **not**
> TİTCK-approved is **legally void** for clinical research. Confirm the
> committee's TİTCK accreditation *before* submitting. This is the single most
> common and most expensive routing error.

Governing instrument: *Beşeri Tıbbi Ürünlerin Klinik Araştırmaları Hakkında
Yönetmelik* (Regulation on Clinical Research of Human Medicinal Products),
mevzuat.gov.tr MevzuatNo 40207 (R.G. 27/5/2023, No. 32203). TİTCK's Clinical
Research Department evaluates and permits human-medicinal-product research
including BA/BE and low-risk scientific studies.

---

## Decision Tree

```
Does the study collect data from human participants?
│
├─ NO  → likely no human-subjects ethics review for this skill's scope.
│        (Animal work, purely computational/secondary-public-data work, etc.
│         have their own regimes — out of scope here.)
│
└─ YES
   │
   ├─ Does it involve a drug, medical device, cosmetic, stem cells, or BA/BE?
   │  │
   │  ├─ YES → DOOR 2: TİTCK-approved Klinik Araştırmalar Etik Kurulu
   │  │         + separate TİTCK permit. Verify committee accreditation.
   │  │
   │  └─ NO
   │     │
   │     └─ Collects via survey / interview / focus group / observation /
   │        experiment?
   │        │
   │        ├─ YES → DOOR 1: university Girişimsel Olmayan Etik Kurulu
   │        │         (TR Dizin 2020 trigger).
   │        │
   │        └─ NO  → check edge cases below; many still need Door 1.
   │
   └─ Hits BOTH doors (e.g. a device trial that also runs a participant survey)?
      → The clinical track governs: escalate to DOOR 2.
```

---

## Edge Cases

- **Retrospective record / secondary-data review.** Use of already-collected,
  identifiable participant data is generally still human-subjects research and
  typically needs Door 1 review; confirm with the institution's committee. If the
  data are fully and irreversibly anonymized, the analysis may fall outside the
  ethics trigger — but the **anonymization status** is a KVKK question; route the
  data-handling determination to `alterlab-kvkk-dmp`.
- **Minors and vulnerable groups** (çocuklar, gebeler, mahpuslar, bilişsel
  kapasitesi kısıtlı kişiler). Additional safeguards and, for minors, parental/
  guardian consent **plus** age-appropriate assent (çocuk rızası) are required.
  Flag these explicitly in the dossier.
- **Mixed clinical + survey study.** Both doors are in play; the clinical track
  (Door 2) governs and the survey component is reviewed within it.
- **Multi-site / multi-university study.** Each institution may require its own
  committee submission; do not assume one approval covers all sites.
- **No fixed embargo / processing rule is asserted here.** Where a fact (e.g.
  exact form fields, fee, or timeline) is institution-specific, send the user to
  their committee's current documents rather than inventing a value.

---

## Primary Sources

- TİTCK — Klinik Araştırmalar (committee approval, TİTCK permit, legal validity):
  https://www.titck.gov.tr/faaliyetalanlari/ilac/klinik-arastirmalar
- *Beşeri Tıbbi Ürünlerin Klinik Araştırmaları Hakkında Yönetmelik* —
  mevzuat.gov.tr MevzuatNo 40207 (R.G. 27/5/2023, No. 32203).
- TR Dizin (TÜBİTAK ULAKBİM) research-and-publication-ethics criteria — ethics
  approval mandatory for participant data collection in publications from 2020:
  https://trdizin.gov.tr/

_Last verified: 2026-06-06. Committee names, the TİTCK regulation, and the TR
Dizin criteria can change — re-verify against the sources above before relying on
a routing decision for submission._
