---
name: alterlab-trdizin
description: "Searches TR Dizin (TÜBİTAK ULAKBİM national citation index) and verifies a journal's current national-index status through its confirmed unauthenticated REST/Elasticsearch API at https://search.trdizin.gov.tr/api/defaultSearch/{publication|journal|author|institution}/ (params q, order e.g. relevance-DESC, page), parsing hits.hits[]._source plus faceted aggregations, and derives indexing status from a journal record's isActive + journalYear coverage vs rejectYearList. Use when the user wants to search TR Dizin, check if a journal is TR Dizin indexed (TR Dizin'de var mı / taranıyor mu), find Turkish-indexed publications, verify national-index status before submitting, or audit doçentlik-eligible venues. For DergiPark hosting prefer alterlab-dergipark; for doçentlik points prefer alterlab-docentlik-eligibility; for teşvik scoring prefer alterlab-akademik-tesvik. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash WebFetch
compatibility: No API key required — queries the keyless TR Dizin search API (https://search.trdizin.gov.tr/api/defaultSearch/) via `uv run python` (requests if present, else stdlib urllib); reports network failure rather than passing silently
metadata:
  skill-author: AlterLab
  version: "1.0.1"
  last_updated: "2026-06-06"
  depends_on: "alterlab-dergipark (hosting vs indexing), alterlab-docentlik-eligibility, alterlab-akademik-tesvik"
---

# TR Dizin — National Index Search & Journal-Status Check

Searches **TR Dizin** (TÜBİTAK ULAKBİM's *ulusal atıf dizini* — the national
citation index) and answers the question Turkish academics actually ask:
**"Is this journal indexed in TR Dizin right now?"** It hits the index's
confirmed keyless API, parses the Elasticsearch records, and for a journal derives
a current-status verdict from the authoritative coverage fields.

TR Dizin status is a career gate: it gates **doçentlik** (associate-professorship)
eligibility and feeds **akademik teşvik** (academic-incentive) / **UBYT** payouts.
This skill verifies *status*; it does **not** compute the points — see the routing
table below.

## Quick Start

```
Is the journal "Bilig" indexed in TR Dizin?
"Toplum ve Bilim" TR Dizin'de taranıyor mu?
Find TR Dizin publications about deprem okuryazarlığı, newest first
Search TR Dizin for an author / institution
```

→ Run `scripts/query_trdizin.py`, read the JSON/table, and report the verdict.
Never assert a journal's status from memory — always query the live index.

## When to Use This Skill

Use it for any of these intents:

- **Check journal status** — "is journal X TR Dizin indexed?", "TR Dizin'de var mı?",
  verify a target venue's national-index status **before submitting**.
- **Search publications** — find Turkish-indexed articles by keyword, sort by year
  or citation count, narrow with the returned year/subject/language facets.
- **Search author / institution** — locate an author or institution record in the
  national index.
- **Audit a venue list** — screen a set of journals for current TR Dizin coverage
  (e.g. before assembling a doçentlik dossier — *but the point math is elsewhere*).

### Does NOT Trigger — route these to the right sibling

| If the request is really about… | Route to |
|---|---|
| DergiPark **journal hosting** / OAI harvest / article BibTeX (hosting ≠ indexing) | `alterlab-dergipark` |
| Computing **doçentlik** eligibility points from a publication list | `alterlab-docentlik-eligibility` |
| Computing **akademik teşvik** / UBYT incentive scores | `alterlab-akademik-tesvik` |
| YÖK **thesis** (tez) search in Ulusal Tez Merkezi | `alterlab-yok-tez` |
| YÖK Akademik **academic profile / affiliation** lookup | `alterlab-yok-akademik` |
| YÖK Atlas **program / admission statistics** | `alterlab-yokatlas` |
| Verifying an arbitrary citation **exists** (Crossref/OpenAlex/etc.) | `alterlab-citation-verifier` |
| **Turkish APA 7 / TR Dizin citation style** formatting | `alterlab-tr-academic-style` |

This skill answers *"is it in the index, and what does the index say?"* — it does
not adjudicate acceptance criteria, compute career points, or format citations.

## How It Works

The TR Dizin SPA is backed by an **unauthenticated** Elasticsearch search API
(verified live 2026-06-06, HTTP 200). One endpoint, four record types:

```
GET https://search.trdizin.gov.tr/api/defaultSearch/{type}/?q=…&order=…&page=…
    type ∈ { publication | journal | author | institution }
```

Full endpoint, parameter, and `_source` field documentation is in
[`references/api_reference.md`](references/api_reference.md). The
journal-status logic is in [`references/journal_status.md`](references/journal_status.md).

Two facts to keep honest:

- **No `limit` param.** The server returns ~10 hits per page and **ignores**
  a client `limit`. To collect *N* records, page through `page=1,2,…` and slice
  client-side — which is exactly what the script's `--limit` does. Do **not** tell
  the user a server-side limit exists.
- **`firstIndexDate` / `indexDate` are query-time stamps** (they come back as
  "now") and carry no index history. Status is derived from `isActive`,
  `journalYear` coverage, and `rejectYearList` only.
- **`isActive` is not trustworthy on its own.** A journal can keep
  `isActive=true` while coverage stopped years ago and recent years are in
  `rejectYearList` (verified: *Eğitim Bilim Toplum*, ISSN 1303-9202 — active,
  coverage→2019, rejected 2020–2025). The script therefore checks `rejectYearList`
  against the latest coverage year **before** ever saying "currently indexed".

## Pipeline

### 1. Pick the mode

| User intent | Command |
|---|---|
| Is journal X indexed? | `query_trdizin.py journal "<title or ISSN>"` |
| Find indexed articles | `query_trdizin.py publication "<terms>" --order publicationYear-DESC` |
| Author / institution | `query_trdizin.py author "<name>"` / `… institution "<name>"` |

### 2. Run the query

```bash
# Journal status (the headline use case)
uv run python skills/turkish-academia/alterlab-trdizin/scripts/query_trdizin.py \
    journal "Bilig" --limit 3

# Publication search, newest first, with facets, JSON out
uv run python skills/turkish-academia/alterlab-trdizin/scripts/query_trdizin.py \
    publication "deprem okuryazarlığı" \
    --order publicationYear-DESC --limit 20 --facets --out trdizin.json
```

- `--order` (verified enum): `relevance-DESC` (default), `publicationYear-ASC|DESC`,
  `title-ASC|DESC`, `orderCitationCount-ASC|DESC`.
- `--limit N` collects up to *N* records by paging client-side (default 10).
- `--facets` adds the year / subject / language aggregations.
- `--json` / `--out PATH` emit the structured report; default is a readable table.
- The script prefers `requests`, falls back to stdlib `urllib` — runs in a bare
  `uv` env with **no API key**.

### 3. Report the verdict

**For a journal**, surface the derived `verdict`, e.g.:

- *Currently indexed in TR Dizin (active; coverage years 2004–2026)* — when
  `isActive` is true, `journalYear` shows recent coverage, and there is **no**
  reject year newer than the last covered year.
- *No longer indexed in TR Dizin — rejected after coverage (…)* — when the most
  recent `rejectYearList` year is newer than the last `journalYear` year. This
  fires **even if `isActive` is still true** (de-indexed venue).
- *Rejected / not indexed (rejected years …)* — when `rejectYearList` is set but
  not newer than coverage.
- *Not currently active in TR Dizin* — when `isActive` is false.

Quote ISSN/eISSN and the coverage years so the user can confirm it is the right
journal (title collisions happen). If it matters for a submission decision, remind
them TR Dizin status can change between terms — re-check before relying on it.

**For publications**, present a table of `(year) title — journal · doi · access`,
sorted as requested, and offer to refine via the facets.

## Self-Check Before Reporting

- Did the API actually respond? If the script exited with `NETWORK UNAVAILABLE`
  (exit 3), say so plainly and do **not** state a status from memory.
- Is the matched journal the right one? Confirm by ISSN/eISSN, not title alone.
- Did the verdict come from `isActive` / `journalYear` / `rejectYearList` — not
  from the query-time `*IndexDate` fields?
- Is this a *status* question? If the user actually wants doçentlik points, teşvik
  scoring, DergiPark hosting, tez search, or citation formatting, hand off to the
  sibling skill named in the routing table above.

## References

- [`references/api_reference.md`](references/api_reference.md) — endpoint,
  parameters, `order` enum, response shape, `_source` fields per type, facets, and
  the no-`limit` / query-time-date caveats (all verified live).
- [`references/journal_status.md`](references/journal_status.md) — the
  indexing-status decision logic, worked examples, and why it gates doçentlik /
  teşvik (with hand-offs to those skills).

Part of the AlterLab Academic Skills suite.
