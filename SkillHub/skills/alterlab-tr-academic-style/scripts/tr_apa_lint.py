#!/usr/bin/env python3
"""Lint a Turkish manuscript for common Türkçe APA 7 mechanical errors.

Catches the high-frequency mistakes that happen when an English APA 7 draft is
translated to Turkish, or when a journal's Türkçe APA 7 conventions are applied
inconsistently:

  * EN-ABBR  - English abbreviation left in (et al., n.d., p./pp., Trans.,
               as cited in, Retrieved from) where the Turkish form is expected.
  * VE-ARK   - the "et al." form is mixed: both `ve ark.` and `vd.` appear, so
               the manuscript is inconsistent (pick one).
  * NARRATIVE-AMP - an ampersand `&` used in apparent narrative prose
               ("Yılmaz & Demir (2020) buldu") where APA wants the word `ve`.
               (`&` is allowed inside parenthetical cites and the reference list.)
  * ASCII-DIA - a likely Turkish word written with ASCII where a diacritic
               belongs (oz/abstract metadata must keep İ/ı, Ş/ş, Ğ/ğ, Ç/ç,
               Ö/ö, Ü/ü). Heuristic, reported as a warning only.

This is a *mechanical* linter — it flags patterns for human review, not a proof
of correctness. It is stdlib-only: no network, no third-party deps. Reads a
file path or `-`/stdin; prints a human table or `--json`. The page-abbreviation
(`p.`/`pp.`) rule ignores matches inside a URL/DOI (e.g. `.../p.2020.04`), but a
heuristic linter can still produce occasional false positives — review hits, do
not auto-apply.

Usage:
    uv run python tr_apa_lint.py manuscript.md
    uv run python tr_apa_lint.py manuscript.tex --json
    cat draft.md | uv run python tr_apa_lint.py -
    uv run python tr_apa_lint.py --self-test   # offline regression fixtures
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass


@dataclass
class Finding:
    line: int
    col: int
    code: str
    severity: str  # "error" | "warning"
    match: str
    message: str


# English abbreviations that should be their Turkish APA 7 equivalents.
# Each: (compiled pattern, suggested Turkish form). Word-boundaried and
# case-sensitive where the Latin abbreviation is conventionally cased.
EN_ABBR_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bet al\.?"), "ve ark. / vd."),
    (re.compile(r"\bn\.\s?d\."), "t.y. (tarih yok)"),
    (re.compile(r"\bpp\.\s*\d"), "ss. (sayfa aralığı)"),
    (re.compile(r"(?<![/.\w])\bp\.\s*\d"), "s. (sayfa)"),
    (re.compile(r"\bTrans\."), "Çev. (çeviren)"),
    (re.compile(r"\bas cited in\b", re.IGNORECASE), "aktaran"),
    (re.compile(r"\bRetrieved from\b", re.IGNORECASE), "Erişim adresi"),
]

VE_ARK = re.compile(r"\bve ark\.")
VD = re.compile(r"\bvd\.")

# `&` immediately preceded by a word and followed by a capitalized word and then
# a "(YYYY)" — i.e. narrative "Surname & Surname (2020)" where APA wants "ve".
NARRATIVE_AMP = re.compile(r"\b[\wçğıöşüÇĞİÖŞÜ]+\s*&\s*[A-ZÇĞİÖŞÜ][\wçğıöşü]+\s*\(\d{4}")

# Heuristic ASCII-diacritic words: common Turkish academic tokens that, written
# in pure ASCII, almost certainly dropped a diacritic. Kept deliberately small
# and high-precision to avoid false positives on English text.
ASCII_DIACRITIC_WORDS = {
    "oz": "öz",
    "yontem": "yöntem",
    "ogrenme": "öğrenme",
    "universite": "üniversite",
    "universitesi": "üniversitesi",
    "cev": "çev",
    "calisma": "çalışma",
    "anahtar kelimeler": "anahtar kelimeler (ensure ş/ğ etc. intact)",
}
ASCII_WORD_RE = re.compile(r"[A-Za-z]+")

# A parenthetical span — `&` inside one of these is allowed, so we suppress the
# NARRATIVE-AMP check when the match sits inside parentheses on the line.


def _in_parentheses(line: str, idx: int) -> bool:
    """True if character index `idx` sits inside a (...) span on this line."""
    depth = 0
    for i, ch in enumerate(line):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if i == idx:
            return depth > 0
    return False


def lint_text(text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()

    saw_ve_ark = False
    saw_vd = False

    for lineno, line in enumerate(lines, start=1):
        # English abbreviations.
        for pattern, suggestion in EN_ABBR_RULES:
            for m in pattern.finditer(line):
                findings.append(
                    Finding(
                        line=lineno,
                        col=m.start() + 1,
                        code="EN-ABBR",
                        severity="error",
                        match=m.group(0),
                        message=f"English abbreviation; Türkçe APA 7 uses: {suggestion}",
                    )
                )

        # Track et-al-form usage for the consistency check.
        if VE_ARK.search(line):
            saw_ve_ark = True
        if VD.search(line):
            saw_vd = True

        # Narrative ampersand (skip if the `&` is inside parentheses).
        for m in NARRATIVE_AMP.finditer(line):
            amp_idx = line.find("&", m.start())
            if amp_idx != -1 and _in_parentheses(line, amp_idx):
                continue
            findings.append(
                Finding(
                    line=lineno,
                    col=m.start() + 1,
                    code="NARRATIVE-AMP",
                    severity="error",
                    match=m.group(0),
                    message="`&` in narrative prose — use the word `ve` (the `&` "
                    "belongs only in parenthetical cites and the reference list)",
                )
            )

        # ASCII-diacritic heuristic (warning only).
        lower = line.lower()
        for ascii_form, correct in ASCII_DIACRITIC_WORDS.items():
            if " " in ascii_form:
                idx = lower.find(ascii_form)
                if idx != -1:
                    findings.append(
                        Finding(
                            line=lineno,
                            col=idx + 1,
                            code="ASCII-DIA",
                            severity="warning",
                            match=line[idx : idx + len(ascii_form)],
                            message=f"Possible dropped Turkish diacritic; expected: {correct}",
                        )
                    )
                continue
            for m in ASCII_WORD_RE.finditer(line):
                if m.group(0).lower() == ascii_form:
                    findings.append(
                        Finding(
                            line=lineno,
                            col=m.start() + 1,
                            code="ASCII-DIA",
                            severity="warning",
                            match=m.group(0),
                            message=f"Possible dropped Turkish diacritic; expected: {correct}",
                        )
                    )

    # Whole-document consistency: both et-al forms present.
    if saw_ve_ark and saw_vd:
        findings.append(
            Finding(
                line=0,
                col=0,
                code="VE-ARK",
                severity="error",
                match="ve ark. + vd.",
                message="Both `ve ark.` and `vd.` are used — pick ONE et-al form "
                "and apply it consistently across the manuscript.",
            )
        )

    findings.sort(key=lambda f: (f.line, f.col))
    return findings


def run_self_test() -> int:
    """Offline, deterministic regression fixtures (no network, no file I/O)."""
    cases: list[tuple[str, set[str]]] = [
        # (line, expected EN-ABBR/NARRATIVE-AMP codes — subset must appear)
        # Leftover English translator abbreviation in a realistic APA context.
        # Regression guard: the old `\bTrans\.\b` pattern never matched these.
        ("Smith, J. (2019). Bir kitap (S. Demir, Trans.). Yayınevi.", {"EN-ABBR"}),
        ("(S. Demir, Trans.)", {"EN-ABBR"}),
        ("Demir, Trans.).", {"EN-ABBR"}),
        # Other English abbreviations that must still fire.
        ("Kaya et al. (2019) buldu.", {"EN-ABBR"}),
        ("Yazar, A. (n.d.). Başlık.", {"EN-ABBR"}),
        ("Bakınız p. 42 ve pp. 10-12.", {"EN-ABBR"}),
        ("Yılmaz & Demir (2020) buldu.", {"NARRATIVE-AMP"}),
        # Clean lines that must NOT flag:
        # `Trans.` substring inside a longer word is not the abbreviation.
        ("Transkript verileri analiz edildi.", set()),
        # `p.NNNN` inside a DOI/URL must not be read as a page abbreviation.
        ("https://doi.org/10.1016/p.2020.04.011 adresinden erişildi.", set()),
        # `&` inside a parenthetical cite is allowed.
        ("Bu bulgu doğrulandı (Yılmaz & Demir, 2020).", set()),
    ]
    ok = True
    for text, expected in cases:
        codes = {f.code for f in lint_text(text)}
        passed = expected.issubset(codes) if expected else not codes
        ok = ok and passed
        print(
            f"[{'PASS' if passed else 'FAIL'}] expected={sorted(expected) or 'no-flags'} "
            f"got={sorted(codes) or 'no-flags'} :: {text[:60]}"
        )
    print("\nSELF-TEST:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "path",
        nargs="?",
        help="manuscript file (.md/.txt/.tex) or '-' for stdin",
    )
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run offline regression fixtures and exit",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if args.path is None:
        parser.error("provide a manuscript path (or '-' for stdin), or use --self-test")

    try:
        text = read_input(args.path)
    except OSError as exc:
        print(f"error: cannot read {args.path!r}: {exc}", file=sys.stderr)
        return 2

    findings = lint_text(text)
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")

    if args.json:
        print(
            json.dumps(
                {
                    "tool": "alterlab-tr-academic-style/tr_apa_lint.py",
                    "version": "1.0.0",
                    "summary": {
                        "total": len(findings),
                        "errors": errors,
                        "warnings": warnings,
                        "verdict": "PASS" if errors == 0 else "FAIL",
                    },
                    "findings": [asdict(f) for f in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        if not findings:
            print("PASS — no Türkçe APA 7 mechanical issues found.")
        else:
            for f in findings:
                loc = f"{f.line}:{f.col}" if f.line else "doc"
                print(f"[{f.severity.upper():7}] {loc:>7}  {f.code:<13} {f.match!r}  — {f.message}")
            print(f"\n{errors} error(s), {warnings} warning(s).")

    # Non-zero exit on any error so the linter is usable in a pipeline.
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
