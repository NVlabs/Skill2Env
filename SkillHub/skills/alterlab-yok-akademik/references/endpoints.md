# YOK Akademik — endpoint map

Base: `https://akademik.yok.gov.tr/AkademikArama/`

YOK Akademik is a **server-rendered Java/JSP application**. It has **no official
public JSON API**. Every "endpoint" below is an HTML/JSP page; the only programmatic
route is polite HTML scraping. Treat the field list as the *visible* schema of the
rendered page, not a stable API contract — markup can change without notice.

> Verification status (re-confirmed live 2026-06-06 via a full end-to-end run, including
> a real search for "Ayşe Yılmaz" and a fetch of every per-author tab for authorId
> `006B496E5F3E4EE2`): the search POST shape, the session requirement, and the
> projects/pubs/theses endpoints below were all captured from live traffic. A cookie
> **session** (JSESSIONID, set by GETting the portal root) is mandatory — a session-less
> search POST returns HTTP 500. Re-confirm against a live run before relying on any
> exact field; the JSP markup itself can change without notice.

## 0. Session priming (mandatory)

`GET` `…/AkademikArama/` once to obtain the **JSESSIONID** cookie, and keep it for the
rest of the run. Without it the search POST returns **HTTP 500**, and the per-author tabs
return **HTTP 500** until the author has been "selected" (see §2).

## 1. Search — `AkademisyenArama` (POST)

`POST` `…/AkademikArama/AkademisyenArama` — **form-encoded body** (verified live):

```
aramaTerim=<UTF-8 name>&islem=1&yazarCheckbox=on&kitapCheckbox=on&PatentCheckbox=on
&projeCheckbox=on&MakaeleCheckbox=on&BildiriCheckbox=on&SanatsalCheckbox=on&TezCheckbox=on
```

- The term field is **`aramaTerim`** (NOT `name`). `islem=1` triggers the initial search;
  the `*Checkbox=on` fields scope which result categories the portal computes (note the
  portal's own misspelling `MakaeleCheckbox`).
- Send `aramaTerim` as **correctly-encoded UTF-8**. Do not ASCII-fold before sending —
  the portal indexes the diacritic forms (see `turkish_names.md`).
- The POST 302-redirects to a **category-overview** page (`view/searchResultview.jsp`)
  that summarises Akademisyenler / Makaleler / Tezler counts. Follow its **Akademisyenler**
  link — `…/AkademikArama/AkademikArama?islem=<opaque token>` — to reach
  `view/searchResultviewListAuthor.jsp`, which lists the authors.
- Each author is a `<tr id="authorInfo_NNN">` row whose avatar link is
  `AkademisyenGorevOgrenimBilgileri?islem=direct&sira=<token>&authorId=<hex>`. The row
  carries:
  - **Ad Soyad** (the display name is the avatar `<img alt="…">`)
  - **Unvan** (rendered long-form & uppercase, e.g. `DOKTOR ÖĞRETİM ÜYESİ`, `DOÇENT`,
    `PROFESÖR`, `ARAŞTIRMA GÖREVLİSİ`)
  - **Üniversite / Fakülte / Bölüm** (in the row text)
  - the **opaque `authorId`** — a 16-hex-char token, e.g. `006B496E5F3E4EE2`

`authorId` is an **opaque token**. Never construct, increment, or guess one — extract
it only from a live search row.

## 2. Profile / select author — `AkademisyenGorevOgrenimBilgileri`

`GET` `…/AkademikArama/AkademisyenGorevOgrenimBilgileri?islem=direct&authorId=<id>`

302-redirects to `view/viewAuthor.jsp` and renders the person's header card: current
**kurum** (institution), **fakülte**, **bölüm**, **unvan**, badge links (ORCID, email),
and the publication/project/thesis tab links. This card is the **authoritative current
affiliation**. Fetching it also **registers the author in the session** — the per-author
tabs in §3–§5 return HTTP 500 until this landing GET has run in the same session.

## 3. Projects — `AkademisyenProjeBilgileri`

`GET` `…/AkademikArama/AkademisyenProjeBilgileri?authorId=<id>` (after §2).

Renders `view/viewAuthorProject.jsp`: portal-listed research projects grouped by type
(AB Projesi / TÜBİTAK Projesi / Araştırma …) with **proje sayısı** (project count) and
year-based completed-project info.

## 4. Publications — `AkademisyenYayinBilgileri`

`GET` `…/AkademikArama/AkademisyenYayinBilgileri?pubType=<token>&authorId=<id>` (after §2).

- `authorId` — required, from search.
- `pubType` — **required and opaque**. An empty or absent `pubType` returns **HTTP 418**
  (verified live). The valid tokens are **per-author** and split publications into typed
  tabs — **Kitaplar** (books), **Makaleler** (articles), **Bildiriler** (proceedings).
  **Discover them live** from the profile page's tab links (each is
  `AkademisyenYayinBilgileri?pubType=<token>&authorId=<id>`); never hardcode a token.

Returns the portal-listed publications. This is the portal's own list — for canonical
metadata (DOIs, citation counts, deduped co-authors) cross-enrich via
`alterlab-openalex`, and to check the cited works actually exist via
`alterlab-citation-verifier`.

## 5. Supervised theses — `AkademisyenYonTezBilgileri`

`GET` `…/AkademikArama/AkademisyenYonTezBilgileri?authorId=<id>`

Returns **danışmanlık yapılan tezler** (theses the academic supervised): thesis title,
**öğrenci** (student), **düzey** (level — Yüksek Lisans / Doktora …), **yıl** (year),
and **kurum** (institution). For the thesis **full text or abstract** itself, this is
*not* the right system — use `alterlab-yok-tez` (Ulusal Tez Merkezi).

## What is verified vs. unverified

| Item | Status |
|------|--------|
| Search is a **POST** to `AkademisyenArama` with body field **`aramaTerim`** (+ `islem=1` + `*Checkbox=on`) | **Verified live 2026-06-06** (captured request body) |
| A JSESSIONID **session** is required (root GET first); session-less search POST → HTTP 500 | **Verified live 2026-06-06** |
| Author rows on `searchResultviewListAuthor.jsp` carry a 16-hex-char `authorId` (e.g. `006B496E5F3E4EE2`) | **Verified live 2026-06-06** |
| `AkademisyenGorevOgrenimBilgileri?islem=direct&authorId=` → `viewAuthor.jsp`; also selects the author for the tabs | **Verified live 2026-06-06** |
| `AkademisyenProjeBilgileri?authorId=` (projects), `AkademisyenYonTezBilgileri?authorId=` (theses) reachable after select | **Verified live 2026-06-06** |
| `AkademisyenYayinBilgileri` needs a non-empty, opaque per-author `pubType` token; empty `pubType` → HTTP 418 | **Verified live 2026-06-06** |
| Exact `pubType` token vocabulary | **Per-author & opaque** — discover from the profile's tab links; never hardcode |
| Exact HTML class/id selectors for each field | **Unverified / volatile** — JSP markup changes; parse defensively |
| Official SOAP CV web service (`servisler.yok.gov.tr`) | **Institution-gated and unverified** — returned 404 on a June-2026 check; do **not** hardcode without a live re-check |

Never assert a field, parameter token, or selector that you have not seen in a live
response. If the page shape changed, say so and fall back to WebFetch.
