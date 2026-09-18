# Author-Share Rule & Scoring Mechanics

How a publication's **face points** (from the field table in
`uak_criteria.md`) become the candidate's **scaled contribution**, plus the exact
lead-author definition and rounding convention used by `score_docentlik.py`.

## The author-share rule (paylaşım kuralı)

A publication's face points are scaled by the candidate's authorship role and the
total author count:

| Author count | Candidate's role | Share factor | Scaled points |
|---|---|---|---|
| 1 (single author) | sole author | **1.0** | full face points |
| 2 | **lead author (başlıca yazar)** | **0.8** | 0.8 × face points |
| 2 | non-lead co-author | **0.5** | 0.5 × face points |
| ≥ 3 | **lead author (başlıca yazar)** | **0.5** | half of face points |
| ≥ 3 | non-lead co-author | **0.5 / (N − 1)** | the other half split equally among the remaining N − 1 authors |

In words for the **two-author** case: the başlıca yazar (lead) gets **0.8** of
the face points, but the **non-lead** second author gets only **0.5** — the two
authors of a 2-author paper are **not** scored equally. For the ≥ 3 case: the
lead author takes **half** the points; the remaining half is divided **equally**
among **all the other** authors. So with N authors (N ≥ 3), a non-lead
co-author's factor is `0.5 / (N − 1)`.

### Worked examples (Sağlık table, Q1 = 30 points)

- **Single-author Q1 article** → 30 × 1.0 = **30.0**.
- **Two-author Q2 article** (20 points), candidate is the **lead (başlıca yazar)**
  → 20 × 0.8 = **16.0**.
- **Two-author Q2 article** (20 points), candidate is the **non-lead** second
  author → 20 × 0.5 = **10.0** (the lead still gets 16.0; the two are not equal).
- **Three-author Q1 article** (30 points), candidate is **lead** → 30 × 0.5 =
  **15.0**.
- **Three-author Q1 article**, candidate is a **non-lead** co-author → other half
  is 30 × 0.5 = 15.0, split between the 2 non-lead authors → 15.0 / 2 = **7.5**.
- **Four-author Q3 article** (15 points), candidate is a **non-lead** co-author →
  (15 × 0.5) / (4 − 1) = 7.5 / 3 = **2.5**.

## Lead author — başlıca yazar

A publication counts toward the **≥ 3 lead-author Q-article** minimum only when
both hold:

1. The journal index tier is one of **Q1, Q2, Q3, Q4** (SCIE/SSCI
   quartile-ranked). **Q4 counts** — for Sağlık Bilimleri the ≥3 başlıca-yazar
   articles may be in any of Q1–Q4 (verified against the live ÜAK Sağlık
   criteria, 2025 March term: "SCIE/SSCI kapsamındaki dergilerden (Q1, Q2, Q3
   veya Q4) … en az 3 makalede başlıca yazar"). AHCI, ESCI and TR Dizin articles
   do **not** qualify for *this* minimum, even though they still earn points
   toward the 100/90 totals.
2. The candidate is the **başlıca yazar (lead author)** — defined by ÜAK as the
   first author, the corresponding author, or the sole supervising (advisor)
   author of a student-derived article.

> **The SCIE/SSCI ≥40-point minimum IS now checked (scorer v2.0.0).** The live
> Sağlık criteria pair the "≥3 başlıca-yazar articles" rule with a **≥40 points
> from SCIE/SSCI (Q1–Q4) articles** floor. This is now modelled as the
> `intl_scie_ge_40` check (post-doctorate Q1–Q4 article points), alongside the
> ≥3 lead-author count. However, **additional field-specific minimums are still
> NOT modelled** — a TR Dizin national-article requirement, a citation (atıf)
> minimum, a scientific-meeting minimum, an education minimum, and per-category
> point caps (see `uak_criteria.md` → *Mandatory minimums — NOT modelled*). So
> passing all four modelled checks is **necessary but not sufficient**: the
> scorer returns `PRESCREEN_PASS_VERIFY_REMAINING`, never "ELIGIBLE". Re-verify
> the full TABLO 10 checklist against the live ÜAK source for the candidate's
> term.

The candidate declares `is_lead` per item. The scorer **trusts** that flag but
echoes it in the per-item output so a reviewer can audit each claim against the
actual byline. The scorer does not adjudicate authorship disputes.

## Post-doctorate points

Each item carries a `post_doc` flag (published after the candidate's doctorate).

- The **total** (≥ 100) check sums **all** scaled points, pre- and post-doctorate.
- The **post-doctorate** (≥ 90) check sums only the scaled points of items with
  `post_doc: true`.

So pre-doctorate work can lift the total toward 100 but cannot help meet the 90.

## Rounding convention

- Per-item scaled points are computed in full floating precision and **not**
  rounded before summing, to avoid cumulative rounding drift.
- Reported figures (per item and totals) are presented to **one decimal place**.
- Threshold comparisons use the unrounded sums, so a value displayed as `90.0`
  that is actually `89.96` correctly fails the `≥ 90` check; the report shows the
  true shortfall.

## Unknown / unscorable tiers

If an item's `index` is not in the field table (or is empty/unknown), the scorer
does **not** guess a value. It marks the item `scorable: false`, contributes
**0** points from it, and lists it under `unscored` so the user resolves the tier
(via `alterlab-trdizin` for TR Dizin status, or the candidate's JCR records for a
quartile) and re-runs. Guessing a tier would fabricate points — never do it.
