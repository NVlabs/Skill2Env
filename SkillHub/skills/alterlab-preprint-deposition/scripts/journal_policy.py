#!/usr/bin/env python3
"""Query the Sherpa Romeo v2 API for a journal's preprint/self-archiving policy.

Sherpa Romeo aggregates publisher open-access policies journal-by-journal. This
helper retrieves a publication record by ISSN (or title) and summarises whether
the *preprint / submitted* version may be archived, plus any conditions. It
NEVER asserts a policy from model memory: with no key or no network it returns a
manual-check instruction instead of a verdict.

Endpoint (verified on v2.sherpa.ac.uk/api): https://v2.sherpa.ac.uk/cgi/retrieve
Requires a free, registered api-key. We send the data (ISSN/title) to Sherpa's
server — nothing else leaves the machine.

Auto-selects an HTTP backend: uses `requests` if installed, else stdlib urllib.

    uv run python scripts/journal_policy.py --issn 1234-5678 --api-key KEY
    uv run python scripts/journal_policy.py --title "Nature Methods" --api-key KEY
    uv run python scripts/journal_policy.py --issn 1234-5678   # no key -> manual instruction
"""
from __future__ import annotations

import argparse
import json
import sys

API_BASE = "https://v2.sherpa.ac.uk/cgi/retrieve"
USER_AGENT = "alterlab-preprint-deposition/1.0 (+https://github.com/AlterLab-IEU)"


class NetworkUnavailable(RuntimeError):
    pass


def _build_filter(issn: str | None, title: str | None) -> str:
    if issn:
        return json.dumps([["issn", "equals", issn]])
    return json.dumps([["title", "contains-word", title]])


def _fetch(url: str, timeout: float) -> dict:
    """GET the URL and parse JSON. Raises NetworkUnavailable on failure."""
    try:
        try:
            import requests  # type: ignore

            resp = requests.get(url, timeout=timeout,
                                headers={"User-Agent": USER_AGENT})
            resp.raise_for_status()
            return resp.json()
        except ImportError:
            import urllib.request

            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
                return json.loads(r.read().decode("utf-8", errors="replace"))
    except Exception as exc:  # noqa: BLE001 - any failure => manual fallback
        raise NetworkUnavailable(str(exc)) from exc


def _manual_instruction(issn, title, reason) -> dict:
    target = f"ISSN {issn}" if issn else f"title '{title}'"
    return {
        "tool": "alterlab-preprint-deposition/journal_policy.py",
        "version": "1.0.0",
        "status": "unverified",
        "reason": reason,
        "manual_instructions": (
            f"Could not verify the preprint policy for {target}. Look it up "
            "manually at https://v2.sherpa.ac.uk/romeo/ or read the publisher's "
            "own preprint/sharing policy page. Do NOT assume a policy."),
    }


def summarise(record: dict) -> dict:
    """Pull the prearchiving (preprint) permission out of a Sherpa record.

    Field names follow the Sherpa Romeo publication object; absent fields are
    reported as 'not stated' rather than guessed.
    """
    policies = record.get("publisher_policy") or record.get("policies") or []
    preprint = {"permitted": "not stated", "conditions": []}
    for pol in policies if isinstance(policies, list) else []:
        perms = pol.get("permitted_oa") or pol.get("permitted") or []
        for perm in perms if isinstance(perms, list) else []:
            versions = perm.get("article_version") or perm.get("version") or []
            if any("submitted" in str(v).lower() for v in versions):
                preprint["permitted"] = "permitted (submitted/preprint version)"
                for cond in (perm.get("conditions") or []):
                    preprint["conditions"].append(str(cond))
                for loc in (perm.get("location", {}) or {}).get(
                        "location_phrase", []) or []:
                    preprint["conditions"].append(f"location: {loc}")
    return preprint


def lookup(issn, title, api_key, timeout) -> dict:
    if not api_key:
        return _manual_instruction(issn, title, "no api-key supplied")
    flt = _build_filter(issn, title)
    url = (f"{API_BASE}?item-type=publication&api-key={api_key}"
           f"&format=Json&limit=1&filter={flt}")
    try:
        data = _fetch(url, timeout)
    except NetworkUnavailable as exc:
        return _manual_instruction(issn, title, f"network/API error: {exc}")

    items = data.get("items") or []
    if not items:
        return {
            "tool": "alterlab-preprint-deposition/journal_policy.py",
            "version": "1.0.0",
            "status": "no_match",
            "query": {"issn": issn, "title": title},
            "manual_instructions": "No Sherpa Romeo publication matched; verify "
                                   "the ISSN/title or read the publisher page.",
        }
    rec = items[0]
    return {
        "tool": "alterlab-preprint-deposition/journal_policy.py",
        "version": "1.0.0",
        "status": "ok",
        "matched_title": rec.get("title", [{}])[0].get("title")
        if isinstance(rec.get("title"), list) else rec.get("title"),
        "issns": rec.get("issns"),
        "preprint_policy": summarise(rec),
        "source": "https://v2.sherpa.ac.uk/romeo/",
        "note": "Confirm conditions (embargo, version, required notice, DOI "
                "link) before posting; see references/journal_policy.md.",
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--issn", help="Journal ISSN, e.g. 1234-5678")
    g.add_argument("--title", help="Journal title (substring/word match)")
    p.add_argument("--api-key", default=None,
                   help="Free Sherpa Romeo v2 api-key. Omit for a manual "
                        "fallback instruction (no policy is asserted).")
    p.add_argument("--timeout", type=float, default=20.0)
    args = p.parse_args(argv)

    report = lookup(args.issn, args.title, args.api_key, args.timeout)
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
