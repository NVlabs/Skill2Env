#!/usr/bin/env python3
"""Triage common materials simulation failure signatures."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List


MAX_LOG_SIZE = 10 * 1024 * 1024
MAX_SYMPTOMS = 50
MAX_SYMPTOM_LEN = 100
MAX_CODE_LEN = 100
STAGES = {"setup", "runtime", "postprocess", "unknown"}

PATTERNS = {
    "nan": ("non-finite values", "Reduce timestep, check initial overlaps, bounds, and material parameters."),
    "inf": ("non-finite values", "Check division by zero, singular matrices, and invalid constitutive state."),
    "nonconvergence": ("solver convergence", "Inspect residual history, preconditioner, tolerance, and initial guess."),
    "exploding-energy": ("instability", "Check timestep, forces, contacts, and thermostat/barostat coupling."),
    "unstable-timestep": ("time integration", "Reduce dt, add ramping, or switch to implicit/adaptive integration."),
    "pressure-blowup": ("bad initial state", "Minimize/equilibrate first and check density, overlaps, and barostat."),
    "missing-potential": ("missing model data", "Locate potential/pseudopotential and verify species mapping."),
    "bad-pseudopotential": ("DFT setup", "Check element, valence, functional compatibility, and cutoff convergence."),
    "corrupted-output": ("I/O failure", "Preserve raw files, check disk/scratch, and rerun smallest case."),
    "incomplete-run": ("interrupted execution", "Check scheduler walltime, restart files, and final completion markers."),
    "out-of-memory": ("memory exhaustion", "Reduce ranks-per-node or domain/grid size, raise --mem/--mem-per-cpu, and check per-rank memory footprint; consider out-of-core options."),
    "crash": ("process crash / memory fault", "Check for out-of-bounds/null-pointer bugs and stack/heap overflow, validate input array sizes and indices, verify available memory and ulimits, and confirm library/MPI/BLAS build/ABI consistency; reproduce under a debugger (gdb/valgrind/ASan) on the smallest case."),
}

LOG_HINTS = {
    "lost atoms": "pressure-blowup",
    "nan": "nan",
    "zbrent": "nonconvergence",
    "sub-space-matrix": "nonconvergence",
    "out of memory": "out-of-memory",
    "oom-kill": "out-of-memory",
    "bad_alloc": "out-of-memory",
    "allocation failed": "out-of-memory",
    "killed": "incomplete-run",
    "segmentation fault": "crash",
    "sigsegv": "crash",
    "signal 11": "crash",
    "core dumped": "crash",
    "potcar": "bad-pseudopotential",
    "pair coeff": "missing-potential",
}


def _split(value: str) -> List[str]:
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def _load_log(path_value: str | None, log_text: str | None) -> str:
    if log_text:
        return log_text[:MAX_LOG_SIZE]
    if not path_value:
        return ""
    path = Path(path_value)
    if path.stat().st_size > MAX_LOG_SIZE:
        raise ValueError(f"log file exceeds size limit ({path.stat().st_size} > {MAX_LOG_SIZE})")
    return path.read_text(encoding="utf-8", errors="replace")[:MAX_LOG_SIZE]


def triage_failure(
    code: str,
    stage: str,
    symptoms: List[str],
    log_text: str,
    recent_change: str | None,
) -> Dict:
    if stage not in STAGES:
        raise ValueError(f"stage must be one of: {', '.join(sorted(STAGES))}")
    if not code.strip():
        raise ValueError("code must not be empty")
    if len(code) > MAX_CODE_LEN:
        raise ValueError(f"code must be at most {MAX_CODE_LEN} characters")
    if len(symptoms) > MAX_SYMPTOMS:
        raise ValueError(f"too many symptoms (max {MAX_SYMPTOMS})")
    for symptom in symptoms:
        if len(symptom) > MAX_SYMPTOM_LEN:
            raise ValueError(f"symptom too long (max {MAX_SYMPTOM_LEN} characters)")
    inferred = list(symptoms)
    lower_log = log_text.lower()
    for phrase, symptom in LOG_HINTS.items():
        if phrase in lower_log and symptom not in inferred:
            inferred.append(symptom)

    likely_causes = []
    for symptom in inferred:
        if symptom in PATTERNS:
            category, action = PATTERNS[symptom]
            likely_causes.append({"symptom": symptom, "category": category, "first_action": action})
        else:
            likely_causes.append(
                {
                    "symptom": symptom,
                    "category": "custom",
                    "first_action": "Preserve evidence and isolate the smallest reproducing case.",
                }
            )

    immediate_actions = [
        "copy logs, inputs, scheduler output, and executable version before rerun",
        "identify the first warning or error, not only the final crash line",
        "rerun a smaller case with extra diagnostics",
    ]
    if recent_change:
        immediate_actions.append(f"revert or isolate recent change: {recent_change}")

    retry_ladder = [
        "validate input files and units",
        "run a short minimized or equilibrated case",
        "tighten diagnostics and reduce timestep/load increment",
        "if memory-bound, reduce ranks-per-node or domain size and raise per-task memory",
        "change one solver or resource parameter at a time",
        "compare against a benchmark or previously working case",
    ]
    stop_conditions = [
        "required potential or pseudopotential cannot be verified",
        "results depend on arbitrary stabilizing changes",
        "conservation or physical bounds fail after numerical fixes",
        "the smallest reproducing case still fails without a clear cause",
    ]
    return {
        "likely_causes": likely_causes,
        "immediate_actions": immediate_actions,
        "retry_ladder": retry_ladder,
        "stop_conditions": stop_conditions,
        "evidence": {
            "code": code,
            "stage": stage,
            "symptoms": inferred,
            "log_excerpt": log_text[:500],
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code", required=True)
    parser.add_argument("--stage", default="unknown")
    parser.add_argument("--symptoms", default="")
    parser.add_argument("--log-file")
    parser.add_argument("--log-text")
    parser.add_argument("--recent-change")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        log_text = _load_log(args.log_file, args.log_text)
        results = triage_failure(
            code=args.code,
            stage=args.stage,
            symptoms=_split(args.symptoms),
            log_text=log_text,
            recent_change=args.recent_change,
        )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = {
        "inputs": {
            "code": args.code,
            "stage": args.stage,
            "symptoms": _split(args.symptoms),
            "log_file": args.log_file,
            "has_log_text": bool(args.log_text),
            "recent_change": args.recent_change,
        },
        "results": results,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for cause in results["likely_causes"]:
            print(f"{cause['symptom']}: {cause['first_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
