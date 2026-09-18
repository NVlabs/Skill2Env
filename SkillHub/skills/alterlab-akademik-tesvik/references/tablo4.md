# TABLO 4 ceilings & coefficients — verified from the regulation

All values below are transcribed from the official **Akademik Teşvik Ödeneği
Yönetmeliği** (Academic Incentive Allowance Regulation) and its annexed tables.

- Source: `https://www.mevzuat.gov.tr/MevzuatMetin/21.5.201811834.pdf`
- Bakanlar Kurulu Kararı: 14/5/2018, No. **2018/11834**
- Resmî Gazete: 27/6/2018, No. **30461**
- Dayanak (legal basis): 2914 sayılı Yükseköğretim Personel Kanunu, ek 4. madde
- Amended by Cumhurbaşkanı Kararı **CK-2043** (RG 17/1/2020, No. 31011)
- Scope (MADDE 1): **Devlet** (state) yükseköğretim kurumları kadrolarındaki
  öğretim elemanları (state higher-education academic staff). Also applies to
  Milli Savunma Üniversitesi, Jandarma/Sahil Güvenlik Akademisi, Polis Akademisi.
- Scope exclusions (MADDE 6): **yabancı uyruklu** (foreign-national) öğretim
  elemanları cannot benefit at all (MADDE 6/9); faaliyetler done while seconded
  (görevlendirme) to a **vakıf** (foundation) university are not counted
  (MADDE 6/7).
- Last verified against the PDF: 2026-06-09.

> Always re-verify against the current regulation text before a real
> başvuru (application); ÜAK/Cumhurbaşkanı amendments revise rows periodically.

## Per-type headline puan (= MADDE 8/3 ceiling)

These are the `(… puan)` headers in the **Faaliyet Hesaplama Tablosu**. Each is
**both** the type multiplier in `türü puanı = Σ(oran) × headline` (MADDE 8/2-a)
**and** the per-type ceiling (MADDE 8/3): a type's puanı cannot exceed it, and
the total cannot exceed 100. All headlines are ≤ 30 — that is how the MADDE 1
%30 weighting is encoded. The calculator key (ASCII-folded) is shown for
`scripts/tesvik_score.py` input.

| Activity type (canonical TR — English gloss) | Headline puan | Calculator key |
|---|---|---|
| PROJE (project)                | 20 | `proje` |
| ARAŞTIRMA (research)           | 15 | `arastirma` |
| YAYIN (publication)            | 30 | `yayin` |
| TASARIM (design)               | 15 | `tasarim` |
| SERGİ (exhibition)             | 15 | `sergi` |
| PATENT (patent)                | 30 | `patent` |
| ATIF (citation)                | 30 | `atif` |
| TEBLİĞ (conference paper)       | 20 | `teblig` |
| ÖDÜL (award)                   | 20 | `odul` |

> The description-seed lists seven types (Proje, Araştırma, Yayın, Patent, Atıf,
> Tebliğ, Ödül). The full regulation table also carries **TASARIM** and **SERGİ**
> (both ceiling 15), included here because the PDF confirms them verbatim.

## Coefficient tables

Each Faaliyet Hesaplama Tablosu cell is an **oran** (a percentage-style
multiplier like `k × p × 60`, `r × 80`, `15 × ay`) built from these coefficients;
`türü puanı = Σ(oran) × headline` (MADDE 8/2). Each coefficient applies only
where the regulation row uses it.

### (k) — author / contributor count (Tablo 1)

| Kişi sayısı (number of contributors) | k |
|---|---|
| 1 | 1 |
| 2 | 0.8 |
| 3 | 0.6 |
| 4 | 0.45 |
| 5 | 1/5 (0.2) |
| 6 | 1/6 (≈0.167) |
| 7 or more | 1 / (number of contributors) |

### (p) — journal quartile (ISI Web of Science çeyreklik grubu)

| Quartile | p |
|---|---|
| Q1 | 1 |
| Q2 | 0.8 |
| Q3 | 0.5 |
| Q4 | 0.25 |

> **AHCI journals** use **p = 0.5** regardless of quartile, and journals with no
> assigned Q value take the lowest coefficient (MADDE 8/6, am. CK-2043/4).

### (r) — project role (Projedeki rol)

| Role | r |
|---|---|
| Yürütücü (PI / coordinator) | 1 |
| Araştırmacı, Bursiyer (researcher, fellow) | 0.5 |

> **No-share / no-ranking activities (MADDE 8/7):** for faaliyetler with no
> special share ratio and no author ordering, the oran is divided by the number
> of contributors (`oran / kişi sayısı`). **Exception:** SERGİ *karma* (group)
> etkinlikler and international performance-based *karma* audio/video recordings
> are scored at **full points (tam puan), with k NOT applied**, regardless of
> contributor count.

## Worked row examples (oran cells, verbatim from Tablo 4)

The table cell is the **oran**; treat its trailing integer as a percentage and
apply k/p/r/months, then `türü puanı = Σ(oran) × headline`.

| Faaliyet (row) | Table cell (oran) | oran as fraction | × headline = türü puanı |
|---|---|---|---|
| YAYIN — SCI/SSCI/AHCI araştırma makalesi (A1/A2 fields) | `k × p × 60` | Q1, 2 authors → 0.8·1.0·0.60 = **0.48** | 0.48 × 30 = **14.4** |
| YAYIN — SCI/SSCI/AHCI araştırma makalesi (A3/A4 fields) | `k × p × 80` | Q1, 2 authors → 0.8·1.0·0.80 = **0.64** | 0.64 × 30 = **19.2** |
| ATIF — SCI/SSCI/AHCI makalesinde atıf | `8` | 1 citation → **0.08** | 0.08 × 30 = **2.4** |
| PATENT — uluslararası patent | `k × 100` | single inventor → **1.00** | 1.00 × 30 = **30** (= tavan) |
| PROJE — H2020 projesi | `r × 100` | yürütücü → **1.00** | 1.00 × 20 = **20** (= tavan) |
| PROJE — TÜBİTAK 1005/3001 | `r × 70` | yürütücü → **0.70** | 0.70 × 20 = **14** |
| ARAŞTIRMA — yurt içi araştırma | `10 × ay` | 6 months → **0.60** | 0.60 × 15 = **9** |

> The cell's trailing integer is a **percentage of the headline**, NOT the
> headline itself: e.g. a Q1 SSCI 2-author article is `k·p·60% = 0.48` of the
> Yayın headline 30 = **14.4**, not 24. The earlier "base = headline" reading was
> wrong (it conflated the cell percentage with the type multiplier). The oran
> columns are field-dependent (A1–A4); read the correct column for the author's
> bilim alanı. A1 = Eğitim/Fen/Mühendislik/Sağlık/Ziraat-Orman-Su; A2 =
> Filoloji/Hukuk/İlahiyat/Sosyal-Beşeri-İdari/Spor; A3 = Mimarlık-Planlama-
> Tasarım; A4 = Güzel Sanatlar.
