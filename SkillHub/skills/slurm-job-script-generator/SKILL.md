---
name: slurm-job-script-generator
description: >
  Generate correct, copy-pasteable SLURM sbatch job scripts and sanity-check
  HPC resource requests — configure nodes, MPI tasks, OpenMP threads, memory
  (per-node or per-cpu), GPUs, walltime, partitions, modules, and environment
  variables, with automatic detection of conflicting directives and
  oversubscription. Use when preparing a SLURM submission script, deciding
  between pure MPI and hybrid MPI+OpenMP layouts, standardizing #SBATCH
  directives across a team, debugging why a job won't launch or gets killed,
  or setting up GPU-accelerated simulation jobs, even if the user only says
  "I need to run this on the cluster" or "my job keeps getting killed."
allowed-tools: Read, Bash, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 5
  last_reviewed: "2026-06-23"
  standards:
    - "SchedMD SLURM sbatch specification (#SBATCH directives, directive-ordering rule, --mem units, --time formats)"
    - "SchedMD SLURM srun task-launch model (srun --ntasks/--cpus-per-task placement, --gpu-bind/--ntasks-per-gpu)"
    - "MPI standard (MPI Forum) and OpenMP API for hybrid MPI+OpenMP layout (OMP_NUM_THREADS = cpus-per-task)"
---

# SLURM Job Script Generator

## Goal

Generate a correct, copy-pasteable SLURM job script (`.sbatch`) for running a simulation, and surface common configuration mistakes (bad walltime format, conflicting memory flags, oversubscription hints).

## Requirements

- Python 3.10+
- No external dependencies (Python standard library only)
- Works on Linux, macOS, and Windows (script generation only)

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Job name | Short identifier for the job | `phasefield-strong-scaling` |
| Walltime | SLURM time limit | `00:30:00` |
| Partition | Cluster partition/queue (if required) | `compute` |
| Account | Project/account (if required) | `matsim` |
| Nodes | Number of nodes to allocate | `2` |
| MPI tasks | Total tasks, or tasks per node | `128` or `64` per node |
| Threads | CPUs per task (OpenMP threads) | `2` |
| Memory | `--mem` or `--mem-per-cpu` (cluster policy dependent) | `32G` |
| GPUs | GPUs per node (optional) | `4` |
| Working directory | Where the run should execute | `$SLURM_SUBMIT_DIR` |
| Modules | Environment modules to load (optional) | `gcc/12`, `openmpi/4.1` |
| Run command | The command to launch under SLURM | `./simulate --config cfg.json` |

## Decision Guidance

### MPI vs MPI+OpenMP layout

```
Does the code use OpenMP / threading?
├── NO  → Use MPI-only: cpus-per-task=1
└── YES → Use hybrid: set cpus-per-task = threads per MPI rank
          and export OMP_NUM_THREADS = cpus-per-task
```

**Rule of thumb:** if you see diminishing strong-scaling efficiency at high MPI ranks, try fewer ranks with more threads per rank (and measure).

### Memory flag selection

- Use **either** `--mem` (per node) **or** `--mem-per-cpu` (per CPU), not both.
- Follow your cluster’s documentation; some sites enforce one style.
- SLURM `--mem` units are integer MB by default, or an integer with suffix `K/M/G/T` (and `--mem=0` commonly means “all memory on node”).

### Launcher selection (avoid double-wrapping)

- By default (`--launcher srun`) the generator prepends `srun --ntasks=N --cpus-per-task=T` to your run command so it inherits SLURM task placement.
- **If your run command already starts with `srun`, `mpirun`, or `mpiexec`, pass `--launcher none`** so the generator does not double-wrap it. Wrapping `srun` around `mpirun` launches N independent copies of `mpirun` (each spawning its own MPI world); wrapping `srun` around `srun` is malformed.
- As a safety net, the generator auto-detects a leading launcher (`srun`, `mpirun`, `mpiexec`, `mpiexec.hydra`, `orterun`, `aprun`, `jsrun`) and falls back to no-wrap, emitting a warning that recommends `--launcher none`.

### GPU layout

- Ranks-per-GPU = `total_ranks / (nodes * gpus_per_node)`. When `--gpus-per-node` is set the generator reports `results.derived.total_gpus` and `results.derived.ranks_per_gpu`.
- Aim to map ranks evenly to devices. If `ntasks` is **not** divisible by the total number of GPUs, the generator emits a "task-to-GPU ratio is not an integer" warning; either adjust `ntasks`/GPUs or document intentional sharing (e.g. NVIDIA MPS).
- Consider binding options such as `--gpu-bind=closest` or `--ntasks-per-gpu` (passed via your run command / `--srun-extra`). GPU and QoS policies are site-specific — confirm with your cluster docs.

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/slurm_script_generator.py` | `results.script`, `results.directives`, `results.derived`, `results.warnings`, `results.run_line` |

`results.derived` reports `ntasks`, `ntasks_per_node`, `cpus_total_requested`, and (when applicable) `cores_per_node`, `cpus_per_node_requested`, `total_gpus`, and `ranks_per_gpu`. `results.warnings` may include CPU oversubscription, task-to-GPU ratio, and double-launcher warnings.

## Workflow

1. Gather cluster constraints (partition/account, GPU policy, memory policy).
2. Choose a process layout (MPI-only vs hybrid MPI+OpenMP).
3. Generate the script with `slurm_script_generator.py`.
4. Inspect warnings (conflicts, suspicious layouts).
5. Save the generated script as `job.sbatch`.
6. Submit with `sbatch job.sbatch` and monitor with `squeue`.

## CLI Examples

```bash
# Preview a job script (prints to stdout)
python3 skills/hpc-deployment/slurm-job-script-generator/scripts/slurm_script_generator.py \
  --job-name phasefield \
  --time 00:10:00 \
  --partition compute \
  --nodes 1 \
  --ntasks-per-node 8 \
  --cpus-per-task 2 \
  --mem 16G \
  --module gcc/12 \
  --module openmpi/4.1 \
  -- \
  ./simulate --config config.json

# Write to a file and also emit structured JSON
python3 skills/hpc-deployment/slurm-job-script-generator/scripts/slurm_script_generator.py \
  --job-name phasefield \
  --time 00:10:00 \
  --nodes 1 \
  --ntasks 16 \
  --cpus-per-task 1 \
  --out job.sbatch \
  --json \
  -- \
  /bin/echo hello
```

## Conversational Workflow Example

**User**: I need an `sbatch` script for my MPI simulation. I want 2 nodes, 64 ranks per node, 2 OpenMP threads per rank, and 2 hours.

**Agent workflow**:
1. Confirm partition/account and whether GPUs are needed.
2. Generate a hybrid job script:
   ```bash
   python3 scripts/slurm_script_generator.py --job-name run --time 02:00:00 --nodes 2 --ntasks-per-node 64 --cpus-per-task 2 -- ./simulate
   ```
3. Explain the mapping:
   - Total ranks = 128
   - Threads per rank = 2 (`OMP_NUM_THREADS=2`)
4. If the user provides node core counts, sanity-check oversubscription using `--cores-per-node`.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `time must be HH:MM:SS or D-HH:MM:SS` | Bad walltime format | Use `00:30:00` or `1-00:00:00` |
| `nodes must be positive` | Non-positive nodes | Provide `--nodes >= 1` |
| `Provide either --mem or --mem-per-cpu, not both` | Conflicting memory directives | Choose one memory style |
| `Provide a run command after --` | Missing launch command | Add `-- ./simulate ...` |
| `--partition must match /^[A-Za-z0-9]...` | Partition/account/qos/constraint/reservation contains spaces or shell metacharacters | Use a plain identifier |
| `module must match /^[A-Za-z0-9]...` | Module name contains shell metacharacters | Use e.g. `gcc/12`, `openmpi/4.1` |
| `nodes must be <= 100000 (got ...)` | Integer request exceeds the sanity upper bound | Re-check the requested value |

## Verification checklist

- [ ] Confirmed the generated `results.script` places **every** `#SBATCH` directive immediately after the shebang and before `set -euo pipefail` (open the script and check the first real command line) — a directive after the first command is silently ignored by SLURM.
- [ ] Inspected `results.warnings` and confirmed it is empty, or recorded each warning (CPU oversubscription, non-integer task-to-GPU ratio, double-launcher) with a deliberate justification for ignoring it.
- [ ] Recorded `results.derived.cpus_total_requested` (= `ntasks * cpus-per-task`) and, when `--cores-per-node` was supplied, confirmed `cpus_per_node_requested <= cores_per_node` so the node is not oversubscribed.
- [ ] For hybrid runs, verified the script's `export OMP_NUM_THREADS` value equals `results.derived` `cpus_per_task` (the generator sets them equal — confirm that matches the intended threads-per-rank).
- [ ] For GPU jobs, recorded `results.derived.total_gpus` and `ranks_per_gpu` and confirmed `ranks_per_gpu` is the intended integer (or documented intentional sharing such as MPS).
- [ ] Verified `results.run_line` is not double-wrapped: if the run command already starts with `srun`/`mpirun`/`mpiexec`/`orterun`/`aprun`/`jsrun`, confirmed `--launcher none` was used (or the auto-detect warning fired) so SLURM does not launch N independent copies.
- [ ] Cross-checked the partition, account, QoS, memory style (`--mem` vs `--mem-per-cpu`), and GPU directive against the actual cluster's documented policy — the generator only validates internal consistency, never site policy.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "It generated a script with no errors, so the resources are correct." | The generator only checks internal consistency — it never queries the cluster. Validate partition/account/QoS/memory style and GPU directives against your site's actual docs before submitting. |
| "I'll keep the `srun`/`mpirun` already in my run command and let the generator wrap it." | Wrapping `srun` around `mpirun` launches N independent `mpirun` processes (each its own MPI world); `srun` around `srun` is malformed. Pass `--launcher none`, and confirm the auto-detect warning fired in `results.warnings`. |
| "I requested the nodes I want, so the job will use them all." | If any `#SBATCH` directive slips below the first command it is silently dropped and the job falls back to cluster defaults. Re-read the generated script and confirm all directives precede `set -euo pipefail`. |
| "ntasks doesn't divide the GPU count, but it ran, so it's fine." | A non-integer `ranks_per_gpu` means ranks map unevenly to devices (idle/oversubscribed GPUs). The generator emits a task-to-GPU warning — fix `ntasks`/GPUs or explicitly document MPS sharing. |
| "I set high `ntasks-per-node` because more ranks is faster." | Without `--cores-per-node` the generator can't catch oversubscription, and `ntasks-per-node*cpus-per-task` exceeding physical cores degrades performance. Pass `--cores-per-node` and check `cpus_per_node_requested`. |
| "I'll set both `--mem` and `--mem-per-cpu` to be safe." | These are mutually exclusive; the generator rejects supplying both. Pick the one your cluster's policy enforces. |
| "OMP_NUM_THREADS doesn't matter for an MPI-only code." | The generator always exports `OMP_NUM_THREADS=cpus-per-task`; for MPI-only runs keep `--cpus-per-task=1` so threaded libraries don't silently oversubscribe cores. |

## Security

### Input Validation
- `--time` is validated against strict `HH:MM:SS` or `D-HH:MM:SS` format via regex (minutes/seconds in `[00,59]`)
- `--nodes`, `--ntasks`, `--ntasks-per-node`, `--cpus-per-task`, `--gpus-per-node`, `--cores-per-node` are validated as positive integers with generous upper bounds (e.g. nodes ≤ 100000, ntasks ≤ 10000000, cpus-per-task ≤ 4096, gpus-per-node ≤ 64); the derived total `ntasks = nodes * ntasks-per-node` is also bounds-checked
- `--mem` and `--mem-per-cpu` are validated against SLURM's accepted format (`^[0-9]+([KMGT])?$`); providing both simultaneously is rejected
- `--job-name` is validated against `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$` (no spaces or shell metacharacters)
- `--partition`, `--account`, `--qos`, `--constraint`, `--reservation`, and `--gpu-type` are validated against a safe-character allowlist `^[A-Za-z0-9][A-Za-z0-9._:,+-]{0,127}$` before being emitted into `#SBATCH` directives
- `--module` values are validated against `^[A-Za-z0-9][A-Za-z0-9._/+-]{0,127}$` to prevent shell injection (no `;`, `|`, `&`, backticks, `$`, or whitespace)
- `--env` keys must be valid shell identifiers (`^[A-Za-z_][A-Za-z0-9_]*$`); values are shell-quoted in the generated `export` lines
- `--srun-extra` is tokenized with `shlex.split` and each token is re-quoted with `shlex.quote`, so it cannot inject shell syntax (`;`, `|`, `&`, `$`, ...) into the run line
- Invalid input causes the CLI to print a message to stderr and exit with code `2`

### File Access
- The script reads no external files; all inputs are provided via CLI arguments
- `--out` writes the generated sbatch script to a single specified file path
- The generated script is a plain-text shell script with `#SBATCH` directives; it contains no dynamically generated code

### Tool Restrictions
- **Read**: Used to inspect script source, references, and existing job scripts
- **Bash**: Used to execute `slurm_script_generator.py` with explicit argument lists; the generated script itself is NOT executed by the agent
- **Write**: Used to save the generated `.sbatch` file; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate existing scripts, configs, and cluster documentation

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- The run command (after `--`) is shell-quoted token-by-token into the generated script but is never executed by the skill itself
- Module names, `--srun-extra` tokens, and identifier-style fields are sanitized/quoted to prevent injection into `module load`, the `srun` invocation, or `#SBATCH` directives
- Generated scripts place all `#SBATCH` directives immediately after the shebang (before any executable command, so SLURM does not stop parsing them) and use `set -euo pipefail` for safe shell execution on the cluster

## Limitations

- Does not query cluster hardware or site policies; it can only validate internal consistency.
- SLURM installations vary (GPU directives, QoS rules, partitions). Adjust directives for your site.

## References

- `references/slurm_directives.md` - Common `#SBATCH` directives and mapping tips

## Version History

- **v1.2.2** (2026-06-24): Added "Verification checklist" and "Common pitfalls & rationalizations" sections covering directive ordering, oversubscription, task-to-GPU mapping, launcher double-wrapping, and the generator's internal-consistency-only scope.
- **v1.2.0** (2026-06-23): Fixed critical directive-ordering bug (all `#SBATCH` lines now precede `set -euo pipefail`), avoided double-launcher wrapping when the run command already starts with `srun`/`mpirun`, added GPU task-to-GPU ratio warning and layout guidance, hardened input validation (integer upper bounds, partition/account/qos/constraint/reservation/gpu-type allowlists, module sanitization, `--srun-extra` quoting), escaped `%j` in `--help`, and corrected the Security and output documentation.
- **v1.1.0** (2026-03-26): Optimized description for discovery, added eval suite, security review, standardized metadata, and CHANGELOG.
- **v1.0.0** (2026-02-25): Initial SLURM job script generator
