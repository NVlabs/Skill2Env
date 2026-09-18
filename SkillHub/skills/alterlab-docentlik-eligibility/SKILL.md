---
name: alterlab-docentlik-eligibility
description: "Runs a PARTIAL pre-screen of a Turkish associate-professorship (doçentlik) publication list against the ÜAK (Üniversitelerarası Kurul) Sağlık Bilimleri TABLO 10 criteria, applying the author-share rule (full; 0.8 + 0.5; lead-author half-the-rest split) and pass-fail checking the four computable minimums (≥100 total, ≥90 post-doctorate, ≥40 SCIE/SSCI article points, ≥3 lead-author Q1–Q4 articles). It deliberately does NOT emit an ELIGIBLE verdict — it lists the unmodelled mandatory minimums (TR Dizin/national article, citation, congress, teaching, per-category caps) for the user to verify. Use when the user wants to estimate doçentlik eligibility, calculate ÜAK points, or audit lead-author (başlıca yazar) requirements; resolve a journal's live TR Dizin status with alterlab-trdizin first, and compute the akademik teşvik (academic-incentive) score with alterlab-akademik-tesvik. Always verify the full live TABLO 10 — criteria change each term and differ per field. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key required — pure offline PARTIAL pre-screen (stdlib Python) over a bundled, dated ÜAK criteria table; never emits an ELIGIBLE verdict; live journal-index status is delegated to alterlab-trdizin
metadata:
  skill-author: AlterLab
  version: "2.0.0"
  last_updated: "2026-06-08"
  depends_on: "alterlab-trdizin (live TR Dizin status feeds scoring), alterlab-akademik-tesvik (separate incentive score)"
---

# Doçentlik Eligibility — PARTIAL Pre-Screen Against the ÜAK Criteria

Pre-screens a candidate's publication list against the **doçentlik** (associate
professorship) point gate set by **ÜAK** (Üniversitelerarası Kurul / the
Inter-University Council) for the **Sağlık Bilimleri (Health Sciences)** field.
Given a publication list with each item's index tier and author role, it applies
the per-field point table, the **author-share rule** (paylaşım kuralı), and
pass-fail-checks the **four mandatory minimums it can compute from a publication
list** — reporting the exact shortfall on any that fail.

> **This is a PARTIAL pre-screen, not an eligibility decision — and it never
> outputs an "ELIGIBLE" verdict.** The live TABLO 10 imposes several more
> mandatory minimums (a TR Dizin / national-article requirement, a citation
> minimum, a scientific-meeting minimum, an education minimum, and per-category
> point caps) that depend on inputs a bare publication list does not carry. The
> scorer lists those unmodelled minimums in every report and the best status it
> can return is `PRESCREEN_PASS_VERIFY_REMAINING` — "all computable checks pass;
> a human must still verify the rest against the live ÜAK source." A failed
> computable check returns `FAIL_MODELLED_CHECK`.

This is a **deterministic offline tool**: the same input always yields the same
status. It does **not** decide the *quality* of a candidate's work — that is the
doçentlik jury's role — and it does **not** look up a journal's live index
status (use `alterlab-trdizin` for that, then feed the result in).

## Quick Start

```
Am I eligible for doçentlik? Here is my publication list with indexes and author roles.
Doçentlik için yeterli puanım var mı? Yayın listem ekte (Q tier + yazar sırası ile).
Calculate my ÜAK doçentlik points for the Sağlık (Health) field.
Do I meet the ≥3 lead-author Q-article requirement, or am I short?
```

→ **Run** `scripts/score_docentlik.py` over the list (JSON), read the
`summary.verdict`, then present the score breakdown, every failed computable
minimum, the **unmodelled mandatory minimums the user must still verify**, and
the **verify-against-current-period** disclaimer below. Never restate the
`PRESCREEN_PASS_VERIFY_REMAINING` status as "eligible" — it is not.

---

## CRITICAL: Verify Against the Current ÜAK Period

ÜAK republishes the doçentlik criteria **each application term** (başvuru
dönemi), and the per-field point tables change between terms. The numbers
bundled in this skill are pinned with a `last_verified` date in
`references/uak_criteria.md` and reflect the **Sağlık Bilimleri (Health
Sciences)** TABLO 10 as captured then.

**Before relying on any output**, the candidate MUST confirm the live criteria
for their own field and term against the primary ÜAK source:
<https://www.uak.gov.tr/> (Doçentlik → Başvuru Şartları / criteria tables). The
binding regulation is the **Doçentlik Yönetmeliği** (RG 15/4/2018 No. 30392),
at <https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=24519&MevzuatTur=7&MevzuatTertip=5>.
Every output this skill produces ends with this disclaimer. Never present a
verdict as the final official decision.

---

## When to Use This Skill

Use it when the request is about **scoring a publication list for the doçentlik
point gate** — total points, post-doctorate points, the lead-author Q-article
minimum, or the co-author share calculation.

### Does NOT Trigger

| The user actually wants… | Route to |
|---|---|
| The **akademik teşvik** (academic-incentive) annual score — different table, k·r·p coefficients, 30% rule, 100-point cap | `alterlab-akademik-tesvik` |
| To check whether a target journal is **currently TR Dizin-indexed** (status feeds this scorer) | `alterlab-trdizin` |
| To check a journal's DergiPark hosting / scope / self-declared indexing | `alterlab-dergipark` |
| Broader Turkish career-track planning (Dr. Öğr. Üyesi → Doçent → Profesör, YÖKSİS dossier) | `alterlab-academic-career` |
| TÜBİTAK ARDEB 1001/1002-A proposal scaffolding | `alterlab-tubitak-proposal` |
| Whether a study needed **etik kurul** (ethics committee) approval | `alterlab-tr-research-ethics` |
| Turkish APA-7 / TR Dizin reference style for a manuscript | `alterlab-tr-academic-style` |
| Verifying that cited references actually **exist** (hallucination check) | `alterlab-citation-verifier` |
| Finding a Turkish graduate **thesis** (tez) | `alterlab-yok-tez` |
| An academic's official current **affiliation / CV** (YÖK Akademik) | `alterlab-yok-akademik` |

---

## The Scoring Model

### Modelled checks (the four this tool computes — all must pass)

1. **Total points ≥ 100** across all scored work.
2. **Post-doctorate points ≥ 90** — points earned from work published *after*
   the candidate received the doctorate / uzmanlık (doktora-uzmanlık sonrası).
   Pre-doctorate work still counts toward the 100 total but not toward this 90.
3. **International SCIE/SSCI article points ≥ 40** — sum of post-doctorate
   **Q1–Q4** article points (the `intl_scie_ge_40` check). AHCI/ESCI/TR Dizin do
   not count toward this floor.
4. **At least 3 lead-author Q-indexed articles** — articles in a Q1–Q4 (SCIE/
   SSCI, quartile-ranked) journal where the candidate is the **başlıca yazar**
   (lead author). For Sağlık, **Q4 counts** toward this ≥3 (verified against the
   live ÜAK Sağlık criteria). See the share rule for who qualifies as lead.

Passing all four returns `PRESCREEN_PASS_VERIFY_REMAINING` (not "eligible").
Failing any returns `FAIL_MODELLED_CHECK` with the exact shortfall.

### Mandatory minimums this tool does NOT model — the user must verify these

The live Sağlık Bilimleri TABLO 10 also requires the following, which a bare
publication list cannot supply. The scorer **lists every one of them** in
`summary.unmodelled_minimums` and cannot clear them:

- **National / TR Dizin articles** — ≥3 ulusal makale, ≥2 in TR Dizin, başlıca
  yazar in ≥2 (resolve TR Dizin status with `alterlab-trdizin` first).
- **Citation (atıf)** — ≥5 post-doctorate citation points.
- **Scientific meeting (bilimsel toplantı / bildiri)** — ≥5 points.
- **Education / teaching (eğitim-öğretim)** — ≥2 points.
- **Per-category point caps** — thesis-derived, books, citation, project, thesis
  supervision, patent, award all have ceilings (values single-source — verify).

> **Why no ELIGIBLE verdict.** Because these minimums are unmodelled, a green
> pass on the four computable checks is **necessary but not sufficient**. The
> tool therefore structurally cannot output "eligible" — re-verify the full
> TABLO 10 checklist against the live ÜAK source for the candidate's term. Full
> detail and provenance: `references/uak_criteria.md`.

### Per-field point table (bundled, dated)

The point a publication earns depends on the **field** (alan) and the journal's
**index tier**. This skill bundles the **Sağlık Bilimleri TABLO 10** values
captured on the `last_verified` date:

| Index tier | Points |
|---|---|
| Q1 (SCI-E / SSCI, 1st quartile) | 30 |
| Q2 | 20 |
| Q3 | 15 |
| Q4 | 10 |
| AHCI (Arts & Humanities Citation Index) | 20 |
| ESCI (Emerging Sources Citation Index) | 10 |
| TR Dizin (ULAKBİM national index) | 10 |

Other fields (Fen, Sosyal, Mühendislik, …) use **different** tables — the script
accepts a field selector but only ships the verified Sağlık table. For another
field, supply that field's table from the live ÜAK source; do **not** reuse the
Sağlık numbers. Full table and provenance: `references/uak_criteria.md`.

### Author-share rule (paylaşım kuralı)

A publication's face points are scaled by the candidate's authorship role:

- **Single author** → full points (×1.0).
- **Two authors** → the **lead author (başlıca yazar)** gets **0.8**; the
  **non-lead** second author gets **0.5** (the two are *not* scored equally).
- **Three or more authors** → the **lead author (başlıca yazar)** takes
  **half** the points; the remaining half is split **equally** among all
  remaining authors.

The script computes the candidate's scaled contribution per item from the author
count and the candidate's role. Worked numeric examples and the exact rounding
convention are in `references/scoring_rules.md`.

> **başlıca yazar (lead author)** — first author, corresponding author, or the
> sole supervising (advisor) author of a student-derived article, per ÜAK's
> definition. The candidate declares this per item; the scorer trusts the flag
> but reports it so a reviewer can audit it.

---

## Pipeline (how to run it)

### 1. Capture the publication list

Each item needs: a title (free text), the **field**, the **index tier** (one of
`Q1 Q2 Q3 Q4 AHCI ESCI TRDizin`), the **author count**, whether the candidate is
**lead author**, and whether it is **post-doctorate**. Example JSON:

```json
{
  "field": "saglik",
  "publications": [
    {"title": "Article A", "index": "Q1", "authors": 3, "is_lead": true,  "post_doc": true},
    {"title": "Article B", "index": "Q2", "authors": 1, "is_lead": true,  "post_doc": true},
    {"title": "Article C", "index": "TRDizin", "authors": 2, "is_lead": false, "post_doc": false}
  ]
}
```

If a journal's index tier is uncertain, resolve it first: for TR Dizin status
run `alterlab-trdizin`; for quartile, check the candidate's records. Do **not**
guess a tier — an unknown tier must be flagged, not scored.

### 2. Run the scorer

```bash
uv run python skills/turkish-academia/alterlab-docentlik-eligibility/scripts/score_docentlik.py \
    publications.json \
    --out docentlik_report.json
```

- The input path may be `-` (stdin) or inline JSON.
- `--field saglik` (default) selects the bundled table; other fields require a
  supplied table file and the script refuses to invent one.
- Omit `--out` to print the JSON report to stdout.

The script is **pure stdlib** — no network, no third-party deps — so it runs in a
bare `uv` environment and is fully reproducible offline.

### 3. Read the report and present it

Parse `summary.verdict` (`FAIL_MODELLED_CHECK` / `PRESCREEN_PASS_VERIFY_REMAINING`
— there is **no** `ELIGIBLE` value) and present:

1. The **headline status** and the four computable check results
   (`total_points`, `post_doc_points`, `intl_scie_points`, `lead_q_articles`)
   against their thresholds (100 / 90 / 40 / 3).
2. A **per-publication table** with each item's face points, the applied share
   factor, and its scaled contribution.
3. For every **failed** minimum, the exact shortfall (e.g. "82 / 100 points — 18
   short" or "2 / 3 lead-author Q articles — 1 short").
4. The **unmodelled mandatory minimums** from `summary.unmodelled_minimums` as a
   checklist the user must verify by hand — make clear the tool could **not**
   check these and that a `PRESCREEN_PASS_VERIFY_REMAINING` is **not** an
   eligibility confirmation.
5. Any items with an **unknown index tier**, flagged as unscored.
6. The **verify-against-current-period disclaimer**, always.

---

## Output Shape (excerpt)

```json
{
  "tool": "alterlab-docentlik-eligibility/score_docentlik.py",
  "version": "2.0.0",
  "field": "saglik",
  "table_last_verified": "2026-06-08",
  "prescreen_only": true,
  "summary": {
    "verdict": "FAIL_MODELLED_CHECK",
    "verdict_meaning": "At least one modelled minimum ... fails — not eligible ...",
    "all_modelled_checks_pass": false,
    "total_points": 95.0,
    "post_doc_points": 85.0,
    "intl_scie_points": 60.0,
    "lead_q_articles": 2,
    "checks": {
      "total_ge_100":         {"pass": false, "value": 95.0, "threshold": 100, "short": 5.0},
      "post_doc_ge_90":       {"pass": false, "value": 85.0, "threshold": 90,  "short": 5.0},
      "intl_scie_ge_40":      {"pass": true,  "value": 60.0, "threshold": 40},
      "lead_q_articles_ge_3": {"pass": false, "value": 2,    "threshold": 3,   "short": 1}
    },
    "unmodelled_minimums": [
      {"id": "national_trdizin_articles", "label_tr": "Ulusal makale / TR Dizin asgari koşulu", "requirement": "...", "why_unmodelled": "..."}
    ]
  },
  "publications": [
    {"title": "Article A", "index": "Q1", "face_points": 30, "share_factor": 0.5, "scaled": 15.0, "counts_lead_q": true, "is_scie_ssci": true}
  ],
  "disclaimer": "PARTIAL PRE-SCREEN — NOT an eligibility decision. ... It therefore NEVER returns 'ELIGIBLE'. ÜAK doçentlik criteria change each application term ... verify the full TABLO 10 at https://www.uak.gov.tr/ ..."
}
```

> The only two `verdict` values are `FAIL_MODELLED_CHECK` and
> `PRESCREEN_PASS_VERIFY_REMAINING`. There is **no** `ELIGIBLE` value by design.

---

## Self-Check Before Reporting

- Did you state the **field** and the table's `last_verified` date? A Sağlık
  result must not be presented as valid for another field.
- Are all **four** modelled checks reported (total / post-doc / intl SCIE-SSCI /
  lead-author Q), even the ones that pass?
- Did you present the **unmodelled mandatory minimums** as a verify-by-hand
  checklist, and make clear the tool did NOT check them?
- Did you avoid calling a `PRESCREEN_PASS_VERIFY_REMAINING` result "eligible"?
  It is **not** an eligibility confirmation.
- Did any item have an **unknown index tier**? Those are unscored — say so, do
  not silently drop or guess them.
- Is the headline `verdict` consistent with the checks (any failed modelled
  minimum → `FAIL_MODELLED_CHECK`)?
- Did you include the **verify-against-current-period disclaimer**?

---

## References

- `references/uak_criteria.md` — the bundled, dated Sağlık Bilimleri TABLO 10
  point table, the four MODELLED minimums, the mandatory minimums NOT modelled
  (verify by hand), and the primary ÜAK source links.
- `references/scoring_rules.md` — the author-share rule with worked numeric
  examples, the lead-author definition, the SCIE/SSCI ≥40 floor, and the
  rounding convention.

Part of the AlterLab Academic Skills suite.
