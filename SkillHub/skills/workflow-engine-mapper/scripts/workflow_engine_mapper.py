#!/usr/bin/env python3
"""Map a materials simulation task to an appropriate workflow engine."""
from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Dict, List


MAX_RUNS = 1_000_000
MAX_TASK_LEN = 2000
MAX_FIELD_LEN = 100


def _positive_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a positive integer")
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    if value > MAX_RUNS:
        raise ValueError(f"{name} must not exceed {MAX_RUNS}")
    return value


def _bounded_text(value: str, name: str, max_len: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    if len(value) > max_len:
        raise ValueError(f"{name} must not exceed {max_len} characters")
    return value


def recommend_engine(
    task: str,
    code: str,
    runs: int,
    needs_provenance: bool,
    needs_restart: bool,
    hpc: bool,
    preferred: str,
) -> Dict:
    _positive_int(runs, "runs")
    _bounded_text(task, "task", MAX_TASK_LEN)
    _bounded_text(code, "code", MAX_FIELD_LEN)
    _bounded_text(preferred, "preferred", MAX_FIELD_LEN)
    if not task.strip():
        raise ValueError("task must not be empty")
    code_key = code.lower().strip()
    preferred_key = preferred.lower().strip()
    allowed = {"auto", "one-off", "jobflow", "atomate2", "aiida", "pyiron"}
    if preferred_key not in allowed:
        raise ValueError(f"preferred must be one of: {', '.join(sorted(allowed))}")

    if preferred_key != "auto":
        engine = preferred_key
    elif runs < 5 and not needs_provenance and not hpc:
        engine = "one-off"
    elif needs_provenance and (hpc or runs >= 50):
        engine = "aiida"
    elif code_key in {"vasp", "qe", "cp2k", "forcefield"} and runs >= 10:
        engine = "atomate2"
    elif code_key in {"ase", "lammps"} and not needs_provenance:
        engine = "pyiron"
    else:
        engine = "jobflow"

    task_lower = task.lower()
    branch = any(word in task_lower for word in ["dos", "band", "phonon", "static"])
    sweep = any(word in task_lower for word in ["screen", "sweep", "campaign", "many", "batch"])
    if branch and sweep:
        dag_pattern = "map over structures -> (relax -> static -> property branches) -> collect -> rank"
    elif sweep:
        dag_pattern = "map over structures/parameters -> collect -> rank"
    elif branch:
        dag_pattern = "relax -> static -> property branches"
    else:
        dag_pattern = "linear"
    if needs_restart:
        dag_pattern += " with restart checkpoints"

    migration_triggers: List[str] = []
    if engine == "one-off":
        migration_triggers.append(
            "migrate to a workflow engine once results will be compared, "
            "published, screened, or resumed, or runs reach ~5+"
        )
    if runs >= 20:
        migration_triggers.append("run count is high enough to need structured metadata")
    if needs_restart:
        migration_triggers.append("restartability is a first-class requirement")
    if needs_provenance:
        migration_triggers.append("results need an auditable provenance trail")
    if hpc:
        migration_triggers.append("remote scheduler interaction should be explicit")

    return {
        "recommended_engine": engine,
        "dag_pattern": dag_pattern,
        "provenance_requirements": {
            "store_inputs": True,
            "store_outputs": True,
            "store_code_version": needs_provenance or runs >= 10,
            "store_environment": hpc or needs_provenance,
        },
        "restart_strategy": {
            "needed": needs_restart,
            "checkpoint_jobs": needs_restart or runs >= 20,
            "idempotent_outputs": True,
            "resume_by_job_id_or_name": engine in {"aiida", "jobflow", "atomate2", "pyiron"},
        },
        "storage_layout": [
            "inputs/",
            "runs/<job-id>/",
            "outputs/",
            "metadata/workflow.json",
            "reports/",
        ],
        "migration_triggers": migration_triggers,
        "notes": [
            "Keep one-off scripts only for exploratory work.",
            "Promote to a workflow engine before running production sweeps.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--code", default="general")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--needs-provenance", action="store_true")
    parser.add_argument("--needs-restart", action="store_true")
    parser.add_argument("--hpc", action="store_true")
    parser.add_argument("--preferred", default="auto")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if not math.isfinite(float(args.runs)):
            raise ValueError("runs must be finite")
        results = recommend_engine(
            task=args.task,
            code=args.code,
            runs=args.runs,
            needs_provenance=args.needs_provenance,
            needs_restart=args.needs_restart,
            hpc=args.hpc,
            preferred=args.preferred,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = {
        "inputs": {
            "task": args.task,
            "code": args.code,
            "runs": args.runs,
            "needs_provenance": args.needs_provenance,
            "needs_restart": args.needs_restart,
            "hpc": args.hpc,
            "preferred": args.preferred,
        },
        "results": results,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Recommended engine: {results['recommended_engine']}")
        print(f"DAG: {results['dag_pattern']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
