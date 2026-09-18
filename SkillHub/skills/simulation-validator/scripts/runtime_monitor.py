#!/usr/bin/env python3
import argparse
import json
import math
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

# Maximum log file size to parse (500 MB), matching the SKILL.md Security section.
MAX_LOG_BYTES = 500 * 1024 * 1024

# Default dt-collapse capture. `\bdt\b` anchors the token (so "width" does not
# false-match), and `\D*?` tolerates intervening words before the number (so
# "dt reduced from 1e-3 to 5e-4" still parses). Matches references/log_patterns.md.
DEFAULT_DT_PATTERN = r"\bdt\b\D*?([0-9][0-9eE+.\-]*)"

# Dedicated adaptive-stepping rule: capture the POST-reduction ("to") value so
# successive collapses register monotonically (e.g. "dt reduced from 1e-3 to 5e-4").
DT_REDUCE_RE = re.compile(
    r"\bdt\b.*?reduc\w*\s+from\s+[0-9][0-9eE+.\-]*\s+to\s+([0-9][0-9eE+.\-]*)",
    re.IGNORECASE,
)

# Left-boundary-anchored NaN/Inf/overflow scan (consistent with
# references/log_patterns.md), avoiding domain words like "nanometer".
NAN_INF_RE = re.compile(
    r"(?<![A-Za-z])(?:nan(?:s)?|inf(?:inity)?|overflow)(?![A-Za-z])", re.IGNORECASE
)


def positive_finite_float(raw: str) -> float:
    """argparse type: accept only finite, strictly-positive floats."""
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"not a number: {raw!r}")
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(
            f"must be a finite positive number, got {raw!r}"
        )
    return value


def parse_log(
    text: str,
    residual_pattern: str,
    dt_pattern: str,
) -> Tuple[List[float], List[float]]:
    residuals: List[float] = []
    dts: List[float] = []
    res_re = re.compile(residual_pattern, re.IGNORECASE)
    dt_re = re.compile(dt_pattern, re.IGNORECASE)

    for line in text.splitlines():
        res_match = res_re.search(line)
        if res_match:
            try:
                residuals.append(float(res_match.group(1)))
            except ValueError:
                continue
        # Prefer the post-reduction ("to") value for adaptive-stepping lines.
        reduce_match = DT_REDUCE_RE.search(line)
        if reduce_match:
            try:
                dts.append(float(reduce_match.group(1)))
                continue
            except ValueError:
                pass
        dt_match = dt_re.search(line)
        if dt_match:
            try:
                dts.append(float(dt_match.group(1)))
            except ValueError:
                continue
    return residuals, dts


def scan_nan_inf(text: str) -> bool:
    """Return True if any NaN/Inf/overflow token appears in the log."""
    return bool(NAN_INF_RE.search(text))


def compute_stats(values: List[float]) -> Dict[str, Optional[float]]:
    if not values:
        return {"min": None, "max": None, "last": None}
    return {"min": min(values), "max": max(values), "last": values[-1]}


def monitor(
    residuals: List[float],
    dts: List[float],
    residual_growth: float,
    dt_drop: float,
    has_nan_inf: bool = False,
) -> Dict[str, object]:
    alerts: List[str] = []
    if has_nan_inf:
        alerts.append("NaN/Inf/overflow detected in log.")
    if residuals:
        for i in range(1, len(residuals)):
            if residuals[i - 1] > 0 and residuals[i] / residuals[i - 1] > residual_growth:
                alerts.append("Residual increased > threshold.")
                break
    if dts:
        # Direction-aware: flag only an actual COLLAPSE, i.e. a later dt that
        # falls below the running maximum by more than the threshold. A healthy
        # dt ramp-up no longer produces a false alert.
        running_max = dts[0]
        for value in dts[1:]:
            if value > running_max:
                running_max = value
            elif value > 0 and running_max / value > dt_drop:
                alerts.append("Time step reduced > threshold.")
                break

    return {
        "alerts": alerts,
        "residual_stats": compute_stats(residuals),
        "dt_stats": compute_stats(dts),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitor runtime logs for convergence and dt issues.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--log", required=True, help="Path to log file")
    parser.add_argument(
        "--residual-pattern",
        default=r"residual[^0-9eE+\-]*([0-9][0-9eE+\.-]*)",
        help="Regex to capture residual value",
    )
    parser.add_argument(
        "--dt-pattern",
        default=DEFAULT_DT_PATTERN,
        help="Regex to capture dt value",
    )
    parser.add_argument(
        "--residual-growth",
        type=positive_finite_float,
        default=10.0,
        help="Residual growth threshold",
    )
    parser.add_argument(
        "--dt-drop",
        type=positive_finite_float,
        default=100.0,
        help="dt reduction threshold (peak/current)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        size = os.path.getsize(args.log)
        if size > MAX_LOG_BYTES:
            print(
                f"Log file too large: {size} bytes exceeds {MAX_LOG_BYTES} byte cap.",
                file=sys.stderr,
            )
            sys.exit(2)
        with open(args.log, "r", encoding="utf-8") as handle:
            text = handle.read()
        residuals, dts = parse_log(text, args.residual_pattern, args.dt_pattern)
        has_nan_inf = scan_nan_inf(text)
        result = monitor(
            residuals, dts, args.residual_growth, args.dt_drop, has_nan_inf
        )
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    payload = {
        "inputs": {
            "log": args.log,
            "residual_pattern": args.residual_pattern,
            "dt_pattern": args.dt_pattern,
            "residual_growth": args.residual_growth,
            "dt_drop": args.dt_drop,
        },
        "results": result,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print("Runtime monitor")
    for alert in result["alerts"]:
        print(f"  alert: {alert}")
    print(f"  residual_stats: {result['residual_stats']}")
    print(f"  dt_stats: {result['dt_stats']}")


if __name__ == "__main__":
    main()
