---
name: alterlab-yok-tez
description: "Searches YÖK Ulusal Tez Merkezi (tez.yok.gov.tr/UlusalTezMerkezi), Turkey's mandatory national graduate-thesis repository, for literature-review discovery and pre-proposal özgünlük (originality) checks. Drives the detailed search form (Tez Adı/Yazar/Danışman/Konu/Anahtar Kelime/Özet, tez türü, year range, language, İzinli/İzinsiz permission status) via the saidsurucu/yoktez-mcp tool, applies Turkish auto-stemming and ve/veya/içermesin boolean operators, runs paired Turkish+English queries, and emits Türkçe APA-7 thesis citations mapping Tez No to the published Yayın No. Use when the user wants to search Turkish theses, ara YÖK tez, check thesis novelty before approving a proposal, find dissertations by advisor (danışman) or university, dedupe a topic against existing tezler, or cite a YÖK thesis; respects the 2000-results-per-search cap and online-view-only access. For non-thesis Turkish journals use alterlab-dergipark or alterlab-trdizin. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) WebFetch
compatibility: "No API key required — searches via the saidsurucu/yoktez-mcp connector (local `uvx` or hosted https://yoktezmcp.fastmcp.app/mcp) or by driving the public tez.yok.gov.tr Detaylı Tarama form; full-text is online-view-only, no bulk download"
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
---

# YÖK Ulusal Tez Merkezi — Turkish National Thesis Search

YÖK Ulusal Tez Merkezi (the Higher Education Council's *National Thesis
Center*) is the single mandatory repository for every Turkish graduate thesis —
*yüksek lisans* (master's), *doktora* (doctorate), *tıpta/diş/eczacılıkta
uzmanlık* (medical/dental/pharmacy specialty), and *sanatta yeterlik* (art
proficiency). It is the authoritative source for two faculty workflows this
skill serves:

1. **Literature discovery** — finding existing Turkish dissertations for a
   review, by topic, *danışman* (advisor), university, or year.
2. **Pre-proposal *özgünlük* (originality) checks** — before a supervisor
   approves a student's thesis topic, scanning whether the same work already
   exists or is embargoed-but-registered.

This skill is **discovery + metadata harvesting + citation**, not bulk
full-text download (full text is online-view-only — see access model below).

## When to Use This Skill

```
YÖK Ulusal Tez Merkezi'nde "sürdürülebilir mimari" konulu tezleri ara
Bir öğrencim "sanal prodüksiyon" üzerine doktora yapmak istiyor; daha önce yapılmış mı?
Find every doctoral dissertation supervised by Prof. X at IEU
Cite this YÖK thesis in APA 7 (Turkish)
Is this thesis topic novel, or has it already been done in Turkey?
```

→ Construct a Detaylı Tarama (detailed search) query, run it through the
`yoktez-mcp` connector (or drive the form), dedupe results into a
`{Tez No, year, university, danışman, title, izin}` table, and — when asked —
emit a Türkçe APA-7 citation.

### Does NOT Trigger — route these elsewhere

| Request | Correct skill |
|---------|---------------|
| Search **Turkish journal articles** on DergiPark | `alterlab-dergipark` |
| Check a **journal's TR Dizin** index status / search the national citation index | `alterlab-trdizin` |
| Look up an **academic's profile / supervised-thesis list / affiliation** on YÖK Akademik | `alterlab-yok-akademik` |
| University **program admission statistics** (kontenjan, taban puan) on YÖK Atlas | `alterlab-yokatlas` |
| Compute **doçentlik** (associate-professorship) eligibility points | `alterlab-docentlik-eligibility` |
| Compute **akademik teşvik** (academic-incentive) score | `alterlab-akademik-tesvik` |
| Hands-on **thesis writing / supervision / defense** coaching (chapters, viva) | `alterlab-thesis-supervisor` |
| Build a **PRISMA systematic review** over biomedical/scientific databases | `alterlab-literature-review` |
| Manage a **Zotero/BibTeX reference library** | `alterlab-citation-mgmt` |
| **Türkçe APA-7 / TR Dizin house style** rules in general (not a thesis cite) | `alterlab-tr-academic-style` |

This skill answers *"does this Turkish thesis exist / has this been done, and how
do I cite it?"* — it does not write the thesis, judge journals, or score careers.

---

## The data path: yoktez-mcp

There is **no official public API** for Ulusal Tez Merkezi. The maintained,
verified community path is the **`saidsurucu/yoktez-mcp`** MCP server (MIT
licensed). Prefer it over scraping.

**Install (uv-first, matches the local toolchain):**

```bash
uvx --from git+https://github.com/saidsurucu/yoktez-mcp yoktez-mcp
```

**Hosted connector:** `https://yoktezmcp.fastmcp.app/mcp`

It exposes exactly two tools:

| Tool | Purpose | Key parameters |
|------|---------|----------------|
| `search_yok_tez_detailed` | Detailed search → paginated thesis summaries + total count | `thesis_title`, `author_name`, `advisor_name`, `university_name`, `institute_name`, `department_name`, `discipline_name`, `thesis_number`, `subject_headings`, `index_terms`, `abstract_text`, `thesis_type`, `permission_status`, `thesis_status`, `language`, `institute_group`, `year_start`, `year_end`, `page`, `results_per_page` |
| `get_yok_tez_document_markdown` | Fetch a permitted thesis PDF as Markdown | `detail_page_url`, `page_number` |

These map one-to-one onto the public **Detaylı Tarama** form fields: *Tez Adı*
(title), *Yazar* (author), *Danışman* (advisor), *Konu* (subject), *Anahtar
Kelime* (keyword), *Özet* (abstract), *Tez No* (thesis number).

If the connector is unavailable, the search form at
`https://tez.yok.gov.tr/UlusalTezMerkezi/` can be driven directly (a real
browser is required — see `references/endpoints.md` for the gated-viewer
caveat). **Never invent a JSON/REST endpoint — none is published.**

A small offline helper, `scripts/yok_tez_query.py`, builds a normalized query
spec and the matching `search_yok_tez_detailed` argument dict from a plain
description (handy for the stemming/boolean rules below) without any network
call. See **Search craft**.

---

## Search craft (apply these automatically)

The full rule set with worked examples is in
[`references/search_syntax.md`](references/search_syntax.md). The essentials:

1. **Search Turkish roots, not inflected forms** — the engine auto-stems Turkish,
   so query `sürdürülebilir` rather than `sürdürülebilirliğin`. Diacritics
   (ç ğ ı İ ö ş ü) need **not** be normalized by the user.
2. **Boolean operators are `ve` / `veya` / `içermesin`** (and / or / must-not-contain),
   not `AND`/`OR`/`NOT`. Phrase-match by keeping words adjacent.
3. **Run BOTH a Turkish and an English query.** English terms only hit the
   *English* title/abstract/keyword fields, so an all-Turkish query silently
   misses theses written/indexed in English, and vice-versa.
4. **Search across `Konu`, `Tez Adı`, and `Özet`** for topic coverage — a title
   may not name the concept the abstract develops.

---

## Originality / supervision check (the repeatable recipe)

When a supervisor asks *"has this thesis topic already been done?"*, do **not**
run a naive open-access-only search — that misses the most important
near-duplicates. Instead:

1. Build paired TR+EN queries (above) across `Konu`, `Tez Adı`, and `abstract_text`.
2. Constrain `thesis_type` (e.g. *Doktora*) and a recent `year_start`–`year_end`
   window if the user gave one.
3. **Set `permission_status` to "Tümü" (All)** so *İzinsiz* (restricted,
   abstract-only) theses still surface — embargoed work is exactly what a naive
   search hides, and it is still prior art for a proposal.
4. Return a **deduplicated table**: `{Tez No, year, university, danışman, title,
   izin}`, sorted newest-first, for the supervisor to scan.
5. State explicitly that this is *registry coverage*, not a plagiarism / text-
   similarity score (that is iThenticate/Turnitin territory, out of scope here).

---

## Access model (set correct expectations)

- **Full text is online-view-only** for *İzinli* (permitted) theses — viewable in
  the browser, **no photocopy / bulk download**. The `get_yok_tez_document_markdown`
  tool works only on permitted theses.
- **Abstracts (*özet*) are always available**, even when full text is embargoed.
- ***İzinsiz* (restricted) theses** show metadata + abstract only; the full text
  is reachable in print via **TÜBESS** / inter-library loan through a university
  library.
- **Pre-2006 closed theses** can be opened by the author submitting a *Tez
  Yayımlama İzin Belgesi* (thesis-publication permission document).
- **Legal basis:** Law 7100 Art. 10 and Higher Education Law 2547 Additional Art.
  40 — theses are electronically accessible by default unless an authorized
  *gizlilik* (confidentiality) decision applies. YÖK's FAQ states **no fixed
  maximum embargo length**; do not assert a "12-month cap."

Full detail in [`references/access_legal.md`](references/access_legal.md).

---

## Caps and bulk harvest

- **Hard cap: 2000 results per search.** For broad topics, split the query by
  **year range**, **university**, or **institute** to stay under it, then merge
  and dedupe locally.
- For large/repeated harvests, the cleaned community mirror **tezara.org**
  ("Tez Arama ve Metaveri Analizi Platformu") offers structured export and
  sidesteps the per-search cap; see
  [`references/endpoints.md`](references/endpoints.md) for what is and isn't
  verified about it.
- Bulk Turkish↔English query expansion, advisor-name normalization, and CSV
  dedup are good fits to offload to a **local LLM** (qwen3-coder / gemma4) rather
  than burning API calls — this work is bulky, repetitive, and privacy-neutral.

---

## Citing a YÖK thesis (Türkçe APA-7)

Map the YÖK **Tez No** directly to APA's **Yayın No.** (publication number).
The `scripts/yok_tez_query.py --cite` mode formats both states; rules and more
examples in [`references/citation_apa7.md`](references/citation_apa7.md).

- **Published / permitted** (has a Yayın No.):
  > Soyad, A. (Yıl). *Tez başlığı* (Yayın No. _NNNNNN_) [Tez türü, Üniversite
  > Adı]. YÖK Ulusal Tez Merkezi.
- **Unpublished / restricted**:
  > Soyad, A. (Yıl). *Tez başlığı* [Yayımlanmamış tez türü tezi]. Üniversite Adı.

Optionally also emit BibTeX `@phdthesis` / `@mastersthesis` with
`note = {YÖK Ulusal Tez Merkezi, Tez No. NNNNNN}`.

---

## Self-check before reporting

- Did you run **both** a Turkish and an English query? An all-Turkish search is
  not complete.
- For an originality check, did you set `permission_status = Tümü` so *İzinsiz*
  theses surfaced? Restricted ≠ nonexistent.
- Did any broad search hit the **2000 cap**? If `total` ≈ 2000, split and re-run —
  you are almost certainly truncated.
- Are citations using **Tez No → Yayın No.** with the correct
  *published* vs *unpublished* template?
- Did you state that registry coverage ≠ a text-similarity / plagiarism score?

---

## References

- [`references/endpoints.md`](references/endpoints.md) — verified vs. unverified
  endpoints, the yoktez-mcp tool surface, the gated TezGoster viewer, tezara.org.
- [`references/search_syntax.md`](references/search_syntax.md) — auto-stemming,
  `ve`/`veya`/`içermesin`, TR+EN pairing, field-targeting, worked queries.
- [`references/access_legal.md`](references/access_legal.md) — İzinli/İzinsiz,
  TÜBESS, pre-2006 opening, Law 7100 / 2547 legal basis, embargo facts.
- [`references/citation_apa7.md`](references/citation_apa7.md) — Türkçe APA-7
  thesis templates and the Tez No → Yayın No. mapping.

Part of the AlterLab Academic Skills suite.
