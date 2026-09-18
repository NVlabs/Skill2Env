# DergiPark Endpoints — Verified vs Unverified

All "verified" rows below were observed live on **2026-06-06** by direct HTTP
request against the production host. Treat anything in the UNVERIFIED section as
unconfirmed — do not present it to a user as fact, and re-check before relying on it.

## OAI-PMH (the primary, gate-free, machine-readable surface)

| Item | Verified value |
|------|----------------|
| Base URL | `https://dergipark.org.tr/api/public/oai/` |
| Protocol | OAI-PMH `2.0` (`<protocolVersion>2.0</protocolVersion>`) |
| `repositoryName` | `DergiPark` |
| `adminEmail` | `oai@dergipark.org.tr` |
| `granularity` (Identify) | `YYYY-MM-DDThh:mm:ssZ` |
| `deletedRecord` | `no` |
| `compression` | `gzip`, `deflate` |
| Metadata prefixes | `oai_dc`, `oai_etdms`, `oai_marc`, `oai_mods` |
| Set scheme | `setSpec` **equals the journal slug** (e.g. `set=mulkiye`) |
| Set example | `<setSpec>mulkiye</setSpec> <setName>Mülkiye Dergisi</setName>` |
| Request identifier | `oai:dergipark.org.tr:article/{id}` (used for `GetRecord&identifier=`) |
| Header identifier (observed) | ListRecords echoes `...:article/{id}`; **GetRecord echoes `...:record/{id}`** — both seen live; parse the numeric tail, do not assume one form |

### Verbs confirmed working

- `?verb=Identify`
- `?verb=ListMetadataFormats`
- `?verb=ListSets` (paginates via `<resumptionToken>`)
- `?verb=ListRecords&metadataPrefix=oai_dc&set={slug}` (paginates via `<resumptionToken>`)
- `?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:dergipark.org.tr:article/{id}`

### oai_dc record shape (GetRecord on article/10)

- `<dc:title>` — article title (Turkish, with diacritics)
- `<dc:creator>` — repeated, `Surname, Given` form
- `<dc:date>` — **publication date** (e.g. `2012-12-25`). USE THIS, not `<datestamp>`.
- `<dc:identifier>` — repeated: the canonical `/en/pub/{slug}/article/{id}` URL **and** an
  `izlik.org` permalink (and a DOI when the article has one).
- `<dc:subject>`, `<dc:language>`, `<dc:publisher>`, `<dc:source>`, `<dc:description>`

### The datestamp trap (usage rule)

The OAI header `<datestamp>` is the platform **re-index time**, not the publication
date — on a fresh re-index it can read e.g. `2026-05-13` for a 2012 article. To find
articles by publication year, **harvest the set, then filter on `dc:date` locally.**
Do not rely on OAI `from`/`until` selective harvest for publication-date queries
(selective-harvest-by-pubdate reliability is UNVERIFIED).

## Open article + asset paths (no human-verification gate)

| Path | Verified |
|------|----------|
| Article HTML | `/{lang}/pub/{slug}/article/{id}` → 200, exposes `citation_*` + `DC.*` meta tags |
| Full-text PDF | value of the page's `citation_pdf_url` meta tag, e.g. `/en/download/article-file/{file-id}` → 200, `content-type: application/pdf` |
| Aim & scope | `/{lang}/pub/{slug}/aim-and-scope` → 200 |
| Self-declared indexes | `/{lang}/pub/{slug}/indexes` → 200 (`/page/indexing` is 404 — do not use) |
| Last-issue RSS | `/{lang}/pub/{slug}/rss/lastissue/{lang}` → 200, `content-type: xml` |

**PDF id ≠ article id.** On article `/10`, `citation_pdf_url` was
`/en/download/article-file/9`. Always take the PDF link from the `citation_pdf_url`
meta tag; never build it from the article id in the page URL.

### Article-page meta tags observed (article/10)

`citation_journal_title`, `citation_issn`, `citation_author` (repeated),
`citation_publisher`, `citation_title`, `citation_publication_date`,
`citation_volume`, `citation_issue`, `citation_firstpage`, `citation_lastpage`,
`citation_abstract`, `citation_abstract_html_url`, `citation_language`,
`citation_pdf_url`; plus `DC.Title`, `DC.Source`, `DC.Type`, `DC.Identifier`,
`DC.Language`.

## UNVERIFIED — do not assert as fact

- **`stats_trdizin_citation_count`** meta tag: described in prior art as an in-page
  signal of TR Dizin coverage, but it was **NOT present** on the articles probed here.
  Treat it as advisory/conditional only; to confirm TR Dizin indexing, query TR Dizin
  itself (see `indexing.md`).
- **On-site Cite/export backend URL** (RIS/BibTeX/EndNote): the UI offers it, but the
  backend route is unverified — this skill formats BibTeX/RIS **locally** from meta
  tags instead and never calls an unverified export endpoint.
- **OJS REST `/api/v1/...` routes**: unverified on this host; do not assume they exist.
- **OAI `from`/`until` selective harvest by publication date**: unverified; use the
  harvest-then-filter-on-`dc:date` pattern.
