#!/usr/bin/env python3
"""score_docentlik.py — PARTIAL pre-screen of a publication list against the ÜAK doçentlik gate.

Given a publication list (JSON), this computes the *modelled* objective point
sub-totals for the Turkish associate-professorship (doçentlik) gate set by ÜAK
(Üniversitelerarası Kurul / the Inter-University Council) for the Sağlık
Bilimleri (Health Sciences) field, applies the author-share rule (paylaşım
kuralı), and pass/fail-checks the minimums it CAN compute from a bare
publication list.

IMPORTANT — this is a PARTIAL PRE-SCREEN, not an eligibility scorer.
  The live Sağlık Bilimleri TABLO 10 imposes SEVERAL mandatory minimums
  (asgari koşullar) beyond raw point totals — a national-article / TR Dizin
  minimum, a citation (atıf) minimum, a scientific-meeting (bilimsel toplantı)
  minimum, an education (eğitim-öğretim) minimum, and per-category point caps.
  Those depend on inputs this scorer does NOT collect, so it CANNOT confirm
  eligibility. By design it NEVER emits an "ELIGIBLE" verdict: the best a
  candidate can reach here is `PRESCREEN_PASS_VERIFY_REMAINING`, meaning every
  modelled check passed and a human must still verify the unmodelled minimums
  against the live ÜAK source. The verdict vocabulary is FAIL / PASS-pending.

Design constraints:
- PURE STDLIB. No network, no third-party deps — fully reproducible offline.
- NO FABRICATION. Ships only the verified Sağlık Bilimleri (Health Sciences)
  TABLO 10 table and the minimums corroborated by multiple sources (see
  ../references/uak_criteria.md). For any other field the caller must supply
  that field's table; the script never invents point values. An unknown index
  tier is flagged as unscored, never guessed.
- ÜAK criteria change each application term. Every report carries a
  verify-against-current-period disclaimer and an explicit list of the
  mandatory minimums NOT modelled here.

Author-share rule (paylaşım kuralı), Sağlık TABLO 10:
  1 author             -> 1.0  x face points
  2 authors, lead       -> 0.8  x face points (başlıca yazar)
  2 authors, non-lead   -> 0.5  x face points
  >=3, lead author      -> 0.5  x face points
  >=3, non-lead         -> (0.5 / (N - 1)) x face points

Modelled mandatory minimums (verified — see ../references/uak_criteria.md):
  total points              >= 100   (all scored work)
  post-doctorate points     >=  90   (items with post_doc == true)
  international SCIE/SSCI pts >=  40   (Q1-Q4 article points, post-doctorate)
  lead-author Q articles    >=   3   (Q1-Q4 articles where candidate is lead)

NOT modelled here (require inputs this scorer does not collect — verify by hand):
  national / TR Dizin articles    (>=3 ulusal, >=2 TR Dizin, >=2 başlıca yazar)
  citation (atıf) points          (>= 5, post-doctorate)
  scientific-meeting (bildiri)    (>= 5)
  education / teaching            (>= 2)
  per-category point caps         (thesis-derived, books, citation, project, ...)

Usage:
  uv run python score_docentlik.py INPUT [--field saglik]
                                         [--table TABLE.json]
                                         [--out report.json]
  uv run python score_docentlik.py - < publications.json   # read stdin

INPUT is a JSON object:
  {"field": "saglik", "publications": [
     {"title": "...", "index": "Q1", "authors": 3, "is_lead": true, "post_doc": true}
  ]}

Exit codes: 0 = ran (see JSON summary.verdict); 2 = bad input/usage.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

# --------------------------------------------------------------------------- #
# Bundled, dated criteria. Sağlık Bilimleri (Health Sciences) TABLO 10 only.    #
# Mirror of ../references/uak_criteria.md. Verify against the live ÜAK source   #
# (https://www.uak.gov.tr/) before relying on any output.                       #
# --------------------------------------------------------------------------- #

VERSION = "2.0.0"
TABLE_LAST_VERIFIED = "2026-06-08"

# Index tiers that count as quartile-ranked "Q articles" for the lead-author
# minimum AND as SCIE/SSCI international-article points for the >=40 floor.
# Sağlık: Q1-Q4 all qualify (Q4 included) — verified against the live ÜAK Sağlık
# Bilimleri TABLO 10 (2025 March term): the >=40 international-article points
# come from SCIE/SSCI Q1-Q4 articles, of which >=3 must have the candidate as
# başlıca yazar ("Q4'ler dahil"). Source: uak.gov.tr TABLO 10 + multi-source
# corroboration in ../references/uak_criteria.md.
Q_TIERS = ("Q1", "Q2", "Q3", "Q4")

# field -> {index tier -> face points}
FIELD_TABLES: dict[str, dict[str, int]] = {
    "saglik": {
        "Q1": 30,
        "Q2": 20,
        "Q3": 15,
        "Q4": 10,
        "AHCI": 20,
        "ESCI": 10,
        "TRDizin": 10,
    },
}

# Modelled mandatory minimums (all of these are checkable from a publication
# list; all must pass before the pre-screen can return PASS-pending). Verified
# values — see ../references/uak_criteria.md. Do NOT add a threshold here
# without a verified source.
MIN_TOTAL = 100        # asgari toplam puan
MIN_POST_DOC = 90      # doktora/uzmanlık sonrası asgari puan
MIN_INTL_SCIE = 40     # uluslararası SCIE/SSCI makale asgari puanı (Q1-Q4)
MIN_LEAD_Q = 3         # en az 3 makalede başlıca yazar (Q1-Q4)

# Mandatory minimums the live TABLO 10 also requires but this scorer does NOT
# model (they need inputs a bare publication list does not carry). These are
# emitted in every report so the verdict can never be mistaken for a complete
# eligibility decision. Verified to EXIST in the criteria; exact thresholds are
# stated where multi-source-corroborated, otherwise flagged for hand-verify.
UNMODELLED_MINIMUMS = [
    {
        "id": "national_trdizin_articles",
        "label_tr": "Ulusal makale / TR Dizin asgari koşulu",
        "requirement": (
            "Post-doctorate national articles: at least 3 ulusal makale, of "
            "which at least 2 in TR Dizin, with the candidate başlıca yazar in "
            "at least 2 — verify exact wording against the live TABLO 10."
        ),
        "why_unmodelled": (
            "Requires distinguishing ulusal vs. TR Dizin status and a "
            "başlıca-yazar count per national article; resolve TR Dizin status "
            "with alterlab-trdizin first."
        ),
    },
    {
        "id": "citation_atif",
        "label_tr": "Atıf (citation) asgari koşulu",
        "requirement": "At least 5 citation (atıf) points from post-doctorate work.",
        "why_unmodelled": "Citation counts are not part of the publication list input.",
    },
    {
        "id": "scientific_meeting_bildiri",
        "label_tr": "Bilimsel toplantı (congress) asgari koşulu",
        "requirement": "At least 5 points from scientific-meeting papers (bildiri).",
        "why_unmodelled": "Congress papers are a separate category not in the article list.",
    },
    {
        "id": "education_egitim_ogretim",
        "label_tr": "Eğitim-öğretim asgari koşulu",
        "requirement": "At least 2 points from teaching / education activity.",
        "why_unmodelled": "Teaching activity is not a publication and is not in the input.",
    },
    {
        "id": "category_point_caps",
        "label_tr": "Kategori puan üst sınırları (caps)",
        "requirement": (
            "Per-category point ceilings apply (e.g. thesis-derived publications, "
            "books, citations, projects, theses supervised, patents, awards). "
            "Verify each cap against the live TABLO 10 — this scorer does not "
            "apply them, so a raw point total here may overstate the usable total."
        ),
        "why_unmodelled": (
            "Caps need each item tagged with its TABLO 10 sub-category; the "
            "publication list input does not carry that classification."
        ),
    },
]

DISCLAIMER = (
    "PARTIAL PRE-SCREEN — NOT an eligibility decision. This tool models only "
    "the point-total / international-article / lead-author minimums that are "
    "computable from a publication list; it does NOT model the national-article "
    "(TR Dizin), citation, scientific-meeting, education, and per-category-cap "
    "minimums that the live Sağlık Bilimleri TABLO 10 also requires (see "
    "summary.unmodelled_minimums). It therefore NEVER returns 'ELIGIBLE'. ÜAK "
    "doçentlik criteria change each application term and differ per field — "
    "verify the full TABLO 10 for your field and term at https://www.uak.gov.tr/ "
    "before relying on anything here. The official doçentlik decision is the "
    "jury's, not this tool's."
)


# --------------------------------------------------------------------------- #
# Scoring                                                                       #
# --------------------------------------------------------------------------- #

def share_factor(authors: int, is_lead: bool) -> float:
    """Author-share factor (paylaşım kuralı) for one publication.

    1 author              -> 1.0
    2 authors, lead       -> 0.8   (başlıca yazar)
    2 authors, non-lead   -> 0.5
    >=3, lead             -> 0.5
    >=3, non-lead         -> 0.5 / (authors - 1)
    """
    if authors <= 1:
        return 1.0
    if authors == 2:
        # Başlıca yazar of a 2-author paper gets 0.8; the other author gets 0.5.
        return 0.8 if is_lead else 0.5
    # authors >= 3
    if is_lead:
        return 0.5
    return 0.5 / (authors - 1)


def score_publication(pub: dict, table: dict[str, int]) -> dict:
    """Score one publication; flag it unscorable if its index tier is unknown."""
    title = str(pub.get("title", "")).strip() or "(untitled)"
    index = str(pub.get("index", "")).strip()
    try:
        authors = int(pub.get("authors", 1))
    except (TypeError, ValueError):
        authors = 1
    if authors < 1:
        authors = 1
    is_lead = bool(pub.get("is_lead", False))
    post_doc = bool(pub.get("post_doc", False))

    if index not in table:
        return {
            "title": title,
            "index": index or "(unknown)",
            "authors": authors,
            "is_lead": is_lead,
            "post_doc": post_doc,
            "scorable": False,
            "face_points": None,
            "share_factor": None,
            "scaled": 0.0,
            "counts_lead_q": False,
            "is_scie_ssci": False,
            "note": "unknown index tier — resolve and re-run (do not guess)",
        }

    face = table[index]
    factor = share_factor(authors, is_lead)
    scaled = face * factor
    is_scie_ssci = index in Q_TIERS
    counts_lead_q = is_lead and is_scie_ssci
    return {
        "title": title,
        "index": index,
        "authors": authors,
        "is_lead": is_lead,
        "post_doc": post_doc,
        "scorable": True,
        "face_points": face,
        "share_factor": round(factor, 4),
        "scaled": scaled,
        "counts_lead_q": counts_lead_q,
        "is_scie_ssci": is_scie_ssci,
    }


def _check(value: float, threshold: float) -> dict:
    passed = value >= threshold
    out = {"pass": passed, "value": round(value, 1), "threshold": threshold}
    if not passed:
        out["short"] = round(threshold - value, 1)
    return out


def score(data: dict, table: dict[str, int], field: str) -> dict:
    pubs = data.get("publications", [])
    if not isinstance(pubs, list):
        raise ValueError("'publications' must be a list")

    scored = [score_publication(p, table) for p in pubs]

    total = sum(p["scaled"] for p in scored)
    post_doc_total = sum(p["scaled"] for p in scored if p["post_doc"])
    # International SCIE/SSCI article points (Q1-Q4), counted post-doctorate only
    # — the >=40 floor is a doktora/uzmanlık-sonrası requirement.
    intl_scie_total = sum(
        p["scaled"] for p in scored if p["is_scie_ssci"] and p["post_doc"]
    )
    lead_q = sum(1 for p in scored if p["counts_lead_q"])
    unscored = [p["title"] for p in scored if not p["scorable"]]

    checks = {
        "total_ge_100": _check(total, MIN_TOTAL),
        "post_doc_ge_90": _check(post_doc_total, MIN_POST_DOC),
        "intl_scie_ge_40": _check(intl_scie_total, MIN_INTL_SCIE),
        "lead_q_articles_ge_3": _check(lead_q, MIN_LEAD_Q),
    }
    all_modelled_pass = all(c["pass"] for c in checks.values())

    # The verdict vocabulary deliberately omits "ELIGIBLE". A green output here
    # only means the MODELLED checks pass and the unmodelled minimums must still
    # be verified by a human. A failed modelled check is a definitive FAIL.
    if not all_modelled_pass:
        verdict = "FAIL_MODELLED_CHECK"
    else:
        verdict = "PRESCREEN_PASS_VERIFY_REMAINING"

    verdict_meaning = {
        "FAIL_MODELLED_CHECK": (
            "At least one modelled minimum (total / post-doctorate / "
            "international SCIE/SSCI / lead-author Q) fails — not eligible "
            "regardless of the unmodelled checks."
        ),
        "PRESCREEN_PASS_VERIFY_REMAINING": (
            "All MODELLED minimums pass. NOT a green light — the unmodelled "
            "mandatory minimums (see unmodelled_minimums) and per-category caps "
            "must still be verified by hand against the live TABLO 10. This tool "
            "cannot and does not declare eligibility."
        ),
    }[verdict]

    return {
        "tool": "alterlab-docentlik-eligibility/score_docentlik.py",
        "version": VERSION,
        "field": field,
        "table_last_verified": TABLE_LAST_VERIFIED,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prescreen_only": True,
        "summary": {
            "verdict": verdict,
            "verdict_meaning": verdict_meaning,
            "all_modelled_checks_pass": all_modelled_pass,
            "total_points": round(total, 1),
            "post_doc_points": round(post_doc_total, 1),
            "intl_scie_points": round(intl_scie_total, 1),
            "lead_q_articles": lead_q,
            "unscored_count": len(unscored),
            "checks": checks,
            "unmodelled_minimums": UNMODELLED_MINIMUMS,
        },
        "unscored": unscored,
        "publications": [
            {**p, "scaled": round(p["scaled"], 2)} for p in scored
        ],
        "disclaimer": DISCLAIMER,
    }


# --------------------------------------------------------------------------- #
# I/O                                                                           #
# --------------------------------------------------------------------------- #

def load_input(arg: str) -> dict:
    if arg == "-":
        raw = sys.stdin.read()
    else:
        try:
            with open(arg, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except OSError:
            # Treat the argument itself as inline JSON.
            raw = arg
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"input is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("input JSON must be an object with a 'publications' list")
    return data


def resolve_table(field: str, table_path: str | None) -> dict[str, int]:
    if table_path:
        with open(table_path, "r", encoding="utf-8") as fh:
            table = json.load(fh)
        if not isinstance(table, dict) or not all(
            isinstance(v, (int, float)) for v in table.values()
        ):
            raise ValueError("--table must be a JSON object of {index_tier: points}")
        return {str(k): int(v) for k, v in table.items()}
    if field not in FIELD_TABLES:
        raise ValueError(
            f"no bundled table for field '{field}'. Only '"
            + "', '".join(FIELD_TABLES)
            + "' is shipped (verified). Supply this field's table with --table "
            "from the live ÜAK source — values are NOT invented."
        )
    return FIELD_TABLES[field]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "PARTIAL pre-screen of a publication list against the ÜAK doçentlik "
            "gate (Sağlık Bilimleri). Never emits an ELIGIBLE verdict."
        )
    )
    parser.add_argument("input", help="JSON file, '-' for stdin, or inline JSON")
    parser.add_argument(
        "--field",
        default="saglik",
        help="ÜAK field selector (default: saglik — the only bundled table)",
    )
    parser.add_argument(
        "--table",
        default=None,
        help="path to a {index_tier: points} JSON table for a non-bundled field",
    )
    parser.add_argument("--out", default=None, help="write report JSON to this path")
    args = parser.parse_args(argv)

    try:
        data = load_input(args.input)
        field = str(data.get("field", args.field)).strip() or args.field
        table = resolve_table(field, args.table)
        report = score(data, table, field)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(payload + "\n")
        print(f"wrote {args.out} — verdict: {report['summary']['verdict']}")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
