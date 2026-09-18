#!/usr/bin/env python3
"""Design Passport state machine (stdlib only).

Enforces the pipeline the orchestrator owns: which gate runs next, whether the current gate is
fail-closed, and which analysis module a design routes to. It holds NO analysis logic — it only
sequences gates and reports routing so a stage cannot run before its prerequisite gate passes.

    python passport.py --stage design --verdict PASS        # -> next gate
    python passport.py --stage inference --verdict BLOCK     # -> must resolve, cannot advance
    python passport.py --route --design-type did             # -> analysis module for this design
"""
from __future__ import annotations

import argparse

# Ordered stages -> (gate skill, fail-closed?).
_STAGES = [
    ("design", "alterlab-ssci-design-gate", True),
    ("measurement", "alterlab-ssci-measurement-gate", False),
    ("sampling", "alterlab-ssci-sampling-gate", False),
    ("analysis", "(dispatched analysis module)", False),
    ("inference", "alterlab-ssci-inference-gate", True),
    ("reporting", "alterlab-paper-writer", False),
]
_ORDER = [s[0] for s in _STAGES]

# design_type / data kind -> analysis module skill.
_MODULE = {
    "experiment": "alterlab-causal-inference",
    "did": "alterlab-causal-inference",
    "iv": "alterlab-causal-inference",
    "rdd": "alterlab-causal-inference",
    "its": "alterlab-causal-inference",
    "fe": "alterlab-causal-inference",
    "observational": "alterlab-causal-inference",
    "sem": "alterlab-sem-psychometrics",
    "cfa": "alterlab-sem-psychometrics",
    "irt": "alterlab-sem-psychometrics",
    "qca": "alterlab-qca",
    "network": "alterlab-sna",
    "abm": "alterlab-abm-mesa",
    "text": "alterlab-text-as-data",
    "survey": "alterlab-survey-analysis",
    "multilevel": "alterlab-multilevel-models",
    "nested": "alterlab-multilevel-models",
    "hierarchical": "alterlab-multilevel-models",
    "meta": "alterlab-meta-analysis",
    "qual-coding": "alterlab-qualitative-analysis",
    "qualitative": "alterlab-qualitative-methods",
    "mixed": "alterlab-mixed-methods",
    "descriptive": "alterlab-statistical-analysis",
}

# Cross-cutting steps that run outside the design_type -> module map.
_CROSSCUTTING = {
    "missing": "alterlab-missing-data (run BEFORE the analysis module — impute + pool)",
}


def next_gate(stage: str, verdict: str) -> tuple[str, str]:
    verdict = verdict.upper()
    if stage not in _ORDER:
        raise ValueError(f"unknown stage '{stage}' (expected one of {_ORDER})")
    _, gate, fail_closed = _STAGES[_ORDER.index(stage)]
    if verdict == "BLOCK":
        if fail_closed:
            return (stage, f"BLOCKED at {stage} ({gate}) — fail-closed. Resolve before advancing; do NOT bypass.")
        return (stage, f"BLOCK escalated at {stage} ({gate}) — a fatal threat was found. Resolve before advancing.")
    i = _ORDER.index(stage)
    if i + 1 >= len(_ORDER):
        return ("done", "Pipeline complete — hand off to reporting (alterlab-paper-writer).")
    nxt, nxt_gate, nxt_fc = _STAGES[i + 1]
    tag = " [MANDATORY, fail-closed]" if nxt_fc else ""
    verdict_note = "" if verdict == "PASS" else " (WARN caveat recorded in gate_log)"
    return (nxt, f"Advance to {nxt} -> {nxt_gate}{tag}{verdict_note}")


def route(design_type: str) -> str:
    key = design_type.lower()
    if key in _CROSSCUTTING:
        return _CROSSCUTTING[key]
    return _MODULE.get(key, "alterlab-statistical-analysis (no causal/latent/relational structure detected)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stage", choices=_ORDER)
    ap.add_argument("--verdict", choices=["PASS", "WARN", "BLOCK", "pass", "warn", "block"])
    ap.add_argument("--route", action="store_true", help="report the analysis module for --design-type")
    ap.add_argument("--design-type", help="design_type from the Passport, e.g. did / cfa / qca / network / abm / text")
    args = ap.parse_args()

    if args.route:
        if not args.design_type:
            ap.error("--route requires --design-type")
        print(f"ANALYSIS MODULE: {route(args.design_type)}")
        return 0

    if not (args.stage and args.verdict):
        ap.error("provide --stage and --verdict (or --route --design-type)")
    nxt, msg = next_gate(args.stage, args.verdict)
    print(f"STAGE:  {args.stage}  VERDICT: {args.verdict.upper()}")
    print(f"NEXT:   {msg}")
    if args.design_type and nxt == "analysis":
        print(f"MODULE: {route(args.design_type)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
