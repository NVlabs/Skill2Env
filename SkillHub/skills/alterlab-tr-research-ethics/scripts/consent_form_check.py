#!/usr/bin/env python3
"""Lint a Turkish informed-consent draft against the TİTCK minimum-content checklist.

Bilgilendirilmiş Gönüllü Olur Formu (informed-consent / onam / olur formu) linter.
Given a draft consent form (Turkish or English, plain text / Markdown), this scans
for each element TİTCK requires (minimum contents updated 29 Mar 2023, see
references/consent_minimum_contents.md) and reports PASS / MISSING per element plus
an overall verdict.

IMPORTANT: a PASS means the checklist *elements are present*, not that the wording
satisfies the committee. This is a completeness aid, never a legal sign-off — the
researcher's own university committee form and decision are authoritative.

Standard library only (no third-party deps) — runs in a bare `uv run` environment.

Usage:
    uv run python consent_form_check.py path/to/olur_formu.md
    uv run python consent_form_check.py -            # read from stdin
    uv run python consent_form_check.py form.md --json --out report.json
    uv run python consent_form_check.py form.md --clinical   # also require clinical-track items

Diacritics are normalized for matching (İ/ı, Ş/ş, Ğ/ğ, Ç/ç, Ö/ö, Ü/ü), so a draft
written with or without Turkish characters is matched the same way.
"""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from typing import List


# --- Element checklist -------------------------------------------------------
# Each element carries Turkish + English keyword variants. An element PASSES when
# at least one variant (ASCII-folded, lowercased substring) is found in the draft.
# Source: references/consent_minimum_contents.md (TİTCK, updated 29 Mar 2023).

@dataclass
class Element:
    id: str
    name_tr: str
    name_en: str
    keywords: List[str]
    clinical_only: bool = False


CHECKLIST: List[Element] = [
    Element("date_version_page", "Tarih, versiyon ve sayfa numarası",
            "Date, version and page numbers",
            ["versiyon", "version", "surum", "sayfa no", "page ", "tarih", "/__"]),
    Element("initials", "Gönüllü parafe (her sayfa)",
            "Volunteer initials per page",
            ["parafe", "initial", "imza alani"], clinical_only=True),
    Element("purpose", "Çalışmanın amacı",
            "Purpose of the study",
            ["amac", "amaci", "purpose", "objective", "aim of"]),
    Element("procedures_duration", "İşlemler ve süre",
            "Procedures and duration",
            ["islem", "yapilacak", "sure", "procedure", "duration", "how long", "ne kadar"]),
    Element("risks", "Öngörülen riskler / rahatsızlıklar",
            "Foreseeable risks / discomforts",
            ["risk", "rahatsiz", "discomfort", "yan etki", "side effect"]),
    Element("benefits", "Beklenen yararlar",
            "Expected benefits",
            ["yarar", "fayda", "benefit"]),
    Element("contact_24h", "24 saat ulaşılabilir iletişim",
            "24-hour contact",
            ["24 saat", "24-hour", "24 hour", "iletisim", "contact", "ulasabilir", "telefon"]),
    Element("voluntary", "Gönüllülük beyanı",
            "Voluntary-participation statement",
            ["gonull", "voluntary", "isteğe bagli", "istege bagli"]),
    Element("withdraw", "İstediği zaman ayrılma hakkı",
            "Right to withdraw at any time",
            ["ayrilabilir", "ayrilma", "withdraw", "cekilebilir", "cekilme", "istediginiz zaman"]),
    Element("no_coercion", "Baskı/zorlama olmadığı beyanı",
            "No-coercion statement",
            ["baski", "zorlama", "no-coercion", "no coercion", "without pressure", "zorla degil"]),
    Element("confidentiality", "Gizlilik / veri kullanımı",
            "Confidentiality / data use",
            ["gizli", "confidential", "veri kullan", "data use", "kvkk", "anonim"]),
    # Clinical-track additions
    Element("insurance", "Sigorta",
            "Insurance",
            ["sigorta", "insurance"], clinical_only=True),
    Element("alternatives", "Alternatif tedaviler",
            "Alternative treatments",
            ["alternatif tedavi", "alternative treatment", "diger tedavi"], clinical_only=True),
    Element("sponsor", "Sponsor / sorumlu araştırmacı",
            "Sponsor / responsible investigator",
            ["sponsor", "sorumlu arastirmaci", "responsible investigator"], clinical_only=True),
]


def fold(text: str) -> str:
    """Lowercase and strip diacritics so Turkish chars match their ASCII base.

    Handles the dotted/dotless-i pair explicitly (İ->i, ı->i) before NFKD folding.
    """
    text = text.replace("İ", "i").replace("I", "i").replace("ı", "i")
    text = text.lower()
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


@dataclass
class Result:
    id: str
    name_tr: str
    name_en: str
    status: str          # "PASS" | "MISSING"
    clinical_only: bool
    matched_on: str = ""


@dataclass
class Report:
    tool: str = "alterlab-tr-research-ethics/consent_form_check.py"
    version: str = "1.0.0"
    clinical_mode: bool = False
    verdict: str = ""
    counts: dict = field(default_factory=dict)
    results: List[Result] = field(default_factory=list)
    disclaimer: str = (
        "Completeness aid only. A PASS means the checklist element is present, "
        "not that its wording satisfies the committee. The institution's own "
        "ethics-committee form and decision are authoritative."
    )


def lint(draft: str, clinical: bool) -> Report:
    folded = fold(draft)
    rep = Report(clinical_mode=clinical)
    for el in CHECKLIST:
        # Skip clinical-only elements unless --clinical was requested.
        if el.clinical_only and not clinical:
            continue
        hit = ""
        for kw in el.keywords:
            if fold(kw) in folded:
                hit = kw
                break
        rep.results.append(Result(
            id=el.id, name_tr=el.name_tr, name_en=el.name_en,
            status="PASS" if hit else "MISSING",
            clinical_only=el.clinical_only, matched_on=hit,
        ))
    passed = sum(1 for r in rep.results if r.status == "PASS")
    missing = sum(1 for r in rep.results if r.status == "MISSING")
    rep.counts = {"checked": len(rep.results), "pass": passed, "missing": missing}
    rep.verdict = "COMPLETE" if missing == 0 else "INCOMPLETE"
    return rep


def render_table(rep: Report) -> str:
    lines = []
    lines.append(f"Consent-form lint — verdict: {rep.verdict} "
                 f"({rep.counts['pass']}/{rep.counts['checked']} elements present)")
    if rep.clinical_mode:
        lines.append("Mode: clinical track (TİTCK clinical-research additions enforced)")
    lines.append("")
    for r in rep.results:
        mark = "PASS   " if r.status == "PASS" else "MISSING"
        lines.append(f"  [{mark}] {r.name_tr} / {r.name_en}")
    if rep.counts["missing"]:
        lines.append("")
        lines.append("MISSING elements must be added before submission:")
        for r in rep.results:
            if r.status == "MISSING":
                lines.append(f"  - {r.name_tr} ({r.name_en})")
    lines.append("")
    lines.append(rep.disclaimer)
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("path", help="Path to the consent draft, or '-' for stdin")
    p.add_argument("--clinical", action="store_true",
                   help="Also require TİTCK clinical-track elements (insurance, alternatives, sponsor, initials)")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    p.add_argument("--out", help="Write the report to this path instead of stdout")
    args = p.parse_args(argv)

    if args.path == "-":
        draft = sys.stdin.read()
    else:
        try:
            with open(args.path, "r", encoding="utf-8") as fh:
                draft = fh.read()
        except OSError as exc:
            print(f"error: cannot read {args.path}: {exc}", file=sys.stderr)
            return 2

    rep = lint(draft, clinical=args.clinical)
    out = json.dumps(_to_dict(rep), ensure_ascii=False, indent=2) if args.json else render_table(rep)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    else:
        print(out)

    # Exit 0 when complete, 1 when elements are missing (useful in CI / make).
    return 0 if rep.verdict == "COMPLETE" else 1


def _to_dict(rep: Report) -> dict:
    d = asdict(rep)
    return d


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
