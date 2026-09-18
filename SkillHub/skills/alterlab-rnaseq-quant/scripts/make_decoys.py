#!/usr/bin/env python3
"""make_decoys.py — build a decoy-aware salmon gentrome + decoys.txt.

A decoy-aware salmon index needs two derived files:
  * decoys.txt  — the genome's sequence (chromosome/scaffold) names, one per line
  * gentrome.fa — transcripts FASTA concatenated with genome FASTA (transcripts FIRST)

salmon then treats the genome entries as decoys, so reads that align better to the
genome than to any transcript are not force-assigned to a transcript.

This helper is pure stdlib (streaming file IO — never loads a whole FASTA into
memory) and adds guards against the two common silent mistakes:
  * empty / unreadable input FASTAs
  * a swapped argument order (genome passed as transcripts) — detected heuristically
    by comparing header counts (transcriptomes have far more records than genomes)

Usage:
  uv run python make_decoys.py --transcripts transcripts.fa --genome genome.fa \\
      --out-gentrome gentrome.fa --out-decoys decoys.txt

Then:
  salmon index -t gentrome.fa -d decoys.txt -i salmon_index -k 31 -p 8

Exit codes: 0 = wrote both files; 2 = bad input/usage.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _first_token(header_line: str) -> str:
    """'>1 dna:chromosome ...' -> '1'. Strip '>' and anything after first space."""
    name = header_line[1:].strip()
    # salmon matches on the first whitespace-delimited token
    return name.split()[0] if name else ""


def collect_decoys(genome_path: Path) -> list[str]:
    """Stream the genome FASTA and return its sequence names (for decoys.txt)."""
    names: list[str] = []
    with genome_path.open("r") as fh:
        for line in fh:
            if line.startswith(">"):
                tok = _first_token(line)
                if tok:
                    names.append(tok)
    return names


def count_headers(path: Path) -> int:
    n = 0
    with path.open("r") as fh:
        for line in fh:
            if line.startswith(">"):
                n += 1
    return n


def append_fasta(src: Path, dst) -> int:
    """Append src FASTA to an open dst file handle. Returns header count."""
    n = 0
    with src.open("r") as fh:
        for line in fh:
            if line.startswith(">"):
                n += 1
            dst.write(line)
    return n


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--transcripts", required=True, type=Path, help="transcriptome FASTA")
    p.add_argument("--genome", required=True, type=Path, help="genome FASTA (decoys)")
    p.add_argument("--out-gentrome", required=True, type=Path)
    p.add_argument("--out-decoys", required=True, type=Path)
    p.add_argument("--force", action="store_true", help="overwrite existing outputs")
    args = p.parse_args(argv)

    for f in (args.transcripts, args.genome):
        if not f.is_file():
            print(f"ERROR: input not found: {f}", file=sys.stderr)
            return 2

    for out in (args.out_gentrome, args.out_decoys):
        if out.exists() and not args.force:
            print(f"ERROR: {out} exists (use --force to overwrite)", file=sys.stderr)
            return 2

    tx_headers = count_headers(args.transcripts)
    decoy_names = collect_decoys(args.genome)
    if tx_headers == 0:
        print(f"ERROR: no FASTA records in transcripts file {args.transcripts}", file=sys.stderr)
        return 2
    if not decoy_names:
        print(f"ERROR: no FASTA records in genome file {args.genome}", file=sys.stderr)
        return 2

    # Heuristic swap guard: a transcriptome normally has many more records than a
    # genome assembly. If transcripts has fewer headers than the genome, warn loudly.
    if tx_headers < len(decoy_names):
        print(
            "WARNING: the transcripts FASTA has fewer records "
            f"({tx_headers}) than the genome ({len(decoy_names)}). "
            "Did you swap --transcripts and --genome? Continuing anyway.",
            file=sys.stderr,
        )

    # decoys.txt
    args.out_decoys.write_text("\n".join(decoy_names) + "\n")

    # gentrome.fa = transcripts FIRST, then genome (decoys last)
    with args.out_gentrome.open("w") as dst:
        append_fasta(args.transcripts, dst)
        append_fasta(args.genome, dst)

    print(
        f"Wrote {args.out_decoys} ({len(decoy_names)} decoy names) and "
        f"{args.out_gentrome} (transcripts then genome).",
        file=sys.stderr,
    )
    print(
        "Next: salmon index -t "
        f"{args.out_gentrome} -d {args.out_decoys} -i salmon_index -k 31 -p 8",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
