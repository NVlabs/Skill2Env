#!/usr/bin/env python3
"""prereg_check.py — structured plan-vs-actual pre-registration self-audit.

A deterministic, **stdlib-only** checklist scorer for the
``alterlab-preregistration-discipline`` skill. It does NOT run any statistics, fit any
model, choose any test, or touch the network — it only compares a *frozen pre-registered
plan* against what was *actually done*, and flags every divergence as a researcher
degree of freedom that must either be pre-specified or labeled exploratory.

It enforces the skill's Iron Law mechanically:

    NO DATA ANALYSIS WITHOUT A PRE-REGISTERED ANALYSIS PLAN FIRST.

so a run with no plan, or with a plan timestamped after the data, cannot earn a
"confirmatory" verdict.

Inputs are two small JSON files (see ``--print-schema`` for the shape):

    plan.json     the frozen pre-registration (hypotheses, primary_outcome, tests,
                  exclusions, outlier_rule, stopping_rule, covariates, plan_timestamp,
                  data_collection_start)
    actual.json   what was actually run (primary_outcome, tests, exclusions,
                  outlier_rule, stopping, covariates, analyses[])

Each ``analyses[]`` item is classified CONFIRMATORY (traces to the frozen plan) or
EXPLORATORY (does not). Any plan/actual divergence on the frozen elements is reported as
a DEVIATION. The repo-level verdict is:

    CONFIRMATORY_OK   plan predates data, no deviations, all reported analyses planned
    DEVIATIONS        a plan exists but at least one frozen element diverged
    EXPLORATORY_ONLY  no valid pre-data plan -> nothing may be reported as confirmatory

Usage:
    uv run python prereg_check.py --plan plan.json --actual actual.json
    uv run python prereg_check.py --print-schema
    uv run python prereg_check.py --help

Exit code is 0 when the verdict is CONFIRMATORY_OK, else 1 (so it can gate CI).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from typing import Any

VERSION = "1.0.0"

# The frozen elements a pre-registration must lock (per references/workflow_gates.md).
# Each entry maps the plan key to the key the actual-analysis file may use for the same
# thing (the stopping rule is phrased as "stopping_rule" when planned, "stopping" when
# enacted), so a faithful run is not flagged on a mere naming difference.
FROZEN_ELEMENTS = [
    "primary_outcome",
    "tests",
    "exclusions",
    "outlier_rule",
    "stopping_rule",
    "covariates",
]

# plan key -> the key the actual-analysis file uses for the same frozen element.
ACTUAL_KEY = {"stopping_rule": "stopping"}

SCHEMA_DOC = {
    "plan.json": {
        "hypotheses": ["list[str] — directional where applicable"],
        "primary_outcome": "str — the single ranked primary outcome",
        "secondary_outcomes": ["list[str] — optional, ranked"],
        "tests": ["list[str] — the pre-specified test(s), e.g. 'two-sample t-test'"],
        "exclusions": ["list[str] — inclusion/exclusion rules"],
        "outlier_rule": "str — pre-specified outlier handling",
        "stopping_rule": "str — planned N or sequential design",
        "covariates": ["list[str] — pre-specified covariates / transforms"],
        "plan_timestamp": "str — ISO date the plan was frozen/registered (YYYY-MM-DD)",
        "data_collection_start": "str — ISO date data collection began (YYYY-MM-DD)",
    },
    "actual.json": {
        "primary_outcome": "str — the outcome actually reported as primary",
        "tests": ["list[str] — test(s) actually run"],
        "exclusions": ["list[str] — exclusions actually applied"],
        "outlier_rule": "str — outlier handling actually used",
        "stopping": "str — how collection actually stopped",
        "covariates": ["list[str] — covariates actually included"],
        "analyses": [
            {
                "name": "str — label for this analysis",
                "outcome": "str — outcome it targets",
                "test": "str — test used",
                "claimed": "str — 'confirmatory' or 'exploratory' as the author claims",
            }
        ],
    },
}


class PlanError(ValueError):
    """Raised when an input file is missing or structurally unusable."""


def _norm(v: Any) -> Any:
    """Normalise a value for order-insensitive comparison."""
    if isinstance(v, list):
        return sorted(str(x).strip().lower() for x in v)
    if v is None:
        return None
    return str(v).strip().lower()


def _parse_date(s: Any) -> _dt.date | None:
    if not s:
        return None
    try:
        return _dt.date.fromisoformat(str(s).strip()[:10])
    except ValueError:
        return None


def load_json(path: str) -> dict:
    try:
        if path == "-":
            return json.load(sys.stdin)
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError as exc:
        raise PlanError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PlanError(f"invalid JSON in {path}: {exc}") from exc


def plan_predates_data(plan: dict) -> tuple[bool, str]:
    """Iron Law check: a valid plan must be timestamped on/before data collection."""
    pt = _parse_date(plan.get("plan_timestamp"))
    ds = _parse_date(plan.get("data_collection_start"))
    if pt is None:
        return False, "plan has no parseable plan_timestamp — cannot prove it predates data"
    if ds is None:
        return False, "no parseable data_collection_start — cannot prove the plan predates data"
    if pt <= ds:
        return True, f"plan frozen {pt.isoformat()} on/before data start {ds.isoformat()}"
    return False, (
        f"plan_timestamp {pt.isoformat()} is AFTER data_collection_start "
        f"{ds.isoformat()} — the plan does not predate the data"
    )


def audit(plan: dict, actual: dict) -> dict:
    deviations: list[dict] = []
    for elem in FROZEN_ELEMENTS:
        if elem not in plan:
            deviations.append({"element": elem, "type": "unplanned",
                               "detail": f"'{elem}' was never frozen in the plan"})
            continue
        actual_key = ACTUAL_KEY.get(elem, elem)
        actual_val = actual.get(actual_key, actual.get(elem))
        if _norm(plan.get(elem)) != _norm(actual_val):
            deviations.append({
                "element": elem,
                "type": "diverged",
                "planned": plan.get(elem),
                "actual": actual_val,
                "detail": f"'{elem}' as run does not match the frozen plan",
            })

    # Classify each reported analysis.
    classified: list[dict] = []
    planned_tests = _norm(plan.get("tests"))
    planned_outcomes = set()
    if plan.get("primary_outcome"):
        planned_outcomes.add(_norm(plan["primary_outcome"]))
    for o in plan.get("secondary_outcomes", []) or []:
        planned_outcomes.add(_norm(o))

    for a in actual.get("analyses", []) or []:
        in_plan = (
            _norm(a.get("outcome")) in planned_outcomes
            and (planned_tests is None or _norm(a.get("test")) in planned_tests)
        )
        verdict = "CONFIRMATORY" if in_plan else "EXPLORATORY"
        claimed = _norm(a.get("claimed"))
        mislabeled = verdict == "EXPLORATORY" and claimed == "confirmatory"
        classified.append({
            "name": a.get("name"),
            "verdict": verdict,
            "claimed": a.get("claimed"),
            "mislabeled": mislabeled,
            "detail": (
                "traces to a frozen plan line" if in_plan
                else "not in the frozen plan — must be reported as exploratory"
            ),
        })

    valid_plan, ts_detail = plan_predates_data(plan)
    mislabeled_any = any(c["mislabeled"] for c in classified)

    if not valid_plan:
        verdict = "EXPLORATORY_ONLY"
    elif deviations or mislabeled_any:
        verdict = "DEVIATIONS"
    else:
        verdict = "CONFIRMATORY_OK"

    return {
        "tool": "alterlab-preregistration-discipline/prereg_check.py",
        "version": VERSION,
        "iron_law": "NO DATA ANALYSIS WITHOUT A PRE-REGISTERED ANALYSIS PLAN FIRST",
        "plan_predates_data": valid_plan,
        "timestamp_detail": ts_detail,
        "verdict": verdict,
        "deviation_count": len(deviations),
        "deviations": deviations,
        "analyses": classified,
        "summary": {
            "confirmatory": sum(c["verdict"] == "CONFIRMATORY" for c in classified),
            "exploratory": sum(c["verdict"] == "EXPLORATORY" for c in classified),
            "mislabeled_confirmatory": sum(c["mislabeled"] for c in classified),
        },
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--plan", help="path to the frozen pre-registration JSON ('-' for stdin)")
    ap.add_argument("--actual", help="path to the actual-analysis JSON ('-' for stdin)")
    ap.add_argument("--print-schema", action="store_true",
                    help="print the expected JSON shape and exit")
    ap.add_argument("--out", help="write the JSON report here instead of stdout")
    ap.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = ap.parse_args(argv)

    if args.print_schema:
        print(json.dumps(SCHEMA_DOC, indent=2))
        return 0

    if not args.plan or not args.actual:
        ap.error("both --plan and --actual are required (or use --print-schema)")

    try:
        plan = load_json(args.plan)
        actual = load_json(args.actual)
    except PlanError as exc:
        print(json.dumps({"error": str(exc), "verdict": "EXPLORATORY_ONLY"}, indent=2),
              file=sys.stderr)
        return 1

    report = audit(plan, actual)
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0 if report["verdict"] == "CONFIRMATORY_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
