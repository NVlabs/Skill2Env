#!/usr/bin/env python3
"""dergipark_oai.py — Harvest journal metadata from DergiPark's OAI-PMH endpoint.

DergiPark (https://dergipark.org.tr) is TÜBİTAK ULAKBİM's national journal-hosting
platform. Its single most reliable machine-readable surface is a platform-wide
OAI-PMH 2.0 endpoint. The interactive search page is gated behind a human-
verification challenge, so OAI harvesting is the robust, gate-free path.

Verified live (2026-06-06):
  base URL            https://dergipark.org.tr/api/public/oai/
  protocolVersion     2.0
  repositoryName      DergiPark
  granularity         YYYY-MM-DDThh:mm:ssZ (record <datestamp> seen as YYYY-MM-DD)
  metadataPrefix      oai_dc | oai_etdms | oai_marc | oai_mods
  set scheme          setSpec == journal slug (e.g. set=mulkiye)
  identifier scheme   oai:dergipark.org.tr:article/{id}

CAVEAT: the OAI <datestamp> is the re-index time, NOT the publication date. To
find articles by publication year, harvest then filter on dc:date locally; do not
rely on from/until selective-harvest for publication-date queries.

Subcommands:
  list-journals                       -> ListSets, prints slug<TAB>name pairs
  harvest SLUG [--prefix oai_dc]      -> ListRecords&set=SLUG with resumptionToken paging
  get RECORD_ID [--prefix oai_dc]     -> GetRecord for oai:dergipark.org.tr:article/{id}

Usage:
  uv run python dergipark_oai.py list-journals [--out sets.tsv]
  uv run python dergipark_oai.py harvest mulkiye --prefix oai_dc --max 200 --out recs.json
  uv run python dergipark_oai.py get 10 --prefix oai_dc

Design: NO API key. Prefers ``requests`` if installed, else stdlib ``urllib``.
Pure stdlib XML parsing (xml.etree). Polite User-Agent. Exit 0 = ran; 2 = usage.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import xml.etree.ElementTree as ET
from typing import Any, Iterator, Optional

OAI_BASE = "https://dergipark.org.tr/api/public/oai/"
IDENTIFIER_PREFIX = "oai:dergipark.org.tr:article/"
VALID_PREFIXES = ("oai_dc", "oai_etdms", "oai_marc", "oai_mods")
USER_AGENT = (
    "alterlab-dergipark/1.0.0 (https://github.com/AlterLab-IEU/"
    "AlterLab-Academic-Skills; mailto:alterlab.ieu@gmail.com)"
)
HTTP_TIMEOUT = 30
RETRIES = 2
BACKOFF = 1.5

NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
}

try:  # pragma: no cover - environment dependent
    import requests as _requests  # type: ignore

    _HAS_REQUESTS = True
except Exception:  # pragma: no cover
    _requests = None
    _HAS_REQUESTS = False

import urllib.error
import urllib.parse
import urllib.request


class NetworkUnavailable(Exception):
    """Raised when a request cannot reach the network (DNS / connection error)."""


class OAIError(Exception):
    """Raised when the endpoint returns an OAI-PMH <error> element."""


def _http_get(params: dict[str, str]) -> str:
    """GET the OAI endpoint with ``params`` and return the raw XML text."""
    url = OAI_BASE + "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": USER_AGENT, "Accept": "application/xml"}
    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES + 1):
        try:
            if _HAS_REQUESTS:
                resp = _requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
                if resp.status_code == 200:
                    return resp.text
                last_exc = OAIError(f"HTTP {resp.status_code} for {url}")
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                    return r.read().decode("utf-8", "replace")
        except (urllib.error.URLError, OSError) as e:  # connection/DNS
            last_exc = NetworkUnavailable(str(e))
        except Exception as e:  # pragma: no cover
            last_exc = e
        if attempt < RETRIES:
            time.sleep(BACKOFF * (attempt + 1))
    if isinstance(last_exc, NetworkUnavailable):
        raise last_exc
    raise OAIError(str(last_exc) if last_exc else "unknown error")


def _check_oai_error(root: ET.Element) -> None:
    err = root.find("oai:error", NS)
    if err is not None:
        code = err.get("code", "unknown")
        raise OAIError(f"OAI error [{code}]: {(err.text or '').strip()}")


def list_journals() -> list[dict[str, str]]:
    """ListSets -> list of {slug, name}. setSpec is the journal slug."""
    out: list[dict[str, str]] = []
    token: Optional[str] = None
    while True:
        params = {"verb": "ListSets"}
        if token:
            params["resumptionToken"] = token
        root = ET.fromstring(_http_get(params))
        _check_oai_error(root)
        for s in root.iterfind(".//oai:set", NS):
            spec = s.findtext("oai:setSpec", default="", namespaces=NS).strip()
            name = s.findtext("oai:setName", default="", namespaces=NS).strip()
            if spec:
                out.append({"slug": spec, "name": name})
        rt = root.find(".//oai:resumptionToken", NS)
        token = (rt.text or "").strip() if rt is not None else ""
        if not token:
            break
    return out


def _parse_dc_record(rec: ET.Element) -> dict[str, Any]:
    """Extract identifier, datestamp, setSpec and dc:* fields from a record."""
    header = rec.find("oai:header", NS)
    identifier = header.findtext("oai:identifier", default="", namespaces=NS).strip() if header is not None else ""
    datestamp = header.findtext("oai:datestamp", default="", namespaces=NS).strip() if header is not None else ""
    setspecs = [e.text.strip() for e in header.iterfind("oai:setSpec", NS)] if header is not None else []
    # The numeric tail. NOTE: the header identifier is echoed as either
    # oai:dergipark.org.tr:article/{id} (ListRecords/ListSets) or
    # oai:dergipark.org.tr:record/{id} (GetRecord) — both observed live; take the tail.
    article_id = identifier.rsplit("/", 1)[-1] if "/" in identifier else ""

    fields: dict[str, list[str]] = {}
    for el in rec.iterfind(".//dc:*", NS):
        tag = el.tag.split("}")[-1]
        val = (el.text or "").strip()
        if val:
            fields.setdefault(tag, []).append(val)

    return {
        "identifier": identifier,
        "article_id": article_id,
        "datestamp": datestamp,  # re-index time, NOT publication date
        "sets": setspecs,
        "title": (fields.get("title") or [""])[0],
        "creators": fields.get("creator", []),
        "date": (fields.get("date") or [""])[0],  # use THIS for publication date
        "identifiers": fields.get("identifier", []),  # canonical /pub URL, izlik, DOI
        "subjects": fields.get("subject", []),
        "language": (fields.get("language") or [""])[0],
        "publisher": (fields.get("publisher") or [""])[0],
        "source": (fields.get("source") or [""])[0],
        "description": (fields.get("description") or [""])[0],
    }


def harvest(slug: str, prefix: str = "oai_dc", max_records: Optional[int] = None) -> Iterator[dict[str, Any]]:
    """ListRecords for one journal set, following resumptionToken until exhausted."""
    if prefix not in VALID_PREFIXES:
        raise ValueError(f"prefix must be one of {VALID_PREFIXES}, got {prefix!r}")
    token: Optional[str] = None
    yielded = 0
    while True:
        if token:
            params = {"verb": "ListRecords", "resumptionToken": token}
        else:
            params = {"verb": "ListRecords", "metadataPrefix": prefix, "set": slug}
        root = ET.fromstring(_http_get(params))
        _check_oai_error(root)
        for rec in root.iterfind(".//oai:record", NS):
            if prefix == "oai_dc":
                yield _parse_dc_record(rec)
            else:
                # For non-DC prefixes return raw XML so callers can parse as needed.
                yield {"raw_xml": ET.tostring(rec, encoding="unicode")}
            yielded += 1
            if max_records is not None and yielded >= max_records:
                return
        rt = root.find(".//oai:resumptionToken", NS)
        token = (rt.text or "").strip() if rt is not None else ""
        if not token:
            break


def get_record(article_id: str, prefix: str = "oai_dc") -> dict[str, Any]:
    """GetRecord for a single article id (the numeric tail of the OAI identifier)."""
    if prefix not in VALID_PREFIXES:
        raise ValueError(f"prefix must be one of {VALID_PREFIXES}, got {prefix!r}")
    identifier = article_id if article_id.startswith(IDENTIFIER_PREFIX) else IDENTIFIER_PREFIX + str(article_id)
    params = {"verb": "GetRecord", "metadataPrefix": prefix, "identifier": identifier}
    root = ET.fromstring(_http_get(params))
    _check_oai_error(root)
    rec = root.find(".//oai:record", NS)
    if rec is None:
        raise OAIError(f"no record returned for {identifier}")
    if prefix == "oai_dc":
        return _parse_dc_record(rec)
    return {"raw_xml": ET.tostring(rec, encoding="unicode")}


def _emit(obj: Any, out: Optional[str]) -> None:
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"wrote {out}", file=sys.stderr)
    else:
        print(text)


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list-journals", help="ListSets: slug<TAB>name pairs")
    pl.add_argument("--out", help="write JSON to file instead of stdout")
    pl.add_argument("--tsv", action="store_true", help="print slug<TAB>name instead of JSON")

    ph = sub.add_parser("harvest", help="ListRecords for a journal set")
    ph.add_argument("slug")
    ph.add_argument("--prefix", default="oai_dc", choices=VALID_PREFIXES)
    ph.add_argument("--max", type=int, default=None, help="stop after N records")
    ph.add_argument("--out", help="write JSON array to file instead of stdout")

    pg = sub.add_parser("get", help="GetRecord for one article id")
    pg.add_argument("article_id")
    pg.add_argument("--prefix", default="oai_dc", choices=VALID_PREFIXES)
    pg.add_argument("--out", help="write JSON to file instead of stdout")

    args = p.parse_args(argv)

    try:
        if args.cmd == "list-journals":
            sets = list_journals()
            if args.tsv and not args.out:
                for s in sets:
                    print(f"{s['slug']}\t{s['name']}")
            else:
                _emit(sets, args.out)
        elif args.cmd == "harvest":
            records = list(harvest(args.slug, args.prefix, args.max))
            _emit(records, args.out)
        elif args.cmd == "get":
            _emit(get_record(args.article_id, args.prefix), args.out)
    except NetworkUnavailable as e:
        print(json.dumps({"error": "network_unavailable", "detail": str(e)}), file=sys.stderr)
        return 1
    except (OAIError, ValueError) as e:
        print(json.dumps({"error": "oai_error", "detail": str(e)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
