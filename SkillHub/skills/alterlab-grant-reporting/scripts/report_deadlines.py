#!/usr/bin/env python3
"""report_deadlines.py — Compute post-award report due dates from award dates.

Reporting deadlines for the major funders are deterministic functions of the
award's budget-period / project dates, and missing one can suspend payments. This
helper computes them from the verified general rules so the user does not have to
recall them from memory. It does NO network I/O and depends only on the Python
standard library.

The encoded rules (each sourced in ../references/funder_formats.md):

  NIH SNAP      Annual RPPR  ~= 45 days BEFORE next budget-period start
  NIH non-SNAP  Annual RPPR  ~= 60 days BEFORE next budget-period start
  NIH Final RPPR             within 120 days AFTER period-of-performance end
  NSF Annual                 90 days BEFORE the budget-period end
  NSF Final report           within 120 days AFTER award end
  NSF Project Outcomes Rpt   within 120 days AFTER award end
  Horizon Europe / ERC       within 60 days AFTER each reporting-period end
  (periodic and final)

IMPORTANT: these are the funders' GENERAL rules. A specific Notice of Award,
cooperative agreement, or Grant Agreement can override them. The output always
restates this — confirm every computed date against the award's own documents.

Usage:
  uv run python report_deadlines.py --funder nih-snap \
      --budget-period-start 2026-09-01 --project-end 2028-08-31
  uv run python report_deadlines.py --funder nsf \
      --budget-period-end 2027-05-31 --project-end 2028-08-31 --json
  uv run python report_deadlines.py --funder eu --period-end 2027-06-30 --json

Exit codes: 0 = computed; 2 = bad/missing arguments.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

FUNDERS = ("nih-snap", "nih-nonsnap", "nsf", "eu")

DISCLAIMER = (
    "General funder rule only — confirm against the Notice of Award / Grant "
    "Agreement; specific programs can override these defaults."
)


def _parse_date(s: str | None, flag: str) -> date | None:
    if s is None:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        print(f"error: {flag} must be ISO date YYYY-MM-DD, got {s!r}", file=sys.stderr)
        raise SystemExit(2)


@dataclass
class Deadline:
    report: str
    due: date
    rule: str

    def as_dict(self) -> dict:
        return {"report": self.report, "due": self.due.isoformat(), "rule": self.rule}


@dataclass
class Result:
    funder: str
    deadlines: list[Deadline] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def compute(args: argparse.Namespace) -> Result:
    funder = args.funder
    res = Result(funder=funder)

    bps = _parse_date(args.budget_period_start, "--budget-period-start")
    bpe = _parse_date(args.budget_period_end, "--budget-period-end")
    pend = _parse_date(args.project_end, "--project-end")
    pend_eu = _parse_date(args.period_end, "--period-end")

    if funder in ("nih-snap", "nih-nonsnap"):
        lead = 45 if funder == "nih-snap" else 60
        kind = "SNAP" if funder == "nih-snap" else "non-SNAP"
        if bps is not None:
            res.deadlines.append(
                Deadline(
                    f"Annual RPPR ({kind})",
                    bps - timedelta(days=lead),
                    f"~{lead} days before the next budget-period start ({bps.isoformat()})",
                )
            )
        else:
            res.notes.append(
                "Annual RPPR needs --budget-period-start (the NEXT budget period's start)."
            )
        if pend is not None:
            res.deadlines.append(
                Deadline(
                    "Final RPPR",
                    pend + timedelta(days=120),
                    f"within 120 days after period-of-performance end ({pend.isoformat()})",
                )
            )
        else:
            res.notes.append("Final RPPR needs --project-end.")

    elif funder == "nsf":
        if bpe is not None:
            res.deadlines.append(
                Deadline(
                    "Annual project report",
                    bpe - timedelta(days=90),
                    f"90 days before the budget-period end ({bpe.isoformat()})",
                )
            )
        else:
            res.notes.append("Annual project report needs --budget-period-end.")
        if pend is not None:
            res.deadlines.append(
                Deadline(
                    "Final project report",
                    pend + timedelta(days=120),
                    f"within 120 days after award end ({pend.isoformat()})",
                )
            )
            res.deadlines.append(
                Deadline(
                    "Project Outcomes Report",
                    pend + timedelta(days=120),
                    f"within 120 days after award end ({pend.isoformat()}); <=800 words, public",
                )
            )
        else:
            res.notes.append("Final report / Project Outcomes Report need --project-end.")

    elif funder == "eu":
        ref_end = pend_eu or pend
        if ref_end is not None:
            label = "Periodic / final report"
            res.deadlines.append(
                Deadline(
                    label,
                    ref_end + timedelta(days=60),
                    f"within 60 days after the reporting-period end ({ref_end.isoformat()})",
                )
            )
        else:
            res.notes.append(
                "Horizon Europe / ERC report needs --period-end (or --project-end)."
            )

    res.notes.append(DISCLAIMER)
    return res


def render_table(res: Result) -> str:
    lines = [f"Funder: {res.funder}", ""]
    if res.deadlines:
        wr = max(len(d.report) for d in res.deadlines)
        lines.append(f"{'Report'.ljust(wr)}  {'Due'.ljust(10)}  Rule")
        lines.append(f"{'-' * wr}  {'-' * 10}  {'-' * 4}")
        for d in res.deadlines:
            lines.append(f"{d.report.ljust(wr)}  {d.due.isoformat()}  {d.rule}")
    else:
        lines.append("(no deadlines computed — see notes)")
    if res.notes:
        lines.append("")
        for n in res.notes:
            lines.append(f"NOTE: {n}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Compute post-award report due dates from award dates (stdlib only, no network)."
    )
    p.add_argument("--funder", required=True, choices=FUNDERS,
                   help="nih-snap | nih-nonsnap | nsf | eu")
    p.add_argument("--budget-period-start", metavar="YYYY-MM-DD",
                   help="NIH: start of the NEXT budget period (for the Annual RPPR)")
    p.add_argument("--budget-period-end", metavar="YYYY-MM-DD",
                   help="NSF: end of the current reporting budget period")
    p.add_argument("--project-end", metavar="YYYY-MM-DD",
                   help="Award / period-of-performance end date (final reports)")
    p.add_argument("--period-end", metavar="YYYY-MM-DD",
                   help="EU: end of the reporting period (periodic/final report)")
    p.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    res = compute(args)
    if args.json:
        print(json.dumps(
            {
                "funder": res.funder,
                "deadlines": [d.as_dict() for d in res.deadlines],
                "notes": res.notes,
            },
            indent=2,
        ))
    else:
        print(render_table(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
