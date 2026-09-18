#!/usr/bin/env python3
"""Diagnose common HPC runtime and scheduler issues."""
from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Dict, List


SYMPTOM_RULES = {
    "oom": ("memory", "Increase memory, reduce ranks per node, or reduce per-rank memory footprint."),
    "killed": ("scheduler", "Check walltime, memory limits, preemption policy, and stdout/stderr."),
    "timeout": ("walltime", "Add checkpoint/restart and request walltime based on measured throughput."),
    "slow-gpu": ("gpu", "Confirm GPU build, device binding, CPU/GPU balance, and accelerator package."),
    "mpi-hang": ("mpi", "Check MPI implementation mismatch, fabric settings, and collective imbalance."),
    "filesystem": ("io", "Move heavy I/O to scratch and reduce metadata-heavy small-file writes."),
    "module": ("environment", "Capture module list and verify compiler/MPI/CUDA ABI compatibility."),
    "restart-missing": ("restart", "Write restart files before walltime and copy them out of scratch."),
}

# Lightweight input caps to keep validation bounded and reject absurd values.
MAX_RESOURCE_COUNT = 1_000_000
MAX_SYMPTOMS = 64
MAX_SYMPTOM_LEN = 64
MAX_WALLTIME_LEN = 32


def _positive_int(value: int, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    if not math.isfinite(float(value)) or value < 0:
        raise ValueError(f"{name} must be a non-negative finite integer")
    if value > MAX_RESOURCE_COUNT:
        raise ValueError(f"{name} must be <= {MAX_RESOURCE_COUNT}")
    return value


def _split_symptoms(value: str) -> List[str]:
    if len(value) > MAX_SYMPTOMS * (MAX_SYMPTOM_LEN + 1):
        raise ValueError(f"symptoms string is too long (max {MAX_SYMPTOMS} entries)")
    items = [item.strip().lower() for item in value.split(",") if item.strip()]
    if len(items) > MAX_SYMPTOMS:
        raise ValueError(f"too many symptoms supplied (max {MAX_SYMPTOMS})")
    for item in items:
        if len(item) > MAX_SYMPTOM_LEN:
            raise ValueError(f"symptom '{item[:16]}...' exceeds {MAX_SYMPTOM_LEN} characters")
    return items


def diagnose_hpc(
    scheduler: str,
    nodes: int,
    tasks: int,
    cpus_per_task: int,
    gpus: int,
    symptoms: List[str],
    uses_mpi: bool,
    uses_openmp: bool,
    uses_gpu: bool,
    walltime: str | None,
    scratch: bool,
    gpus_per_node: int = 0,
) -> Dict:
    for name, value in {
        "nodes": nodes,
        "tasks": tasks,
        "cpus_per_task": cpus_per_task,
        "gpus": gpus,
        "gpus_per_node": gpus_per_node,
    }.items():
        _positive_int(value, name)
    if nodes == 0:
        raise ValueError("nodes must be at least 1")
    if tasks == 0:
        raise ValueError("tasks must be at least 1")
    if cpus_per_task == 0:
        raise ValueError("cpus_per_task must be at least 1")
    if walltime is not None and len(walltime) > MAX_WALLTIME_LEN:
        raise ValueError(f"walltime must be <= {MAX_WALLTIME_LEN} characters")

    # tasks_per_node: report an int when divisible, otherwise keep the float so the
    # uneven layout is visible. A real scheduler treats a non-divisible layout as a
    # placement issue, so we surface it as a warning (not a hard rejection).
    quotient, remainder = divmod(tasks, nodes)
    tasks_per_node = quotient if remainder == 0 else tasks / nodes
    total_cpus = tasks * cpus_per_task

    # Resolve total GPU count. --gpus is the WHOLE-JOB GPU count. When --gpus-per-node
    # is supplied it takes precedence and total = gpus_per_node * nodes (SLURM
    # --gres=gpu:N semantics, where N is per node).
    if gpus_per_node:
        total_gpus = gpus_per_node * nodes
    else:
        total_gpus = gpus

    diagnoses = []
    for symptom in symptoms:
        if symptom in SYMPTOM_RULES:
            category, action = SYMPTOM_RULES[symptom]
            diagnoses.append({"symptom": symptom, "category": category, "recommended_action": action})
        else:
            diagnoses.append(
                {
                    "symptom": symptom,
                    "category": "custom",
                    "recommended_action": "Collect scheduler stderr, stdout, module list, and command line.",
                }
            )

    warnings: List[str] = []
    if uses_openmp and cpus_per_task == 1:
        warnings.append("OpenMP requested but cpus_per_task is 1.")
    if uses_gpu and total_gpus == 0:
        warnings.append("GPU execution requested but no GPUs are allocated.")
    if uses_mpi and tasks < nodes:
        warnings.append("MPI task count is lower than node count; check scheduler layout.")
    if remainder != 0:
        warnings.append(
            f"tasks ({tasks}) is not evenly divisible by nodes ({nodes}); ranks will be "
            "placed unevenly across nodes, risking load imbalance -- set a balanced "
            "--ntasks-per-node or adjust --tasks/--nodes."
        )
    # Unit-consistent GPU oversubscription check: total ranks per total GPU.
    if total_gpus:
        ranks_per_gpu = tasks / total_gpus
        if ranks_per_gpu > 16:
            warnings.append(
                f"Many MPI ranks per GPU ({ranks_per_gpu:.1f} ranks/GPU) may reduce GPU efficiency."
            )
    if not scratch and ("filesystem" in symptoms or tasks >= 64):
        warnings.append("Large parallel jobs should use node-local or parallel scratch for heavy I/O.")

    return {
        "resource_layout": {
            "scheduler": scheduler,
            "nodes": nodes,
            "tasks": tasks,
            "tasks_per_node": tasks_per_node,
            "cpus_per_task": cpus_per_task,
            "total_cpus": total_cpus,
            "gpus": total_gpus,
            "gpus_per_node": gpus_per_node if gpus_per_node else None,
            "walltime": walltime,
        },
        "diagnoses": diagnoses,
        "environment_checks": [
            "record module list and loaded compiler/MPI stack",
            "record executable path and version",
            "verify MPI launcher matches the loaded MPI",
            "verify CUDA/Kokkos/OpenMP build flags when using accelerators",
            "capture scheduler stdout and stderr",
        ],
        "retry_plan": [
            "rerun the smallest reproducing case",
            "enable frequent restart/checkpoint files",
            "change one resource variable at a time",
            "save scheduler script and environment snapshot with results",
        ],
        "scheduler_notes": [
            "SLURM: compare --ntasks, --ntasks-per-node, and --cpus-per-task",
            "PBS/LSF: translate resources carefully; names differ across sites",
            "GPU queues often require account, partition, constraint, or gres flags",
        ],
        "warnings": warnings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scheduler", default="slurm")
    parser.add_argument("--nodes", type=int, default=1)
    parser.add_argument("--tasks", type=int, default=1)
    parser.add_argument("--cpus-per-task", type=int, default=1)
    parser.add_argument(
        "--gpus",
        type=int,
        default=0,
        help="Total (whole-job) GPU count.",
    )
    parser.add_argument(
        "--gpus-per-node",
        type=int,
        default=0,
        help="GPUs per node (SLURM --gres=gpu:N). When set, total GPUs = value * nodes "
        "and this overrides --gpus.",
    )
    parser.add_argument("--symptoms", default="")
    parser.add_argument("--uses-mpi", action="store_true")
    parser.add_argument("--uses-openmp", action="store_true")
    parser.add_argument("--uses-gpu", action="store_true")
    parser.add_argument("--walltime")
    parser.add_argument("--scratch", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def _print_human_readable(results: Dict) -> None:
    layout = results["resource_layout"]
    print(
        "RESOURCE LAYOUT: "
        f"scheduler={layout['scheduler']} nodes={layout['nodes']} "
        f"tasks={layout['tasks']} tasks_per_node={layout['tasks_per_node']} "
        f"cpus_per_task={layout['cpus_per_task']} total_cpus={layout['total_cpus']} "
        f"gpus={layout['gpus']}"
    )

    if not results["diagnoses"]:
        print(
            "No symptoms supplied; showing resource layout, warnings, "
            "environment checks, and retry plan."
        )
    else:
        print("DIAGNOSES:")
        for item in results["diagnoses"]:
            print(f"- {item['symptom']}: {item['recommended_action']}")

    if results["warnings"]:
        print("WARNINGS:")
        for warning in results["warnings"]:
            print(f"- {warning}")

    print("ENVIRONMENT CHECKS:")
    for check in results["environment_checks"]:
        print(f"- {check}")

    print("RETRY PLAN:")
    for step in results["retry_plan"]:
        print(f"- {step}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        symptoms = _split_symptoms(args.symptoms)
        results = diagnose_hpc(
            scheduler=args.scheduler,
            nodes=args.nodes,
            tasks=args.tasks,
            cpus_per_task=args.cpus_per_task,
            gpus=args.gpus,
            symptoms=symptoms,
            uses_mpi=args.uses_mpi,
            uses_openmp=args.uses_openmp,
            uses_gpu=args.uses_gpu,
            walltime=args.walltime,
            scratch=args.scratch,
            gpus_per_node=args.gpus_per_node,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = {"inputs": vars(args), "results": results}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_human_readable(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
