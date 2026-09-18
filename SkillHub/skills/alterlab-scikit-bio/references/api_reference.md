# scikit-bio API Reference

This document provides detailed API information, advanced examples, and troubleshooting guidance for working with scikit-bio.

## Table of Contents
1. [Sequence Classes](#sequence-classes)
2. [Alignment Methods](#alignment-methods)
3. [Phylogenetic Trees](#phylogenetic-trees)
4. [Diversity Metrics](#diversity-metrics)
5. [Ordination](#ordination)
6. [Statistical Tests](#statistical-tests)
7. [Distance Matrices](#distance-matrices)
8. [File I/O](#file-io)
9. [Troubleshooting](#troubleshooting)

## Sequence Classes

### DNA, RNA, and Protein Classes

```python
from skbio import DNA, RNA, Protein, Sequence

# Creating sequences
dna = DNA('ATCGATCG', metadata={'id': 'seq1', 'description': 'Example'})
rna = RNA('AUCGAUCG')
protein = Protein('ACDEFGHIKLMNPQRSTVWY')

# Sequence operations
dna_rc = dna.reverse_complement()  # Reverse complement
rna = dna.transcribe()  # DNA -> RNA
protein = rna.translate()  # RNA -> Protein

# Using genetic code tables
protein = rna.translate(genetic_code=11)  # Bacterial code
```

### Sequence Searching and Pattern Matching

```python
# Find motifs using regex
dna = DNA('ATGCGATCGATGCATCG')
motif_locs = dna.find_with_regex('ATG.{3}')  # Start codons

# Find all positions
import re
for match in re.finditer('ATG', str(dna)):
    print(f"ATG found at position {match.start()}")

# k-mer counting (method on the sequence object)
kmers = dna.kmer_frequencies(k=3)
```

### Handling Sequence Metadata

```python
# Sequence-level metadata
dna = DNA('ATCG', metadata={'id': 'seq1', 'source': 'E. coli'})
print(dna.metadata['id'])

# Positional metadata (per-base quality scores from FASTQ)
from skbio import DNA
seqs = DNA.read('reads.fastq', format='fastq', phred_offset=33)
quality_scores = seqs.positional_metadata['quality']

# Interval metadata (features/annotations)
dna.interval_metadata.add([(5, 15)], metadata={'type': 'gene', 'name': 'geneA'})
```

### Distance Calculations

```python
from skbio import DNA

seq1 = DNA('ATCGATCG')
seq2 = DNA('ATCG--CG')

# Hamming distance (default)
dist = seq1.distance(seq2)

# Custom distance function
from skbio.sequence.distance import kmer_distance
dist = seq1.distance(seq2, metric=kmer_distance)
```

## Alignment Methods

### Pairwise Alignment

scikit-bio 0.7 unifies pairwise alignment under `pair_align` (plus the
`pair_align_nucl` / `pair_align_prot` convenience wrappers). The legacy
`local_pairwise_align_ssw`, `StripedSmithWaterman`, `AlignScorer`, and the
`*_pairwise_align` functions were removed or demoted to slow educational
helpers — do not use them in new code.

```python
from skbio.alignment import pair_align, pair_align_nucl, pair_align_prot
from skbio import DNA, Protein

# Local alignment (Smith-Waterman). Default mode is 'global' (Needleman-Wunsch).
seq1 = DNA('ATCGATCGATCG')
seq2 = DNA('ATCGGGGATCG')
res = pair_align(seq1, seq2, mode='local')

# pair_align returns a named tuple: (score, paths, matrices)
print(f"Score: {res.score}")
best = res.paths[0]                      # a PairAlignPath
aligned_seqs = best.to_aligned((seq1, seq2))
cigar = best.to_cigar((seq1, seq2))

# Custom scoring: match/mismatch tuple + affine gap (open, extend)
res = pair_align(seq1, seq2, sub_score=(2.0, -3.0), gap_cost=(5.0, 2.0))

# Nucleotide / protein wrappers (substitution matrix by name)
res_n = pair_align_nucl(seq1, seq2)
p1, p2 = Protein('ACDEFGHIKLMNPQRSTVWY'), Protein('ACDEFMNPQRSTVWY')
res_p = pair_align_prot(p1, p2, sub_score='BLOSUM62', gap_cost=(11.0, 1.0))
```

### Multiple Sequence Alignment

```python
from skbio.alignment import TabularMSA
from skbio import DNA

# Read MSA from file
msa = TabularMSA.read('alignment.fasta', constructor=DNA)

# Create MSA manually
seqs = [
    DNA('ATCG--'),
    DNA('ATGG--'),
    DNA('ATCGAT')
]
msa = TabularMSA(seqs)

# MSA operations
consensus = msa.consensus()
majority_consensus = msa.majority_consensus()

# Calculate conservation
conservation = msa.conservation()

# Access sequences
first_seq = msa[0]
column = msa[:, 2]  # Third column

# Filter gaps
degapped_msa = msa.omit_gap_positions(maximum_gap_frequency=0.5)

# Calculate position-specific scores
position_entropies = msa.position_entropies()
```

### CIGAR String Handling

```python
from skbio.alignment import PairAlignPath, pair_align

# Parse a CIGAR string into a pairwise alignment path
path = PairAlignPath.from_cigar("10M2I5M3D10M")

# Convert a computed alignment back to CIGAR
res = pair_align(seq1, seq2)
cigar_string = res.paths[0].to_cigar((seq1, seq2))
```

## Phylogenetic Trees

### Tree Construction

```python
from skbio import TreeNode, DistanceMatrix
from skbio.tree import nj, upgma

# Distance matrix
dm = DistanceMatrix([[0, 5, 9, 9],
                     [5, 0, 10, 10],
                     [9, 10, 0, 8],
                     [9, 10, 8, 0]],
                    ids=['A', 'B', 'C', 'D'])

# Neighbor joining
nj_tree = nj(dm)

# UPGMA (assumes molecular clock)
upgma_tree = upgma(dm)

# Balanced Minimum Evolution (scalable for large trees)
from skbio.tree import bme
bme_tree = bme(dm)
```

### Tree Manipulation

```python
from skbio import TreeNode

# Read tree
tree = TreeNode.read('tree.nwk', format='newick')

# Traversal
for node in tree.traverse():
    print(node.name)

# Preorder, postorder, levelorder
for node in tree.preorder():
    print(node.name)

# Get tips only
tips = list(tree.tips())

# Find specific node
node = tree.find('taxon_name')

# Root tree at midpoint
rooted_tree = tree.root_at_midpoint()

# Prune tree to specific taxa
pruned = tree.shear(['taxon1', 'taxon2', 'taxon3'])

# Get subtree
lca = tree.lowest_common_ancestor(['taxon1', 'taxon2'])
subtree = lca.copy()

# Add/remove nodes
parent = tree.find('parent_name')
child = TreeNode(name='new_child', length=0.5)
parent.append(child)

# Remove node
node_to_remove = tree.find('taxon_to_remove')
node_to_remove.parent.remove(node_to_remove)
```

### Tree Distances and Comparisons

```python
# Patristic distance (branch-length distance)
node1 = tree.find('taxon1')
node2 = tree.find('taxon2')
patristic = node1.distance(node2)

# Cophenetic matrix (all pairwise distances)
cophenetic_dm = tree.cophenetic_matrix()

# Robinson-Foulds distance (topology comparison); 'robinson_foulds' was renamed
rf_dist = tree.compare_rfd(other_tree)

# Normalized (proportion) RF distance in [0, 1]
rf_prop = tree.compare_rfd(other_tree, proportion=True)

# Pairwise RF across many trees -> DistanceMatrix
from skbio.tree import rf_dists
dm = rf_dists([tree, other_tree, third_tree])

# Tip-to-tip distances
tip_distances = tree.tip_tip_distances()
```

### Tree Visualization

```python
# ASCII art visualization
print(tree.ascii_art())

# For advanced visualization, export to external tools
tree.write('tree.nwk', format='newick')

# Then use ete3, toytree, or ggtree for publication-quality figures
```

## Diversity Metrics

### Alpha Diversity

```python
from skbio.diversity import alpha_diversity, get_alpha_diversity_metrics
import numpy as np

# Sample count data (samples x features)
counts = np.array([
    [10, 5, 0, 3],
    [2, 0, 8, 4],
    [5, 5, 5, 5]
])
sample_ids = ['Sample1', 'Sample2', 'Sample3']

# List available metrics
print(get_alpha_diversity_metrics())

# Calculate various alpha diversity metrics
shannon = alpha_diversity('shannon', counts, ids=sample_ids)
simpson = alpha_diversity('simpson', counts, ids=sample_ids)
observed = alpha_diversity('observed_features', counts, ids=sample_ids)  # was 'observed_otus'
chao1 = alpha_diversity('chao1', counts, ids=sample_ids)

# Note: 'shannon' uses natural log (base e) by default as of 0.6.1
# (was base 2 in earlier releases). Pass base=2 for the old behaviour.

# Phylogenetic alpha diversity (requires tree)
from skbio import TreeNode

tree = TreeNode.read('tree.nwk')
feature_ids = ['OTU1', 'OTU2', 'OTU3', 'OTU4']  # must match tree tip names

faith_pd = alpha_diversity('faith_pd', counts, ids=sample_ids,
                          tree=tree, taxa=feature_ids)  # 'taxa', renamed from 'otu_ids'
```

### Beta Diversity

```python
from skbio.diversity import beta_diversity, partial_beta_diversity

# Beta diversity (all pairwise comparisons)
bc_dm = beta_diversity('braycurtis', counts, ids=sample_ids)

# Jaccard (presence/absence)
jaccard_dm = beta_diversity('jaccard', counts, ids=sample_ids)

# Phylogenetic beta diversity (UniFrac); 'taxa' was renamed from 'otu_ids'
unifrac_dm = beta_diversity('unweighted_unifrac', counts,
                           ids=sample_ids,
                           tree=tree,
                           taxa=feature_ids)

weighted_unifrac_dm = beta_diversity('weighted_unifrac', counts,
                                    ids=sample_ids,
                                    tree=tree,
                                    taxa=feature_ids)

# Compute only specific pairs (more efficient)
pairs = [('Sample1', 'Sample2'), ('Sample1', 'Sample3')]
partial_dm = partial_beta_diversity('braycurtis', counts,
                                   ids=sample_ids,
                                   id_pairs=pairs)
```

### Rarefaction and Subsampling

```python
from skbio.stats import subsample_counts  # moved out of skbio.diversity

# Rarefy each sample to a fixed depth (subsampling without replacement)
depth = 1000
rarefied = [subsample_counts(row, n=depth) for row in counts]

# Multiple rarefactions for confidence intervals
import numpy as np
rarefactions = []
for i in range(100):
    rarefied_counts = np.array([subsample_counts(row, n=1000) for row in counts])
    shannon_rare = alpha_diversity('shannon', rarefied_counts)
    rarefactions.append(shannon_rare)

# Calculate mean and std
mean_shannon = np.mean(rarefactions, axis=0)
std_shannon = np.std(rarefactions, axis=0)
```

## Ordination

### Principal Coordinate Analysis (PCoA)

```python
from skbio.stats.ordination import pcoa
from skbio import DistanceMatrix
import numpy as np

# PCoA from distance matrix
dm = DistanceMatrix(...)
pcoa_results = pcoa(dm)

# Access coordinates
pc1 = pcoa_results.samples['PC1']
pc2 = pcoa_results.samples['PC2']

# Proportion explained
prop_explained = pcoa_results.proportion_explained

# Eigenvalues
eigenvalues = pcoa_results.eigvals

# Save results
pcoa_results.write('pcoa_results.txt')

# Plot with matplotlib
import matplotlib.pyplot as plt
plt.scatter(pc1, pc2)
plt.xlabel(f'PC1 ({prop_explained[0]*100:.1f}%)')
plt.ylabel(f'PC2 ({prop_explained[1]*100:.1f}%)')
```

### Canonical Correspondence Analysis (CCA)

```python
from skbio.stats.ordination import cca
import pandas as pd
import numpy as np

# Species abundance matrix (samples x species)
species = np.array([
    [10, 5, 3],
    [2, 8, 4],
    [5, 5, 5]
])

# Environmental variables (samples x variables)
env = pd.DataFrame({
    'pH': [6.5, 7.0, 6.8],
    'temperature': [20, 25, 22],
    'depth': [10, 15, 12]
})

# CCA: cca(y, x) where y = samples-by-features, x = samples-by-constraints.
# ID kwargs are sample_ids / feature_ids / constraint_ids.
cca_results = cca(species, env,
                 sample_ids=['Site1', 'Site2', 'Site3'],
                 feature_ids=['SpeciesA', 'SpeciesB', 'SpeciesC'])

# Access constrained axes
cca1 = cca_results.samples['CCA1']
cca2 = cca_results.samples['CCA2']

# Biplot scores for environmental variables
env_scores = cca_results.biplot_scores
```

### Redundancy Analysis (RDA)

```python
from skbio.stats.ordination import rda

# Similar to CCA but for linear relationships
rda_results = rda(species, env,
                 sample_ids=['Site1', 'Site2', 'Site3'],
                 feature_ids=['SpeciesA', 'SpeciesB', 'SpeciesC'])
```

## Statistical Tests

### PERMANOVA

```python
from skbio.stats.distance import permanova
from skbio import DistanceMatrix
import numpy as np

# Distance matrix
dm = DistanceMatrix(...)

# Grouping variable
grouping = ['Group1', 'Group1', 'Group2', 'Group2', 'Group3', 'Group3']

# Run PERMANOVA
results = permanova(dm, grouping, permutations=999)

print(f"Test statistic: {results['test statistic']}")
print(f"p-value: {results['p-value']}")
print(f"Sample size: {results['sample size']}")
print(f"Number of groups: {results['number of groups']}")
```

### ANOSIM

```python
from skbio.stats.distance import anosim

# ANOSIM test
results = anosim(dm, grouping, permutations=999)

print(f"R statistic: {results['test statistic']}")
print(f"p-value: {results['p-value']}")
```

### PERMDISP

```python
from skbio.stats.distance import permdisp

# Test homogeneity of dispersions
results = permdisp(dm, grouping, permutations=999)

print(f"F statistic: {results['test statistic']}")
print(f"p-value: {results['p-value']}")
```

### Mantel Test

```python
from skbio.stats.distance import mantel
from skbio import DistanceMatrix

# Two distance matrices to compare
dm1 = DistanceMatrix(...)  # e.g., genetic distance
dm2 = DistanceMatrix(...)  # e.g., geographic distance

# Mantel test
r, p_value, n = mantel(dm1, dm2, method='pearson', permutations=999)

print(f"Correlation: {r}")
print(f"p-value: {p_value}")
print(f"Sample size: {n}")

# Spearman correlation; one-sided test; reproducible permutations via seed
r_spearman, p, n = mantel(dm1, dm2, method='spearman',
                          alternative='greater', permutations=999, seed=42)
```

Signature: `mantel(x, y, method='pearson', permutations=999,
alternative='two-sided', strict=True, lookup=None, seed=None)` and returns
`(corr_coeff, p_value, n)`. Note: scikit-bio's `mantel` does **not** implement a
partial Mantel test (no control matrix); use an external implementation
(e.g. `scikit-bio`'s Mantel on residualized matrices, or `ecodist`/`vegan` in R)
if you need to control for a third distance matrix.

## Distance Matrices

### Creating and Manipulating Distance Matrices

```python
from skbio import DistanceMatrix, DissimilarityMatrix
import numpy as np

# Create from array
data = np.array([[0, 1, 2],
                 [1, 0, 3],
                 [2, 3, 0]])
dm = DistanceMatrix(data, ids=['A', 'B', 'C'])

# Access elements
dist_ab = dm['A', 'B']
row_a = dm['A']

# Slicing
subset_dm = dm.filter(['A', 'C'])

# Asymmetric dissimilarity matrix
asym_data = np.array([[0, 1, 2],
                      [3, 0, 4],
                      [5, 6, 0]])
dissim = DissimilarityMatrix(asym_data, ids=['X', 'Y', 'Z'])

# Read/write
dm.write('distances.txt')
dm2 = DistanceMatrix.read('distances.txt')

# Convert to condensed form (for scipy)
condensed = dm.condensed_form()

# Convert to dataframe
df = dm.to_data_frame()
```

## File I/O

### Reading Sequences

```python
import skbio

# Read single sequence
dna = skbio.DNA.read('sequence.fasta', format='fasta')

# Read multiple sequences (generator)
for seq in skbio.io.read('sequences.fasta', format='fasta', constructor=skbio.DNA):
    print(seq.metadata['id'], len(seq))

# Read into list
sequences = list(skbio.io.read('sequences.fasta', format='fasta',
                               constructor=skbio.DNA))

# Read FASTQ with quality scores
for seq in skbio.io.read('reads.fastq', format='fastq', constructor=skbio.DNA):
    quality = seq.positional_metadata['quality']
    print(f"Mean quality: {quality.mean()}")
```

### Writing Sequences

```python
# Write single sequence
dna.write('output.fasta', format='fasta')

# Write multiple sequences
sequences = [dna1, dna2, dna3]
skbio.io.write(sequences, format='fasta', into='output.fasta')

# Write with custom line wrapping
dna.write('output.fasta', format='fasta', max_width=60)
```

### BIOM Tables

```python
from skbio.table import Table  # not the top-level skbio namespace

# Read BIOM table
table = Table.read('table.biom', format='hdf5')

# Access data
sample_ids = table.ids(axis='sample')
feature_ids = table.ids(axis='observation')
matrix = table.matrix_data.toarray()  # if sparse

# Filter samples
abundant_samples = table.filter(lambda row, id_, md: row.sum() > 1000, axis='sample')

# Filter features (OTUs/ASVs)
prevalent_features = table.filter(lambda col, id_, md: (col > 0).sum() >= 3,
                                 axis='observation')

# Normalize
relative_abundance = table.norm(axis='sample', inplace=False)

# Write
table.write('filtered_table.biom', format='hdf5')
```

### Format Conversion

```python
# FASTQ to FASTA
seqs = skbio.io.read('input.fastq', format='fastq', constructor=skbio.DNA)
skbio.io.write(seqs, format='fasta', into='output.fasta')

# GenBank to FASTA
seqs = skbio.io.read('genes.gb', format='genbank', constructor=skbio.DNA)
skbio.io.write(seqs, format='fasta', into='genes.fasta')
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: "ValueError: Ids must be unique"
```python
# Problem: Duplicate sequence IDs
# Solution: Make IDs unique or filter duplicates
seen = set()
unique_seqs = []
for seq in sequences:
    if seq.metadata['id'] not in seen:
        unique_seqs.append(seq)
        seen.add(seq.metadata['id'])
```

#### Issue: "ValueError: Counts must be integers"
```python
# Problem: Relative abundances instead of counts
# Solution: Convert to integer counts or use appropriate metrics
counts_int = (abundance_table * 1000).astype(int)
```

#### Issue: Memory error with large files
```python
# Problem: Loading entire file into memory
# Solution: Use generators
for seq in skbio.io.read('huge.fasta', format='fasta', constructor=skbio.DNA):
    # Process one at a time
    process(seq)
```

#### Issue: Tree tips don't match OTU IDs
```python
# Problem: Mismatch between tree tip names and feature IDs
# Solution: Verify and align IDs
tree_tips = {tip.name for tip in tree.tips()}
feature_ids = set(feature_ids)
missing_in_tree = feature_ids - tree_tips
missing_in_table = tree_tips - feature_ids

# Prune tree to match table
tree_pruned = tree.shear(feature_ids)
```

#### Issue: Alignment fails with sequences of different lengths
```python
# Problem: Trying to align pre-aligned sequences
# Solution: Degap sequences first or ensure sequences are unaligned
seq1_degapped = seq1.degap()
seq2_degapped = seq2.degap()
alignment = pair_align(seq1_degapped, seq2_degapped, mode='local')
```

### Performance Tips

1. **Use appropriate data structures**: BIOM HDF5 for large tables, generators for large sequence files
2. **Parallel processing**: Use `partial_beta_diversity()` for subset calculations that can be parallelized
3. **Subsample large datasets**: For exploratory analysis, work with subsampled data first
4. **Cache results**: Save distance matrices and ordination results to avoid recomputation

### Integration Examples

#### With pandas
```python
import pandas as pd
from skbio import DistanceMatrix

# Distance matrix to DataFrame
dm = DistanceMatrix(...)
df = dm.to_data_frame()

# Alpha diversity to DataFrame
alpha = alpha_diversity('shannon', counts, ids=sample_ids)
alpha_df = pd.DataFrame({'shannon': alpha})
```

#### With matplotlib/seaborn
```python
import matplotlib.pyplot as plt
import seaborn as sns

# PCoA plot
fig, ax = plt.subplots()
scatter = ax.scatter(pc1, pc2, c=grouping, cmap='viridis')
ax.set_xlabel(f'PC1 ({prop_explained[0]*100:.1f}%)')
ax.set_ylabel(f'PC2 ({prop_explained[1]*100:.1f}%)')
plt.colorbar(scatter)

# Heatmap of distance matrix
sns.heatmap(dm.to_data_frame(), cmap='viridis')
```

#### With QIIME 2
```python
# scikit-bio objects are compatible with QIIME 2
# Export from QIIME 2
# qiime tools export --input-path table.qza --output-path exported/

# Read in scikit-bio
table = Table.read('exported/feature-table.biom')

# Process with scikit-bio
# ...

# Import back to QIIME 2 if needed
table.write('processed-table.biom')
# qiime tools import --input-path processed-table.biom --output-path processed.qza
```
