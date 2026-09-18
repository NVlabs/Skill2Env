# Endpoints — verified vs. unverified

Everything here is either verified live during authoring (2026-06-06) or marked
**UNVERIFIED**. Do not promote an UNVERIFIED item to a hard claim without
re-checking against the live source.

## YÖK Ulusal Tez Merkezi (the official site)

| Surface | URL | Status |
|---------|-----|--------|
| Repository home / search entry | `https://tez.yok.gov.tr/UlusalTezMerkezi/` | Verified live |
| Detailed search form | `https://tez.yok.gov.tr/UlusalTezMerkezi/tarama.jsp` | From key_resources (pre-verified) |
| Gated full-text viewer | `https://tez.yok.gov.tr/UlusalTezMerkezi/TezGoster` | From key_resources (pre-verified) — gated |

**No official public API exists.** The site is a server-rendered JSP form.
There is **no published JSON/REST endpoint** — do not fabricate one.

The **TezGoster** viewer is gated and serves full text **online-view-only** for
*İzinli* theses (no photocopy, no bulk download). Restricted (*İzinsiz*) theses
expose metadata + abstract only.

Driving the form programmatically requires a **real browser** (the search and
viewer pages use session state / challenges), not plain HTTP GET. Prefer the
`yoktez-mcp` connector below.

## yoktez-mcp (the recommended data path)

- **Repo:** `github.com/saidsurucu/yoktez-mcp` — **MIT** licensed. *(Verified
  live: license + tool surface, 2026-06-06.)*
- **Local install (uv-first):**
  `uvx --from git+https://github.com/saidsurucu/yoktez-mcp yoktez-mcp`
- **Hosted connector:** `https://yoktezmcp.fastmcp.app/mcp`

### Tools exposed (verified from the repo README)

**`search_yok_tez_detailed`** — detailed search, returns paginated thesis
summaries + a total result count. Parameters:

```
thesis_title, author_name, advisor_name, university_name, institute_name,
department_name, discipline_name, thesis_number, subject_headings, index_terms,
abstract_text, thesis_type, permission_status, thesis_status, language,
institute_group, year_start, year_end, page, results_per_page
```

**`get_yok_tez_document_markdown`** — retrieves a *permitted* thesis PDF as
Markdown. Parameters: `detail_page_url`, `page_number`. Returns Markdown
content, total page count, metadata. Works only on *İzinli* theses.

### Form-field ↔ parameter mapping (verified field labels)

| Form label (Turkish) | English gloss | `search_yok_tez_detailed` param |
|----------------------|---------------|---------------------------------|
| Tez Adı | Thesis title | `thesis_title` |
| Yazar | Author | `author_name` |
| Danışman | Advisor | `advisor_name` |
| Konu | Subject | `subject_headings` |
| Anahtar Kelime | Keyword | `index_terms` |
| Özet | Abstract | `abstract_text` |
| Tez No | Thesis number | `thesis_number` |
| (Üniversite) | University | `university_name` |
| (Tez Türü) | Thesis type | `thesis_type` |
| (İzin Durumu) | Permission status | `permission_status` |

## tezara.org (community mirror)

- **What it is:** "Tez Arama ve Metaveri Analizi Platformu" (Thesis Search and
  Metadata Analysis Platform) — a cleaned community mirror of Ulusal Tez Merkezi
  records. *(Site identity verified live, 2026-06-06.)*
- **Use for:** large/repeated metadata harvests that would hit the official
  2000-results-per-search cap.
- **From key_resources (pre-verified):** offers CSV/JSON export and bypasses the
  2000-row cap; per-thesis URL pattern `tezara.org/theses/{thesisNo}`.
- **UNVERIFIED at authoring time:** the homepage did not expose the export UI or
  the `/theses/{id}` path in the fetched markup. Treat the export feature and the
  exact URL pattern as documented-but-unconfirmed; verify on the live site before
  relying on them in an automated harvest.

## Result cap

- **2000 results per search** — hard cap (from key_resources / research, not
  re-verifiable without running a 2000+ query). Split by year range / university
  / institute and merge locally. If a search's `total` is ~2000, assume it is
  truncated.
