#!/usr/bin/env python3
"""yok_tez_query.py — build YÖK Ulusal Tez Merkezi search args and format citations.

This is an OFFLINE, deterministic helper. It does **not** call any network
endpoint — there is no official public API for tez.yok.gov.tr, and the live
search runs through the `saidsurucu/yoktez-mcp` connector (local `uvx` or hosted
https://yoktezmcp.fastmcp.app/mcp). This script's job is to turn a plain topic
description into:

  1. a normalized query spec applying the verified search-craft rules
     (Turkish root forms, ve/veya/içermesin booleans, paired TR+EN queries,
     field targeting, permission_status=Tümü for originality checks), and
  2. the exact `search_yok_tez_detailed` argument dict to pass to yoktez-mcp.

It also formats a Türkçe APA-7 thesis citation (and optional BibTeX) from a
record dict, mapping the YÖK Tez No to APA's Yayın No.

Stdlib only — runs in a bare `uv run` env. No third-party deps.

Usage:
  # Build search args for an originality / supervision check (TR+EN paired):
  uv run python yok_tez_query.py search \
      --topic-tr "sanal prodüksiyon ve sinema" \
      --topic-en "virtual production ve film" \
      --thesis-type Doktora --year-start 2015 --year-end 2026 --originality

  # Format a citation from a record JSON (stdin or --record):
  echo '{"author":"Yılmaz, A.","year":2021,
         "title":"Sanal prodüksiyonun sinematografiye etkileri",
         "tez_no":"654321","thesis_type":"Doktora tezi",
         "university":"İzmir Ekonomi Üniversitesi","permission":"İzinli"}' \
    | uv run python yok_tez_query.py cite --bibtex
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict

# The verified search-form field -> yoktez-mcp search_yok_tez_detailed parameter.
FIELD_PARAM = {
    "title": "thesis_title",
    "author": "author_name",
    "advisor": "advisor_name",
    "subject": "subject_headings",
    "keyword": "index_terms",
    "abstract": "abstract_text",
    "tez_no": "thesis_number",
    "university": "university_name",
}

# Turkish boolean operators (NOT AND/OR/NOT).
TR_BOOLEAN = {"and": "ve", "or": "veya", "not": "içermesin"}

# Topic search targets all three high-recall fields per the search-craft rules.
TOPIC_FIELDS = ("subject_headings", "thesis_title", "abstract_text")


@dataclass
class QuerySpec:
    """One concrete yoktez-mcp search call."""

    label: str
    args: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)


def _warn_inflected(term: str) -> list:
    """Flag obviously inflected Turkish tokens; suggest searching the root.

    Heuristic only (no morphological analyzer in stdlib): common possessive /
    genitive / dative suffixes that almost always mean the engine's auto-stemmer
    would do better on a shorter root.
    """
    notes = []
    suffixes = ("liğin", "lığın", "lığı", "liği", "nin", "nın", "nün", "nun",
                "lerin", "ların", "leşmenin", "laşmanın")
    for tok in term.split():
        low = tok.lower()
        if any(low.endswith(s) for s in suffixes) and len(low) > 7:
            notes.append(
                f"'{tok}' looks inflected — consider the root form so Turkish "
                f"auto-stemming widens the match."
            )
    return notes


def build_search(args: argparse.Namespace) -> dict:
    """Return paired TR/EN QuerySpecs plus a merged-output instruction."""
    specs: list[QuerySpec] = []
    common: dict = {}
    if args.thesis_type:
        common["thesis_type"] = args.thesis_type
    if args.year_start:
        common["year_start"] = args.year_start
    if args.year_end:
        common["year_end"] = args.year_end
    if args.advisor:
        common["advisor_name"] = args.advisor
    if args.university:
        common["university_name"] = args.university
    if args.language:
        common["language"] = args.language

    # Originality checks MUST include İzinsiz (restricted) theses — they are
    # still prior art. "Tümü" = All in the permission_status filter.
    if args.originality:
        common["permission_status"] = "Tümü"

    def make_topic_spec(label: str, topic: str | None) -> QuerySpec | None:
        if not topic:
            return None
        a = dict(common)
        # Apply the same topic string to the three high-recall fields.
        for f in TOPIC_FIELDS:
            a[f] = topic
        notes = _warn_inflected(topic)
        if any(op in f" {topic} " for op in (" and ", " or ", " not ")):
            notes.append(
                "Use Turkish booleans ve/veya/içermesin, not AND/OR/NOT."
            )
        return QuerySpec(label=label, args=a, notes=notes)

    s_tr = make_topic_spec("turkish", args.topic_tr)
    s_en = make_topic_spec("english", args.topic_en)
    for s in (s_tr, s_en):
        if s:
            specs.append(s)

    if args.advisor and not specs:
        # Advisor-only discovery (no topic) is a single query.
        specs.append(QuerySpec(label="advisor", args=dict(common)))

    out = {
        "tool": "alterlab-yok-tez/yok_tez_query.py",
        "mode": "search",
        "connector": "saidsurucu/yoktez-mcp :: search_yok_tez_detailed",
        "queries": [asdict(s) for s in specs],
        "merge_instruction": (
            "Run each query via search_yok_tez_detailed, then MERGE and DEDUPE "
            "on thesis_number (Tez No). Return newest-first "
            "{tez_no, year, university, advisor, title, permission}."
        ),
        "boolean_operators": TR_BOOLEAN,
    }
    if not args.topic_en and args.topic_tr:
        out.setdefault("warnings", []).append(
            "Only a Turkish query was given. English terms hit only the English "
            "fields — add --topic-en to avoid missing English-language theses."
        )
    if args.originality:
        out.setdefault("warnings", []).append(
            "Originality check: permission_status=Tümü so İzinsiz (restricted) "
            "theses surface. This is registry coverage, NOT a plagiarism / "
            "text-similarity score."
        )
    return out


def format_apa7(rec: dict) -> str:
    """Türkçe APA-7 thesis citation, switching on permission state."""
    author = rec.get("author", "Soyad, A.")
    year = rec.get("year", "Yıl")
    title = rec.get("title", "Tez başlığı")
    ttype = rec.get("thesis_type", "tez")
    univ = rec.get("university", "Üniversite Adı")
    tez_no = rec.get("tez_no")
    permission = str(rec.get("permission", "")).lower()

    published = permission.startswith("izinli") or permission.startswith("i̇zinli")
    if published and tez_no:
        # Tez No maps directly to APA Yayın No.
        return (
            f"{author} ({year}). {title} (Yayın No. {tez_no}) "
            f"[{ttype}, {univ}]. YÖK Ulusal Tez Merkezi."
        )
    # Unpublished / restricted form. Turkish APA lowercases the type phrase,
    # e.g. "Yüksek Lisans tezi" -> "yüksek lisans tezi". The search form and the
    # --thesis-type flag use bare labels ("Doktora", "Yüksek Lisans"), so ensure
    # the phrase ends in "tezi" — the template is "[Yayımlanmamış ... tezi]".
    low_type = ttype.lower().strip() if ttype else "tez"
    if not low_type.endswith("tez") and not low_type.endswith("tezi"):
        low_type = f"{low_type} tezi"
    return (
        f"{author} ({year}). {title} "
        f"[Yayımlanmamış {low_type}]. {univ}."
    )


def _ascii_key(s: str) -> str:
    """ASCII-fold a Turkish surname into a safe BibTeX cite key.

    BibTeX cite keys must be ASCII; e.g. 'Yılmaz' -> 'yilmaz', 'Şahin' -> 'sahin'.
    """
    tr_map = str.maketrans({
        "ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g",
        "ç": "c", "Ç": "c", "ö": "o", "Ö": "o", "ü": "u", "Ü": "u",
    })
    folded = s.translate(tr_map).lower()
    return "".join(ch for ch in folded if ch.isascii() and ch.isalnum())


def format_bibtex(rec: dict) -> str:
    ttype = str(rec.get("thesis_type", "")).lower()
    entry = "phdthesis" if "doktora" in ttype or "phd" in ttype else "mastersthesis"
    key = (_ascii_key(str(rec.get("author", "thesis")).split(",")[0])
           or "thesis") + str(rec.get("year", ""))
    note = "YÖK Ulusal Tez Merkezi"
    if rec.get("tez_no"):
        note += f", Tez No. {rec['tez_no']}"
    return (
        f"@{entry}{{{key},\n"
        f"  author = {{{rec.get('author', '')}}},\n"
        f"  title  = {{{rec.get('title', '')}}},\n"
        f"  school = {{{rec.get('university', '')}}},\n"
        f"  year   = {{{rec.get('year', '')}}},\n"
        f"  note   = {{{note}}}\n"
        f"}}"
    )


def cmd_cite(args: argparse.Namespace) -> int:
    if args.record:
        rec = json.loads(args.record)
    else:
        data = sys.stdin.read().strip()
        if not data:
            print("error: no record JSON on stdin or via --record", file=sys.stderr)
            return 2
        rec = json.loads(data)
    print(format_apa7(rec))
    if args.bibtex:
        print()
        print(format_bibtex(rec))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    print(json.dumps(build_search(args), ensure_ascii=False, indent=2))
    return 0


def main(argv: list | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("search", help="build search_yok_tez_detailed args")
    ps.add_argument("--topic-tr", help="Turkish topic query (use ve/veya/içermesin)")
    ps.add_argument("--topic-en", help="English topic query")
    ps.add_argument("--advisor", help="advisor (danışman) name")
    ps.add_argument("--university", help="university name")
    ps.add_argument("--thesis-type", help="e.g. Doktora, Yüksek Lisans")
    ps.add_argument("--year-start", type=int)
    ps.add_argument("--year-end", type=int)
    ps.add_argument("--language", help="e.g. Türkçe, İngilizce")
    ps.add_argument("--originality", action="store_true",
                    help="set permission_status=Tümü so İzinsiz theses surface")
    ps.set_defaults(func=cmd_search)

    pc = sub.add_parser("cite", help="format Türkçe APA-7 / BibTeX from a record")
    pc.add_argument("--record", help="record JSON inline (else read stdin)")
    pc.add_argument("--bibtex", action="store_true", help="also emit BibTeX")
    pc.set_defaults(func=cmd_cite)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
