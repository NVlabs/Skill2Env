# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- "Verification checklist" section (7 evidence-based items) requiring agents to
  record concrete generator outputs (`results.script` directive ordering,
  `results.warnings`, `results.derived.cpus_total_requested`, `OMP_NUM_THREADS`,
  `total_gpus`/`ranks_per_gpu`, `results.run_line` launcher) and to cross-check
  site policy before submitting.
- "Common pitfalls & rationalizations" table (7 rows) covering internal-only
  validation scope, launcher double-wrapping, directive ordering, non-integer
  task-to-GPU ratios, oversubscription, mutually exclusive memory flags, and
  `OMP_NUM_THREADS` for MPI-only codes.

## [1.2.0] - 2026-06-23

### Fixed
- **Critical:** Generated scripts placed `set -euo pipefail` before the `#SBATCH`
  directives, so SLURM stopped parsing and ignored every requested resource. All
  `#SBATCH` directives now immediately follow the shebang and precede any
  executable command.
- Avoided emitting a double launcher: when the run command already starts with a
  launcher (`srun`, `mpirun`, `mpiexec`, `mpiexec.hydra`, `orterun`, `aprun`,
  `jsrun`) the generator no longer wraps it in `srun` and instead emits a warning
  recommending `--launcher none`.
- Escaped `%j` in the `--output`/`--error` help strings so `--help` no longer
  crashes with `ValueError: unsupported format character 'j'`.

### Added
- GPU layout sanity check: derives `total_gpus` and `ranks_per_gpu`, and warns
  when `ntasks` is not divisible by the total number of GPUs.
- GPU-layout and launcher-selection guidance in SKILL.md Decision Guidance.

### Security
- Integer requests (`--nodes`, `--ntasks`, `--ntasks-per-node`, `--cpus-per-task`,
  `--gpus-per-node`, `--cores-per-node`) now enforce generous upper bounds.
- `--partition`, `--account`, `--qos`, `--constraint`, `--reservation`, and
  `--gpu-type` are validated against a safe-character allowlist before being
  emitted into `#SBATCH` directives.
- `--module` values are validated against a strict allowlist.
- `--srun-extra` is tokenized with `shlex.split` and re-quoted with
  `shlex.quote`, preventing shell-metacharacter injection into the run line.
- Corrected the SKILL.md Security section to match the enforced validation.

## [1.1.0] - 2026-03-26

### Added
- Optimized description for agent discovery (agentskills.io compliant)
- Evaluation suite with test cases and assertions
- Security review documentation with risk tier classification
- Standardized metadata block (author, version, security_tier, tested_with)
- This CHANGELOG file

### Changed
- Updated SKILL.md frontmatter with metadata block

## [1.0.0] - 2026-02-25

### Added
- Initial release
- SLURM sbatch script generation with MPI/OpenMP/GPU support, resource conflict detection, oversubscription warnings
- CLI scripts with --json output and argparse interface
- Reference documentation
