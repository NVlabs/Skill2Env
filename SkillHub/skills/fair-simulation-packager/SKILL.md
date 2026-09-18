---
name: fair-simulation-packager
description: >
  Create FAIR-minded reproducibility bundles for materials simulations by
  collecting input/output file inventories, hashes, units, engine versions,
  structure identifiers, provenance, and NOMAD/OPTIMADE/Materials Project
  friendly metadata. Use before publishing, sharing, archiving, or handing
  simulation results to another agent.
allowed-tools: Read, Bash, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-23"
  eval_cases: 3
  last_reviewed: "2026-06-24"
  standards:
    - "FAIR Guiding Principles (Wilkinson et al. 2016, Sci. Data)"
    - "OPTIMADE API specification"
    - "NOMAD Metainfo / Materials Project metadata schema"
    - "FIPS 180-4 Secure Hash Standard (SHA-256)"
---

# FAIR Simulation Packager

## Goal

Build a minimal reproducibility manifest for materials simulation results so another person or agent can understand what was run, with which inputs, and how outputs should be interpreted.

## Requirements

- Python 3.10+
- No external dependencies
- Works on Linux, macOS, and Windows

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Project name | Human-readable bundle name | `al-cu-diffusion-study` |
| Engine | Simulation code | `LAMMPS`, `VASP`, `MOOSE` |
| Input files | Files needed to rerun | `in.lammps,data.lmp` |
| Output files | Files needed to verify results | `log.lammps,traj.dump` |
| Structure ID | Database or local identifier | `mp-149` |
| Units | Field/unit mapping | `energy=eV,length=angstrom` |

## Decision Guidance

- Always include input files, output files, code version, and units.
- Include hashes for every file that exists locally.
- Include structure identifiers when using Materials Project, NOMAD, OPTIMADE, CIF, POSCAR, or internal database records.
- Record missing files as warnings instead of silently dropping them.

## Script Outputs

`scripts/fair_packager.py --json` prints an envelope with two top-level keys:

- `inputs`: the parsed CLI arguments echoed back (note: `inputs.inputs` is the raw
  comma-separated string passed via `--inputs`, not the per-file records).
- `results`: contains a single key `manifest`.

`results.manifest` contains these fields:

- `project_name`, `engine`, `engine_version`, `structure_id`, `units`
- `file_inventory` with `inputs` and `outputs`, each a list of per-file records
  (`path`, `exists`, and when the file exists, `size_bytes` and `sha256`)
- `missing_files`: paths that do not exist on disk
- `provenance` (`working_directory`, `manifest_schema`)
- `fair_checks`: `has_inputs`, `has_outputs`, `has_units`, `has_engine_version`, and
  `has_hashes_for_existing_files` (`true`/`false`, or `null` when no files exist so the
  check is not applicable)
- `recommended_next_steps`

Parse fields at `results.manifest.<field>`. When `--out PATH` is given, only the bare
`manifest` object (not the `inputs`/`results` envelope) is written to `PATH`.

## Workflow

```bash
python3 skills/data-management/fair-simulation-packager/scripts/fair_packager.py \
  --project-name al-cu-diffusion \
  --engine LAMMPS \
  --inputs in.lammps,data.lmp \
  --outputs log.lammps,traj.dump \
  --units energy=eV,length=angstrom,time=ps \
  --structure-id local:alcu-cell-001 \
  --json
```

Use `--out manifest.json` only when the user wants a manifest file written.

## Error Handling

Missing files are reported in `missing_files` (exit code 0). Invalid input stops with
exit code 2: malformed unit entries, fields containing control characters, fields longer
than 4096 characters, more than 1000 input or output entries, or a file larger than
500 MB. Note that ordinary file paths — including absolute paths and paths containing
`..` — are accepted and inventoried; the tool reads file contents only to compute
metadata and SHA-256 hashes.

## Limitations

This skill creates a metadata manifest. It does not upload to NOMAD, Materials Project, or an OPTIMADE provider.

## Verification checklist

- [ ] Confirmed `fair_checks.has_hashes_for_existing_files` is `true` (not `null` or `false`); a `null` means no listed file existed on disk, so re-run from the directory where the files actually live before trusting the manifest.
- [ ] Reviewed `missing_files` and confirmed it is empty, or recorded an explicit reason for each entry — every missing path means an input/output was named but not hashed, so the bundle is not reproducible as-is.
- [ ] Spot-checked at least one `sha256` in `results.manifest.file_inventory` against an independent `sha256sum`/`Get-FileHash` of the same file to confirm the recorded digest matches the bytes on disk.
- [ ] Confirmed `engine_version` is a real version string and not the default `"unknown"`; pass `--engine-version` so the bundle records the exact code build.
- [ ] Verified `units` is non-empty and every reported quantity (energy, length, time, etc.) has an entry, so downstream consumers do not have to guess the unit system.
- [ ] Confirmed `structure_id` is populated when a Materials Project / NOMAD / OPTIMADE / CIF / POSCAR structure was used, so the structure identity is recoverable.
- [ ] When `--out PATH` was used, opened `PATH` and confirmed it holds the bare `manifest` object (not the `inputs`/`results` envelope) and that no unintended path outside the working directory was written.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "It exited 0, so the bundle is complete." | Exit 0 only means no validation error; missing files are reported in `missing_files` with exit 0. Inspect `missing_files` and `fair_checks` before trusting completeness. |
| "`has_hashes_for_existing_files` is `null`, close enough to `true`." | `null` means *no listed file existed on disk* — nothing was hashed. Re-run from the correct directory so the files are found and actually digested. |
| "Skip `--engine-version`, the engine name is enough." | The script defaults `engine_version` to `"unknown"`, which silently breaks reproducibility. Always pass the concrete build/version. |
| "Parsing `inputs.inputs` from the JSON gives me the per-file records." | `inputs.inputs` is the raw comma-separated CLI string echoed back, not the records. Read per-file data from `results.manifest.file_inventory.inputs/outputs`. |
| "The manifest captures the structure, so the run is fully reproducible." | This skill only inventories files, hashes, units, and IDs. It does not record code commit, container digest, or parser versions — follow `recommended_next_steps` and add those yourself. |
| "Absolute paths or `..` will be rejected, so the inventory is sandboxed." | Paths are not sandboxed — absolute and `..` paths are inventoried as given, and `--out` can write outside the working directory. Verify the paths you pass are the intended ones. |

## Security

### Input Validation

- `--project-name` and `--engine` are required and must be non-empty after stripping
  whitespace; an empty value stops with exit code 2.
- `--project-name`, `--engine`, `--structure-id` (when given), and every file path are
  checked for control characters (`ord < 32`) and a 4096-character maximum length; either
  condition stops with exit code 2.
- `--inputs` and `--outputs` are split on commas and capped at 1000 entries each; more
  entries stop with exit code 2.
- `--units` entries must be `key=value`; both the key and the value must match the
  allowlist `^[A-Za-z0-9_.:/@+-]+$`. A missing `=` or a non-matching key/value stops with
  exit code 2.
- There are no numeric inputs, so no finite/positive numeric checks are performed.

### File Access

- The script reads each existing input/output file in 1 MB chunks to compute its
  `size_bytes` and SHA-256 hash; files that do not exist are recorded but not read.
- A file larger than 500 MB stops with exit code 2 before it is hashed.
- The script writes no files unless `--out PATH` is given, in which case it writes exactly
  one file (the bare manifest JSON) to that path; otherwise all output goes to stdout.
- Paths are not sandboxed: absolute paths and paths containing `..` are accepted for both
  the inventoried files and `--out`. If `--out` points outside the working directory, the
  file is written there as requested.

### Tool Restrictions

- `Bash` is used to run the bundled `scripts/fair_packager.py`.
- `Read`, `Write`, `Grep`, and `Glob` are declared so the skill can inspect the working
  directory and read or write manifest/metadata files when guiding the user; they are not
  invoked by the script itself, which performs all of its own file I/O directly.

### Safety Measures

- No `eval`, `exec`, `os.system`, or `subprocess` calls; the script does not shell out and
  parses arguments with `argparse`.
- Output is emitted as JSON via `json.dumps` (or a short plain-text summary without
  `--json`).
- DoS caps bound resource use: 500 MB per file, 1000 entries per input/output list, and
  4096 characters per field.

## References

- See `references/fair_manifest.md` for recommended manifest fields.

## Version History

- 1.2.0: Made eval cases discriminating by pinning the script's exact `--json`
  output (per-file `sha256`/`size_bytes`, `units`, `structure_id`, `engine_version`,
  `missing_files`, and the tri-state `has_hashes_for_existing_files`) against
  committed `evals/files/` fixtures.
- 1.1.0: Documented the real `--json` envelope shape; made
  `has_hashes_for_existing_files` tri-state (`null` when no files exist); added entry-count
  (1000) and field-length (4096) caps; corrected the Error Handling and Security wording
  to describe actual path behavior.
- 1.0.0: Initial FAIR simulation packaging skill.
