# SLURM `#SBATCH` directives (quick reference)

This reference is intentionally short and practical. SLURM policies vary by site; always check your cluster documentation.

## Core directives

- `#SBATCH --job-name=<name>`: Human-friendly name shown in `squeue`.
- `#SBATCH --time=<time>`: Walltime limit (common portable formats: `HH:MM:SS` or `D-HH:MM:SS`; SLURM also accepts minutes-only and other variants).
- `#SBATCH --partition=<partition>`: Queue/partition (if required).
- `#SBATCH --account=<account>`: Project/account (if required).
- `#SBATCH --nodes=<N>`: Number of nodes.
- `#SBATCH --ntasks=<R>`: Total MPI ranks/tasks.
- `#SBATCH --ntasks-per-node=<rpn>`: Ranks per node (if `--ntasks` is not set, total ranks is typically `nodes * rpn`).
- `#SBATCH --cpus-per-task=<t>`: CPU cores per rank (commonly used for OpenMP threads).
- `#SBATCH --mem=<size>`: Memory per node (integer MB by default, or with suffix `K/M/G/T`, e.g. `32G`; `0` often means “all memory on node”).
- `#SBATCH --mem-per-cpu=<size>`: Memory per CPU core (same units as `--mem`).

## GPUs

GPU directives differ across clusters. A common portable pattern is:

- `#SBATCH --gres=gpu:<count>` (or `gpu:<type>:<count>`)

Examples:

- `#SBATCH --gres=gpu:4`
- `#SBATCH --gres=gpu:a100:4`

## Output and diagnostics

- `#SBATCH --output=slurm-%j.out`: Stdout file (`%j` is job id).
- `#SBATCH --error=slurm-%j.err`: Stderr file.

Inside the script, useful diagnostics:

```bash
echo "job_id=$SLURM_JOB_ID"
echo "nodes=$SLURM_JOB_NODELIST"
echo "submit_dir=$SLURM_SUBMIT_DIR"
```

## Directive placement (important)

Per SchedMD's `sbatch` specification: *"Once the first non-comment, non-whitespace
line has been reached in the script, no more `#SBATCH` directives will be processed."*
Therefore **all `#SBATCH` directives must appear immediately after the shebang and
before any executable command** (including `set -euo pipefail`). A directive placed
after the first real command is silently ignored, and the job falls back to cluster
defaults.

## Common mapping advice

- **MPI-only:** `cpus-per-task=1`, increase `ntasks`.
- **Hybrid MPI+OpenMP:** set `cpus-per-task = OMP_NUM_THREADS`, reduce `ntasks`.
- Prefer `srun` inside SLURM allocations; it integrates with SLURM’s task placement.
