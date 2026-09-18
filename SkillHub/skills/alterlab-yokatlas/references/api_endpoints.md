# YÖK Atlas JSON API & yokatlas-py reference

Verified 2026-06-06. Sources: `yokatlas.yok.gov.tr/api/tercih-kilavuz/universiteler`
(fetched live), `github.com/saidsurucu/yokatlas-py` and its PyPI v0.6.0 release
metadata. Treat anything not listed here as unverified — do not invent fields,
paths, or enum values.

## The migration (why only the JSON API)

YÖK Atlas migrated from server-rendered PHP to a **React SPA** backed by a JSON
API. As of **April 2026** the legacy pages return only an empty SPA shell:

- `lisans.php?y=…` — **DEAD**
- `lisans-panel.php` — **DEAD**
- `tercih-sihirbazi-*.php` — **DEAD**

Every pre-April-2026 HTML scraper broke. Use only the JSON API below, ideally
through `yokatlas-py` which wraps it.

## JSON API surface — `https://yokatlas.yok.gov.tr/api/tercih-kilavuz/`

| Path | Returns | Status |
|------|---------|--------|
| `/universiteler` | JSON array of `{"universiteAdi": str, "universiteId": int}` | **Verified live** (raw API field names) |
| `/universite-iller` | provinces (il) list | From key_resources (not re-fetched) |
| `/universite-programlar` | programs for a university | From key_resources |
| `/search` | program search driven by `SearchFilters` | From key_resources |

Verified first record of `/universiteler`:

```json
{ "universiteAdi": "ABDULLAH GÜL ÜNİVERSİTESİ (KAYSERİ)", "universiteId": 173499 }
```

`list_universities()` via yokatlas-py returned **227 records** on the
2026-06-06 live check, each as `{"universite_id": int, "universite_adi": str}`
(the wrapper normalizes the raw camelCase API keys to snake_case). The upstream
README cites "221 universities"; the live count drifts as YÖK updates the guide,
so report the count you actually observe rather than a fixed number. No API key
is required for any path.

## yokatlas-py (the wrapper this skill uses)

- **Version:** 0.6.0 (released 2026-04-29). Pin **>=0.6.0**.
- **License:** MIT. **Python:** >=3.10.
- **Install / run:** `pip install yokatlas-py`, or run ad-hoc with
  `uv run --with yokatlas-py python …` (this skill's convention — no global install).
- **Runtime deps:** httpx >=0.28.1, pydantic (>=2.7,<3), pydantic-settings.
  (So this is **not** stdlib-only; the helper script imports `yokatlas-py` and
  fails loudly with manual instructions if it is absent.)

### Public API

Module-level shortcuts:

| Function | Signature | Returns |
|----------|-----------|---------|
| `search_programs` | `search_programs(filters_dict, size=…)` | paginated page of `Program` |
| `get_program` | `get_program(kilavuz_kodu: int)` | one `Program` or `None` |
| `list_universities` | `list_universities()` | every university (count drifts — see above; ~221–227 observed) |

Object API: `YokAtlasClient` (sync) / `AsyncYokAtlasClient` (async),
`SearchFilters`, `Program`, `YearlyStats`, `Settings`.

```python
from yokatlas_py import YokAtlasClient, SearchFilters
with YokAtlasClient() as client:
    page = client.search(SearchFilters(puan_turu="SAY", universite="boğaziçi"), size=20)
    for prog in page.content:
        print(prog.current.min_puan, prog.current.basari_sirasi)
```

`Program` carries up to four years: `prog.current` (latest), `prog.history`
(three prior years), `prog.all_years`.

### SearchFilters fields

| Field | Type | Values / meaning |
|-------|------|------------------|
| `puan_turu` | str | `"SAY"`, `"SÖZ"`, `"EA"`, `"DİL"`, `"TYT"` (note diacritics) |
| `universite` / `universite_id` | str/list or int/list | fuzzy name(s) or id(s) |
| `program` / `birim_grup_id` | str/list or int/list | program name(s) or group id(s) |
| `il` / `il_kodu` | str/list or int/list | province name(s) or code(s) |
| `universite_turu` | str | `"DEVLET"` (state), `"VAKIF"` (foundation/private) |
| `birim_turu_id` | int | `46` = Lisans (bachelor's), `47` = Önlisans (associate) |
| `burs_orani_id` | int | scholarship ratio |
| `ogrenim_turu_id` | int | study mode (full-time / part-time) |
| `kilavuz_kodu` | int | single-program filter (the guide code); snake_case in `SearchFilters` — the camelCase `kilavuzKodu` only appears in the wire payload built by `to_payload()` |
| `min_basari_sirasi` / `max_basari_sirasi` | int | success-rank window |

### Returned statistic fields (`YearlyStats`)

`year, kontenjan, yerlesen, kontenjan_obs, kontenjan_y34, prof, doc, dou,
ogr_gor, ar_gor, kpss1, kpss2, min_puan, basari_sirasi`

| Field | Türkçe → English gloss |
|-------|------------------------|
| `kontenjan` | kontenjan → quota (seats offered) |
| `yerlesen` | yerleşen → placed/enrolled students |
| `min_puan` | taban puan → minimum admission score |
| `basari_sirasi` | başarı sırası → success rank (national rank of last placed student) |
| `prof` | profesör → full professors |
| `doc` | doçent → associate professors |
| `dou` | doktor öğretim üyesi → assistant professors (Dr. lecturer) |
| `ogr_gor` | öğretim görevlisi → instructors |
| `ar_gor` | araştırma görevlisi → research assistants |

**v0.6.0 caveat:** demographic breakdowns (gender, high-school-type splits) are
**not** returned. Only the fields above are available — do not promise others.

## Turkish-character handling

yokatlas-py normalizes İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü for fuzzy matching, so
`"boğaziçi"` and `"bogazici"` both resolve. User-facing output should preserve
correct Turkish spelling with diacritics (e.g. "Boğaziçi Üniversitesi").
