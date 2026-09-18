# deepTools Usage Playbook

How to respond to common user requests, per-task playbooks, example
interactions, and grep recipes for searching the other reference files. The
main SKILL.md links here for "how should I drive this skill" guidance; the
command-level detail lives in `tools_reference.md`, `workflows.md`,
`normalization_methods.md`, and `effective_genome_sizes.md`.

## Handling User Requests

### For New Users

1. Verify installation (`uv pip install deeptools`).
2. Validate input files using `scripts/validate_files.py`.
3. Recommend an appropriate workflow based on experiment type.
4. Generate a workflow template using `scripts/workflow_generator.py`.
5. Guide through customization and execution.

### For Experienced Users

1. Provide specific tool commands for requested operations.
2. Reference the appropriate sections in `references/tools_reference.md`.
3. Suggest optimizations and best practices.
4. Offer troubleshooting for issues.

### For Specific Tasks

**"Convert BAM to bigWig":**
- Use bamCoverage with appropriate normalization.
- Recommend RPGC or CPM based on use case.
- Provide effective genome size for the organism.
- Suggest relevant parameters (extendReads, ignoreDuplicates, binSize).

**"Check ChIP quality":**
- Run full QC workflow or use plotFingerprint specifically.
- Explain interpretation of results.
- Suggest follow-up actions based on results.

**"Create heatmap":**
- Guide through the two-step process: computeMatrix → plotHeatmap.
- Help choose appropriate matrix mode (reference-point vs scale-regions).
- Suggest visualization parameters and clustering options.

**"Compare samples":**
- Recommend bamCompare for two-sample comparison.
- Suggest multiBamSummary + plotCorrelation for multiple samples.
- Guide normalization method selection.

### Referencing Documentation

When users need detailed information:
- **Tool details**: Direct to specific sections in `references/tools_reference.md`.
- **Workflows**: Use `references/workflows.md` for complete analysis pipelines.
- **Normalization**: Consult `references/normalization_methods.md` for method selection.
- **Genome sizes**: Reference `references/effective_genome_sizes.md`.

Search references using grep patterns:

```bash
# Find tool documentation
grep -A 20 "^### toolname" references/tools_reference.md

# Find workflow
grep -A 50 "^## Workflow Name" references/workflows.md

# Find normalization method
grep -A 15 "^### Method Name" references/normalization_methods.md
```

## Example Interactions

**User: "I need to analyze my ChIP-seq data"**

Response approach:
1. Ask about files available (BAM files, peaks, genes).
2. Validate files using the validation script.
3. Generate the chipseq_analysis workflow template.
4. Customize for their specific files and organism.
5. Explain each step as the script runs.

**User: "Which normalization should I use?"**

Response approach:
1. Ask about experiment type (ChIP-seq, RNA-seq, etc.).
2. Ask about comparison goal (within-sample or between-sample).
3. Consult `references/normalization_methods.md` selection guide.
4. Recommend an appropriate method with justification.
5. Provide a command example with parameters.

**User: "Create a heatmap around TSS"**

Response approach:
1. Verify bigWig and gene BED files are available.
2. Use computeMatrix with reference-point mode at TSS.
3. Generate plotHeatmap with appropriate visualization parameters.
4. Suggest clustering if the dataset is large.
5. Offer a profile plot as a complement.

## Inline Command Examples by Category

These are quick starting points; full parameter detail is in
`tools_reference.md`.

### BAM/bigWig Processing

**Convert BAM to normalized coverage:**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC --effectiveGenomeSize 2913022398 \
    --binSize 10 --numberOfProcessors 8
```

**Compare two samples (log2 ratio):**
```bash
bamCompare -b1 treatment.bam -b2 control.bam -o ratio.bw \
    --operation log2 --scaleFactorsMethod readCount
```

**Key tools:** bamCoverage, bamCompare, multiBamSummary, multiBigwigSummary, correctGCBias, alignmentSieve
(see `tools_reference.md` → "BAM and bigWig File Processing Tools")

### Quality Control

**Check ChIP enrichment:**
```bash
plotFingerprint -b input.bam chip.bam -o fingerprint.png \
    --extendReads 200 --ignoreDuplicates
```

**Sample correlation:**
```bash
multiBamSummary bins --bamfiles *.bam -o counts.npz
plotCorrelation -in counts.npz --corMethod pearson \
    --whatToShow heatmap -o correlation.png
```

**Key tools:** plotFingerprint, plotCoverage, plotCorrelation, plotPCA, bamPEFragmentSize
(see `tools_reference.md` → "Quality Control Tools")

### Visualization

**Create heatmap around TSS:**
```bash
# Compute matrix
computeMatrix reference-point -S signal.bw -R genes.bed \
    -b 3000 -a 3000 --referencePoint TSS -o matrix.gz

# Generate heatmap
plotHeatmap -m matrix.gz -o heatmap.png \
    --colorMap RdBu --kmeans 3
```

**Create profile plot:**
```bash
plotProfile -m matrix.gz -o profile.png \
    --plotType lines --colors blue red
```

**Key tools:** computeMatrix, plotHeatmap, plotProfile, plotEnrichment
(see `tools_reference.md` → "Visualization Tools")
