#!/usr/bin/env python3
"""aol_matrix.py — Validate a curriculum-to-outcome (Assurance-of-Learning) matrix.

A program AoL package maps each required course to the program learning outcomes
(AACSB competency goals / ABET student outcomes) it covers, recording a coverage
level per cell — commonly I (Introduced) / R (Reinforced) / M (Mastered), with
M or A marking an assessment point. A peer-review team flags two structural
problems immediately:

  * an outcome that NO course covers (orphan outcome), and
  * an outcome that is covered but never ASSESSED (only Introduced/Reinforced,
    no M/A cell) — there is no place data is collected for it.

This helper checks the matrix for exactly those structural/coverage issues so the
user does not have to eyeball it. It checks STRUCTURE and COVERAGE only — it makes
no judgment about whether the pedagogy or the assessment design is sound; that
stays with the faculty. It does NO network I/O and depends only on the Python
standard library.

Input CSV layout (see ../references/aol_templates.md):
  * a first column named ``course`` (case-insensitive), and
  * one column per outcome (header = the outcome id, e.g. PLO1 / SO3).
  * cells hold coverage codes (I, R, M, A) or are blank.

Example:
  course,PLO1,PLO2,PLO3,PLO4
  BUS101,I,I,,
  BUS480,M,M,M,M

Usage:
  uv run python aol_matrix.py matrix.csv
  uv run python aol_matrix.py matrix.csv --assessed-levels M,A --json
  uv run python aol_matrix.py - < matrix.csv            # read from stdin

Exit codes:
  0 = matrix parsed and every outcome is covered AND assessed (verdict OK)
  1 = matrix parsed but coverage gaps were found (verdict GAPS)
  2 = bad/missing arguments or unreadable/empty CSV
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from dataclasses import dataclass, field

COURSE_COL = "course"


@dataclass
class OutcomeReport:
    outcome: str
    covered: bool
    assessed: bool
    level_counts: dict[str, int] = field(default_factory=dict)
    courses_assessing: list[str] = field(default_factory=list)


def _read_rows(path: str) -> tuple[list[dict[str, str]], list[str]]:
    if path == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(path, encoding="utf-8-sig", newline="") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"error: cannot read {path!r}: {exc}", file=sys.stderr)
            raise SystemExit(2)
    if not text.strip():
        print("error: input CSV is empty", file=sys.stderr)
        raise SystemExit(2)
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        print("error: input CSV has no header row", file=sys.stderr)
        raise SystemExit(2)
    return list(reader), reader.fieldnames


def _resolve_course_col(fieldnames: list[str]) -> str:
    for name in fieldnames:
        if name and name.strip().lower() == COURSE_COL:
            return name
    print(
        f"error: no {COURSE_COL!r} column found; headers were {fieldnames!r}",
        file=sys.stderr,
    )
    raise SystemExit(2)


def analyze(
    rows: list[dict[str, str]],
    fieldnames: list[str],
    assessed_levels: set[str],
) -> dict:
    course_col = _resolve_course_col(fieldnames)
    outcome_cols = [c for c in fieldnames if c and c != course_col]
    if not outcome_cols:
        print("error: no outcome columns found beside the course column", file=sys.stderr)
        raise SystemExit(2)

    reports: list[OutcomeReport] = []
    orphan_courses: list[str] = []

    # course-level: any coverage at all?
    for row in rows:
        course = (row.get(course_col) or "").strip()
        if not course:
            continue
        if not any((row.get(c) or "").strip() for c in outcome_cols):
            orphan_courses.append(course)

    for col in outcome_cols:
        counts: dict[str, int] = {}
        assessing: list[str] = []
        for row in rows:
            course = (row.get(course_col) or "").strip()
            code = (row.get(col) or "").strip().upper()
            if not code:
                continue
            counts[code] = counts.get(code, 0) + 1
            if code in assessed_levels and course:
                assessing.append(course)
        covered = bool(counts)
        assessed = bool(assessing)
        reports.append(
            OutcomeReport(
                outcome=col,
                covered=covered,
                assessed=assessed,
                level_counts=counts,
                courses_assessing=assessing,
            )
        )

    gaps = [r.outcome for r in reports if not (r.covered and r.assessed)]
    verdict = "OK" if not gaps else "GAPS"
    return {
        "tool": "alterlab-accreditation-aol/aol_matrix.py",
        "version": "1.0.0",
        "summary": {
            "courses": sum(1 for row in rows if (row.get(course_col) or "").strip()),
            "outcomes": len(outcome_cols),
            "assessed_levels": sorted(assessed_levels),
            "verdict": verdict,
            "outcomes_with_gaps": gaps,
            "orphan_courses": orphan_courses,
        },
        "outcomes": [
            {
                "outcome": r.outcome,
                "covered": r.covered,
                "assessed": r.assessed,
                "level_counts": r.level_counts,
                "courses_assessing": r.courses_assessing,
            }
            for r in reports
        ],
    }


def _print_table(result: dict) -> None:
    s = result["summary"]
    print(f"AoL matrix: {s['courses']} courses x {s['outcomes']} outcomes")
    print(f"Assessment levels: {', '.join(s['assessed_levels'])}")
    print("-" * 60)
    for o in result["outcomes"]:
        flag = "OK " if (o["covered"] and o["assessed"]) else "GAP"
        levels = ", ".join(f"{k}:{v}" for k, v in sorted(o["level_counts"].items())) or "(none)"
        note = ""
        if not o["covered"]:
            note = "  <- no course covers this outcome"
        elif not o["assessed"]:
            note = "  <- covered but never assessed"
        print(f"[{flag}] {o['outcome']:<10} {levels}{note}")
    print("-" * 60)
    if s["orphan_courses"]:
        print(f"Courses covering no outcome: {', '.join(s['orphan_courses'])}")
    print(f"VERDICT: {s['verdict']}", end="")
    if s["outcomes_with_gaps"]:
        print(f"  (gaps: {', '.join(s['outcomes_with_gaps'])})")
    else:
        print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a curriculum-to-outcome AoL coverage matrix (structure only)."
    )
    parser.add_argument("csv", help="path to the matrix CSV, or '-' for stdin")
    parser.add_argument(
        "--assessed-levels",
        default="M,A",
        help="comma-separated coverage codes that count as an assessment point (default: M,A)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = parser.parse_args(argv)

    assessed = {p.strip().upper() for p in args.assessed_levels.split(",") if p.strip()}
    if not assessed:
        print("error: --assessed-levels must list at least one code", file=sys.stderr)
        return 2

    rows, fieldnames = _read_rows(args.csv)
    result = analyze(rows, fieldnames, assessed)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        _print_table(result)

    return 0 if result["summary"]["verdict"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
