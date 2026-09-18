#!/usr/bin/env python3
"""reporting_gate.py — A transparency linter for a results claim.

Enforces the Iron Law of alterlab-results-transparency:

    NO RESULTS CLAIM WITHOUT REPORTING EVERY ANALYSIS RUN

Given a small JSON *claim manifest* describing one results claim and every test
actually run for it, this checks that the claim clears the Gate Function steps
2-5 (see ../references/gate_function.md):

  Step 2  LIST    — every test run is reported (none silently dropped).
  Step 3  CHECK   — assumption results are reported for every reported test.
  Step 4  CHECK   — every confirmatory claim carries an effect size AND a 95% CI.
  Step 5  CHECK   — every deviation from the frozen plan is labelled exploratory.
  Escalation      — 3+ tests on one claim warns about multiple comparisons.

This is a COMPLETENESS / DISCLOSURE linter, NOT a statistics engine. It never
computes a p-value, an effect size, or a confidence interval — that is
alterlab-statistical-analysis's job. It only checks that those outputs are
present and disclosed before a sentence is written.

Design constraints (mirrors the house exemplar):
- Standard library ONLY. No third-party deps, no network, no API keys.
- Deterministic: the same manifest always yields the same verdict.
- Exit code 0 = claim clears the gate; non-zero = it does not.

Manifest shape (see ../references/gate_function.md for the full schema):
  {
    "claim": "<the sentence you intend to write>",
    "preregistered": true,
    "tests_run": [
      {"name": "...", "reported": true, "confirmatory": true,
       "statistic": "t(58) = 2.71", "p_value": "0.009",
       "effect_size": "d = 0.70", "ci_95": "[0.18, 1.22]",
       "assumptions_reported": true}
    ],
    "deviations": [
      {"description": "added covariate", "labelled_exploratory": true}
    ]
  }

Usage:
  uv run python reporting_gate.py claim.json
  uv run python reporting_gate.py -            # read manifest from stdin
  uv run python reporting_gate.py claim.json --json   # machine-readable report
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

MULTIPLE_COMPARISON_THRESHOLD = 3


def _truthy_str(value: Any) -> bool:
    """A field counts as 'present' only if it is a non-empty string."""
    return isinstance(value, str) and value.strip() != ""


def evaluate(manifest: dict[str, Any]) -> dict[str, Any]:
    """Run the gate over one claim manifest and return a structured report."""
    failures: list[str] = []
    warnings: list[str] = []

    claim = manifest.get("claim")
    if not _truthy_str(claim):
        failures.append("IDENTIFY: 'claim' is missing or empty — state the exact sentence you intend to write.")

    tests = manifest.get("tests_run")
    if not isinstance(tests, list) or not tests:
        failures.append("LIST: 'tests_run' is missing or empty — list EVERY test run for this claim, including the ones that did not work.")
        tests = []

    reported_count = 0
    for i, test in enumerate(tests):
        if not isinstance(test, dict):
            failures.append(f"LIST: tests_run[{i}] is not an object.")
            continue
        label = test.get("name") or f"tests_run[{i}]"

        # Step 2 — every test run must be reported.
        if not test.get("reported", False):
            failures.append(
                f"LIST (step 2): '{label}' was run but reported=false — an unreported analysis is selective reporting. "
                "Report it (a supplementary 'all analyses run' table is standard) or justify it as exploratory in the frozen plan."
            )
            continue
        reported_count += 1

        # Step 3 — assumptions reported for every reported test.
        if not test.get("assumptions_reported", False):
            failures.append(
                f"CHECK (step 3): '{label}' is reported without assumption results — include the normality / homogeneity / "
                "linearity / outlier checks from alterlab-statistical-analysis (scripts/assumption_checks.py)."
            )

        # Step 4 — confirmatory claims need effect size AND 95% CI.
        if test.get("confirmatory", False):
            if not _truthy_str(test.get("effect_size")):
                failures.append(
                    f"CHECK (step 4): confirmatory '{label}' has no effect size — a bare p-value never clears the gate. "
                    "Report the effect size (alterlab-statistical-analysis owns the computation)."
                )
            if not _truthy_str(test.get("ci_95")):
                failures.append(
                    f"CHECK (step 4): confirmatory '{label}' has no 95% confidence interval — report the effect size WITH its CI."
                )

    # Step 5 — deviations from the frozen plan must be labelled exploratory.
    deviations = manifest.get("deviations", [])
    if not isinstance(deviations, list):
        failures.append("CHECK (step 5): 'deviations' must be a list.")
        deviations = []
    for i, dev in enumerate(deviations):
        if not isinstance(dev, dict):
            failures.append(f"CHECK (step 5): deviations[{i}] is not an object.")
            continue
        desc = dev.get("description") or f"deviations[{i}]"
        if not dev.get("labelled_exploratory", False):
            failures.append(
                f"CHECK (step 5): deviation '{desc}' is not labelled exploratory — every difference from the frozen plan "
                "(alterlab-preregistration-discipline) must be named and labelled confirmatory vs. exploratory."
            )

    if manifest.get("preregistered") is False and deviations:
        warnings.append(
            "No frozen plan declared (preregistered=false) but deviations are listed — without a pre-registration, "
            "ALL of these analyses are exploratory; claims cannot be reported as confirmatory."
        )

    # Escalation gate — multiple comparisons / test-shopping.
    if len(tests) >= MULTIPLE_COMPARISON_THRESHOLD:
        warnings.append(
            f"ESCALATION: {len(tests)} tests on one claim. This is multiple comparisons / test-shopping — correct for ALL of "
            "them (Bonferroni / FDR via alterlab-statistical-analysis) or declare the analysis exploratory. Do NOT run test #4 to find p < .05."
        )

    cleared = not failures
    return {
        "tool": "alterlab-results-transparency/reporting_gate.py",
        "iron_law": "NO RESULTS CLAIM WITHOUT REPORTING EVERY ANALYSIS RUN",
        "claim": claim if _truthy_str(claim) else None,
        "tests_total": len(tests),
        "tests_reported": reported_count,
        "cleared": cleared,
        "verdict": "CLEAR" if cleared else "BLOCKED",
        "failures": failures,
        "warnings": warnings,
    }


def _load_manifest(path: str) -> dict[str, Any]:
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object (one claim per file).")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("manifest", help="path to the claim manifest JSON, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="emit the machine-readable JSON report instead of prose")
    args = parser.parse_args(argv)

    try:
        manifest = _load_manifest(args.manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: could not read manifest: {exc}", file=sys.stderr)
        return 2

    report = evaluate(manifest)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Iron Law: {report['iron_law']}")
        if report["claim"]:
            print(f"Claim:    {report['claim']}")
        print(f"Tests:    {report['tests_reported']}/{report['tests_total']} reported")
        print(f"Verdict:  {report['verdict']}")
        for w in report["warnings"]:
            print(f"  [warn] {w}")
        for f in report["failures"]:
            print(f"  [FAIL] {f}")
        if report["cleared"]:
            print("\nGate cleared — the claim may be written, with test, df, exact p, effect size + 95% CI, and its label.")
        else:
            print("\nGate BLOCKED — do not write the claim until every [FAIL] above is resolved.")

    return 0 if report["cleared"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
