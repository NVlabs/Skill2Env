# gget Module Examples

Worked CLI and Python usage examples for every gget module. For full parameter
tables see `module_reference.md`; for queried-database details see
`database_info.md`; for multi-module pipelines see `workflows.md`.

Most modules return:
- **Command-line**: JSON (default) or CSV with `-csv` flag
- **Python**: DataFrame or dictionary

Common flags across modules: `-o/--out` (save to file), `-q/--quiet` (suppress
progress), `-csv` (CSV format, command-line only).

---

## Reference & Gene Information

### gget ref — Reference Genome Downloads

Retrieve download links and metadata for Ensembl reference genomes.

```bash
# List available species
gget ref --list_species

# Get all reference files for human
gget ref homo_sapiens

# Download only GTF annotation for mouse
gget ref -w gtf -d mouse

# Multiple file types: comma-separated, no spaces (GTF + cDNA)
gget ref -w gtf,cdna -d mouse
```

```python
gget.ref("homo_sapiens")
gget.ref("mus_musculus", which="gtf", download=True)
# In Python, multiple types are passed as a list
gget.ref("mus_musculus", which=["gtf", "cdna"], download=True)
```

### gget search — Gene Search

Locate genes by name or description across species. Returns ensembl_id,
gene_name, ensembl_description, ext_ref_description, biotype, URL.

```bash
# Search for GABA-related genes in human
gget search -s human gaba gamma-aminobutyric

# Find specific gene, require all terms
gget search -s mouse -ao and pax7 transcription
```

```python
gget.search(["gaba", "gamma-aminobutyric"], species="homo_sapiens")
```

### gget info — Gene/Transcript Information

Retrieve gene/transcript metadata from Ensembl, UniProt, and NCBI. Limit ~1000
IDs. Returns UniProt ID, NCBI gene ID, gene name, synonyms, protein names,
descriptions, biotype, canonical transcript.

```bash
# Get info for multiple genes
gget info ENSG00000034713 ENSG00000104853 ENSG00000170296

# Include PDB IDs
gget info ENSG00000034713 -pdb
```

```python
gget.info(["ENSG00000034713", "ENSG00000104853"], pdb=True)
```

### gget seq — Sequence Retrieval

Fetch nucleotide or amino acid sequences for genes and transcripts (FASTA).

```bash
# Get nucleotide sequences
gget seq ENSG00000034713 ENSG00000104853

# Get all protein isoforms
gget seq -t -iso ENSG00000034713
```

```python
gget.seq(["ENSG00000034713"], translate=True, isoforms=True)
```

---

## Sequence Analysis & Alignment

### gget blast — BLAST Searches

BLAST nucleotide or amino acid sequences against standard databases. Program and
sequence type are auto-detected.

```bash
# BLAST protein sequence
gget blast MKWMFKEDHSLEHRCVESAKIRAKYPDRVPVIVEKVSGSQIVDIDKRKYLVPSDITVAQFMWIIRKRIQLPSEKAIFLFVDKTVPQSR

# BLAST from file with specific database
gget blast sequence.fasta -db swissprot -l 10
```

```python
gget.blast("MKWMFK...", database="swissprot", limit=10)
```

### gget blat — BLAT Searches

Locate genomic positions of sequences using UCSC BLAT. Returns genome, query
size, alignment positions, matches, mismatches, alignment percentage.

```bash
# Find genomic location in human
gget blat ATCGATCGATCGATCG

# Search in different assembly
gget blat -a mm39 ATCGATCGATCGATCG
```

```python
gget.blat("ATCGATCGATCGATCG", assembly="mouse")
```

### gget muscle — Multiple Sequence Alignment

Align multiple sequences using Muscle5. Returns ClustalW or aligned FASTA (.afa).

```bash
# Align sequences from file
gget muscle sequences.fasta -o aligned.afa

# Use Super5 for large dataset
gget muscle large_dataset.fasta -s5
```

```python
gget.muscle("sequences.fasta", save=True)
```

### gget diamond — Local Sequence Alignment

Fast local protein or translated DNA alignment using DIAMOND. Returns identity
percentage, sequence lengths, match positions, gap openings, E-values, bit scores.

```bash
# Align against reference
gget diamond GGETISAWESQME -ref reference.fasta --threads 4

# Save database for reuse
gget diamond query.fasta -ref ref.fasta --diamond_db my_db.dmnd
```

```python
gget.diamond("GGETISAWESQME", reference="reference.fasta", threads=4)
```

---

## Structural & Protein Analysis

### gget pdb — Protein Structures

Query RCSB Protein Data Bank for structure and metadata. Returns PDB format
(structures) or JSON (metadata).

```bash
# Download PDB structure
gget pdb 7S7U -o 7S7U.pdb

# Get metadata
gget pdb 7S7U -r entry
```

```python
gget.pdb("7S7U", save=True)
```

### gget alphafold — Protein Structure Prediction

Predict 3D protein structures using simplified AlphaFold2. Multiple sequences
trigger multimer modeling. Returns PDB structure, JSON alignment error, optional
3D visualization.

**Setup required:**
```bash
# Install OpenMM first
uv pip install openmm

# Then setup AlphaFold
gget setup alphafold
```

```bash
# Predict single protein structure
gget alphafold MKWMFKEDHSLEHRCVESAKIRAKYPDRVPVIVEKVSGSQIVDIDKRKYLVPSDITVAQFMWIIRKRIQLPSEKAIFLFVDKTVPQSR

# Predict multimer with higher accuracy
gget alphafold sequence1.fasta -mr 20 -r
```

```python
# Python with visualization
gget.alphafold("MKWMFK...", plot=True, show_sidechains=True)

# Multimer prediction
gget.alphafold(["sequence1", "sequence2"], multimer_recycles=20)
```

### gget elm — Eukaryotic Linear Motifs

Predict Eukaryotic Linear Motifs in protein sequences. Returns two outputs:
**ortholog_df** (motifs from orthologous proteins) and **regex_df** (motifs
directly matched in the input sequence).

**Setup required:**
```bash
gget setup elm
```

```bash
# Predict motifs from sequence
gget elm LIAQSIGQASFV -o results

# Use UniProt accession with expanded info
gget elm --uniprot Q02410 -e
```

```python
ortholog_df, regex_df = gget.elm("LIAQSIGQASFV")
```

---

## Expression & Disease Data

### gget archs4 — Gene Correlation & Tissue Expression

Query ARCHS4 for correlated genes (100 most correlated) or tissue expression.

```bash
# Get correlated genes
gget archs4 ACE2

# Get tissue expression
gget archs4 -w tissue ACE2
```

```python
gget.archs4("ACE2", which="tissue")
```

### gget cellxgene — Single-Cell RNA-seq Data

Query CZ CELLxGENE Discover Census. Gene names are **case-sensitive**
('PAX7' for human, 'Pax7' for mouse). Returns AnnData (or metadata-only frames).

**Setup required:**
```bash
gget setup cellxgene
```

```bash
# Get single-cell data for specific genes and cell types
gget cellxgene --gene ACE2 ABCA1 --tissue lung --cell_type "mucus secreting cell" -o lung_data.h5ad

# Metadata only
gget cellxgene --gene PAX7 --tissue muscle --meta_only -o metadata.csv
```

```python
adata = gget.cellxgene(gene=["ACE2", "ABCA1"], tissue="lung", cell_type="mucus secreting cell")
```

### gget enrichr — Enrichment Analysis

Ontology enrichment analysis on gene lists using Enrichr.

**Database shortcuts:**
- `pathway` → KEGG_2021_Human
- `transcription` → ChEA_2016
- `ontology` → GO_Biological_Process_2021
- `diseases_drugs` → GWAS_Catalog_2019
- `celltypes` → PanglaoDB_Augmented_2021

```bash
# Enrichment analysis for ontology
gget enrichr -db ontology ACE2 AGT AGTR1

# Save KEGG pathways
gget enrichr -db pathway ACE2 AGT AGTR1 -ko ./kegg_images/
```

```python
gget.enrichr(["ACE2", "AGT", "AGTR1"], database="ontology", plot=True)
```

### gget bgee — Orthology & Expression

Retrieve orthology and gene expression data from Bgee.

```bash
# Get orthologs
gget bgee ENSG00000169194

# Get expression data
gget bgee ENSG00000169194 -t expression

# Multiple genes
gget bgee ENSBTAG00000047356 ENSBTAG00000018317 -t expression
```

```python
gget.bgee("ENSG00000169194", type="orthologs")
```

### gget opentargets — Disease & Drug Associations

Retrieve disease and drug associations from OpenTargets. Resources: diseases
(default), drugs, tractability, pharmacogenetics, expression, depmap, interactions.

```bash
# Get associated diseases
gget opentargets ENSG00000169194 -r diseases -l 5

# Get associated drugs
gget opentargets ENSG00000169194 -r drugs -l 10

# Get tissue expression
gget opentargets ENSG00000169194 -r expression --filter_tissue brain
```

```python
gget.opentargets("ENSG00000169194", resource="diseases", limit=5)
```

### gget cbio — cBioPortal Cancer Genomics

Plot cancer genomics heatmaps using cBioPortal data. Two subcommands: `search`
(find study IDs) and `plot` (generate heatmaps).

```bash
# Search for studies
gget cbio search esophag ovary

# Create heatmap
gget cbio plot -s msk_impact_2017 -g AKT1 ALK BRAF -st tissue -vt mutation_occurrences
```

```python
gget.cbio_search(["esophag", "ovary"])
gget.cbio_plot(["msk_impact_2017"], ["AKT1", "ALK"], stratification="tissue")
```

### gget cosmic — COSMIC Database

Search COSMIC (Catalogue Of Somatic Mutations In Cancer). License fees apply for
commercial use; requires COSMIC account credentials.

```bash
# First download database
gget cosmic -d --email user@example.com --password xxx -cp cancer

# Then query
gget cosmic EGFR -ctp cosmic_data.tsv -l 10
```

```python
gget.cosmic("EGFR", cosmic_tsv_path="cosmic_data.tsv", limit=10)
```

---

## Additional Tools

### gget mutate — Generate Mutated Sequences

Generate mutated nucleotide sequences from mutation annotations (FASTA output).

```bash
# Single mutation
gget mutate ATCGCTAAGCT -m "c.4G>T"

# Multiple sequences with mutations from file
gget mutate sequences.fasta -m mutations.csv -o mutated.fasta
```

```python
import pandas as pd
mutations_df = pd.DataFrame({"seq_ID": ["seq1"], "mutation": ["c.4G>T"]})
gget.mutate(["ATCGCTAAGCT"], mutations=mutations_df)
```

### gget gpt — OpenAI Text Generation

Generate natural language text using OpenAI's API. Free tier limited to 3 months
after account creation; set monthly billing limits.

**Setup required:**
```bash
gget setup gpt
```

```bash
gget gpt "Explain CRISPR" --api_key your_key_here
```

```python
gget.gpt("Explain CRISPR", api_key="your_key_here")
```

### gget setup — Install Dependencies

Install/download third-party dependencies for specific modules.

Modules requiring setup:
- `alphafold` — downloads ~4GB of model parameters
- `cellxgene` — installs cellxgene-census (may not support latest Python)
- `elm` — downloads local ELM database
- `gpt` — configures OpenAI integration

```bash
# Setup AlphaFold
gget setup alphafold

# Setup ELM with custom directory
gget setup elm -o /path/to/elm_data
```

```python
gget.setup("alphafold")
```
