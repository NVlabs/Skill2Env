# TR Dizin Search API — Reference

TR Dizin (TÜBİTAK ULAKBİM national citation index) ships a single-page app whose
backend is an **unauthenticated REST/Elasticsearch search API**. No key, no login.

> **Verified live** on 2026-06-06: HTTP 200 from all four endpoints; field names
> below were captured directly from the JSON. The frontend config at
> `https://search.trdizin.gov.tr/assets/env.json` reports
> `apiUrl: https://search.trdizin.gov.tr`.

## Endpoint

```
GET https://search.trdizin.gov.tr/api/defaultSearch/{type}/?q={query}&order={order}&page={page}
```

`{type}` is one of: `publication` | `journal` | `author` | `institution`.

### Query parameters

| Param | Meaning | Notes |
|-------|---------|-------|
| `q` | search string | URL-encode; UTF-8 Turkish characters (İ ı Ş ş Ğ ğ Ç ç Ö ö Ü ü) pass through fine |
| `order` | sort key | see enum below; default `relevance-DESC` |
| `page` | 1-based page | server returns **~10 hits per page** |

**`order` enum (verified against the SPA):**
`relevance-DESC`, `publicationYear-ASC`, `publicationYear-DESC`,
`title-ASC`, `title-DESC`, `orderCitationCount-ASC`, `orderCitationCount-DESC`.

> **Caveat — `limit` is not honored.** Sending `limit=N` does **not** cap the page
> size; the server returns its fixed ~10-per-page regardless. To collect *N*
> records, walk `page=1,2,…` and slice client-side. `scripts/query_trdizin.py`
> does exactly this (`--limit` is applied client-side). Do not advertise a
> server-side `limit`.

## Response shape

A raw Elasticsearch response:

```jsonc
{
  "took": 12,
  "hits": {
    "total": { "value": 28, "relation": "eq" },   // total matches
    "hits": [ { "_source": { /* the record */ } }, ... ]
  },
  "aggregations": {                                 // facets (see below)
    "facet-publication_year": { "buckets": [ {"key": 2025, "doc_count": 120}, ... ] },
    "facet-subject": { "buckets": [ ... ] },
    "facet-publicationLanguage": { "buckets": [ ... ] }
  }
}
```

Parse `hits.total.value` for the count and iterate `hits.hits[]._source`.

## `_source` fields by type

### `publication`
`id`, `orderTitle` (the display title), `authors[]` (each with `inPublicationName`,
`authorId`, `institution`, `duty`), `journal` (`name`, `issn`, `eissn`, `id`),
`publicationYear`, `doi`, `accessType` (`OPEN` / `CLOSED`), `pdf`, `docType`,
`language`, `abstracts[]` (`abstract`), `orderCitationCount`, `subjects`,
`databases`, `viewCount`, `downloadCount`.

> The human-readable title is in **`orderTitle`**, not `title`, for publications.

### `journal`
`id`, `title`, `issn`, `eissn`, `isActive` (bool), `journalYear[]`
(per-year index entries; each has `year` and `databases[]` + subject labels),
`lastYearList`, `rejectYearList` (list of `{id, year}` when rejected; `null`
otherwise), `indexedBy`, `journalDatabase[]` (e.g. `["SOCIAL"]`), `webAddress`,
`firstPublishYear`, `newJournal`, `oldJournal`, `firstIndexDate`, `indexDate`.

> **Do not trust `firstIndexDate` / `indexDate`** as index history — on this
> endpoint they are populated at query time (they equal "now"). The authoritative
> coverage signal is the set of years in `journalYear[]`. See
> `journal_status.md`.

### `author`
`id`, `fullName` (the populated display name), `firstName`, `lastName`,
`orderTitle` (same as `fullName`), `otherNames`, `orcid`, `hindex`,
`orderPublicationCount`, `orderCitationCount`, `indexedBy`, `status`, `userId`,
`firstIndexDate`, `indexedDate`.

> **There is no `name` / `title` field on author records.** Verified live: across
> every hit of an author query both `name` and `title` come back `null` (they are
> not even in the `_source` keys). Read the name from **`fullName`**, falling back
> to `orderTitle`. `scripts/query_trdizin.py` does this
> (`fullName or orderTitle or …`).

### `institution`
`id`, `name` (or `title`).

## Aggregations (facets)

Each `aggregations.{name}.buckets[]` is `{key, doc_count}`. The `publication`
endpoint returns ~13 facets; the full observed set (verified live 2026-06-06) is:
`facet-publication_year`, `facet-subject`, `facet-publicationLanguage`,
`facet-accessType`, `facet-database`, `facet-documentType`, `facet-publicationType`,
`facet-journalName`, `facet-authorName`, `facet-projectGroup`,
`facet-facetAuthorCity`, `facet-facetAuthorCountry`, `facet-facetAuthorInstitution`.

> The year facet key is **`facet-publication_year`** (not `facet-year`). The
> script's `_facets()` is generic, so it surfaces whatever facet keys the API
> returns regardless of these exact names.

Use facets to refine a broad query (e.g. narrow by year or subject) without a
second full search.

## Authoritative cross-references

- Journal acceptance criteria: <https://trdizin.gov.tr/kriterler/> (HTTP 200).
- Frontend config (apiUrl): <https://search.trdizin.gov.tr/assets/env.json>.
- The management API base (`https://yonetim.trdizin.gov.tr/api/v1`) is exposed in
  `env.json` but is the editorial/admin surface — **not used here, not verified,
  do not call it.**
