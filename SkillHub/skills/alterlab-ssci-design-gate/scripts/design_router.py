#!/usr/bin/env python3
"""Design-gate router: print the design family and its required identifying assumption.

Stdlib-only. Answer a few structural questions (via flags or the interactive prompts) and the
router names the design and the assumption the causal claim must rest on. It does NOT estimate
anything — it enforces that the assumption is named before analysis.

    python design_router.py --random-assignment yes
    python design_router.py --random-assignment no --exogenous did
    python design_router.py            # interactive
"""
from __future__ import annotations

import argparse

# Design family -> (label, identifying assumption to defend).
_QED = {
    "did": ("Difference-in-differences",
            "PARALLEL TRENDS — treated and control would have moved together absent treatment"),
    "iv": ("Instrumental variables",
           "EXCLUSION RESTRICTION + relevance — the instrument affects the outcome only through the treatment"),
    "rdd": ("Regression discontinuity",
            "CONTINUITY at the cutoff — no manipulation of the running variable"),
    "its": ("Interrupted time series",
            "the modeled pre-trend counterfactual would have continued absent the intervention"),
    "fe": ("Fixed effects / panel",
           "no TIME-VARYING confounders (unit/time confounders differenced out)"),
    "obs": ("Observational / selection-on-observables",
            "CONDITIONAL IGNORABILITY — no unmeasured confounding (the strongest, least testable assumption)"),
}


def route(random_assignment: str, exogenous: str | None, qualitative: bool) -> tuple[str, str]:
    if qualitative:
        return ("Qualitative (route to alterlab-qualitative-methods)",
                "sample size is governed by SATURATION / information power, not a power formula")
    if random_assignment == "yes":
        return ("True experiment (RCT / lab / field)",
                "randomization -> IGNORABILITY (assignment independent of potential outcomes)")
    if exogenous in _QED:
        return _QED[exogenous]
    return _QED["obs"]


def _ask(prompt: str, choices: list[str]) -> str:
    while True:
        ans = input(f"{prompt} {choices}: ").strip().lower()
        if ans in choices:
            return ans
        print(f"  please answer one of {choices}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--random-assignment", choices=["yes", "no"])
    ap.add_argument("--exogenous", choices=sorted(_QED), default=None,
                    help="source of exogenous variation when assignment is not random")
    ap.add_argument("--qualitative", action="store_true")
    args = ap.parse_args()

    ra = args.random_assignment
    qual = args.qualitative
    exo = args.exogenous
    if ra is None and not qual:
        qual = _ask("Interpretive / theory-building aim (not effect estimation)?", ["yes", "no"]) == "yes"
        if not qual:
            ra = _ask("Is the cause randomly ASSIGNED by the researcher?", ["yes", "no"])
            if ra == "no":
                exo = _ask("Source of exogenous variation?", sorted(_QED))

    label, assumption = route(ra or "no", exo, qual)
    print(f"DESIGN:     {label}")
    print(f"ASSUMPTION: {assumption}")
    print("Pin this assumption in the Design Passport BEFORE any estimation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
