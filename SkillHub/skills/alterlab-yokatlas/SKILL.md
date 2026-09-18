---
name: alterlab-yokatlas
description: "Retrieves Türkiye higher-education program and admission statistics from YÖK Atlas (yokatlas.yok.gov.tr) — quotas (kontenjan), placements (yerleşen), minimum admission scores (taban puan), success ranks (başarı sırası), and per-title academic-staff counts — via the keyless yokatlas-py (>=0.6.0, MIT) wrapper over the JSON API at /api/tercih-kilavuz/ (search, universiteler, universite-programlar), with SearchFilters for puan türü (SAY/SÖZ/EA/DİL/TYT), university type (DEVLET/VAKIF), province, and success-rank ranges. Use when the request mentions YÖK Atlas, program statistics, kontenjan/quota data, taban puan/minimum admission score, başarı sırası/success rank, placement counts, or program staff counts for institutional research, program benchmarking, or student advising. For an academic's CV/profile/affiliation prefer alterlab-yok-akademik; for theses prefer alterlab-yok-tez. Legacy PHP endpoints are dead post-April-2026; only the JSON API is used. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash WebFetch
compatibility: No API key required — wraps the keyless YÖK Atlas JSON API (/api/tercih-kilavuz/) through yokatlas-py v0.6.0 (MIT, Python >=3.10) run via `uv run --with yokatlas-py python`; degrades to a documented manual lookup when offline
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-yok-akademik (academic profiles), alterlab-research-lookup (publication enrichment)"
---

# YÖK Atlas — Türkiye University Program & Admission Statistics

Retrieves official program-level statistics from **YÖK Atlas** (Yükseköğretim
Kurulu Atlası — the Council of Higher Education's program atlas) for any
undergraduate (*lisans*) or associate (*önlisans*) program in Türkiye: quotas,
placements, minimum admission scores, success ranks, and academic-staff head
counts by title. It wraps the **keyless** YÖK Atlas JSON API through the
maintained `yokatlas-py` package, so the same query yields the same structured
records — no HTML scraping, no API key.

This is the **statistics** skill. It does **not** look up an individual
academic's CV, publications, or affiliation — that is `alterlab-yok-akademik`,
a separately architected YÖK system (see the routing table below).

## When to Use This Skill

Use it when the user wants program- or university-level numbers from YÖK Atlas:

```
YÖK Atlas'tan Boğaziçi Bilgisayar Mühendisliği taban puanını ve başarı sırasını çıkar
Compare the kontenjan and yerleşen counts for all Tıp programs at state universities
What was the minimum SAY score for Hacettepe Elektrik-Elektronik Mühendisliği last year?
List every university in YÖK Atlas and the academic-staff counts for a given program
How many professors vs. araştırma görevlisi does this department have?
```

→ Run `scripts/yokatlas_lookup.py` (a thin `yokatlas-py` wrapper), read the JSON,
then present the requested statistics as a table. Always state the data year and
that figures come from YÖK Atlas.

### Canonical Turkish terms (English gloss on first use)

| Turkish | Gloss | API field |
|---------|-------|-----------|
| kontenjan | quota (seats offered) | `kontenjan` |
| yerleşen | placed (students enrolled) | `yerlesen` |
| taban puan | minimum admission score | `min_puan` |
| başarı sırası | success rank (national rank of last placed student) | `basari_sirasi` |
| puan türü | score type (SAY/SÖZ/EA/DİL/TYT) | `puan_turu` |
| lisans / önlisans | bachelor's / associate degree | `birim_turu_id` 46 / 47 |
| kılavuz kodu | guide code (unique program id) | `kilavuzKodu` |

Academic-staff title counts are returned as `prof` (profesör), `doc` (doçent),
`dou` (doktor öğretim üyesi), `ogr_gor` (öğretim görevlisi), and `ar_gor`
(araştırma görevlisi — research assistant).

## ⚠️ Endpoint caveat (read before scraping anything)

As of **April 2026** YÖK Atlas migrated from server-rendered PHP to a React SPA
backed by a JSON API. The **legacy PHP endpoints are dead** — `lisans.php?y=…`,
`lisans-panel.php`, and `tercih-sihirbazi-*.php` now return only an empty SPA
shell. **Never scrape them.** Use only the JSON API under
`/api/tercih-kilavuz/` (or, as this skill does, `yokatlas-py` which wraps it).
Endpoint and field details: `references/api_endpoints.md`.

## Does NOT Trigger — route these elsewhere

| The user actually wants… | Route to |
|--------------------------|----------|
| An academic's CV, publications, projects, theses supervised, or **official affiliation** (akademik.yok.gov.tr) | `alterlab-yok-akademik` |
| A graduate **thesis** (tez) — full text, abstract, originality/novelty check (Ulusal Tez Merkezi) | `alterlab-yok-tez` |
| Whether a **journal** is indexed in TR Dizin, or a journal/article search | `alterlab-trdizin` |
| Articles hosted on **DergiPark** (harvest, BibTeX, journal scope) | `alterlab-dergipark` |
| Computing **doçentlik** (associate-professor) eligibility points | `alterlab-docentlik-eligibility` |
| Computing **akademik teşvik** (academic-incentive) score | `alterlab-akademik-tesvik` |
| Scaffolding a **TÜBİTAK** ARDEB 1001/1002-A proposal | `alterlab-tubitak-proposal` |
| Publication metadata for an author (DOIs, citations, h-index) | `alterlab-research-lookup` / `alterlab-openalex` |

This skill answers **"what are the admission/quota/staff numbers for this
program or university?"** — nothing about an individual scholar's output.

## How It Works

### The data source

| Surface | What it returns |
|---------|-----------------|
| `/api/tercih-kilavuz/universiteler` | the university list (`{universiteAdi, universiteId}`) — verified live |
| `/api/tercih-kilavuz/universite-iller` | provinces (il) |
| `/api/tercih-kilavuz/universite-programlar` | programs per university |
| `/api/tercih-kilavuz/search` | program search with `SearchFilters` |

`yokatlas-py` (MIT, Python >=3.10) exposes these as module-level functions
`search_programs(filters_dict, size=…)`, `get_program(kilavuz_kodu)`, and
`list_universities()` (227 records on the 2026-06-06 live check; plus a
`YokAtlasClient` / `SearchFilters` / `Program` object API). It normalizes
Turkish characters (İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü)
for fuzzy matching, so `"boğaziçi"` and `"bogazici"` both resolve. Full filter
and field reference: `references/api_endpoints.md`.

### Pipeline

1. **Pick the operation** from the request: list universities, search programs,
   or fetch one program by its kılavuz kodu (guide code).
2. **Build filters.** The common `SearchFilters` fields are `puan_turu`
   (SAY/SÖZ/EA/DİL/TYT), `universite`, `program`, `il` (province),
   `universite_turu` (DEVLET/VAKIF), and `min_basari_sirasi`/`max_basari_sirasi`
   for a success-rank window. See `references/api_endpoints.md` for the full list.
3. **Run the helper:**

   ```bash
   uv run --with yokatlas-py python \
     skills/turkish-academia/alterlab-yokatlas/scripts/yokatlas_lookup.py \
     search --puan-turu SAY --universite "boğaziçi" --program "bilgisayar" --size 20
   ```

   Other subcommands:

   ```bash
   # All universities (id + name)
   uv run --with yokatlas-py python .../yokatlas_lookup.py universities

   # One program's multi-year statistics by guide code
   uv run --with yokatlas-py python .../yokatlas_lookup.py program --kod 102210277
   ```

   The script prints a JSON envelope (`{"tool", "operation", "count", "results"}`).
   If `yokatlas-py` or the network is unavailable it prints a structured
   `{"error": …, "manual_instructions": …}` and exits non-zero — it never
   fabricates statistics.

4. **Read the JSON and report.** For each program surface the year, `kontenjan`,
   `yerlesen`, `min_puan`, `basari_sirasi`, and (when asked) the staff counts.
   Each `Program` carries up to four years (`current` + `history`); state which
   year a number is from.

5. **Cross-link if the user drifts.** If they then ask about a person's CV or
   publications, hand off to `alterlab-yok-akademik`; for theses,
   `alterlab-yok-tez`.

## Worked Patterns

- **Program benchmarking.** Search the same `program` across `universite_turu`
  DEVLET vs VAKIF, then tabulate `min_puan` / `basari_sirasi` side by side.
- **Student advising.** Given a target başarı sırası, filter with
  `max_basari_sirasi` to list programs realistically in reach.
- **Institutional research.** Fetch a program by kılavuz kodu and report the
  staff mix (`prof`/`doc`/`dou`/`ogr_gor`/`ar_gor`) and the kontenjan→yerleşen
  fill rate across the available years.

More query recipes: `references/query_recipes.md`.

## Caveats & Self-Check

- **Pin the wrapper.** `yokatlas-py` is pinned to **>=0.6.0**; the upstream JSON
  API changed once (April 2026) and broke every legacy scraper. If results look
  empty or malformed, re-verify the package version before reporting.
- **v0.6.0 dropped demographic breakdowns** (gender / high-school-type splits).
  Do not promise those fields — only the staff/quota/score fields above are returned.
- **Score type matters.** A program's `min_puan` is only meaningful next to its
  `puan_turu`; always report them together.
- **Data year.** Numbers are historical (latest plus three prior years). Never
  imply a figure is "current admissions" without naming its year.
- **Did the script reach the network?** If it returned an `error` envelope, say
  so and relay the `manual_instructions` — do not infer numbers from memory.

## References

- `references/api_endpoints.md` — the `/api/tercih-kilavuz/` endpoints, the full
  `SearchFilters` field list, enums (puan türü, university type, birim türü), and
  the returned statistic fields, with the legacy-PHP-dead caveat.
- `references/query_recipes.md` — worked `yokatlas_lookup.py` invocations for
  benchmarking, advising, and institutional-research questions.

Part of the AlterLab Academic Skills suite.
