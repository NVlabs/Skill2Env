#!/usr/bin/env python3
"""Test-selection router for alterlab-test-selection-guard.

Walks the same decision tree as SKILL.md / references/decision_tree.md and prints the
NAMED statistical test implied by the *structure of the data* — outcome type, number of
groups, pairing, and the pre-specified normality branch. It deliberately takes **no
p-value as input**: the whole point of the guard is that the test is fixed before any
result is seen. Hand the named test to alterlab-statistical-analysis to actually run it.

Standard library only — runs in a bare `uv run python` env with zero extra dependencies.

Usage (flags):
    uv run python test_picker.py --outcome continuous --groups 2 --paired no --normal yes
    uv run python test_picker.py --outcome continuous --groups 3 --paired yes --normal no
    uv run python test_picker.py --outcome categorical --expected-cell-ge5 no
    uv run python test_picker.py --outcome association --both-continuous yes --linear-normal no
    uv run python test_picker.py --outcome association --both-continuous no --pred-outcome binary

Interactive (no flags): answer the prompts.
JSON: add --json for a machine-readable verdict.
"""
from __future__ import annotations

import argparse
import json
import sys

# The Iron Law, surfaced on every run so the discipline travels with the answer.
IRON_LAW = "NO TEST CHOSEN AFTER SEEING THE P-VALUE."


def _yn(value: str) -> bool:
    return str(value).strip().lower() in {"y", "yes", "true", "1", "paired", "repeated"}


def pick_test(
    outcome: str,
    groups: str | None = None,
    paired: str | None = None,
    normal: str | None = None,
    expected_cell_ge5: str | None = None,
    both_continuous: str | None = None,
    linear_normal: str | None = None,
    pred_outcome: str | None = None,
) -> dict:
    """Return {test, branch, note} for the supplied data structure.

    Raises ValueError when a required answer for the chosen branch is missing.
    """
    outcome = (outcome or "").strip().lower()

    # --- group comparison (continuous / ordinal outcome) -----------------
    if outcome in {"continuous", "ordinal"}:
        if groups is None or paired is None or normal is None:
            raise ValueError(
                "continuous/ordinal outcome needs --groups, --paired, and --normal"
            )
        g = str(groups).strip()
        is_paired = _yn(paired)
        is_normal = _yn(normal)
        if g == "2":
            if not is_paired:
                test = "independent t-test (Welch if unequal variance)" if is_normal else "Mann-Whitney U"
            else:
                test = "paired t-test" if is_normal else "Wilcoxon signed-rank"
        elif g in {"3", "3+", "4", "5", "many", "3plus"}:
            if not is_paired:
                test = "one-way ANOVA (+ planned post-hoc)" if is_normal else "Kruskal-Wallis"
            else:
                test = "repeated-measures ANOVA" if is_normal else "Friedman"
        else:
            raise ValueError(f"unrecognized --groups value: {groups!r} (use 2 or 3+)")
        return {
            "test": test,
            "branch": f"groups={g}, paired={is_paired}, normal={is_normal}",
            "note": "Normality is decided by the assumption-check gate (Shapiro-Wilk / Levene), "
            "NOT by which test comes out significant.",
        }

    # --- categorical counts ---------------------------------------------
    if outcome in {"categorical", "counts", "category"}:
        if expected_cell_ge5 is None:
            raise ValueError("categorical outcome needs --expected-cell-ge5 (yes/no)")
        test = "chi-square test" if _yn(expected_cell_ge5) else "Fisher's exact test"
        return {
            "test": test,
            "branch": f"expected_cell_ge5={_yn(expected_cell_ge5)}",
            "note": "Decided by EXPECTED cell counts computed before testing, not by significance.",
        }

    # --- association -----------------------------------------------------
    if outcome in {"association", "relationship", "correlation"}:
        if both_continuous is None:
            raise ValueError(
                "association outcome needs --both-continuous (yes/no); if no, add --pred-outcome"
            )
        if _yn(both_continuous):
            if linear_normal is None:
                raise ValueError("both-continuous association needs --linear-normal (yes/no)")
            test = "Pearson r" if _yn(linear_normal) else "Spearman rho"
            branch = f"both_continuous=True, linear_normal={_yn(linear_normal)}"
        else:
            po = (pred_outcome or "").strip().lower()
            if po in {"binary", "logistic", "dichotomous"}:
                test = "logistic regression"
            elif po in {"continuous", "linear"}:
                test = "linear regression"
            else:
                raise ValueError("predictor model needs --pred-outcome continuous|binary")
            branch = f"predictors -> outcome={po}"
        return {
            "test": test,
            "branch": branch,
            "note": "Check linearity / residual normality before interpreting (regression).",
        }

    raise ValueError(
        f"unrecognized --outcome: {outcome!r} (use continuous|ordinal|categorical|association)"
    )


def _interactive() -> dict:
    def ask(q: str) -> str:
        return input(q).strip()

    outcome = ask("Outcome type (continuous/categorical/association)? ")
    o = outcome.lower()
    if o in {"continuous", "ordinal"}:
        return pick_test(outcome, groups=ask("How many groups (2 / 3+)? "),
                         paired=ask("Paired / repeated (yes/no)? "),
                         normal=ask("Normal per the assumption check (yes/no)? "))
    if o in {"categorical", "counts", "category"}:
        return pick_test(outcome, expected_cell_ge5=ask("Expected cell count >= 5 (yes/no)? "))
    if o in {"association", "relationship", "correlation"}:
        bc = ask("Both variables continuous (yes/no)? ")
        if _yn(bc):
            return pick_test(outcome, both_continuous="yes",
                             linear_normal=ask("Linear & normal (yes/no)? "))
        return pick_test(outcome, both_continuous="no",
                         pred_outcome=ask("Outcome for regression (continuous/binary)? "))
    raise ValueError(f"unrecognized outcome: {outcome!r}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--outcome", help="continuous | ordinal | categorical | association")
    p.add_argument("--groups", help="2 | 3+")
    p.add_argument("--paired", help="yes | no")
    p.add_argument("--normal", help="yes | no (from the assumption-check gate, NOT the p-value)")
    p.add_argument("--expected-cell-ge5", dest="expected_cell_ge5", help="yes | no")
    p.add_argument("--both-continuous", dest="both_continuous", help="yes | no")
    p.add_argument("--linear-normal", dest="linear_normal", help="yes | no")
    p.add_argument("--pred-outcome", dest="pred_outcome", help="continuous | binary")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args(argv)

    try:
        if args.outcome is None:
            result = _interactive()
        else:
            result = pick_test(
                args.outcome, args.groups, args.paired, args.normal,
                args.expected_cell_ge5, args.both_continuous,
                args.linear_normal, args.pred_outcome,
            )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    result["iron_law"] = IRON_LAW
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Iron Law: {IRON_LAW}")
        print(f"Named test: {result['test']}")
        print(f"Branch:     {result['branch']}")
        print(f"Reminder:   {result['note']}")
        print("Next: run it + report assumption checks via alterlab-statistical-analysis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
