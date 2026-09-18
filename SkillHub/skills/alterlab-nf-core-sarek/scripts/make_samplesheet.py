#!/usr/bin/env python3
"""Build and validate an nf-core/sarek 3.8.1 `--input` samplesheet from a FASTQ dir.

Generates the FASTQ-entry samplesheet for `--step mapping`, the common starting
point. Pairs R1/R2 files in a directory, fills the required columns
(patient, sample, lane, fastq_1, fastq_2) and the optional sex/status columns,
validates the schema, and writes (or appends to) a CSV ready for:

    nextflow run nf-core/sarek -r 3.8.1 -profile docker \\
        --input samplesheet.csv --outdir ./results \\
        --genome GATK.GRCh38 --tools haplotypecaller

Schema source: https://nf-co.re/sarek/3.8.1/docs/usage/
  Required (mapping): patient, sample, lane, fastq_1, fastq_2
  Optional: sex (XX/XY, default NA), status (0=normal / 1=tumor, default 0)

Stdlib only — no third-party deps; runs in a bare `uv run python` env. It does
NOT call any network service and does NOT run the pipeline; it only prepares the
samplesheet. Review the CSV before launching a (compute-heavy) run.

Examples
--------
    # One tumor sample, auto-pairing R1/R2 in ./fastq
    uv run python make_samplesheet.py --fastq-dir ./fastq \\
        --patient PATIENT_01 --sample TUMOR_01 --status 1 --sex XY \\
        --out samplesheet.csv

    # Append the matched normal under the SAME patient
    uv run python make_samplesheet.py --fastq-dir ./fastq_normal \\
        --patient PATIENT_01 --sample NORMAL_01 --status 0 --sex XY \\
        --out samplesheet.csv --append
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

HEADER = ["patient", "sex", "status", "sample", "lane", "fastq_1", "fastq_2"]

# R1/R2 mate tokens seen in Illumina-style names: _R1 / _R1_001 / _1 before .fastq.gz
R1_PAT = re.compile(r"(.+?)([._-])R?1((?:_\d+)?)(\.f(?:ast)?q\.gz)$", re.IGNORECASE)


def _mate2_name(r1: Path) -> Path:
    """Return the expected R2 path for an R1 filename, or raise if it isn't an R1."""
    m = R1_PAT.search(r1.name)
    if not m:
        raise ValueError(f"Not an R1-style FASTQ name: {r1.name}")
    stem, sep, tail, ext = m.groups()
    # Mirror whichever token form was used (R1 -> R2, or 1 -> 2).
    token = "R2" if re.search(r"R1", r1.name[m.start(2):], re.IGNORECASE) else "2"
    # Reconstruct using the exact separator + optional _001 tail + extension.
    return r1.with_name(f"{stem}{sep}{token}{tail}{ext}")


def pair_fastqs(fastq_dir: Path) -> list[tuple[Path, Path]]:
    """Find R1/R2 pairs in a directory. Returns sorted (r1, r2) absolute-path pairs."""
    if not fastq_dir.is_dir():
        raise NotADirectoryError(f"--fastq-dir not found: {fastq_dir}")
    candidates = sorted(p for p in fastq_dir.iterdir()
                        if p.is_file() and re.search(r"\.f(ast)?q\.gz$", p.name, re.IGNORECASE))
    pairs: list[tuple[Path, Path]] = []
    for r1 in candidates:
        if not R1_PAT.search(r1.name):
            continue  # skip R2 (and unmatched) files; they're picked up via their R1
        r2 = _mate2_name(r1)
        if not r2.exists():
            raise FileNotFoundError(f"R1 {r1.name} has no matching R2 (expected {r2.name})")
        pairs.append((r1.resolve(), r2.resolve()))
    if not pairs:
        raise FileNotFoundError(
            f"No R1/R2 FASTQ pairs found in {fastq_dir} "
            "(expected names like *_R1_001.fastq.gz / *_R1.fq.gz)")
    return pairs


def build_rows(pairs, patient, sample, status, sex, lane_prefix):
    """One CSV row per R1/R2 pair; lanes auto-numbered L001, L002, ... if >1 pair."""
    rows = []
    multi = len(pairs) > 1
    for i, (r1, r2) in enumerate(pairs, start=1):
        lane = f"{lane_prefix}{i:03d}" if multi else f"{lane_prefix}001"
        rows.append({
            "patient": patient, "sex": sex, "status": str(status),
            "sample": sample, "lane": lane,
            "fastq_1": str(r1), "fastq_2": str(r2),
        })
    return rows


def validate_rows(rows):
    """Raise ValueError on any schema violation. Mirrors sarek 3.8.1 requirements."""
    errors = []
    seen_keys = set()
    for n, row in enumerate(rows, start=1):
        for col in ("patient", "sample", "lane", "fastq_1", "fastq_2"):
            if not row.get(col):
                errors.append(f"row {n}: missing required column '{col}'")
        if row.get("status") not in {"0", "1"}:
            errors.append(f"row {n}: status must be 0 (normal) or 1 (tumor), got {row.get('status')!r}")
        if row.get("sex") not in {"XX", "XY", "NA"}:
            errors.append(f"row {n}: sex should be XX/XY/NA, got {row.get('sex')!r}")
        key = (row["patient"], row["sample"], row["lane"])
        if key in seen_keys:
            errors.append(f"row {n}: duplicate patient/sample/lane {key}")
        seen_keys.add(key)
    if errors:
        raise ValueError("Samplesheet validation failed:\n  - " + "\n  - ".join(errors))


def write_csv(rows, out: Path, append: bool):
    existing = []
    if append and out.exists():
        with out.open(newline="") as fh:
            existing = list(csv.DictReader(fh))
    all_rows = existing + rows
    validate_rows(all_rows)  # re-validate the merged sheet (catches cross-row dups)
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        w.writerows(all_rows)
    return len(all_rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fastq-dir", required=True, type=Path, help="Directory of R1/R2 .fastq.gz files")
    ap.add_argument("--patient", required=True, help="Subject ID (tumor+normal share this)")
    ap.add_argument("--sample", required=True, help="Sample ID (unique per sample)")
    ap.add_argument("--status", type=int, choices=(0, 1), default=0,
                    help="0=normal, 1=tumor (default 0)")
    ap.add_argument("--sex", choices=("XX", "XY", "NA"), default="NA", help="default NA")
    ap.add_argument("--lane-prefix", default="L", help="Lane label prefix (default 'L')")
    ap.add_argument("--out", type=Path, default=Path("samplesheet.csv"))
    ap.add_argument("--append", action="store_true",
                    help="Append to an existing sheet (e.g. add the matched normal)")
    args = ap.parse_args(argv)

    try:
        pairs = pair_fastqs(args.fastq_dir)
        rows = build_rows(pairs, args.patient, args.sample, args.status, args.sex, args.lane_prefix)
        total = write_csv(rows, args.out, args.append)
    except (ValueError, FileNotFoundError, NotADirectoryError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"Wrote {len(rows)} row(s) for sample '{args.sample}' "
          f"({'tumor' if args.status == 1 else 'normal'}); sheet now has {total} row(s): {args.out}")
    print("Next: nextflow run nf-core/sarek -r 3.8.1 -profile docker "
          f"--input {args.out} --outdir ./results --genome GATK.GRCh38 --tools haplotypecaller")
    print("Reminder: set --tools explicitly — sarek defaults to Strelka if you omit it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
