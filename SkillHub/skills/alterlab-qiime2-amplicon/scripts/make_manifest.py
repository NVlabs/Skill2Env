#!/usr/bin/env python3
"""make_manifest.py — Build a QIIME 2 paired-end manifest (V2) from a FASTQ folder.

QIIME 2 imports demultiplexed reads from a *manifest*: a TSV mapping each sample-id
to the ABSOLUTE paths of its forward (and, for paired data, reverse) FASTQ files.
This produces a ``PairedEndFastqManifestPhred33V2`` (or single-end) manifest that
``qiime tools import`` accepts directly:

    qiime tools import \\
      --type 'SampleData[PairedEndSequencesWithQuality]' \\
      --input-format PairedEndFastqManifestPhred33V2 \\
      --input-path manifest.tsv --output-path demux.qza

It pairs files by a configurable read-tag (default Illumina ``_R1``/``_R2``) and
derives the sample-id from the filename prefix before that tag. Nothing is uploaded
anywhere; it only inspects local filenames. Pure standard library — runs under a bare
``uv run python`` with no QIIME 2 environment.

Usage:
  uv run python make_manifest.py FASTQ_DIR [--out manifest.tsv]
                                 [--fwd-tag _R1] [--rev-tag _R2]
                                 [--single] [--ext .fastq.gz]
  uv run python make_manifest.py ./reads --out manifest.tsv      # paired, R1/R2
  uv run python make_manifest.py ./reads --single --fwd-tag _R1  # single-end

Exit codes: 0 = wrote a manifest; 2 = bad usage / no FASTQs found / unpaired files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def sample_id_from(name: str, tag: str) -> str:
    """Derive a sample-id from a filename: everything before the read tag.

    e.g. 'gut42_S3_L001_R1_001.fastq.gz' with tag '_R1' -> 'gut42_S3_L001'.
    """
    base = name
    idx = base.find(tag)
    if idx != -1:
        base = base[:idx]
    else:
        # No tag present: strip a trailing extension chain (.fastq.gz, .fq, ...).
        base = re.sub(r"\.(fastq|fq)(\.gz)?$", "", base)
    return base.rstrip("_.")


def collect(directory: Path, ext: str) -> list[Path]:
    files = sorted(p for p in directory.iterdir() if p.is_file() and p.name.endswith(ext))
    return files


def build_paired(files: list[Path], fwd_tag: str, rev_tag: str) -> list[tuple[str, Path, Path]]:
    fwd = {sample_id_from(p.name, fwd_tag): p for p in files if fwd_tag in p.name}
    rev = {sample_id_from(p.name, rev_tag): p for p in files if rev_tag in p.name}
    rows: list[tuple[str, Path, Path]] = []
    missing: list[str] = []
    for sid in sorted(fwd):
        if sid in rev:
            rows.append((sid, fwd[sid], rev[sid]))
        else:
            missing.append(sid)
    orphan_rev = sorted(set(rev) - set(fwd))
    if missing or orphan_rev:
        msg = []
        if missing:
            msg.append(f"forward reads with no reverse mate: {', '.join(missing)}")
        if orphan_rev:
            msg.append(f"reverse reads with no forward mate: {', '.join(orphan_rev)}")
        raise SystemExit("ERROR: unpaired files — " + "; ".join(msg))
    return rows


def build_single(files: list[Path], fwd_tag: str) -> list[tuple[str, Path]]:
    return [(sample_id_from(p.name, fwd_tag), p) for p in files]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("fastq_dir", help="Directory containing demultiplexed FASTQ files")
    ap.add_argument("--out", default="manifest.tsv", help="Output manifest path (default manifest.tsv)")
    ap.add_argument("--fwd-tag", default="_R1", help="Forward-read filename tag (default _R1)")
    ap.add_argument("--rev-tag", default="_R2", help="Reverse-read filename tag (default _R2)")
    ap.add_argument("--single", action="store_true", help="Single-end (one column) manifest")
    ap.add_argument("--ext", default=".fastq.gz", help="FASTQ extension to match (default .fastq.gz)")
    args = ap.parse_args(argv)

    directory = Path(args.fastq_dir).expanduser().resolve()
    if not directory.is_dir():
        print(f"ERROR: not a directory: {directory}", file=sys.stderr)
        return 2

    files = collect(directory, args.ext)
    if not files:
        print(f"ERROR: no '*{args.ext}' files in {directory}", file=sys.stderr)
        return 2

    out = Path(args.out).expanduser()
    if args.single:
        rows = build_single(files, args.fwd_tag)
        with out.open("w") as fh:
            fh.write("sample-id\tabsolute-filepath\n")
            for sid, p in rows:
                fh.write(f"{sid}\t{p}\n")
        print(f"Wrote {len(rows)} single-end samples -> {out}")
        print("Import with: --type 'SampleData[SequencesWithQuality]' "
              "--input-format SingleEndFastqManifestPhred33V2")
    else:
        rows = build_paired(files, args.fwd_tag, args.rev_tag)
        with out.open("w") as fh:
            fh.write("sample-id\tforward-absolute-filepath\treverse-absolute-filepath\n")
            for sid, f, r in rows:
                fh.write(f"{sid}\t{f}\t{r}\n")
        print(f"Wrote {len(rows)} paired-end samples -> {out}")
        print("Import with: --type 'SampleData[PairedEndSequencesWithQuality]' "
              "--input-format PairedEndFastqManifestPhred33V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
