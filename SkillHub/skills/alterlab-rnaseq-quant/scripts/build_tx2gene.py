#!/usr/bin/env python3
"""build_tx2gene.py — make a transcript->gene (tx2gene) map from a GTF/GFF.

tximport needs a two-column transcript_id -> gene_id table to summarize
transcript-level salmon/kallisto estimates up to genes. This parses the GTF
attribute column for transcript_id and gene_id and writes a deduplicated TSV.

Pure stdlib (no pandas needed). Handles both GTF style
  gene_id "ENSG..."; transcript_id "ENST...";
and GFF3 style
  ID=transcript:ENST...;Parent=gene:ENSG...
attribute fields, preferring GTF; falls back to GFF3 keys when GTF keys are absent.

Usage:
  uv run python build_tx2gene.py annotation.gtf --out tx2gene.tsv
  uv run python build_tx2gene.py annotation.gtf --strip-version --out tx2gene.tsv

Output: a TSV with header `transcript_id\tgene_id`, one row per unique transcript.

Exit codes: 0 = wrote map; 2 = bad input / no transcript records found.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# GTF: key "value"; GFF3: key=value within a ;-separated attribute string.
_GTF_ATTR = re.compile(r'(\w+)\s+"([^"]*)"')
_GFF_ATTR = re.compile(r"(\w+)=([^;]+)")


def _strip_ver(x: str) -> str:
    """ENST00000456328.2 -> ENST00000456328 (drop a trailing .<digits>)."""
    return re.sub(r"\.\d+$", "", x)


def parse_attrs(attr_field: str) -> dict[str, str]:
    attrs = {k: v for k, v in _GTF_ATTR.findall(attr_field)}
    if "transcript_id" not in attrs and "gene_id" not in attrs:
        # try GFF3 form
        for k, v in _GFF_ATTR.findall(attr_field):
            attrs.setdefault(k, v)
    return attrs


def transcript_gene(attrs: dict[str, str]) -> tuple[str, str] | None:
    tx = attrs.get("transcript_id")
    gene = attrs.get("gene_id")
    # GFF3 fallbacks
    if tx is None:
        raw = attrs.get("ID", "")
        if raw.startswith("transcript:"):
            tx = raw.split(":", 1)[1]
    if gene is None:
        parent = attrs.get("Parent", "")
        if parent.startswith("gene:"):
            gene = parent.split(":", 1)[1]
    if tx and gene:
        return tx, gene
    return None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("gtf", type=Path, help="GTF/GFF annotation (matching the transcriptome)")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument(
        "--strip-version",
        action="store_true",
        help="drop trailing .N version suffixes from IDs (match Ensembl reference vs annotation)",
    )
    p.add_argument("--force", action="store_true", help="overwrite existing output")
    args = p.parse_args(argv)

    if not args.gtf.is_file():
        print(f"ERROR: annotation not found: {args.gtf}", file=sys.stderr)
        return 2
    if args.out.exists() and not args.force:
        print(f"ERROR: {args.out} exists (use --force)", file=sys.stderr)
        return 2

    seen: dict[str, str] = {}
    with args.gtf.open("r") as fh:
        for line in fh:
            if not line or line.startswith("#"):
                continue
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 9:
                continue
            feature = cols[2]
            # only feature rows that carry transcript_id (transcript/exon/etc.)
            attrs = parse_attrs(cols[8])
            tg = transcript_gene(attrs)
            if tg is None:
                continue
            tx, gene = tg
            if args.strip_version:
                tx, gene = _strip_ver(tx), _strip_ver(gene)
            seen.setdefault(tx, gene)  # first mapping wins; one row per transcript
            _ = feature  # feature kind not needed once transcript_id is present

    if not seen:
        print(
            "ERROR: no transcript_id/gene_id pairs found. Is this a valid GTF/GFF3 "
            "with transcript_id and gene_id attributes?",
            file=sys.stderr,
        )
        return 2

    with args.out.open("w") as out:
        out.write("transcript_id\tgene_id\n")
        for tx, gene in sorted(seen.items()):
            out.write(f"{tx}\t{gene}\n")

    print(f"Wrote {args.out}: {len(seen)} transcript->gene rows.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
