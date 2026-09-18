#!/usr/bin/env python3
"""yokatlas_lookup.py — Retrieve YÖK Atlas program & admission statistics.

A thin, reproducible wrapper over ``yokatlas-py`` (>=0.6.0, MIT, Python >=3.10),
which itself wraps the keyless YÖK Atlas JSON API at
``https://yokatlas.yok.gov.tr/api/tercih-kilavuz/``. No API key is used.

Why wrap rather than reimplement: YÖK Atlas migrated to a React SPA + JSON API in
April 2026, breaking every legacy HTML scraper. ``yokatlas-py`` tracks the live
JSON API and normalizes Turkish characters (İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü) for
fuzzy matching, so we depend on it instead of hand-rolling brittle requests.

Subcommands:
  universities                 list all universities ({universiteAdi, universiteId})
  search   [filters]           search programs (SearchFilters)
  program  --kod KILAVUZKODU   fetch one program's multi-year statistics

Run keyless via uv (no global install):
  uv run --with yokatlas-py python yokatlas_lookup.py universities
  uv run --with yokatlas-py python yokatlas_lookup.py search \
      --puan-turu SAY --universite "boğaziçi" --program "bilgisayar" --size 20
  uv run --with yokatlas-py python yokatlas_lookup.py program --kod 102210277

Output: a JSON envelope on stdout —
  {"tool", "operation", "count", "results"}                  on success
  {"tool", "operation", "error", "manual_instructions"}      on failure (exit 1)

GRACEFUL DEGRADATION: if ``yokatlas-py`` is not importable, or the network is
unavailable, the script prints an error envelope with manual instructions and
exits non-zero. It NEVER fabricates statistics.

Exit codes: 0 = succeeded; 1 = could not retrieve (missing dep / network);
2 = bad usage.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

TOOL = "alterlab-yokatlas/yokatlas_lookup.py"
ATLAS_URL = "https://yokatlas.yok.gov.tr"
PUAN_TURU = ("SAY", "SÖZ", "EA", "DİL", "TYT")
UNIVERSITE_TURU = ("DEVLET", "VAKIF")


def _fail(operation: str, error: str, hint: str) -> int:
    """Print a structured error envelope and signal failure (never fabricate)."""
    json.dump(
        {
            "tool": TOOL,
            "operation": operation,
            "error": error,
            "manual_instructions": hint,
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    sys.stdout.write("\n")
    return 1


def _ok(operation: str, results: Any) -> int:
    count = len(results) if isinstance(results, list) else (0 if results is None else 1)
    json.dump(
        {"tool": TOOL, "operation": operation, "count": count, "results": results},
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


def _import_yokatlas():
    """Import yokatlas-py or raise a friendly ImportError."""
    try:
        import yokatlas_py  # noqa: F401  (presence check)
        from yokatlas_py import (  # type: ignore
            get_program,
            list_universities,
            search_programs,
        )
    except Exception as exc:  # pragma: no cover - environment dependent
        raise ImportError(
            "yokatlas-py (>=0.6.0) is required. Run this script with "
            "`uv run --with yokatlas-py python ...`."
        ) from exc
    return search_programs, get_program, list_universities


def _jsonable(obj: Any) -> Any:
    """Best-effort conversion of pydantic models / pages to plain JSON.

    yokatlas-py returns pydantic v2 models and paginated page objects. We avoid
    assuming a specific schema beyond the documented public surface, falling
    back through the common serialization hooks.
    """
    # pydantic v2 model
    for attr in ("model_dump", "dict"):
        fn = getattr(obj, attr, None)
        if callable(fn):
            try:
                return _jsonable(fn())
            except Exception:
                pass
    # paginated page exposing .content
    content = getattr(obj, "content", None)
    if content is not None and not isinstance(obj, (str, bytes, dict)):
        return [_jsonable(x) for x in content]
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(x) for x in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    # last resort: stringify so the envelope stays valid JSON
    return str(obj)


def cmd_universities(_args: argparse.Namespace) -> int:
    op = "universities"
    try:
        _, _, list_universities = _import_yokatlas()
    except ImportError as exc:
        return _fail(op, str(exc), f"Browse {ATLAS_URL} manually, or install yokatlas-py.")
    try:
        unis = list_universities()
    except Exception as exc:  # network / upstream change
        return _fail(
            op,
            f"YÖK Atlas request failed: {exc}",
            f"Check connectivity to {ATLAS_URL} and that yokatlas-py is >=0.6.0.",
        )
    return _ok(op, _jsonable(unis))


def cmd_search(args: argparse.Namespace) -> int:
    op = "search"
    try:
        search_programs, _, _ = _import_yokatlas()
    except ImportError as exc:
        return _fail(op, str(exc), f"Browse {ATLAS_URL} manually, or install yokatlas-py.")

    filters: dict[str, Any] = {}
    if args.puan_turu:
        filters["puan_turu"] = args.puan_turu
    if args.universite:
        filters["universite"] = args.universite
    if args.program:
        filters["program"] = args.program
    if args.il:
        filters["il"] = args.il
    if args.universite_turu:
        filters["universite_turu"] = args.universite_turu
    if args.min_basari_sirasi is not None:
        filters["min_basari_sirasi"] = args.min_basari_sirasi
    if args.max_basari_sirasi is not None:
        filters["max_basari_sirasi"] = args.max_basari_sirasi

    if not filters:
        return _fail(
            op,
            "No filters supplied.",
            "Provide at least one of --puan-turu/--universite/--program/--il/"
            "--universite-turu/--min-basari-sirasi/--max-basari-sirasi.",
        )

    try:
        page = search_programs(filters, size=args.size)
    except Exception as exc:
        return _fail(
            op,
            f"YÖK Atlas search failed: {exc}",
            f"Verify filters and connectivity to {ATLAS_URL}; ensure yokatlas-py >=0.6.0.",
        )
    return _ok(op, _jsonable(page))


def cmd_program(args: argparse.Namespace) -> int:
    op = "program"
    try:
        _, get_program, _ = _import_yokatlas()
    except ImportError as exc:
        return _fail(op, str(exc), f"Browse {ATLAS_URL} manually, or install yokatlas-py.")
    try:
        prog = get_program(args.kod)
    except Exception as exc:
        return _fail(
            op,
            f"YÖK Atlas program lookup failed: {exc}",
            f"Verify the kılavuz kodu and connectivity to {ATLAS_URL}.",
        )
    if prog is None:
        return _fail(
            op,
            f"No program found for kılavuz kodu {args.kod}.",
            "Double-check the guide code; list candidates via the `search` subcommand.",
        )
    return _ok(op, _jsonable(prog))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="yokatlas_lookup.py",
        description=__doc__.split("\n")[0],
    )
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("universities", help="list all universities (id + name)").set_defaults(
        func=cmd_universities
    )

    s = sub.add_parser("search", help="search programs with SearchFilters")
    s.add_argument("--puan-turu", choices=PUAN_TURU, help="score type")
    s.add_argument("--universite", help="university name (fuzzy, Turkish-aware)")
    s.add_argument("--program", help="program name (fuzzy)")
    s.add_argument("--il", help="province (il) name")
    s.add_argument("--universite-turu", choices=UNIVERSITE_TURU, help="DEVLET or VAKIF")
    s.add_argument("--min-basari-sirasi", type=int, help="lower bound of success rank")
    s.add_argument("--max-basari-sirasi", type=int, help="upper bound of success rank")
    s.add_argument("--size", type=int, default=20, help="max results (default 20)")
    s.set_defaults(func=cmd_search)

    g = sub.add_parser("program", help="fetch one program by kılavuz kodu")
    g.add_argument("--kod", type=int, required=True, help="guide code (kılavuz kodu)")
    g.set_defaults(func=cmd_program)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
