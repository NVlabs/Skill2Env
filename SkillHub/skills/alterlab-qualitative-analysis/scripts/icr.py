#!/usr/bin/env python3
"""Intercoder-reliability for NOMINAL coding — stdlib only (no numpy / no krippendorff dep).

Computes percent agreement, Cohen's kappa (2 coders), and **Krippendorff's alpha (nominal)** with
a nonparametric bootstrap 95% CI over units. The `krippendorff` PyPI package returns only a point
estimate, so the bootstrap CI here is genuinely useful. For ORDINAL / INTERVAL alpha, weighted
kappa, or production use, use the `krippendorff` package or R `irrCAC` / `icr` (see the skill body).

Input CSV: one row per UNIT, one column per CODER (header = coder names). Blank cell = missing.

    python icr.py codings.csv
    python icr.py --demo
"""
from __future__ import annotations

import argparse
import csv
import random
from collections import Counter
from itertools import combinations


def _pairable_units(by_unit: list[list[str]]) -> list[list[str]]:
    """Keep only units with >= 2 non-missing codes (Krippendorff pairability)."""
    return [[c for c in unit if c is not None and c != ""] for unit in by_unit
            if sum(1 for c in unit if c is not None and c != "") >= 2]


def krippendorff_alpha_nominal(by_unit: list[list[str]]) -> float | None:
    """Nominal Krippendorff's alpha via the coincidence-matrix method.

    by_unit: list of units; each unit is a list of codes (missing already dropped by caller
    or given as '' / None). Returns None if not estimable.
    """
    units = _pairable_units(by_unit)
    if not units:
        return None
    # Coincidence matrix o[c][k] and marginals n_c.
    o: dict[str, Counter] = {}
    for unit in units:
        m = len(unit)
        if m < 2:
            continue
        w = 1.0 / (m - 1)
        for a, b in combinations(range(m), 2):
            ca, cb = unit[a], unit[b]
            # each unordered pair contributes to both (ca,cb) and (cb,ca)
            o.setdefault(ca, Counter())[cb] += w
            o.setdefault(cb, Counter())[ca] += w
    n_c = {c: sum(row.values()) for c, row in o.items()}
    n = sum(n_c.values())
    if n <= 1:
        return None
    diag = sum(o.get(c, Counter()).get(c, 0.0) for c in n_c)          # sum o_cc
    sum_nc2 = sum(v * v for v in n_c.values())                         # sum n_c^2
    denom = n * n - sum_nc2
    if denom == 0:
        return 1.0  # no expected disagreement possible → perfect
    # alpha = 1 - (n-1) * (observed off-diagonal) / (expected off-diagonal)
    return 1.0 - (n - 1) * (n - diag) / denom


def cohens_kappa_2(col_a: list[str], col_b: list[str]) -> float | None:
    """Cohen's kappa for exactly two coders, nominal. Pairs with any missing are dropped."""
    pairs = [(a, b) for a, b in zip(col_a, col_b)
             if a not in (None, "") and b not in (None, "")]
    if not pairs:
        return None
    n = len(pairs)
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    cats = set(ca) | set(cb)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def percent_agreement(by_unit: list[list[str]]) -> float | None:
    units = _pairable_units(by_unit)
    agree = total = 0
    for unit in units:
        for a, b in combinations(unit, 2):
            total += 1
            agree += 1 if a == b else 0
    return agree / total if total else None


def _bootstrap_ci(by_unit: list[list[str]], reps: int = 2000, seed: int = 12345) -> tuple[float, float] | None:
    """Percentile 95% CI by resampling UNITS with replacement. Seeded for reproducibility."""
    n = len(by_unit)
    if n < 2:
        return None
    rng = random.Random(seed)
    ests = []
    for _ in range(reps):
        sample = [by_unit[rng.randrange(n)] for _ in range(n)]
        a = krippendorff_alpha_nominal(sample)
        if a is not None:
            ests.append(a)
    if len(ests) < 2:
        return None
    ests.sort()
    lo = ests[max(0, int(0.025 * len(ests)))]
    hi = ests[min(len(ests) - 1, int(0.975 * len(ests)))]
    return lo, hi


def _read_csv(path: str) -> tuple[list[str], list[list[str]]]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    header, data = rows[0], rows[1:]
    by_unit = [[cell.strip() for cell in row] for row in data if any(c.strip() for c in row)]
    return header, by_unit


def _report(coders: list[str], by_unit: list[list[str]]) -> int:
    alpha = krippendorff_alpha_nominal(by_unit)
    pa = percent_agreement(by_unit)
    print(f"coders: {len(coders)} ({', '.join(coders)})   units: {len(by_unit)}")
    print(f"percent agreement (pairwise): {pa:.3f}" if pa is not None else "percent agreement: n/a")
    if alpha is None:
        print("Krippendorff alpha (nominal): not estimable")
        return 0
    ci = _bootstrap_ci(by_unit)
    ci_s = f"  95% CI [{ci[0]:.3f}, {ci[1]:.3f}] (bootstrap over units)" if ci else ""
    print(f"Krippendorff alpha (nominal): {alpha:.3f}{ci_s}")
    if len(coders) == 2:
        k = cohens_kappa_2([u[0] for u in by_unit], [u[1] for u in by_unit])
        if k is not None:
            print(f"Cohen's kappa (2 coders): {k:.3f}")
    verdict = ("RELIABLE (>= .80)" if alpha >= 0.80 else
               "TENTATIVE conclusions only (.667-.80)" if alpha >= 0.667 else
               "UNRELIABLE (< .667)")
    print(f"interpretation: {verdict}  [Krippendorff cutoffs]")
    print("Note: nominal only. For ordinal/interval/weighted use the `krippendorff` pkg or R irrCAC/icr.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("csv", nargs="?", help="CSV: rows=units, cols=coders, header=coder names")
    ap.add_argument("--demo", action="store_true", help="run a built-in 2-coder example")
    args = ap.parse_args()
    if args.demo:
        coders = ["coder_A", "coder_B"]
        by_unit = [["1", "1"], ["1", "2"], ["3", "3"], ["2", "2"], ["1", "1"], ["2", "2"]]
        return _report(coders, by_unit)
    if not args.csv:
        ap.error("provide a CSV path or --demo")
    coders, by_unit = _read_csv(args.csv)
    return _report(coders, by_unit)


if __name__ == "__main__":
    raise SystemExit(main())
