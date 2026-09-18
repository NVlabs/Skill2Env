#!/usr/bin/env python3
"""journal_info.py — Fetch a DergiPark journal's aim/scope and self-declared indexes.

Given a journal slug, this fetches the open journal pages:
  /{lang}/pub/{slug}/aim-and-scope   -> scope text (verified 200, 2026-06-06)
  /{lang}/pub/{slug}/indexes         -> the list of indexing databases (verified 200)

CRITICAL CAVEAT (surfaced in output): the /indexes page is SELF-DECLARED by the
journal and is NOT verified by DergiPark. DergiPark = hosting (no quality gate);
TR Dizin = a SEPARATE ULAKBİM national citation index requiring its own
application. Presence on DergiPark does NOT imply TR Dizin indexing. To confirm
real indexing status, cross-check authoritative sources:
  - TR Dizin national index:  https://search.trdizin.gov.tr  (or the alterlab-trdizin skill)
  - DOAJ open-access status:  https://doaj.org/api/v4/search/journals/{query}

This script only RETRIEVES and reports the journal's own pages plus the cross-check
pointers; it makes no indexing claim of its own.

Usage:
  uv run python journal_info.py SLUG [--lang en|tr] [--json]
  uv run python journal_info.py mulkiye --lang en

Design: NO API key. Prefers ``requests`` if installed, else stdlib ``urllib``.
HTML text extraction via ``html.parser`` (stdlib). Exit 0 = ran; 1 = fetch error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from html.parser import HTMLParser
from typing import Any, Optional

SITE_ROOT = "https://dergipark.org.tr"
TRDIZIN_SEARCH = "https://search.trdizin.gov.tr"
DOAJ_API = "https://doaj.org/api/v4/search/journals/"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "alterlab-dergipark/1.0.0 (+https://github.com/AlterLab-IEU/AlterLab-Academic-Skills)"
)
HTTP_TIMEOUT = 30
RETRIES = 2
BACKOFF = 1.5

try:  # pragma: no cover
    import requests as _requests  # type: ignore

    _HAS_REQUESTS = True
except Exception:  # pragma: no cover
    _requests = None
    _HAS_REQUESTS = False

import urllib.error
import urllib.parse
import urllib.request


class NetworkUnavailable(Exception):
    pass


def _http_get_text(url: str) -> tuple[int, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html"}
    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES + 1):
        try:
            if _HAS_REQUESTS:
                resp = _requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
                return resp.status_code, resp.text
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:  # 404 etc. still informative
            return e.code, ""
        except (urllib.error.URLError, OSError) as e:
            last_exc = NetworkUnavailable(str(e))
        except Exception as e:  # pragma: no cover
            last_exc = e
        if attempt < RETRIES:
            time.sleep(BACKOFF * (attempt + 1))
    if isinstance(last_exc, NetworkUnavailable):
        raise last_exc
    raise RuntimeError(str(last_exc) if last_exc else "unknown error")


class _TextExtractor(HTMLParser):
    """Collect visible text, skipping script/style; also collect <a> hrefs."""

    _SKIP = {"script", "style", "noscript"}

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self.chunks: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag in self._SKIP:
            self._skip_depth += 1
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.links.append(v)

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            t = data.strip()
            if t:
                self.chunks.append(t)


def _extract_text(html: str) -> str:
    p = _TextExtractor()
    p.feed(html)
    text = " ".join(p.chunks)
    return re.sub(r"\s+", " ", text).strip()


def fetch_journal_info(slug: str, lang: str = "en") -> dict[str, Any]:
    base = f"{SITE_ROOT}/{lang}/pub/{slug}"
    scope_status, scope_html = _http_get_text(f"{base}/aim-and-scope")
    idx_status, idx_html = _http_get_text(f"{base}/indexes")

    scope_text = _extract_text(scope_html) if scope_status == 200 else ""
    idx_text = _extract_text(idx_html) if idx_status == 200 else ""

    return {
        "slug": slug,
        "journal_url": base,
        "aim_and_scope": {
            "url": f"{base}/aim-and-scope",
            "status": scope_status,
            "text": scope_text[:4000],
        },
        "self_declared_indexes": {
            "url": f"{base}/indexes",
            "status": idx_status,
            "text": idx_text[:4000],
            "DISCLAIMER": (
                "Self-declared by the journal; NOT verified by DergiPark. "
                "DergiPark hosting does not imply TR Dizin indexing."
            ),
        },
        "verify_indexing_against": {
            "tr_dizin": f"{TRDIZIN_SEARCH} (national citation index; or use the alterlab-trdizin skill)",
            "doaj_open_access": f"{DOAJ_API}{urllib.parse.quote(slug)}",
        },
    }


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("slug")
    p.add_argument("--lang", default="en", choices=["en", "tr"])
    p.add_argument("--json", action="store_true", help="emit full JSON (default)")
    args = p.parse_args(argv)

    try:
        info = fetch_journal_info(args.slug, args.lang)
    except NetworkUnavailable as e:
        print(json.dumps({"error": "network_unavailable", "detail": str(e)}), file=sys.stderr)
        return 1
    except Exception as e:
        print(json.dumps({"error": "fetch_error", "detail": str(e)}), file=sys.stderr)
        return 1

    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
