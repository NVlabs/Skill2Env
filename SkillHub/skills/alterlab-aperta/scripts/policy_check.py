#!/usr/bin/env python3
"""Light reachability probe for the TÜBİTAK Open Science Policy & Aperta sources.

Checks that the three canonical sources this skill relies on are live and, where
relevant, that the page still mentions the expected keywords. It is a *sanity
probe*, not a scraper: it does NOT extract or assert any policy mandate, embargo
figure, or repository feature — those live in references/policy_mandates.md and
references/aperta_repository.md and must be verified by a human against the
current policy PDF.

Emits a JSON report to stdout. Network failures degrade gracefully to a
"status": "unreachable" verdict per source (never silently passes).

Auto-selects an HTTP backend: uses `requests` if installed, else the stdlib
(`urllib`), so it runs in a bare `uv run` environment with zero extra deps.

    uv run python scripts/policy_check.py
    uv run python scripts/policy_check.py --timeout 20
"""
from __future__ import annotations

import argparse
import json
import sys

# Canonical sources (URL, human label, keywords we expect to still be present).
# Keywords are lowercased substrings; PDFs are checked for reachability only.
SOURCES = [
    {
        "id": "policy_pdf",
        "url": "https://tubitak.gov.tr/sites/default/files/tubitak_acik_bilim_politikasi_190316.pdf",
        "label": "TÜBİTAK Açık Bilim Politikası (PDF)",
        "keywords": [],  # binary PDF — reachability only
    },
    {
        "id": "ulakbim_aperta",
        "url": "https://ulakbim.tubitak.gov.tr/en/turkey-open-archive-aperta/",
        "label": "ULAKBİM — Türkiye Açık Arşivi / Aperta",
        "keywords": ["aperta"],
    },
    {
        "id": "aperta_repo",
        "url": "https://aperta.ulakbim.gov.tr/",
        "label": "Aperta repository",
        "keywords": [],  # SPA shell may not expose keywords in raw HTML
    },
]

USER_AGENT = "alterlab-aperta/1.0 (+https://github.com/AlterLab-IEU)"


def _fetch(url: str, timeout: float):
    """Return (status_code, text). Raises on network failure."""
    try:
        import requests  # type: ignore

        resp = requests.get(url, timeout=timeout,
                            headers={"User-Agent": USER_AGENT})
        # resp.text always decodes (apparent-encoding fallback when no charset
        # header). Returning it unconditionally keeps this backend consistent
        # with the urllib branch; gating on resp.encoding would drop the body
        # for charset-less pages and falsely flag keywords as missing.
        return resp.status_code, resp.text
    except ImportError:
        import urllib.request

        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
            raw = r.read()
            try:
                text = raw.decode("utf-8", errors="replace")
            except Exception:
                text = ""
            return getattr(r, "status", 200), text


def probe(source: dict, timeout: float) -> dict:
    url = source["url"]
    result = {"id": source["id"], "label": source["label"], "url": url}
    try:
        status, text = _fetch(url, timeout)
    except Exception as exc:  # noqa: BLE001 — any network error -> unreachable
        result.update(status="unreachable", http_status=None,
                      detail=f"{type(exc).__name__}: {exc}")
        return result

    reachable = 200 <= int(status) < 400
    low = (text or "").lower()
    missing = [k for k in source["keywords"] if k not in low]
    if not reachable:
        result.update(status="error", http_status=status,
                      detail=f"HTTP {status}")
    elif missing:
        result.update(status="reachable_keywords_missing", http_status=status,
                      detail=f"Missing expected keyword(s): {missing}")
    else:
        result.update(status="ok", http_status=status,
                      detail="Reachable; expected keywords present"
                      if source["keywords"] else "Reachable")
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--timeout", type=float, default=15.0,
                   help="Per-request timeout in seconds (default 15)")
    args = p.parse_args(argv)

    results = [probe(s, args.timeout) for s in SOURCES]
    any_unreachable = any(r["status"] in ("unreachable", "error") for r in results)
    report = {
        "tool": "alterlab-aperta/policy_check.py",
        "note": "Reachability/keyword sanity probe only — does NOT assert any "
                "policy mandate. Verify mandates against the current policy PDF.",
        "all_ok": not any_unreachable,
        "sources": results,
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
