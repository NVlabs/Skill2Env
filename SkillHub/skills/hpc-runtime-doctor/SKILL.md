---
name: hpc-runtime-doctor
description: >
  Diagnose HPC runtime and scheduler problems for materials simulations,
  including MPI/OpenMP/GPU layout, modules, CUDA/Kokkos hints, scratch paths,
  walltime, job arrays, restart strategy, scheduler portability, and resource
  mismatch. Use when an ALREADY-SUBMITTED job failed, ran slowly, got killed, or
  behaved differently on a cluster than on a workstation. To author or vet a NEW
  submission script before running, use slurm-job-script-generator instead.
allowed-tools: Read, Bash, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.1.3"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-23"
  eval_cases: 3
  last_reviewed: "2026-06-24"
  standards:
    - "SchedMD SLURM sbatch / GRES specification (--gpus, --gpus-per-node, --gres=gpu:N, --cpus-per-task)"
    - "MPI Standard (MPI Forum) process/rank model"
    - "OpenMP API specification (OMP_NUM_THREADS thread/task affinity)"
    - "NVIDIA CUDA programming model and Kokkos performance-portability backend"
---

# HPC Runtime Doctor

## Goal

Turn cluster symptoms into a resource-layout diagnosis, environment checklist, and safe retry plan.

## Requirements

- Python 3.10+
- No external dependencies
- Works on Linux, macOS, and Windows

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Scheduler | SLURM, PBS, LSF, local | `slurm` |
| Nodes/tasks/threads | Runtime layout | `2 nodes, 128 tasks, 2 threads` |
| GPUs | Total (whole-job) GPUs via `--gpus`, or per node via `--gpus-per-node` | `--gpus 4` or `--gpus-per-node 1` |
| Symptoms | Observed failure | `oom,killed,slow-gpu` |
| MPI/OpenMP/GPU use | Parallel modes | `mpi+openmp+gpu` |
| Walltime | Requested time | `12:00:00` |
| Scratch | Whether scratch is used | `true` |

## Decision Guidance

- Check resource layout before changing physics settings.
- Confirm module/compiler/MPI/CUDA consistency before debugging solver behavior.
- Treat missing restart files and scratch cleanup as workflow failures, not physics failures.
- For GPU jobs, confirm the executable was built with the requested accelerator backend.

## Script Outputs

`scripts/hpc_runtime_doctor.py` emits:

- `resource_layout` (includes `tasks_per_node`, `total_cpus`, total `gpus`, and `gpus_per_node`)
- `diagnoses`
- `environment_checks`
- `retry_plan`
- `scheduler_notes`
- `warnings` (layout flags such as ranks-per-GPU oversubscription, OpenMP/thread mismatch, and uneven task placement)

In default (non-JSON) mode the script also prints the resource-layout summary, any
`warnings`, environment checks, and retry plan, so the most actionable items are never hidden.

## Workflow

`--gpus` is the **total** (whole-job) GPU count. Use `--gpus-per-node` (SLURM
`--gres=gpu:N` semantics) when you know the per-node allocation; total GPUs are then
`gpus_per_node * nodes` and it overrides `--gpus`.

```bash
python3 skills/hpc-deployment/hpc-runtime-doctor/scripts/hpc_runtime_doctor.py \
  --scheduler slurm \
  --nodes 2 \
  --tasks 128 \
  --cpus-per-task 2 \
  --gpus 4 \
  --symptoms oom,slow-gpu \
  --uses-mpi \
  --uses-openmp \
  --uses-gpu \
  --json
```

The example above shares 128 ranks across 4 GPUs (32 ranks/GPU), so the
`warnings` list surfaces `Many MPI ranks per GPU (32.0 ranks/GPU) may reduce GPU
efficiency.` The ranks-per-GPU check uses total ranks over total GPUs, so it fires
correctly on multi-node jobs (the threshold is 16 ranks/GPU).

## Error Handling

Invalid resource counts stop with exit code 2. Unknown symptoms are preserved as custom items for human review.

## Limitations

This skill does not query a live scheduler. It diagnoses from the submitted layout and symptoms.

## Verification checklist

- [ ] Recorded the script's `resource_layout` block and confirmed `tasks_per_node` is an integer (no fractional value) and `total_cpus` equals `tasks * cpus_per_task`; if `tasks_per_node` is fractional, the uneven-placement warning was triaged before retrying.
- [ ] For GPU jobs, recorded the resolved total `gpus` (and `gpus_per_node` when set) and computed ranks/GPU = `tasks / gpus`, confirming it is at or below the 16 ranks/GPU threshold or that the resulting `Many MPI ranks per GPU` warning was deliberately accepted.
- [ ] Reviewed every entry in the `warnings` list (OpenMP-with-`cpus_per_task=1`, GPU-requested-but-zero-GPUs, `tasks < nodes`, uneven placement, scratch-for-heavy-I/O) and resolved or justified each one rather than ignoring it.
- [ ] Completed the `environment_checks` items as real artifacts: captured the module list, executable path/version, MPI launcher-vs-library match, accelerator build flags (CUDA/Kokkos/OpenMP), and scheduler stdout/stderr.
- [ ] Mapped each observed symptom to a `diagnoses` entry and verified no symptom landed in the `custom` category unaddressed (every `custom` item had stderr/stdout/module list/command line collected for human review).
- [ ] Followed the `retry_plan`: reran the smallest reproducing case, changed exactly one resource variable, enabled restart/checkpoint, and saved the scheduler script plus environment snapshot alongside the results.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "It ran without crashing, so the layout is fine." | Run completion is not correctness. Review the `warnings` list and `resource_layout` -- oversubscription, uneven placement, or an idle GPU can silently slow or corrupt results without a crash. |
| "Per-node ranks fit the GPUs, so there's no oversubscription." | Oversubscription is total ranks over total GPUs, not per-node. The script computes `tasks / gpus`; a multi-node job can hide a high ranks/GPU value that only the unit-consistent check exposes. |
| "I passed `--gpus`, so per-node GPU count doesn't matter." | `--gpus` is the whole-job total. If the cluster allocates per node, use `--gpus-per-node` (SLURM `--gres=gpu:N`); it overrides `--gpus` and total becomes `gpus_per_node * nodes`. Mixing them up misreports ranks/GPU. |
| "The job was killed, so it's a physics/solver bug." | `killed`/`oom`/`timeout` are scheduler and resource categories, not physics. Check walltime, memory limits, and preemption from stdout/stderr before touching simulation parameters. |
| "An unknown symptom isn't in the rules, so I can skip it." | Unknown symptoms become `custom` diagnoses, not no-ops. Collect scheduler stderr/stdout, the module list, and the command line for human review -- silence is not a clean bill of health. |
| "Just change ranks, threads, and the build together to fix it faster." | Changing multiple variables at once makes the failure undiagnosable. The `retry_plan` mandates one variable at a time on the smallest reproducing case. |

## Security

### Input Validation

- Inputs are scalar CLI values and booleans only; there is no free-form code path.
- Resource counts (`--nodes`, `--tasks`, `--cpus-per-task`, `--gpus`, `--gpus-per-node`)
  are validated as integers (booleans rejected), required to be non-negative and finite,
  and capped at 1,000,000. `--nodes`, `--tasks`, and `--cpus-per-task` must additionally
  be at least 1. Out-of-range, non-integer, or zero values exit with code 2.
- The `--symptoms` string is capped at 64 comma-separated entries of at most 64 characters
  each; `--walltime` is capped at 32 characters. Oversized input exits with code 2.
- Symptoms are split, trimmed, and lower-cased. Unknown symptoms are not rejected: they are
  preserved as `custom` diagnoses for human review.
- `--scheduler` is accepted as a free-form string and is not checked against an allowlist;
  it is only echoed back in the resource layout.

### File Access

- The script reads and writes no files. All I/O is CLI args in and stdout out
  (indented JSON with `--json`, otherwise a human-readable summary); errors go to stderr.
- Because no paths are accepted or opened, there is no filesystem traversal surface and no
  path-sandboxing concern.

### Tool Restrictions

- `allowed-tools` is `Read, Bash, Write, Grep, Glob`.
- `Bash` is used only to run the bundled `scripts/hpc_runtime_doctor.py`.
- `Read`, `Grep`, and `Glob` are used to inspect the skill's own files and any logs or
  submission scripts the user points at; `Write` is used to record diagnosis notes or a
  retry plan when asked.

### Safety Measures

- No `eval`, `exec`, `os.system`, or `subprocess`; the script does not launch a scheduler
  or any external process and does not inspect environment variables.
- Argument parsing is handled by `argparse`, and machine-readable output is emitted as JSON.
- DoS exposure is bounded by the resource-count cap (1,000,000), the symptom caps
  (64 entries x 64 characters), and the walltime cap (32 characters).

## References

- See `references/hpc_runtime_patterns.md` for scheduler and runtime diagnosis patterns.

## Version History

- 1.1.3: Added a Verification checklist (evidence-based items tied to
  `resource_layout`, `warnings`, ranks/GPU, `environment_checks`, `diagnoses`,
  and the `retry_plan`) and a Common pitfalls & rationalizations table.
- 1.1.1: Discriminating evals -- each case now pins the script's specific output
  (exact ranks-per-GPU warning, diagnosis categories, resource-layout fields) via
  deterministic `script_checks`.
- 1.1.0: Unit-consistent ranks-per-GPU warning (total ranks / total GPUs), new
  `--gpus-per-node` argument, integer `tasks_per_node` with an uneven-placement warning,
  full human-readable (non-JSON) output, and input caps for resource counts, symptoms,
  and walltime.
- 1.0.0: Initial HPC runtime diagnosis skill.
