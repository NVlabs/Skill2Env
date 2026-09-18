#!/usr/bin/env python3
"""import_quant.py — aggregate salmon/kallisto transcript estimates to a gene matrix.

A Python convenience that reproduces tximport's gene-level summarization so the
RNA-seq quant workflow can stay in `uv` before handing off to alterlab-pydeseq2.
It reads every per-sample quant file under a directory, maps transcripts to genes
via a tx2gene TSV, and writes:

  * a gene x sample COUNT matrix (lengthScaledTPM, integer-rounded) for DESeq2
  * a gene x sample TPM matrix

Auto-detects salmon (`<sample>/quant.sf`) and kallisto (`<sample>/abundance.tsv`)
outputs. Pure stdlib — no pandas required, so it runs in a bare `uv run` env.

SEMANTICS — countsFromAbundance="lengthScaledTPM": this implements tximport's
`makeCountsFromAbundance(..., countsFromAbundance="lengthScaledTPM")` at the
transcript level, then sums to genes (matching how tximport applies the scaling
before gene summarization). For each transcript t and sample s:

    newCounts[t, s] = TPM[t, s] * mean_over_samples(effLength[t, :])

then each sample column is rescaled so its total equals that sample's original
mapped-read total:

    counts[t, s] = newCounts[t, s] * (sum_t NumReads[t, s] / sum_t newCounts[t, s])

Finally counts are summed per gene and rounded. This is length-corrected and
library-size-scaled — NOT a plain sum of raw NumReads. For full tximeta
provenance or exact parity with a published DESeq2/tximport pipeline, use the
Bioconductor tximport/tximeta packages (see ../references/tximport_handoff.md).

Usage:
  uv run python import_quant.py --quants quants --tx2gene tx2gene.tsv \\
      --out-counts gene_counts.tsv --out-tpm gene_tpm.tsv

Exit codes: 0 = wrote matrices; 2 = bad input / no quant files found.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# salmon quant.sf cols:   Name  Length  EffectiveLength  TPM  NumReads
# kallisto abundance.tsv: target_id  length  eff_length  est_counts  tpm


def load_tx2gene(path: Path, strip_version: bool) -> dict[str, str]:
    mapping: dict[str, str] = {}
    with path.open("r") as fh:
        for i, line in enumerate(fh):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            tx, gene = parts[0], parts[1]
            if i == 0 and tx.lower() in {"transcript_id", "target_id", "name"}:
                continue  # header
            if strip_version:
                tx = tx.split(".")[0]
            mapping[tx] = gene
    return mapping


def find_quant_files(root: Path) -> list[tuple[str, Path, str]]:
    """Return (sample_name, file_path, kind) for each per-sample subdir."""
    found: list[tuple[str, Path, str]] = []
    for sub in sorted(p for p in root.iterdir() if p.is_dir()):
        salmon = sub / "quant.sf"
        kallisto = sub / "abundance.tsv"
        if salmon.is_file():
            found.append((sub.name, salmon, "salmon"))
        elif kallisto.is_file():
            found.append((sub.name, kallisto, "kallisto"))
    return found


def parse_quant(path: Path, kind: str, strip_version: bool):
    """Yield (transcript_id, eff_length, tpm, num_reads) rows."""
    with path.open("r") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        idx = {name: i for i, name in enumerate(header)}
        if kind == "salmon":
            c_id, c_eff, c_tpm, c_reads = (
                idx["Name"], idx["EffectiveLength"], idx["TPM"], idx["NumReads"],
            )
        else:  # kallisto
            c_id, c_eff, c_tpm, c_reads = (
                idx["target_id"], idx["eff_length"], idx["tpm"], idx["est_counts"],
            )
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if len(cols) <= max(c_id, c_eff, c_tpm, c_reads):
                continue
            tx = cols[c_id].split(".")[0] if strip_version else cols[c_id]
            try:
                yield tx, float(cols[c_eff]), float(cols[c_tpm]), float(cols[c_reads])
            except ValueError:
                continue


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--quants", required=True, type=Path, help="dir of per-sample quant subdirs")
    p.add_argument("--tx2gene", required=True, type=Path)
    p.add_argument("--out-counts", required=True, type=Path)
    p.add_argument("--out-tpm", required=True, type=Path)
    p.add_argument("--strip-version", action="store_true")
    args = p.parse_args(argv)

    if not args.quants.is_dir():
        print(f"ERROR: --quants dir not found: {args.quants}", file=sys.stderr)
        return 2
    if not args.tx2gene.is_file():
        print(f"ERROR: --tx2gene not found: {args.tx2gene}", file=sys.stderr)
        return 2

    tx2gene = load_tx2gene(args.tx2gene, args.strip_version)
    if not tx2gene:
        print("ERROR: tx2gene map is empty.", file=sys.stderr)
        return 2

    samples = find_quant_files(args.quants)
    if not samples:
        print(
            f"ERROR: no quant.sf or abundance.tsv under {args.quants}/*/ — "
            "did salmon/kallisto write per-sample subdirs?",
            file=sys.stderr,
        )
        return 2

    sample_names: list[str] = [s[0] for s in samples]

    # First pass: read every transcript row from every sample. We need the full
    # per-transcript effective-length and TPM/NumReads tables BEFORE we can apply
    # lengthScaledTPM, because the length factor is averaged over samples and the
    # rescale factor depends on per-sample totals.
    #   tx_eff[tx][sample]   = effective length
    #   tx_tpm[tx][sample]   = TPM
    #   tx_reads[tx][sample] = NumReads (raw, used only to recover library size)
    tx_eff: dict[str, dict[str, float]] = {}
    tx_tpm: dict[str, dict[str, float]] = {}
    tx_reads: dict[str, dict[str, float]] = {}
    reads_total: dict[str, float] = {s: 0.0 for s in sample_names}
    unmapped = 0
    seen_tx: set[str] = set()

    for sample, path, kind in samples:
        for tx, eff, tpm, reads in parse_quant(path, kind, args.strip_version):
            reads_total[sample] += reads  # library size = sum of ALL mapped reads
            if tx2gene.get(tx) is None:
                if tx not in seen_tx:
                    unmapped += 1
                    seen_tx.add(tx)
                continue
            seen_tx.add(tx)
            tx_eff.setdefault(tx, {})[sample] = eff
            tx_tpm.setdefault(tx, {})[sample] = tpm
            tx_reads.setdefault(tx, {})[sample] = reads

    if not tx_tpm:
        print(
            "ERROR: no transcripts mapped to genes. Check that tx2gene IDs match "
            "the quant file IDs (try --strip-version).",
            file=sys.stderr,
        )
        return 2

    # lengthScaledTPM, transcript level (tximport::makeCountsFromAbundance):
    #   newCounts[tx, s] = TPM[tx, s] * mean_over_samples(effLength[tx, :])
    # then rescale each sample column so its total matches the sample's original
    # mapped-read count (countsSum / newSum). Effective lengths <= 0 are skipped
    # in the row mean (salmon/kallisto can emit 0 for unexpressed transcripts).
    avg_eff: dict[str, float] = {}
    for tx, per_sample in tx_eff.items():
        vals = [v for v in per_sample.values() if v > 0]
        avg_eff[tx] = (sum(vals) / len(vals)) if vals else 0.0

    new_counts: dict[str, dict[str, float]] = {}
    new_sum: dict[str, float] = {s: 0.0 for s in sample_names}
    for tx, tpm_row in tx_tpm.items():
        L = avg_eff.get(tx, 0.0)
        row = {}
        for s in sample_names:
            nc = tpm_row.get(s, 0.0) * L
            row[s] = nc
            new_sum[s] += nc
        new_counts[tx] = row

    # Per-sample rescale factor countsSum/newSum (countsSum = library size).
    scale: dict[str, float] = {}
    for s in sample_names:
        scale[s] = (reads_total[s] / new_sum[s]) if new_sum[s] > 0 else 0.0

    # Summarize scaled transcript counts (and raw TPM) up to gene level.
    gene_counts: dict[str, dict[str, float]] = {}
    gene_tpm: dict[str, dict[str, float]] = {}
    for tx, row in new_counts.items():
        gene = tx2gene[tx]
        gc = gene_counts.setdefault(gene, {})
        gt = gene_tpm.setdefault(gene, {})
        tpm_row = tx_tpm[tx]
        for s in sample_names:
            gc[s] = gc.get(s, 0.0) + row[s] * scale[s]
            gt[s] = gt.get(s, 0.0) + tpm_row.get(s, 0.0)

    genes = sorted(gene_counts)

    def write_matrix(out: Path, data: dict[str, dict[str, float]], integer: bool) -> None:
        with out.open("w") as fh:
            fh.write("gene_id\t" + "\t".join(sample_names) + "\n")
            for g in genes:
                row = data.get(g, {})
                vals = []
                for s in sample_names:
                    v = row.get(s, 0.0)
                    vals.append(str(int(round(v))) if integer else f"{v:.4f}")
                fh.write(g + "\t" + "\t".join(vals) + "\n")

    write_matrix(args.out_counts, gene_counts, integer=True)
    write_matrix(args.out_tpm, gene_tpm, integer=False)

    print(
        f"Wrote {args.out_counts} and {args.out_tpm}: "
        f"{len(genes)} genes x {len(sample_names)} samples "
        f"({unmapped} transcript rows had no gene mapping).",
        file=sys.stderr,
    )
    print("Next: hand gene_counts.tsv + a condition sheet to alterlab-pydeseq2.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
