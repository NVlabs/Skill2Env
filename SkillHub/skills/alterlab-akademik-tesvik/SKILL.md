---
name: alterlab-akademik-tesvik
description: "Computes the annual Turkish academic-incentive (akademik teşvik) score for Devlet (state) university öğretim elemanı (academic staff) from a classified activity list, applying the verified Akademik Teşvik Ödeneği Yönetmeliği (2018/11834) Faaliyet Hesaplama Tablosu headline puanları (Proje 20, Araştırma 15, Yayın 30, Patent 30, Atıf 30, Tebliğ 20, Ödül 20) with the k (author-count), p (Q1 1/Q2 0.8/Q3 0.5/Q4 0.25), and r (project-role) coefficients via türü puanı = Σ(faaliyet oranları) × headline (MADDE 8/2), then enforcing the per-type headline ceilings, the 100 cap (MADDE 8/3), and the net-30 payment gate (MADDE 10/3) in a deterministic scripts/tesvik_score.py. Use when the user wants to calculate akademik teşvik puanı, check the en az 30 (net-30) threshold, apply TABLO 4 ceilings, or estimate teşvik eligibility; keeps its coefficients separate from doçentlik scoring. For doçentlik point eligibility prefer alterlab-docentlik-eligibility. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key and no network required — applies the regulation's tables offline via `uv run python`; the regulation PDF is on mevzuat.gov.tr for re-verification
metadata:
  skill-author: AlterLab
  version: "1.0.1"
  last_updated: "2026-06-09"
---

# Akademik Teşvik — Annual Incentive Score Calculator

Computes the **akademik teşvik** (academic-incentive) puanı for a Turkish
**Devlet** (state) university **öğretim elemanı** (academic staff member) for one
calendar year, and decides whether the incentive is payable. It applies the
**Akademik Teşvik Ödeneği Yönetmeliği** (Academic Incentive Allowance
Regulation; Bakanlar Kurulu 2018/11834, RG 27/6/2018 No. 30461, amended CK-2043
of 2020) deterministically and offline, so the same activity list always yields
the same score.

This is an **annual** calculation distinct from **doçentlik** (associate-
professorship) eligibility scoring: the two rule systems use different
coefficients and thresholds, and this skill keeps them separate on purpose.

## Quick Start

```
Calculate my akademik teşvik score for this year
Akademik teşvik puanımı hesapla — 30 barajını geçiyor muyum?
Does this activity list clear the net-30 incentive threshold?
Apply the TABLO 4 ceilings and the 30% rule to my publications
```

→ Classify each activity into its regulation type, build a JSON activity list,
run `scripts/tesvik_score.py`, then report the final score, the per-type
breakdown, and the **net-30** pay/no-pay verdict.

## When to Use This Skill

Use it when the request is about the **annual teşvik (incentive) score or its
payment threshold** — calculating the puan, applying the **TABLO 4 / Faaliyet
Hesaplama Tablosu** ceilings, checking the **en az 30** (net-30) gate, the
per-type headline ceilings (the **%30** table weighting), the **100** cap, or
estimating whether a year's research output qualifies for the incentive payment.

### Does NOT Trigger

Route adjacent requests to the right sibling skill:

| The request is really about… | Use this skill instead |
|---|---|
| Doçentlik (associate-prof) point eligibility & ÜAK minimums | `alterlab-docentlik-eligibility` |
| TÜBİTAK ARDEB 1001/1002-A proposal drafting | `alterlab-tubitak-proposal` |
| Whether a journal is in **TR Dizin** (live index status) | `alterlab-trdizin` |
| DergiPark journal/article metadata or OAI harvest | `alterlab-dergipark` |
| Turkish APA-7 / TR Dizin manuscript formatting & öz | `alterlab-tr-academic-style` |
| YÖK Akademik profile / official affiliation lookup | `alterlab-yok-akademik` |
| Verifying that cited references actually exist | `alterlab-citation-verifier` |

If the user asks for the **TRY payout amount**, this skill computes the score and
shows the formula, but does **not** quote money from a hardcoded salary
coefficient (it changes every six months) — see "Payout" below.

## What the Score Is Built From

The regulation's method (**MADDE 8/2**) is two steps, **not** a per-activity
`base × k × p × r`:

> **türü puanı = (Σ faaliyet oranları) × headline puan** *(MADDE 8/2-a)*; then
> **akademik teşvik puanı = Σ türü puanları** *(MADDE 8/2-b)*.

Each Faaliyet Hesaplama Tablosu row gives an **oran** — a percentage-style
multiplier like `k × p × 60`, `r × 80`, or `15 × ay` — which you express as a
**fraction of that type's headline puan** before summing. The verified tables
(transcribed from the regulation PDF) live in
[`references/tablo4.md`](references/tablo4.md):

- **Per-type headline puan (also the MADDE 8/3 ceiling):** Proje 20,
  Araştırma 15, Yayın 30, Tasarım 15, Sergi 15, Patent 30, Atıf 30, Tebliğ 20,
  Ödül 20.
- **k (author count):** 1→1, 2→0.8, 3→0.6, 4→0.45, 5→1/5, 6→1/6, 7+→1/n.
- **p (journal quartile):** Q1 1, Q2 0.8, Q3 0.5, Q4 0.25 (AHCI uses p=0.5,
  MADDE 8/6).
- **r (project role):** yürütücü (PI) 1, araştırmacı/bursiyer 0.5.

The full calculation pipeline, the worked example, and the payout formula are in
[`references/hesaplama.md`](references/hesaplama.md).

## The Three Gates (do not skip any)

1. **Per-type headline ceiling + the %30 weighting** — each type's puanı cannot
   exceed its headline puan (**MADDE 8/3**). Those headlines (all ≤ 30) are how
   the regulation *encodes* the MADDE 1 rule that each type's weight stays within
   **30% of the 100-point total** — the %30 is a fixed **table-design** constraint
   on the ceilings, **not** a per-run "rescale to 30% of this year's gross" step.
2. **100 cap** — the total score is capped at **100** (MADDE 8/3; the payout
   formula uses `puan/100`).
3. **Net-30 gate** — the incentive is payable **only if the final score ≥ 30**:
   *"Akademik teşvik ödeneğinin ödenebilmesi için akademik teşvik puanının en az
   otuz olması gerekir"* (**MADDE 10/3**, "Diğer hükümler"). Below 30, no payment
   regardless of output volume.

## How to Run It

### 1. Classify activities into a JSON list

Each item needs a `type` (one of the nine canonical türler) and an `oran` — the
regulation row's value (`k × p × 60`, `r × 80`, `15 × ay`, the bare integer for
citations/awards, …) **expressed as a fraction of that type's headline puan**.
Take the table cell, treat its trailing integer as a percentage, and apply
k/p/r/months:

```json
[
  {"type": "Yayın",  "oran": 0.48, "label": "Q1 SSCI, 2 authors → k0.8·p1.0·0.60"},
  {"type": "Proje",  "oran": 0.80, "label": "TÜBİTAK 1001 yürütücü (A1) → r1.0·0.80"},
  {"type": "Atıf",   "oran": 0.08, "count": 12, "label": "12 SCI citations → 0.08 each"}
]
```

Type names accept Turkish spelling with diacritics (`Yayın`, `Atıf`, `Tebliğ`);
the script ASCII-folds them internally. `count` (default 1) multiplies the oran
for identical repeated activities. See
[`references/hesaplama.md`](references/hesaplama.md) for how to derive each
`oran` from the table, with worked rows.

### 2. Run the calculator

```bash
uv run python skills/turkish-academia/alterlab-akademik-tesvik/scripts/tesvik_score.py \
    activities.json --json
```

Pass `-` to read the JSON list from stdin. Omit `--json` for a readable table.

### 3. Report the result

Present, in this order:

1. The **final score** and whether it was **capped at 100**.
2. The **net-30 verdict**: payable (≥30) or not payable (<30).
3. The **per-type breakdown** (Σoran → raw türü puanı → final after the headline
   ceiling), surfacing any type the MADDE 8/3 ceiling reduced.
4. Any **warnings** (unknown type, missing `oran`, ceiling reduction, gate failure).

## Payout (score → TRY)

The TRY amount is `(kadro oranı) × (score/100) × [(1500 + 8000) × memur aylık
katsayısı]` (**MADDE 8/1**), with kadro oranı = Profesör %100, Doçent %90,
**Dr. Öğr. Üyesi %80**, araştırma görevlisi / öğretim görevlisi %70. The
**memur aylık katsayısı** is revised ~twice a year and is **not** hardcoded;
report the formula and ask the user to apply the current period's coefficient
before quoting money.

## Self-Check Before Reporting

- Did you classify each activity into a real regulation type, or did the script
  warn about an unknown type (then it was dropped)?
- Did you apply the **headline ceilings (MADDE 8/3), the 100 cap, and the net-30
  gate (MADDE 10/3)** — and derive each `oran` from the table, not invent a base?
- Are you reporting a **score**, not a fabricated TRY amount from a guessed
  salary coefficient?
- Is this an **annual teşvik** question — or a **doçentlik** one that belongs to
  `alterlab-docentlik-eligibility`?
- Is the subject a **Devlet** (state) university staff member? Foundation/private
  universities are out of scope; **yabancı uyruklu** (foreign-national) staff
  cannot benefit at all (MADDE 6/9), and faaliyetler done while seconded to a
  **vakıf** university are not counted (MADDE 6/7).

## References

- [`references/tablo4.md`](references/tablo4.md) — verified ceilings and k/p/r
  coefficient tables, with the regulation source and last-verified date.
- [`references/hesaplama.md`](references/hesaplama.md) — full calculation
  pipeline, worked example, the payout formula, and common pitfalls.
- Regulation PDF: `https://www.mevzuat.gov.tr/MevzuatMetin/21.5.201811834.pdf`
  (Akademik Teşvik Ödeneği Yönetmeliği). Re-verify before a real başvuru.

Part of the AlterLab Academic Skills suite.
