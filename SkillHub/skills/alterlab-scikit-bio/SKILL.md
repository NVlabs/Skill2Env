---
name: alterlab-scikit-bio
description: Analyze biological data with scikit-bio — sequence analysis and alignments, phylogenetic trees, alpha/beta diversity metrics (including UniFrac), ordination (PCoA), PERMANOVA statistics, and FASTA/Newick I/O. Use for microbiome and community-ecology analysis — computing diversity, distance matrices, and ordination from feature tables. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# scikit-bio

## Overview

scikit-bio is a comprehensive Python library for working with biological data. Apply this skill for bioinformatics analyses spanning sequence manipulation, alignment, phylogenetics, microbial ecology, and multivariate statistics.

## When to Use This Skill

This skill should be used when the user:
- Works with biological sequences (DNA, RNA, protein)
- Needs to read/write biological file formats (FASTA, FASTQ, GenBank, Newick, BIOM, etc.)
- Performs sequence alignments or searches for motifs
- Constructs or analyzes phylogenetic trees
- Calculates diversity metrics (alpha/beta diversity, UniFrac distances)
- Performs ordination analysis (PCoA, CCA, RDA)
- Runs statistical tests on biological/ecological data (PERMANOVA, ANOSIM, Mantel)
- Analyzes microbiome or community ecology data
- Works with protein embeddings from language models
- Needs to manipulate biological data tables

## Core Capabilities

### 1. Sequence Manipulation

Work with biological sequences using specialized classes for DNA, RNA, and protein data.

**Key operations:**
- Read/write sequences from FASTA, FASTQ, GenBank, EMBL formats
- Sequence slicing, concatenation, and searching
- Reverse complement, transcription (DNA→RNA), and translation (RNA→protein)
- Find motifs and patterns using regex
- Calculate distances (Hamming, k-mer based)
- Handle sequence quality scores and metadata

**Common patterns:**
```python
import skbio

# Read sequences from file
seq = skbio.DNA.read('input.fasta')

# Sequence operations
rc = seq.reverse_complement()
rna = seq.transcribe()
protein = rna.translate()

# Find motifs
motif_positions = seq.find_with_regex('ATG[ACGT]{3}')

# Check for properties
has_degens = seq.has_degenerates()
seq_no_gaps = seq.degap()
```

**Important notes:**
- Use `DNA`, `RNA`, `Protein` classes for grammared sequences with validation
- Use `Sequence` class for generic sequences without alphabet restrictions
- Quality scores automatically loaded from FASTQ files into positional metadata
- Metadata types: sequence-level (ID, description), positional (per-base), interval (regions/features)

### 2. Sequence Alignment

Perform pairwise and multiple sequence alignments using dynamic programming algorithms.

**Key capabilities:**
- Global (Needleman-Wunsch) and local (Smith-Waterman) pairwise alignment via the unified `pair_align` API
- Configurable scoring (match/mismatch tuple, named substitution matrix, affine gap costs)
- CIGAR string handling via `PairAlignPath`
- Multiple sequence alignment storage and manipulation with `TabularMSA`

**Common patterns:**
```python
from skbio.alignment import pair_align, pair_align_nucl, pair_align_prot, TabularMSA
from skbio import DNA

# Pairwise alignment (0.7+ unified API). mode='global' (default) or 'local'.
seq1, seq2 = DNA('ATCGATCGATCG'), DNA('ATCGGGGATCG')
res = pair_align(seq1, seq2, mode='local')
print(res.score)
aligned = res.paths[0].to_aligned((seq1, seq2))  # tuple of aligned sequences

# Nucleotide / protein convenience wrappers with sensible defaults
res = pair_align_nucl(seq1, seq2)                       # DNA/RNA
# res = pair_align_prot(p1, p2, sub_score='BLOSUM62')   # protein

# Read multiple alignment from file
msa = TabularMSA.read('alignment.fasta', constructor=DNA)
consensus = msa.consensus()
```

**Important notes:**
- `pair_align` returns a named tuple `(score, paths, matrices)`; `paths` is a list of `PairAlignPath` objects (up to `max_paths`).
- `sub_score` accepts a `(match, mismatch)` tuple, a named matrix string (e.g. `'BLOSUM62'`), or a `SubstitutionMatrix`; `gap_cost` takes a single value (linear) or `(open, extend)` tuple (affine — recommended for biological sequences).
- The older `local_pairwise_align_ssw`, `StripedSmithWaterman`, and `*_pairwise_align`/`AlignScorer` interfaces were removed/deprecated in 0.6–0.7; use `pair_align*` instead.

### 3. Phylogenetic Trees

Construct, manipulate, and analyze phylogenetic trees representing evolutionary relationships.

**Key capabilities:**
- Tree construction from distance matrices (UPGMA, WPGMA, Neighbor Joining, GME, BME)
- Tree manipulation (pruning, rerooting, traversal)
- Distance calculations (patristic, cophenetic, Robinson-Foulds)
- ASCII visualization
- Newick format I/O

**Common patterns:**
```python
from skbio import TreeNode
from skbio.tree import nj

# Read tree from file
tree = TreeNode.read('tree.nwk')

# Construct tree from distance matrix
tree = nj(distance_matrix)

# Tree operations
subtree = tree.shear(['taxon1', 'taxon2', 'taxon3'])
tips = [node for node in tree.tips()]
lca = tree.lowest_common_ancestor(['taxon1', 'taxon2'])

# Calculate distances
patristic_dist = tree.find('taxon1').distance(tree.find('taxon2'))
cophenetic_matrix = tree.cophenetic_matrix()

# Compare tree topologies (Robinson-Foulds)
rf_distance = tree.compare_rfd(other_tree)
```

**Important notes:**
- Tree construction lives in `skbio.tree`: `nj` (neighbor joining), `upgma` (assumes a molecular clock), and `gme`/`bme` (greedy/balanced minimum evolution).
- Robinson-Foulds is `tree.compare_rfd(other)`; the module-level `rf_dists()` computes pairwise RF distances across many trees. (`robinson_foulds` was renamed.)
- GME and BME are highly scalable for large trees.
- Trees can be rooted or unrooted; some metrics require specific rooting.

### 4. Diversity Analysis

Calculate alpha and beta diversity metrics for microbial ecology and community analysis.

**Key capabilities:**
- Alpha diversity: richness, Shannon entropy, Simpson index, Faith's PD, Pielou's evenness
- Beta diversity: Bray-Curtis, Jaccard, weighted/unweighted UniFrac, Euclidean distances
- Phylogenetic diversity metrics (require tree input)
- Rarefaction and subsampling
- Integration with ordination and statistical tests

**Common patterns:**
```python
from skbio.diversity import alpha_diversity, beta_diversity
import skbio

# Alpha diversity
alpha = alpha_diversity('shannon', counts_matrix, ids=sample_ids)
faith_pd = alpha_diversity('faith_pd', counts_matrix, ids=sample_ids,
                          tree=tree, taxa=feature_ids)

# Beta diversity
bc_dm = beta_diversity('braycurtis', counts_matrix, ids=sample_ids)
unifrac_dm = beta_diversity('unweighted_unifrac', counts_matrix,
                           ids=sample_ids, tree=tree, taxa=feature_ids)

# Get available metrics
from skbio.diversity import get_alpha_diversity_metrics
print(get_alpha_diversity_metrics())
```

**Important notes:**
- Counts must be integers representing abundances, not relative frequencies.
- The feature-ID parameter for phylogenetic metrics is `taxa=` (renamed from `otu_ids=` in 0.6; "OTU" terminology was replaced by "taxon" project-wide). Plain richness is `observed_features`, not the old `observed_otus`.
- Phylogenetic metrics (Faith's PD, UniFrac) require a `tree` plus `taxa` (feature) IDs that match the tree tips.
- Use `partial_beta_diversity()` for computing specific sample pairs only.
- Alpha diversity returns a `pandas.Series`; beta diversity returns a `DistanceMatrix`.

### 5. Ordination Methods

Reduce high-dimensional biological data to visualizable lower-dimensional spaces.

**Key capabilities:**
- PCoA (Principal Coordinate Analysis) from distance matrices
- CA (Correspondence Analysis) for contingency tables
- CCA (Canonical Correspondence Analysis) with environmental constraints
- RDA (Redundancy Analysis) for linear relationships
- Biplot projection for feature interpretation

**Common patterns:**
```python
from skbio.stats.ordination import pcoa, cca

# PCoA from distance matrix
pcoa_results = pcoa(distance_matrix)
pc1 = pcoa_results.samples['PC1']
pc2 = pcoa_results.samples['PC2']

# CCA: y = samples-by-features table, x = samples-by-constraints (environment)
cca_results = cca(feature_table, environmental_matrix)

# Save/load ordination results
pcoa_results.write('ordination.txt')
results = skbio.OrdinationResults.read('ordination.txt')
```

**Important notes:**
- PCoA works with any distance/dissimilarity matrix
- CCA reveals environmental drivers of community composition
- Ordination results include eigenvalues, proportion explained, and sample/feature coordinates
- Results integrate with plotting libraries (matplotlib, seaborn, plotly)

### 6. Statistical Testing

Perform hypothesis tests specific to ecological and biological data.

**Key capabilities:**
- PERMANOVA: test group differences using distance matrices
- ANOSIM: alternative test for group differences
- PERMDISP: test homogeneity of group dispersions
- Mantel test: correlation between distance matrices
- Bioenv: find environmental variables correlated with distances

**Common patterns:**
```python
from skbio.stats.distance import permanova, anosim, mantel

# Test if groups differ significantly
permanova_results = permanova(distance_matrix, grouping, permutations=999)
print(f"p-value: {permanova_results['p-value']}")

# ANOSIM test
anosim_results = anosim(distance_matrix, grouping, permutations=999)

# Mantel test between two distance matrices
mantel_results = mantel(dm1, dm2, method='pearson', permutations=999)
print(f"Correlation: {mantel_results[0]}, p-value: {mantel_results[1]}")
```

**Important notes:**
- Permutation tests provide non-parametric significance testing
- Use 999+ permutations for robust p-values
- PERMANOVA sensitive to dispersion differences; pair with PERMDISP
- Mantel tests assess matrix correlation (e.g., geographic vs genetic distance)

### 7. File I/O and Format Conversion

Read and write 19+ biological file formats with automatic format detection.

**Supported formats:**
- Sequences: FASTA, FASTQ, GenBank, EMBL, QSeq
- Alignments: Clustal, PHYLIP, Stockholm
- Trees: Newick
- Tables: BIOM (HDF5 and JSON)
- Distances: delimited square matrices
- Analysis: BLAST+6/7, GFF3, Ordination results
- Metadata: TSV/CSV with validation

**Common patterns:**
```python
import skbio

# Read with automatic format detection
seq = skbio.DNA.read('file.fasta', format='fasta')
tree = skbio.TreeNode.read('tree.nwk')

# Write to file
seq.write('output.fasta', format='fasta')

# Generator for large files (memory efficient)
for seq in skbio.io.read('large.fasta', format='fasta', constructor=skbio.DNA):
    process(seq)

# Convert formats
seqs = list(skbio.io.read('input.fastq', format='fastq', constructor=skbio.DNA))
skbio.io.write(seqs, format='fasta', into='output.fasta')
```

**Important notes:**
- Use generators for large files to avoid memory issues
- Format can be auto-detected when `into` parameter specified
- Some objects can be written to multiple formats
- Support for stdin/stdout piping with `verify=False`

### 8. Distance Matrices

Create and manipulate distance/dissimilarity matrices with statistical methods.

**Key capabilities:**
- Store symmetric (DistanceMatrix) or asymmetric (DissimilarityMatrix) data
- ID-based indexing and slicing
- Integration with diversity, ordination, and statistical tests
- Read/write delimited text format

**Common patterns:**
```python
from skbio import DistanceMatrix
import numpy as np

# Create from array
data = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
dm = DistanceMatrix(data, ids=['A', 'B', 'C'])

# Access distances
dist_ab = dm['A', 'B']
row_a = dm['A']

# Read from file
dm = DistanceMatrix.read('distances.txt')

# Use in downstream analyses
pcoa_results = pcoa(dm)
permanova_results = permanova(dm, grouping)
```

**Important notes:**
- DistanceMatrix enforces symmetry and zero diagonal
- DissimilarityMatrix allows asymmetric values
- IDs enable integration with metadata and biological knowledge
- Compatible with pandas, numpy, and scikit-learn

### 9. Biological Tables

Work with feature tables (OTU/ASV tables) common in microbiome research.

**Key capabilities:**
- BIOM format I/O (HDF5 and JSON)
- Integration with pandas, polars, AnnData, numpy
- Data augmentation techniques (phylomix, mixup, compositional methods)
- Sample/feature filtering and normalization
- Metadata integration

**Common patterns:**
```python
from skbio.table import Table

# Read BIOM table
table = Table.read('table.biom')

# Access data
sample_ids = table.ids(axis='sample')
feature_ids = table.ids(axis='observation')
counts = table.matrix_data  # scipy sparse; .toarray() for dense

# Filter
filtered = table.filter(sample_ids_to_keep, axis='sample')

# To pandas (sparse by default)
df = table.to_dataframe(dense=True)
```

**Important notes:**
- `Table` is scikit-bio's re-export of the BIOM `Table`; import it from `skbio.table` (not the top-level `skbio` namespace).
- In BIOM convention `observation` = features (taxa/OTUs/ASVs), `sample` = samples; `matrix_data` is observations-by-samples sparse.
- Build from existing data via the `Table(data, observation_ids, sample_ids)` constructor or `Table.from_tsv` / `from_json` / `from_hdf5` (there is no `from_dataframe`).
- BIOM tables are standard in QIIME 2 workflows; HDF5 is more efficient than JSON for large tables.

### 10. Protein Embeddings

Work with protein language model embeddings for downstream analysis.

**Key capabilities:**
- Store embeddings from protein language models (ESM, ProtTrans, etc.)
- Convert embeddings to distance matrices
- Generate ordination objects for visualization
- Export to numpy/pandas for ML workflows

**Common patterns:**
```python
from skbio.embedding import (
    ProteinEmbedding, ProteinVector,
    embed_vec_to_distances, embed_vec_to_ordination, embed_vec_to_numpy,
)

# Per-residue embedding for one protein (e.g. an ESM output)
emb = ProteinEmbedding(embedding_array, sequence)

# One fixed-length vector per protein (e.g. a mean-pooled embedding)
vecs = [ProteinVector(vec, seq) for vec, seq in zip(vectors, sequences)]

# Module-level helpers operate on a collection of *Vector objects:
arr = embed_vec_to_numpy(vecs)                      # ndarray for ML
dm = embed_vec_to_distances(vecs, metric='euclidean')   # DistanceMatrix
ord_results = embed_vec_to_ordination(vecs)             # OrdinationResults (PCoA)
```

**Important notes:**
- Distinguish `*Embedding` (per-position matrix for a single sequence) from `*Vector` (one summary vector per sequence).
- The `to_distances`/`to_ordination`/`to_numpy`/`to_dataframe` conversions are **module-level functions** (`embed_vec_to_*`) over a list of vectors, not methods on the embedding objects.
- Outputs (`DistanceMatrix`, `OrdinationResults`) plug straight into scikit-bio's diversity/ordination/statistics ecosystem.

## Best Practices

### Installation
```bash
uv pip install "scikit-bio>=0.7,<0.8"   # examples here target the 0.7 API
```
The 0.6→0.7 line renamed several interfaces (`otu_ids`→`taxa`, `observed_otus`→`observed_features`, `robinson_foulds`→`compare_rfd`) and replaced the old pairwise-alignment functions with `pair_align*`. Pin if you depend on these.

### Performance Considerations
- Use generators for large sequence files to minimize memory usage
- For massive phylogenetic trees, prefer GME or BME over NJ
- Beta diversity calculations can be parallelized with `partial_beta_diversity()`
- BIOM format (HDF5) more efficient than JSON for large tables

### Integration with Ecosystem
- Sequences interoperate with Biopython via standard formats
- Tables integrate with pandas, polars, and AnnData
- Distance matrices compatible with scikit-learn
- Ordination results visualizable with matplotlib/seaborn/plotly
- Works seamlessly with QIIME 2 artifacts (BIOM, trees, distance matrices)

### Common Workflows
1. **Microbiome diversity analysis**: Read BIOM table → Calculate alpha/beta diversity → Ordination (PCoA) → Statistical testing (PERMANOVA)
2. **Phylogenetic analysis**: Read sequences → Align → Build distance matrix → Construct tree → Calculate phylogenetic distances
3. **Sequence processing**: Read FASTQ → Quality filter → Trim/clean → Find motifs → Translate → Write FASTA
4. **Comparative genomics**: Read sequences → Pairwise alignment → Calculate distances → Build tree → Analyze clades

## Reference Documentation

For detailed API information, parameter specifications, and advanced usage examples, refer to `references/api_reference.md` which contains comprehensive documentation on:
- Complete method signatures and parameters for all capabilities
- Extended code examples for complex workflows
- Troubleshooting common issues
- Performance optimization tips
- Integration patterns with other libraries

## Additional Resources

- Official documentation: https://scikit.bio/docs/latest/
- GitHub repository: https://github.com/scikit-bio/scikit-bio
- Forum support: https://forum.qiime2.org (scikit-bio is part of QIIME 2 ecosystem)

