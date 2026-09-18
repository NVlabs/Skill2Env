---
name: alterlab-dergipark
description: "Harvests article metadata, abstracts, and full-text PDFs from DergiPark (TÜBİTAK ULAKBİM's national journal-hosting platform, ~2,537 journals) via its verified platform-wide OAI-PMH endpoint (https://dergipark.org.tr/api/public/oai/; verbs Identify/ListSets/ListRecords/GetRecord; prefixes oai_dc/oai_mods/oai_marc/oai_etdms; setSpec=journal-slug), parses Highwire citation_* and DC.* meta tags on /pub/{slug}/article/{id} pages, pulls PDFs from the citation_pdf_url path, and emits BibTeX/RIS locally. Use when the user wants to harvest a Turkish journal, fetch DergiPark articles, list a journal archive, get BibTeX/RIS for a DergiPark paper, or read a journal aim-and-scope (öz/kapsam). For TR Dizin indexing status use alterlab-trdizin; for YÖK theses use alterlab-yok-tez; for academic profiles use alterlab-yok-akademik. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash WebFetch
compatibility: No API key required — harvests DergiPark's public OAI-PMH 2.0 endpoint and open article pages via `uv run python` (requests if present, else stdlib urllib); degrades gracefully offline by emitting a network_unavailable error rather than fabricating records
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
---

# DergiPark — National Journal Harvester (TÜBİTAK ULAKBİM)

DergiPark (https://dergipark.org.tr) is **TÜBİTAK ULAKBİM's national
journal-hosting platform** — ~2,537 Turkish scholarly journals on OJS-based
infrastructure. This skill harvests its metadata, abstracts, and full-text PDFs
**reproducibly**, by going through the one stable machine surface: a platform-wide
**OAI-PMH** (Open Archives Initiative Protocol for Metadata Harvesting) endpoint,
plus open article pages. It never guesses bibliographic data — every field comes
from the live endpoint, and it emits BibTeX/RIS locally from parsed meta tags.

The interactive search page is gated behind a human-verification challenge, so
this skill does **not** scrape search over plain HTTP. OAI set-harvest and direct
article-page fetches are the robust paths (see `references/oai-cookbook.md`).

## When to Use This Skill

Use it when the request is about getting data **out of DergiPark**:

- harvest / fetch all articles of a Turkish (DergiPark) journal
- list a journal's archive or find its slug
- get BibTeX or RIS (an export format) for a DergiPark article
- download a DergiPark full-text PDF
- read a journal's **aim-and-scope** (*öz/kapsam* — abstract/scope) or its
  self-declared index list

Canonical Turkish terms you may see: **öz** (abstract), **kapsam** (scope),
**dergi** (journal), **künye** (citation/masthead). Preserve Turkish spelling with
diacritics in all user-facing strings (e.g. *Mülkiye Dergisi*).

### Does NOT Trigger — route adjacent requests to the right sibling

| The request is really about… | Route to |
|------------------------------|----------|
| Whether a journal is **indexed in TR Dizin** (national citation index) / its TR Dizin status | **alterlab-trdizin** |
| Finding/searching a **graduate thesis** (YÖK Ulusal Tez Merkezi) | **alterlab-yok-tez** |
| An **academic's profile / affiliation** (YÖK Akademik) | **alterlab-yok-akademik** |
| University **program admission statistics** (YÖK Atlas) | **alterlab-yokatlas** |
| Computing **doçentlik** (associate-professorship) eligibility points | **alterlab-docentlik-eligibility** |
| Computing **akademik teşvik** (academic-incentive) score | **alterlab-akademik-tesvik** |
| Depositing a manuscript/data in **Aperta** (TÜBİTAK open archive) | **alterlab-aperta** |
| **Verifying that cited references exist** / hallucination audit | **alterlab-citation-verifier** |
| Turkish APA / TR Dizin **writing-style** conventions | **alterlab-tr-academic-style** |

## How It Works — Three Scripts

All run with `uv run python` from the skill directory. No API key. Each prefers
`requests` if installed, else falls back to stdlib `urllib`. Full recipes and
gotchas are in `references/oai-cookbook.md`; the verified endpoint table is in
`references/endpoints.md`.

### 1. `scripts/dergipark_oai.py` — OAI harvest (primary path)

```bash
# Find a journal's slug (slug == OAI setSpec)
uv run python scripts/dergipark_oai.py list-journals --tsv | rg -i "mülkiye"

# Harvest a whole journal (follows resumptionToken paging automatically)
uv run python scripts/dergipark_oai.py harvest mulkiye --prefix oai_dc --out mulkiye.json

# One article's structured oai_dc record
uv run python scripts/dergipark_oai.py get 10 --prefix oai_dc
```

Verbs: `Identify / ListSets / ListRecords / GetRecord`. Prefixes:
`oai_dc` (parsed into clean fields) and `oai_mods / oai_marc / oai_etdms`
(returned as raw record XML for callers that want the richer schema).

### 2. `scripts/article_meta.py` — one article → BibTeX / RIS

```bash
uv run python scripts/article_meta.py /en/pub/mulkiye/article/10 --format bibtex
uv run python scripts/article_meta.py /en/pub/mulkiye/article/10 --format ris
uv run python scripts/article_meta.py /en/pub/mulkiye/article/10 --format json
```

Parses the page's `citation_*` + `DC.*` meta tags and formats BibTeX/RIS
**locally** — it does not call any on-site export backend (that route is
unverified). The JSON output includes a resolved `pdf_url`.

### 3. `scripts/journal_info.py` — aim-and-scope + self-declared indexes

```bash
uv run python scripts/journal_info.py mulkiye --lang en
```

Returns the *aim-and-scope* text and the `/indexes` page, the latter stamped with
a `DISCLAIMER` and cross-check pointers to TR Dizin and DOAJ.

## Three Rules That Prevent Wrong Answers

1. **Publication date ≠ OAI datestamp.** The OAI `<datestamp>` is the platform
   *re-index* time, not the publication date. To slice by publication year,
   **harvest then filter on `dc:date`** locally — do not rely on `from`/`until`.
2. **PDF id ≠ article id.** Take the PDF link from the page's `citation_pdf_url`
   meta tag (e.g. `/en/download/article-file/9` for article `/10`); never build it
   from the article id.
3. **Hosting ≠ indexing.** Being on DergiPark says nothing about quality or TR
   Dizin coverage. The `/indexes` page is *self-declared* and unverified by
   DergiPark. For an authoritative TR Dizin status verdict, route to
   **alterlab-trdizin**. See `references/indexing.md`.

## Graceful Degradation

Network failures surface as a `network_unavailable` / `oai_error` JSON object on
stderr (exit 1) — the scripts **never** fabricate a record or a verdict. If the
endpoint is unreachable, say so and stop; do not invent metadata from memory.

## References

- `references/endpoints.md` — every verified endpoint, prefix, and identifier
  scheme (with what is explicitly UNVERIFIED), observed live 2026-06-06.
- `references/oai-cookbook.md` — copy-paste recipes: slug lookup, full harvest,
  year filtering, PDF download, and the gated-search workaround via Playwright.
- `references/indexing.md` — the DergiPark-vs-TR Dizin distinction and how to
  cross-check real indexing against TR Dizin and DOAJ.

Part of the AlterLab Academic Skills suite.
