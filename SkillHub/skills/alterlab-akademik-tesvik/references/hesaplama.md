# Score calculation method & the net-30 gate

How `scripts/tesvik_score.py` turns a list of activities into an annual akademik
teşvik (academic-incentive) score and a pay/no-pay verdict. Every rule below
traces to the **Akademik Teşvik Ödeneği Yönetmeliği** (2018/11834, am. 2020) —
see `tablo4.md` for source provenance and the numeric tables.

## The regulation's computation method (MADDE 8/2)

The official method (MADDE 8, fıkra 2) is **two steps**. There is **no** dynamic
"rescale each type to 30% of this year's gross" step — that was a misreading.

> **(a)** *"Öncelikle her bir akademik faaliyet türünün puanı hesaplanır. Bu
> hesaplama, … almış olduğu oranların toplamı ile her bir akademik faaliyet
> türü için belirlenmiş olan puanın çarpılması sonucu elde edilir
> [Akademik faaliyet türü puanı = faaliyet oranları toplamı × akademik faaliyet
> türü için belirlenmiş olan puan]."*
>
> **(b)** *"Her bir akademik faaliyet türünden elde edilen puanların
> toplanmasıyla … akademik teşvik puanı hesaplanır."*

So:

```
türü puanı          = (Σ faaliyet oranları) × headline puan      (MADDE 8/2-a)
akademik teşvik puanı = Σ türü puanları                          (MADDE 8/2-b)
```

**MADDE 8/3** then caps each türü puanı at its headline puan, and the total at
**100**: *"…faaliyet türü için belirlenmiş olan puanı, akademik teşvik puanı …
ise yüz puanı geçemez."*

### Where the %30 actually comes from

**MADDE 1** defines the regulation's purpose, including setting *"faaliyetlerin
puan karşılıkları, akademik teşvik toplam puanının %30'unu geçmemek üzere her
bir akademik faaliyet türünün … ağırlıkları"*. The %30 is a constraint on **how
the table is designed** — it is why every per-type headline puan is **≤ 30**
(Yayın/Patent/Atıf 30, Tebliğ/Proje/Ödül 20, Araştırma/Tasarım/Sergi 15). It is
**not** a per-run reduction applied to a single year's computed total. The
per-type headline ceilings (MADDE 8/3) already encode it.

## The `oran` input model

Each Faaliyet Hesaplama Tablosu cell is an **oran** — a percentage-style
multiplier such as `k × p × 60`, `r × 80`, `15 × ay`, or a bare integer. The
script takes that oran **as a fraction of the type headline** (treat the
trailing integer as a percentage, then apply k/p/r/months). The full per-row
oran catalog is field-dependent (A1–A4 columns) and not reproduced here in full;
`tablo4.md` lists the verified k/p/r tables and representative rows. Derive each
activity's oran from the table, then feed it in:

| Activity (table cell) | Coefficients | oran (fraction of headline) | Type (headline) |
|---|---|---|---|
| Q1 SSCI research article, 2 authors (`k × p × 60`) | k=0.8, p=1.0 | 0.8·1.0·0.60 = **0.48** | Yayın (30) |
| TÜBİTAK 1001 yürütücü, A1 alanı (`r × 80`) | r=1.0 | 1.0·0.80 = **0.80** | Proje (20) |
| Yurt içi araştırma, 6 months (`10 × ay`) | — | 0.10·6 = **0.60** | Araştırma (15) |
| 1 citation in an SCI-indexed article (`8`) | — | **0.08** | Atıf (30) |
| International full paper / tam bildiri (`20`) | — | **1.00** | Tebliğ (20) |
| TÜBA Akademi Ödülü (`20`) | — | **1.00** | Ödül (20) |

Note `count` multiplies an oran for repeated identical activities (e.g. twelve
identical SCI citations → `oran 0.08, count 12`).

## The calculation pipeline

1. **Classify each activity into a türü (type)** and read its row's oran from
   the Faaliyet Hesaplama Tablosu. The skill scores *already-classified*
   activities — it does not decide which table row a publication belongs to.

2. **Sum each type's oranları** (`Σ oran × count` over that type's activities).

3. **Multiply by the headline puan** (MADDE 8/2-a):
   `türü puanı = (Σ oran) × headline`.

4. **Apply the per-type ceiling (MADDE 8/3)**: `türü puanı = min(türü puanı,
   headline)`. Each headline (all ≤ 30) is where the MADDE 1 %30 weighting lives.

5. **Sum the type puanları and apply the 100 cap** (MADDE 8/2-b + 8/3): the total
   akademik teşvik puanı cannot exceed 100.

6. **Apply the net-30 gate (MADDE 10/3)**: the incentive is **payable only if the
   final score ≥ 30** — *"Akademik teşvik ödeneğinin ödenebilmesi için akademik
   teşvik puanının en az otuz olması gerekir."* This sentence is in **MADDE 10**
   ("Diğer hükümler"), fıkra 3 — not MADDE 7. Below 30, no payment is made
   regardless of activity volume.

## Worked end-to-end example

Activities (oranları derived from the table as above):

- Q1 SSCI article, 2 authors → Yayın, oran 0.48 → türü puanı `0.48 × 30 = 14.40`.
- TÜBİTAK 1001 yürütücü (A1) → Proje, oran 0.80 → `0.80 × 20 = 16.00`.
- 12 SCI citations (oran 0.08 each) → Atıf, Σoran 0.96 → `0.96 × 30 = 28.80`.
- International tam bildiri → Tebliğ, oran 1.00 → `1.00 × 20 = 20.00`.
- TÜBA Akademi Ödülü → Ödül, oran 1.00 → `1.00 × 20 = 20.00`.

Totals:

- Per-type puanları: Yayın 14.40, Proje 16.00, Atıf 28.80, Tebliğ 20.00,
  Ödül 20.00 — none exceeds its headline ceiling (MADDE 8/3 not binding here).
- Sum = **99.20**; 99.20 < 100, so no cap.
- Net-30 gate: 99.20 ≥ 30 → **payable**.

Now drop everything except the article: total 14.40 < 30 → **not payable**, even
though the work is real. The gate is unforgiving by design. (A publication-heavy
record is also bounded by the Yayın headline ceiling of 30 via MADDE 8/3, so a
single türü can carry at most 30 of the 100 points.)

## The TRY payout — why this skill stops at the score

The score is only the input to the money formula. From the regulation
(**MADDE 8/1**):

> Akademik teşvik ödemesi tutarı = en yüksek Devlet memuru brüt aylığı ×
> (akademik kadro unvanına göre belirlenmiş oran) × (akademik teşvik puanı / 100)

where the en yüksek Devlet memuru brüt aylığı itself is
`(ana gösterge 1.500 + ek gösterge 8.000) × **memur aylık katsayısı**`.

Kadro oranları (rate by title), verbatim from MADDE 8/1:

| Kadro (title) | Oran |
|---|---|
| Profesör | %100 |
| Doçent (associate professor) | %90 |
| Doktor öğretim üyesi (Dr. Öğr. Üyesi) | %80 |
| Araştırma görevlisi, öğretim görevlisi (research/teaching assistant) | %70 |

The **memur aylık katsayısı** (civil-servant salary coefficient) is revised by
the government roughly every six months. This skill deliberately does **NOT**
hardcode it: a stale coefficient would produce a wrong TRY figure. Report the
score and the formula, and tell the user to plug in the current katsayısı (or to
verify the period's announced figure) before quoting an amount.

## Common pitfalls the skill should catch

- **Confusing teşvik with doçentlik scoring.** These are two different rule
  systems with different coefficients and thresholds. For associate-professor
  eligibility scoring, route to `alterlab-docentlik-eligibility` — do NOT reuse
  these `k/p/r` values or the net-30 gate there.
- **Treating the headline puan as a per-activity base.** The headline (30/20/15)
  is the *type* multiplier in `türü puanı = Σ(oran) × headline` and the type
  ceiling — it is **not** an activity's raw score. Each activity contributes an
  `oran` (a fraction), not the headline.
- **Inventing a "30% of this year's gross" rescaling step.** The %30 is a fixed
  table-design weight (MADDE 1) realised as the ≤30 headline ceilings; there is
  no dynamic per-run rescaling in the regulation.
- **Assuming a high activity count guarantees payment.** The headline ceilings +
  the net-30 gate can leave a single-type-heavy CV below threshold.
- **Quoting money from a stale katsayısı.** Always flag the as-of date.
- **Out-of-scope subjects.** The regulation covers Devlet (state) staff only.
  **Yabancı uyruklu** (foreign-national) öğretim elemanları cannot benefit at all
  (MADDE 6/9); faaliyetler performed while seconded (görevlendirme) to a **vakıf**
  (foundation) university are not counted (MADDE 6/7).
- **Forgetting the no-ranking divisor / sergi exception (MADDE 8/7).** Activities
  with no share ratio or author ordering take `oran / kişi sayısı`; but SERGİ
  *karma* etkinlikler and international performance-based *karma* audio/video
  recordings are scored at full points regardless of contributor count.
