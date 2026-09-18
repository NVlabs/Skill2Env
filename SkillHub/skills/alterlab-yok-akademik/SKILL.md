---
name: alterlab-yok-akademik
description: "Looks up a Turkish academic's official YOKSIS-backed profile, current affiliation, unvan (academic title), publications, research projects, and supervised theses on the YOK Akademik portal (akademik.yok.gov.tr/AkademikArama/), a server-rendered JSP app with no public JSON API, by scraping its verified endpoints (AkademisyenArama POST search, viewAuthor.jsp profile, AkademisyenProjeBilgileri, AkademisyenYonTezBilgileri) keyed by an opaque authorId, with Turkish-character (Iı Şş Ğğ Çç Öö Üü) normalization for name matching. Use when the request is to verify a Turkish academic's current institution, find a researcher on YOK Akademik, confirm affiliation for authorship or a recommendation letter, or list someone's supervised theses or projects. For admission statistics (kontenjan, taban puan) use alterlab-yokatlas; for the national thesis full-text archive use alterlab-yok-tez; for publication metadata enrichment use alterlab-openalex. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash WebFetch
compatibility: No API key required — scrapes the public YOK Akademik JSP portal (akademik.yok.gov.tr/AkademikArama/) via `uv run python` (requests + BeautifulSoup, stdlib fallback) and WebFetch; there is NO official public JSON API
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-yokatlas (admission stats), alterlab-yok-tez (thesis full text), alterlab-openalex (publication metadata)"
---

# YOK Akademik — Official Turkish Academic Profile & Affiliation Lookup

**YOK Akademik** (Yükseköğretim Kurulu Akademik — the Turkish Council of Higher
Education's academic search portal) is the **authoritative source for a Turkish
academic's official current affiliation**. It is YÖKSİS-backed (the national
higher-education information system), so for Turkish institutions it is more
reliable than ORCID or OpenAlex affiliation strings, which lag and fragment.

This skill resolves a name to that official record: current **kurum** (institution),
**fakülte/bölüm** (faculty/department), **unvan** (academic title — e.g. *Prof. Dr.*,
*Doç. Dr.*, *Dr. Öğr. Üyesi*), plus the person's portal-listed publications, research
**projeler** (projects), and **danışmanlık yapılan tezler** (supervised theses).

> **No public JSON API exists.** The portal at `akademik.yok.gov.tr/AkademikArama/`
> is a server-rendered Java/JSP app. The only route is polite HTML scraping of its
> verified endpoints. Treat every record as authoritative-but-scraped: confirm a
> candidate match with the user before asserting an affiliation.

## When to Use This Skill

Use this skill when the request is to:

- **Verify a Turkish academic's current institution / affiliation** (for authorship
  bylines, a recommendation letter, a grant team, an editorial-board check).
- **Find / look up a researcher on YOK Akademik** by name.
- **Read someone's official unvan** (title) and faculty/department.
- **List the theses someone has supervised** (master's / doctorate), with student,
  year, and institution.
- Pull the person's portal-listed publications or research projects as a starting set.

### Does NOT Trigger

Route these adjacent asks to the correct sibling skill — do **not** answer them here:

| The request is really about… | Use instead |
|------------------------------|-------------|
| University/program admission statistics — kontenjan, taban puan, başarı sırası, yerleşen | `alterlab-yokatlas` |
| Reading or citing a **thesis full text / abstract** from the national archive (Ulusal Tez Merkezi) | `alterlab-yok-tez` |
| Searching the national journal-hosting platform DergiPark | `alterlab-dergipark` |
| Whether a **journal** is indexed in TR Dizin (the national citation index) | `alterlab-trdizin` |
| Enriching/verifying **publication metadata** (DOIs, citation counts, co-authors) | `alterlab-openalex` |
| Checking whether the cited papers actually **exist** (fabricated citations) | `alterlab-citation-verifier` |
| Computing **doçentlik** (associate-professorship) eligibility points from a publication list | `alterlab-docentlik-eligibility` |
| Computing the **akademik teşvik** (academic-incentive) score | `alterlab-akademik-tesvik` |

YOK Akademik answers **"who is this academic, officially, and where are they now?"**
It does **not** judge research quality, compute career-progression points, or fetch
thesis full text.

## The verified endpoints (no API key)

All under the base `https://akademik.yok.gov.tr/AkademikArama/`. There is **no**
documented JSON API; these are HTML/JSP pages. See
[`references/endpoints.md`](references/endpoints.md) for the full map, parameters,
and verification status of each.

| Step | Endpoint | Returns |
|------|----------|---------|
| Search by name | **POST** `AkademisyenArama` with `aramaTerim=<name>&islem=1&…Checkbox=on` → category page → follow its **Akademisyenler** link → `view/searchResultviewListAuthor.jsp` | Candidate rows: name, unvan, university, faculty/department, and the profile link carrying the **opaque `authorId`** |
| Profile / select author | `AkademisyenGorevOgrenimBilgileri?islem=direct&authorId=<id>` → renders `view/viewAuthor.jsp` | The person's header: current kurum, fakülte, bölüm, unvan, ORCID/email badges. This GET also **registers the author** in the session (the tabs below 500 without it). |
| Projects | `AkademisyenProjeBilgileri?authorId=<id>` | Portal-listed research projects (AB / TÜBİTAK / araştırma …) |
| Publications | `AkademisyenYayinBilgileri?pubType=<token>&authorId=<id>` | Typed tabs (Kitaplar / Makaleler / Bildiriler). `pubType` is **required & opaque** — discover the tokens from the profile page (empty `pubType` → HTTP 418) |
| Supervised theses | `AkademisyenYonTezBilgileri?authorId=<id>` | Danışmanlık tezleri: title, student, level, year, institution |

`authorId` is an **opaque** value (a 16-hex-char token, e.g. `006B496E5F3E4EE2`) — never
construct or guess one; only use IDs you obtained from a live search result. A cookie
**session** is mandatory: the helper GETs the portal root first so the server sets the
JSESSIONID the search POST needs (a session-less POST returns HTTP 500).

## Workflow

### 1. Normalize the name and search

Turkish casing is a real trap: `İ→i` and `I→ı` are *not* the ASCII fold. Search the
name **as the user gave it** (correctly-encoded UTF-8), and also try a diacritic-folded
variant so `"Cağrı"`, `"Cagri"`, and `"Çağrı"` all reach the same person. The helper
script does both. See [`references/turkish_names.md`](references/turkish_names.md) for
the exact İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü rules and matching strategy.

```bash
uv run python skills/turkish-academia/alterlab-yok-akademik/scripts/yok_akademik.py \
    search "Ayşe Yılmaz"
```

This returns the candidate list (pretty JSON by default; add `--json` for compact
single-line output). **Each candidate carries its `authorId`, name, and unvan.**

### 2. Disambiguate with the user

Common names return many people. Present the candidates as a table —
**name · unvan · university · faculty/department** — and ask the user which one (or
confirm the institution they expected). Do **not** silently pick the first row and
assert an affiliation; that is exactly how a wrong byline or letter gets written.

### 3. Pull the chosen profile / projects / theses / publications

The `authorId` you pass must come from a live search row. Each per-author command first
**lands on the profile** (which selects the author in the session) before fetching its
tab — the helper handles that for you.

```bash
# Profile header (affiliation, unvan)
uv run python .../scripts/yok_akademik.py profile  --author-id <authorId>

# Research projects (AB / TÜBİTAK / araştırma …)
uv run python .../scripts/yok_akademik.py projects --author-id <authorId>

# Supervised theses
uv run python .../scripts/yok_akademik.py theses   --author-id <authorId>

# Portal-listed publications (typed tabs: Kitaplar / Makaleler / Bildiriler)
uv run python .../scripts/yok_akademik.py pubs     --author-id <authorId>
```

### 4. Report — and state provenance

When you report an affiliation, say it came from **YOK Akademik (YÖKSİS)** and give
the date, because people move. If the scrape failed or the portal returned a 302/500
(it does so intermittently), say so and fall back to WebFetch on the search page —
**never** invent an affiliation, authorId, title, or thesis from memory.

## Politeness & robustness rules

The portal is a public service with no API; scrape gently.

- One descriptive `User-Agent`; **throttle** (≈1–2 s between requests); retry the
  frequent transient 302/500 responses with backoff before giving up.
- Cache results within a session — don't re-hit the same `authorId` repeatedly.
- The script prefers `requests` + `BeautifulSoup`; if `BeautifulSoup` is absent it
  degrades to a stdlib `html.parser` extraction so it still runs in a bare `uv` env.
- On total failure it emits a structured `{"status": "unavailable", ...}` record with
  manual-lookup instructions, never a fabricated profile.

## Self-Check Before Reporting

- Did a **live search** return the `authorId` I'm using, or did I guess it? (Never guess.)
- Did I **disambiguate** when more than one candidate matched the name?
- Is the affiliation I'm reporting attributed to **YOK Akademik / YÖKSİS** with a date?
- Did the request actually want admission stats (`alterlab-yokatlas`) or thesis full
  text (`alterlab-yok-tez`) instead? Re-check the "Does NOT Trigger" table.
- If the portal failed, did I say so plainly rather than filling the gap from memory?

## References

- [`references/endpoints.md`](references/endpoints.md) — the verified JSP endpoint map,
  parameters, the `authorId` note, and what is verified vs. unverified.
- [`references/turkish_names.md`](references/turkish_names.md) — Turkish casing/diacritic
  rules (İ/ı etc.) and the name-matching strategy.
- [`references/affiliation_verification.md`](references/affiliation_verification.md) —
  why YÖKSİS beats ORCID/OpenAlex for TR affiliation, and the disambiguation checklist.

Part of the AlterLab Academic Skills suite.
