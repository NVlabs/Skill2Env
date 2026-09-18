#!/usr/bin/env python3
"""yok_akademik.py — Look up an official Turkish academic profile on YOK Akademik.

YOK Akademik (akademik.yok.gov.tr/AkademikArama/) is the Turkish Council of Higher
Education's academic search portal — a server-rendered Java/JSP app, YÖKSİS-backed,
and the authoritative source for a Turkish academic's official CURRENT affiliation
(more reliable than ORCID/OpenAlex for TR institutions). There is **no official
public JSON API**; the only route is polite HTML scraping of its verified endpoints.

Subcommands
-----------
  search "Ad Soyad"         -> candidate rows (name, unvan, university, dept, authorId)
  profile  --author-id ID   -> the profile header (current kurum/fakülte/bölüm/unvan)
  pubs     --author-id ID   -> portal-listed publications (optional --pub-type)
  projects --author-id ID   -> portal-listed research projects (AB/TÜBİTAK/…)
  theses   --author-id ID   -> supervised theses (title, student, level, year, kurum)

Design constraints (mirror skills/core/alterlab-citation-verifier conventions)
------------------------------------------------------------------------------
- NO API keys. Prefers ``requests`` + ``BeautifulSoup``; degrades to the stdlib
  (``urllib`` + ``html.parser``) so it runs in a bare ``uv`` env.
- POLITE: descriptive User-Agent, 1–2 s throttle, retry the portal's frequent
  transient 302/500 responses with backoff.
- Turkish-character aware: queries are sent UTF-8 as given AND retried diacritic-folded;
  matching folds İ/ı Ş/ş Ğ/ğ Ç/ç Ö/ö Ü/ü (see ../references/turkish_names.md).
- GRACEFUL DEGRADATION: on failure it emits ``{"status": "unavailable", ...}`` with
  manual-lookup instructions — NEVER a fabricated profile, affiliation, or authorId.

SEARCH REQUEST (verified live 2026-06-06 via the rendered portal): name search is a
**POST** to ``AkademisyenArama`` with a form body — the term field is ``aramaTerim``
(NOT ``name``), plus ``islem=1`` and the category checkboxes (``yazarCheckbox=on`` …
``projeCheckbox=on``). It 302-redirects to ``view/searchResultviewListAuthor.jsp``,
whose author rows link to ``AkademisyenGorevOgrenimBilgileri?islem=direct&sira=…&
authorId=<hex>`` (the per-author landing, which itself renders ``view/viewAuthor.jsp``).
See ../references/endpoints.md for the captured request body.

NOTE ON SELECTORS: the JSP markup is volatile and the exact field selectors are
UNVERIFIED. This script parses defensively (multiple heuristics) and tells you when it
could not extract a field rather than guessing. ``authorId`` is an OPAQUE token (a
16-hex-char value, e.g. ``006B496E5F3E4EE2``); this script never constructs one — it
only reads IDs out of live search results.

Usage
-----
  uv run python yok_akademik.py search "Ayşe Yılmaz" --json
  uv run python yok_akademik.py profile  --author-id <id> --json
  uv run python yok_akademik.py projects --author-id <id> --json
  uv run python yok_akademik.py theses   --author-id <id> --json

Exit codes: 0 = ran (see JSON ``status``); 2 = bad input/usage.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import quote, urljoin

# --------------------------------------------------------------------------- #
# Constants                                                                    #
# --------------------------------------------------------------------------- #

BASE = "https://akademik.yok.gov.tr/AkademikArama/"
SEARCH_PATH = "AkademisyenArama"  # POST target for name search (see SEARCH_FORM below)
PROFILE_PATH = "AkademisyenGorevOgrenimBilgileri"  # per-author landing → viewAuthor.jsp
PUBS_PATH = "AkademisyenYayinBilgileri"
PROJECTS_PATH = "AkademisyenProjeBilgileri"
THESES_PATH = "AkademisyenYonTezBilgileri"

# Verified search POST body (captured live 2026-06-06). ``aramaTerim`` carries the name;
# ``islem=1`` triggers the initial search; the *Checkbox fields scope which result
# categories the portal computes (we keep author + project + thesis on).
SEARCH_FORM = {
    "islem": "1",
    "yazarCheckbox": "on",
    "kitapCheckbox": "on",
    "PatentCheckbox": "on",
    "projeCheckbox": "on",
    "MakaeleCheckbox": "on",  # portal's own spelling (sic)
    "BildiriCheckbox": "on",
    "SanatsalCheckbox": "on",
    "TezCheckbox": "on",
}

USER_AGENT = (
    "alterlab-yok-akademik/1.0.0 (AlterLab Academic Skills; "
    "academic-profile lookup; mailto:alterlab.ieu@gmail.com)"
)
HTTP_TIMEOUT = 20
RETRIES = 3
BACKOFF = 1.5
THROTTLE_SECONDS = 1.5  # polite delay between requests to a no-API public service

# Turkish diacritic fold (for matching only; display keeps the originals).
_FOLD = str.maketrans(
    {
        "İ": "i", "I": "i", "ı": "i", "i": "i",
        "Ç": "c", "ç": "c",
        "Ğ": "g", "ğ": "g",
        "Ö": "o", "ö": "o",
        "Ş": "s", "ş": "s",
        "Ü": "u", "ü": "u",
    }
)


def fold_tr(s: str) -> str:
    """Diacritic-fold a Turkish string to lowercase ASCII for MATCHING only."""
    return s.translate(_FOLD).lower().strip()


# --------------------------------------------------------------------------- #
# HTTP layer — prefer requests, fall back to urllib (stdlib). No keys, polite. #
# --------------------------------------------------------------------------- #

try:  # pragma: no cover - environment dependent
    import requests as _requests  # type: ignore

    _HAS_REQUESTS = True
except Exception:  # pragma: no cover
    _requests = None
    _HAS_REQUESTS = False

try:  # pragma: no cover - environment dependent
    from bs4 import BeautifulSoup  # type: ignore

    _HAS_BS4 = True
except Exception:  # pragma: no cover
    BeautifulSoup = None  # type: ignore
    _HAS_BS4 = False


class NetworkUnavailable(RuntimeError):
    """Raised when the portal could not be reached after retries."""


# A SESSION is mandatory: the portal hands out a JSESSIONID cookie on the root GET and
# REJECTS the search POST with HTTP 500 if that cookie is absent (verified live
# 2026-06-06). We keep one cookie-bearing session for the whole run and prime it once.
_SESSION: Any = None
_SESSION_PRIMED = False


def _get_session() -> Any:
    """Return a cookie-persisting client: a requests.Session, else a urllib opener."""
    global _SESSION
    if _SESSION is not None:
        return _SESSION
    if _HAS_REQUESTS:
        s = _requests.Session()
        s.headers.update({"User-Agent": USER_AGENT})
        _SESSION = s
    else:
        import http.cookiejar
        import urllib.request

        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        )
        opener.addheaders = [("User-Agent", USER_AGENT)]
        _SESSION = opener
    return _SESSION


def _prime_session() -> None:
    """GET the portal root once so the server sets the JSESSIONID the search POST needs."""
    global _SESSION_PRIMED
    if _SESSION_PRIMED:
        return
    try:
        _http_get(BASE, _prime=True)
    except NetworkUnavailable:
        pass  # let the actual request surface the error; priming is best-effort
    _SESSION_PRIMED = True


def _http_get(url: str, params: Optional[dict] = None, _prime: bool = False) -> str:
    """GET ``url`` with polite UA, throttle, retry/backoff, and the shared session."""
    return _http_request(url, params=params, data=None, _prime=_prime)


def _http_post(url: str, data: dict) -> str:
    """POST form ``data`` to ``url`` (name search) over the primed cookie session.

    The portal 500s a session-less POST, so we prime the JSESSIONID first; the POST then
    302-redirects to the result page, which requests/urllib follow by default.
    """
    _prime_session()
    return _http_request(url, params=None, data=data)


def _http_request(
    url: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    _prime: bool = False,
) -> str:
    """Shared HTTP core: polite UA, throttle, retry/backoff, cookie session. POST iff data."""
    is_post = data is not None
    if not _prime:
        _prime_session()  # GETs of per-author tabs also need the session cookie
    session = _get_session()
    last_err: Optional[Exception] = None
    for attempt in range(RETRIES):
        if attempt:
            time.sleep(BACKOFF**attempt)
        else:
            time.sleep(THROTTLE_SECONDS)
        try:
            if _HAS_REQUESTS:
                if is_post:
                    resp = session.post(url, data=data, timeout=HTTP_TIMEOUT)
                else:
                    resp = session.get(url, params=params, timeout=HTTP_TIMEOUT)
                # The portal intermittently returns 500/502/503 — retry those. (The
                # search POST's own 302 redirect is followed by the session, so a 302
                # surfacing here means the page bounced: retry it too.)
                if resp.status_code in (302, 500, 502, 503):
                    last_err = RuntimeError(f"HTTP {resp.status_code}")
                    continue
                resp.raise_for_status()
                resp.encoding = resp.encoding or "utf-8"
                return resp.text
            # stdlib fallback: the cookie-aware opener follows redirects by default.
            import urllib.parse
            import urllib.request

            if is_post:
                body = urllib.parse.urlencode(data).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
            else:
                full = url
                if params:
                    full = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
                req = urllib.request.Request(full)
            with session.open(req, timeout=HTTP_TIMEOUT) as r:  # noqa: S310
                raw = r.read()
            return raw.decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue
    raise NetworkUnavailable(f"YOK Akademik unreachable for {url}: {last_err}")


# --------------------------------------------------------------------------- #
# Parsing — defensive. BeautifulSoup if present, else stdlib regex extraction.  #
# --------------------------------------------------------------------------- #


_AUTHOR_ID_RE = re.compile(r"authorId=([^&\"'#]+)", re.IGNORECASE)


def _extract_author_id(href: str) -> Optional[str]:
    m = _AUTHOR_ID_RE.search(href or "")
    if m:
        return m.group(1)
    return None


# Each author on searchResultviewListAuthor.jsp is a <tr id="authorInfo_NNN"> row; the
# display name is the <img alt="…"> on the avatar link (the link's own text is empty),
# and the row text carries unvan + university + department.
_AUTHOR_ROW_RE = re.compile(
    r'<tr[^>]*id="authorInfo[^"]*"[^>]*>(.*?)</tr>', re.IGNORECASE | re.DOTALL
)
_IMG_ALT_RE = re.compile(r'<img[^>]*\balt="([^"]+)"', re.IGNORECASE)


def parse_search_results(html_text: str) -> list[dict[str, Any]]:
    """Extract candidate rows from the author-list page.

    The exact markup is volatile/unverified, so we anchor on the ``authorInfo`` row,
    take the display name from the avatar ``<img alt>``, and keep the whole row's visible
    text as ``context`` for the caller to read unvan/university from — marking anything we
    cannot confidently extract as ``None`` rather than guessing.
    """
    candidates: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    if _HAS_BS4:
        soup = BeautifulSoup(html_text, "html.parser")
        rows = soup.select('tr[id^="authorInfo"]') or soup.find_all("tr")
        for row in rows:
            link = row.find("a", href=_AUTHOR_ID_RE)
            if not link:
                continue
            author_id = _extract_author_id(link["href"])
            if not author_id or author_id in seen_ids:
                continue
            seen_ids.add(author_id)
            img = row.find("img", alt=True)
            name = (img["alt"].strip() if img else "") or link.get_text(
                " ", strip=True
            ) or None
            context = row.get_text(" ", strip=True) or (name or "")
            candidates.append(_row_record(author_id, name, context, link["href"]))
        if candidates:
            return candidates
        # Fall through to regex if the page shape was unexpected (no authorInfo rows).

    # stdlib (and bs4-miss) fallback: walk authorInfo <tr> blocks with regex.
    for block in _AUTHOR_ROW_RE.findall(html_text):
        href_m = _AUTHOR_ID_RE.search(block)
        if not href_m:
            continue
        author_id = href_m.group(1)
        if author_id in seen_ids:
            continue
        seen_ids.add(author_id)
        alt_m = _IMG_ALT_RE.search(block)
        name = html.unescape(alt_m.group(1).strip()) if alt_m else None
        context = re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", block))).strip()
        href = f"authorId={author_id}"
        full_href_m = re.search(r'href="([^"]*authorId=[^"]+)"', block)
        if full_href_m:
            href = html.unescape(full_href_m.group(1))
        candidates.append(_row_record(author_id, name or None, context, href))
    return candidates


# Heuristic unvan (title) tokens, longest-first so "Dr. Öğr. Üyesi" beats "Dr.".
# The list page renders LONG, UPPERCASE forms (e.g. "DOKTOR ÖĞRETİM ÜYESİ", "PROFESÖR");
# the profile/abbreviated forms also appear elsewhere — we match both, case-insensitively.
_UNVAN_PATTERNS = [
    # Long, list-page forms first (most specific). "Doktor Öğretim Üyesi" MUST precede
    # "Doçent" because that row's text is "DOKTOR ÖĞRETİM ÜYESİ (Unvan:Doçent)".
    "Doktor Öğretim Üyesi",
    "Öğretim Görevlisi",
    "Araştırma Görevlisi",
    "Profesör",
    "Doçent",
    # Abbreviated profile forms.
    "Prof. Dr.",
    "Doç. Dr.",
    "Dr. Öğr. Üyesi",
    "Öğr. Gör. Dr.",
    "Arş. Gör. Dr.",
    "Öğr. Gör.",
    "Arş. Gör.",
    "Dr.",
]


def _detect_unvan(text: str) -> Optional[str]:
    # Match via the Turkish-aware fold (fold_tr) so the İ/ı casing trap can't make
    # "ÖĞRETİM ÜYESİ" miss "Öğretim Üyesi" (plain str.lower would break on İ→i̇).
    # Patterns are ordered most-specific-first so longer titles win over substrings.
    folded = fold_tr(text)
    for u in _UNVAN_PATTERNS:
        if fold_tr(u) in folded:
            return u
    return None


def _row_record(author_id: str, name: Optional[str], context: str, href: str) -> dict[str, Any]:
    return {
        "author_id": author_id,  # OPAQUE — extracted live, never constructed
        "name": name,
        "name_folded": fold_tr(name) if name else None,
        "unvan": _detect_unvan(context),
        "context": context[:400] if context else None,  # raw row text for the caller
        "profile_url": urljoin(BASE, href),
        "_note": "unvan/university/department parsed heuristically from row text; "
        "confirm against the live profile page (selectors are unverified).",
    }


# --------------------------------------------------------------------------- #
# Commands                                                                     #
# --------------------------------------------------------------------------- #


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _envelope(status: str, command: str, **extra: Any) -> dict[str, Any]:
    env = {
        "tool": "alterlab-yok-akademik/yok_akademik.py",
        "version": "1.0.0",
        "source": "YOK Akademik (akademik.yok.gov.tr) — YÖKSİS-backed; no public API",
        "retrieved_at": _now(),
        "command": command,
        "status": status,
        "http_backend": "requests" if _HAS_REQUESTS else "urllib(stdlib)",
        "html_parser": "bs4" if _HAS_BS4 else "html.parser(stdlib)",
    }
    env.update(extra)
    return env


def _unavailable(command: str, detail: str, manual_hint: str) -> dict[str, Any]:
    return _envelope(
        "unavailable",
        command,
        error=detail,
        manual_instructions=(
            "The portal could not be reached or parsed. Do NOT fabricate a result. "
            + manual_hint
        ),
    )


# The category overview page links each result group ("Akademisyenler", "Makaleler",
# "Tezler") to /AkademikArama/AkademikArama?islem=<token>. We follow the AKADEMISYENLER
# one to reach the page that actually lists authors with their authorId.
_AKADEMISYEN_LINK_RE = re.compile(
    r'href="(/AkademikArama/AkademikArama\?islem=[^"]+)"[^>]*>'
    r"(?:(?!</a>).)*?Akademisyen",
    re.IGNORECASE | re.DOTALL,
)


def _akademisyen_results_url(category_html: str) -> Optional[str]:
    """From the search category-overview page, find the 'Akademisyenler' results link."""
    if _HAS_BS4:
        soup = BeautifulSoup(category_html, "html.parser")
        for a in soup.find_all("a", href=True):
            if "AkademikArama?islem=" in a["href"] and "akademisyen" in a.get_text(
                " ", strip=True
            ).lower():
                return urljoin(BASE, html.unescape(a["href"]))
        return None
    m = _AKADEMISYEN_LINK_RE.search(category_html)
    if m:
        return urljoin(BASE, html.unescape(m.group(1)))
    return None


def cmd_search(query: str) -> dict[str, Any]:
    """Search by name via the verified POST; send as-given AND folded, merge results.

    Verified flow (live 2026-06-06): POST ``aramaTerim``+checkboxes to ``AkademisyenArama``
    over a primed JSESSIONID session -> a category-overview page; follow its
    'Akademisyenler' ``AkademikArama?islem=`` link -> ``searchResultviewListAuthor.jsp``,
    whose author rows carry the ``authorId`` we extract. The portal indexes the diacritic
    forms, so we run the exact string first and a folded variant second, de-dup by id.
    """
    variants = [query]
    folded = query.translate(_FOLD)  # diacritic-folded ASCII variant; portal is lenient
    if folded != query:
        variants.append(folded)

    all_candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    errors: list[str] = []
    for v in variants:
        try:
            overview = _http_post(
                urljoin(BASE, SEARCH_PATH), data={"aramaTerim": v, **SEARCH_FORM}
            )
            authors_url = _akademisyen_results_url(overview)
            if not authors_url:
                # No 'Akademisyenler' group => the search found no academics for this term.
                continue
            page = _http_get(authors_url)
        except NetworkUnavailable as exc:
            errors.append(str(exc))
            continue
        for c in parse_search_results(page):
            if c["author_id"] not in seen:
                seen.add(c["author_id"])
                all_candidates.append(c)

    if not all_candidates and errors:
        return _unavailable(
            "search",
            "; ".join(errors),
            f"Search manually at {BASE} (type '{query}' into the search box and open "
            "the 'Akademisyenler' results).",
        )

    return _envelope(
        "ok",
        "search",
        query=query,
        query_variants=variants,
        count=len(all_candidates),
        candidates=all_candidates,
        disambiguation_required=len(all_candidates) > 1,
        note="If more than one candidate, confirm WHICH person with the user "
        "(by university/unvan) before asserting an affiliation. authorId is opaque.",
    )


def _select_author(author_id: str) -> str:
    """Land on the author's profile, which REGISTERS the author in the session.

    Verified live 2026-06-06: the per-author tab endpoints (projects/pubs/theses) return
    HTTP 500 unless this landing GET — ``AkademisyenGorevOgrenimBilgileri?islem=direct&
    authorId=<hex>`` — has been fetched first in the same cookie session. It
    302-redirects to ``view/viewAuthor.jsp`` and returns the populated profile HTML.
    """
    return _http_get(
        urljoin(BASE, PROFILE_PATH), params={"islem": "direct", "authorId": author_id}
    )


def _author_page(path: str, author_id: str, extra_params: Optional[dict] = None) -> str:
    """Select the author (landing) THEN fetch a per-author tab, reusing the session.

    The tab GET 500s on a cold session, so we always land first (cheap; cached cookies).
    """
    _select_author(author_id)
    params = {"authorId": author_id}
    if extra_params:
        params.update(extra_params)
    return _http_get(urljoin(BASE, path), params=params)


def cmd_profile(author_id: str) -> dict[str, Any]:
    # The landing GET (AkademisyenGorevOgrenimBilgileri?islem=direct&authorId=…) both
    # registers the author in the session AND 302-redirects to view/viewAuthor.jsp,
    # returning the populated profile header.
    try:
        page = _select_author(author_id)
    except NetworkUnavailable as exc:
        return _unavailable(
            "profile",
            str(exc),
            f"Open {urljoin(BASE, PROFILE_PATH)}?islem=direct&authorId={author_id} "
            "in a browser.",
        )
    text = _visible_text(page)
    return _envelope(
        "ok",
        "profile",
        author_id=author_id,
        unvan=_detect_unvan(text),
        profile_url=f"{urljoin(BASE, PROFILE_PATH)}?islem=direct&authorId={quote(author_id)}",
        raw_text_excerpt=text[:1200],
        note="Affiliation fields (kurum/fakülte/bölüm) come from YÖKSİS but the exact "
        "selectors are unverified — read kurum/fakülte/bölüm from raw_text_excerpt and "
        "confirm. Report provenance as 'YOK Akademik (YÖKSİS), as of <date>'.",
    )


# Publications are split into typed tabs (Kitaplar/Makaleler/Bildiriler …), each reached
# via AkademisyenYayinBilgileri?pubType=<OPAQUE token>&authorId=<id>. The portal REJECTS
# an empty/absent pubType with HTTP 418 (verified live), so we must discover the real,
# per-author pubType tokens from the landing page rather than guessing or hardcoding them.
_PUBTYPE_LINK_RE = re.compile(
    r'href="[^"]*AkademisyenYayinBilgileri\?pubType=([^"&]+)&authorId=[^"]*"[^>]*>'
    r"(.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)


def _discover_pub_types(landing_html: str) -> list[dict[str, str]]:
    """Return [{'pub_type': <token>, 'label': <Kitaplar/Makaleler/…>}] from the profile."""
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    if _HAS_BS4:
        soup = BeautifulSoup(landing_html, "html.parser")
        for a in soup.find_all("a", href=True):
            m = re.search(r"AkademisyenYayinBilgileri\?pubType=([^&]+)&authorId=", a["href"])
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                out.append({"pub_type": m.group(1), "label": a.get_text(" ", strip=True)})
        return out
    for tok, inner in _PUBTYPE_LINK_RE.findall(landing_html):
        if tok in seen:
            continue
        seen.add(tok)
        label = re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", inner))).strip()
        out.append({"pub_type": tok, "label": label})
    return out


def cmd_pubs(author_id: str, pub_type: str = "") -> dict[str, Any]:
    # AkademisyenYayinBilgileri needs a valid pubType token (empty => HTTP 418). Land on
    # the profile first (selects the author AND exposes the pubType tab links), discover
    # the live tokens, then fetch the requested type (or all of them).
    try:
        landing = _select_author(author_id)
    except NetworkUnavailable as exc:
        return _unavailable(
            "pubs",
            str(exc),
            f"Open {urljoin(BASE, PROFILE_PATH)}?islem=direct&authorId={author_id} and "
            "click a publication tab (Kitaplar / Makaleler / Bildiriler).",
        )
    pub_types = _discover_pub_types(landing)
    if not pub_types:
        return _unavailable(
            "pubs",
            "no publication-type tabs found on the profile page",
            f"Open {urljoin(BASE, PROFILE_PATH)}?islem=direct&authorId={author_id} and "
            "read the publication tabs directly (the person may have no listed works).",
        )
    wanted = [pt for pt in pub_types if pt["pub_type"] == pub_type] if pub_type else pub_types
    if pub_type and not wanted:
        return _unavailable(
            "pubs",
            f"pubType token {pub_type!r} not among this author's tabs",
            "Available tabs: "
            + ", ".join(f"{p['label']}={p['pub_type']}" for p in pub_types),
        )
    sections: list[dict[str, Any]] = []
    errors: list[str] = []
    for pt in wanted:
        try:
            page = _http_get(
                urljoin(BASE, PUBS_PATH),
                params={"pubType": pt["pub_type"], "authorId": author_id},
            )
        except NetworkUnavailable as exc:
            errors.append(f"{pt['label']}: {exc}")
            continue
        sections.append(
            {
                "label": pt["label"],
                "pub_type": pt["pub_type"],
                "raw_text_excerpt": _visible_text(page)[:2000],
            }
        )
    if not sections and errors:
        return _unavailable("pubs", "; ".join(errors), "Retry, or read the tabs in a browser.")
    return _envelope(
        "ok",
        "pubs",
        author_id=author_id,
        pub_type=pub_type or "(all discovered tabs)",
        available_pub_types=[{"label": p["label"], "pub_type": p["pub_type"]} for p in pub_types],
        sections=sections,
        note="Portal-listed publications, by typed tab (pubType tokens discovered live "
        "from the profile, never hardcoded). For canonical DOIs/citation counts enrich "
        "via alterlab-openalex; to check the works exist use alterlab-citation-verifier.",
    )


def cmd_projects(author_id: str) -> dict[str, Any]:
    try:
        page = _author_page(PROJECTS_PATH, author_id)
    except NetworkUnavailable as exc:
        return _unavailable(
            "projects",
            str(exc),
            f"Open {urljoin(BASE, PROJECTS_PATH)}?authorId={author_id} in a browser.",
        )
    return _envelope(
        "ok",
        "projects",
        author_id=author_id,
        raw_text_excerpt=_visible_text(page)[:2000],
        note="Portal-listed research projects (AB / TÜBİTAK / araştırma …) from the "
        "'Projeler' tab. Selectors are unverified — read the project rows from "
        "raw_text_excerpt rather than asserting fields.",
    )


def cmd_theses(author_id: str) -> dict[str, Any]:
    try:
        page = _author_page(THESES_PATH, author_id)
    except NetworkUnavailable as exc:
        return _unavailable(
            "theses",
            str(exc),
            f"Open {urljoin(BASE, THESES_PATH)}?authorId={author_id} in a browser.",
        )
    return _envelope(
        "ok",
        "theses",
        author_id=author_id,
        raw_text_excerpt=_visible_text(page)[:2000],
        note="Supervised theses (danışmanlık). For thesis FULL TEXT/abstract use "
        "alterlab-yok-tez (Ulusal Tez Merkezi), not this portal.",
    )


def _visible_text(html_text: str) -> str:
    """Collapse a page to visible text for the caller to read fields from."""
    if _HAS_BS4:
        soup = BeautifulSoup(html_text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    # stdlib: strip tags crudely
    no_scripts = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html_text)
    stripped = re.sub(r"(?s)<[^>]+>", " ", no_scripts)
    return re.sub(r"\s+", " ", html.unescape(stripped)).strip()


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="search academics by name")
    p_search.add_argument("query", help="Ad Soyad (full name; UTF-8, diacritics OK)")

    p_profile = sub.add_parser("profile", help="fetch a profile by authorId")
    p_profile.add_argument("--author-id", required=True)

    p_pubs = sub.add_parser("pubs", help="fetch portal-listed publications by authorId")
    p_pubs.add_argument("--author-id", required=True)
    p_pubs.add_argument("--pub-type", default="", help="pubType filter token (default: all)")

    p_projects = sub.add_parser("projects", help="fetch portal-listed projects by authorId")
    p_projects.add_argument("--author-id", required=True)

    p_theses = sub.add_parser("theses", help="fetch supervised theses by authorId")
    p_theses.add_argument("--author-id", required=True)

    for p in (parser, p_search, p_profile, p_pubs, p_projects, p_theses):
        p.add_argument(
            "--json",
            action="store_true",
            help="emit compact single-line JSON (default: pretty, indented JSON)",
        )

    args = parser.parse_args(argv)

    if args.command == "search":
        result = cmd_search(args.query)
    elif args.command == "profile":
        result = cmd_profile(args.author_id)
    elif args.command == "pubs":
        result = cmd_pubs(args.author_id, args.pub_type)
    elif args.command == "projects":
        result = cmd_projects(args.author_id)
    elif args.command == "theses":
        result = cmd_theses(args.author_id)
    else:  # pragma: no cover
        parser.error(f"unknown command {args.command!r}")
        return 2

    # --json => compact single-line; default => pretty, indented (human-readable).
    if args.json:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
