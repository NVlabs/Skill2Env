# Peptide and Protein Identification

## Overview

PyOpenMS supports peptide/protein identification through integration with search engines and provides tools for post-processing identification results including FDR control, protein inference, and annotation.

## Supported Search Engines

PyOpenMS integrates with these search engines:

- **Comet**: Fast tandem MS search
- **Mascot**: Commercial search engine
- **MSGFPlus**: Spectral probability-based search
- **XTandem**: Open-source search tool
- **OMSSA**: NCBI search engine
- **Myrimatch**: High-throughput search
- **MSFragger**: Ultra-fast search

## Reading Identification Data

### idXML Format

```python
import pyopenms as ms

# Load identification results.
# pyOpenMS 3.x: peptide_ids MUST be a PeptideIdentificationList (a plain []
# is rejected by load()); protein_ids stays a plain list.
protein_ids = []
peptide_ids = ms.PeptideIdentificationList()

ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

print(f"Protein identifications: {len(protein_ids)}")
print(f"Peptide identifications: {len(peptide_ids)}")
```

### Access Peptide Identifications

```python
# Iterate through peptide IDs
for peptide_id in peptide_ids:
    # Spectrum metadata
    print(f"RT: {peptide_id.getRT():.2f}")
    print(f"m/z: {peptide_id.getMZ():.4f}")

    # Get peptide hits (ranked by score)
    hits = peptide_id.getHits()
    print(f"Number of hits: {len(hits)}")

    for hit in hits:
        sequence = hit.getSequence()
        print(f"  Sequence: {sequence.toString()}")
        print(f"  Score: {hit.getScore()}")
        print(f"  Charge: {hit.getCharge()}")
        print(f"  Mass error (ppm): {hit.getMetaValue('mass_error_ppm')}")

        # Get modifications
        if sequence.isModified():
            for i in range(sequence.size()):
                residue = sequence.getResidue(i)
                if residue.isModified():
                    print(f"    Modification at position {i}: {residue.getModificationName()}")
```

### Access Protein Identifications

```python
# Access protein-level information
for protein_id in protein_ids:
    # Search parameters
    search_params = protein_id.getSearchParameters()
    print(f"Search engine: {protein_id.getSearchEngine()}")
    print(f"Database: {search_params.db}")

    # Protein hits
    hits = protein_id.getHits()
    for hit in hits:
        print(f"  Accession: {hit.getAccession()}")
        print(f"  Score: {hit.getScore()}")
        print(f"  Coverage: {hit.getCoverage()}")
        print(f"  Sequence: {hit.getSequence()}")
```

## False Discovery Rate (FDR)

### FDR Filtering

Apply FDR filtering to control false positives.

Prerequisite: `fdr.apply()` needs each hit annotated with a `target_decoy`
meta value (`"target"` / `"decoy"`). That annotation is produced by searching a
concatenated target-decoy database and running `PeptideIndexer`; without it,
`apply()` raises "Meta value 'target_decoy' does not exist". After `apply()`,
each hit's **score becomes its q-value** (lower is better), so filtering at 1%
FDR is just a score threshold — use `IDFilter` rather than hand-rolled loops:

```python
# Create FDR object and rewrite scores to q-values
fdr = ms.FalseDiscoveryRate()
fdr.apply(peptide_ids)              # peptide_ids is a PeptideIdentificationList

# Filter at 1% FDR. filterHitsByScore respects each ID's score orientation
# (apply() sets it to lower-is-better), so this keeps hits with q-value <= 0.01.
ms.IDFilter().filterHitsByScore(peptide_ids, 0.01)
ms.IDFilter().removeEmptyIdentifications(peptide_ids)

print(f"Peptide IDs passing 1% FDR: {len(peptide_ids)}")
```

### Inspecting q-values

After `apply()`, the hit score is the q-value:

```python
for peptide_id in peptide_ids:
    for hit in peptide_id.getHits():
        print(f"Sequence: {hit.getSequence().toString()}, q-value: {hit.getScore()}")
```

## Protein Inference

### ID Mapper

Map peptide identifications to proteins:

```python
# Create mapper
mapper = ms.IDMapper()

# Map to features (peptide_ids is a PeptideIdentificationList)
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Annotate features with IDs
mapper.annotate(feature_map, peptide_ids, protein_ids)

# Check annotated features
for feature in feature_map:
    pep_ids = feature.getPeptideIdentifications()
    if pep_ids:
        for pep_id in pep_ids:
            for hit in pep_id.getHits():
                print(f"Feature {feature.getMZ():.4f}: {hit.getSequence().toString()}")
```

### Protein Grouping

Group proteins by shared peptides:

```python
# Create protein inference algorithm
inference = ms.BasicProteinInferenceAlgorithm()

# Run inference
inference.run(peptide_ids, protein_ids)

# Access protein groups
for protein_id in protein_ids:
    hits = protein_id.getHits()
    if len(hits) > 1:
        print("Protein group:")
        for hit in hits:
            print(f"  {hit.getAccession()}")
```

## Peptide Sequence Handling

### AASequence Object

Work with peptide sequences:

```python
# Create peptide sequence
seq = ms.AASequence.fromString("PEPTIDE")

print(f"Sequence: {seq.toString()}")
print(f"Monoisotopic mass: {seq.getMonoWeight():.4f}")
print(f"Average mass: {seq.getAverageWeight():.4f}")
print(f"Length: {seq.size()}")

# Access individual amino acids
for i in range(seq.size()):
    residue = seq.getResidue(i)
    print(f"Position {i}: {residue.getOneLetterCode()}, mass: {residue.getMonoWeight():.4f}")
```

### Modified Sequences

Handle post-translational modifications:

```python
# Sequence with modifications
mod_seq = ms.AASequence.fromString("PEPTIDEM(Oxidation)K")

print(f"Modified sequence: {mod_seq.toString()}")
print(f"Mass with mods: {mod_seq.getMonoWeight():.4f}")

# Check if modified
print(f"Is modified: {mod_seq.isModified()}")

# Get modification info
for i in range(mod_seq.size()):
    residue = mod_seq.getResidue(i)
    if residue.isModified():
        print(f"Residue {residue.getOneLetterCode()} at position {i}")
        print(f"  Modification: {residue.getModificationName()}")
```

### Peptide Digestion

Simulate enzymatic digestion:

```python
# Create digestion enzyme
enzyme = ms.ProteaseDigestion()
enzyme.setEnzyme("Trypsin")

# Set missed cleavages
enzyme.setMissedCleavages(2)

# Digest protein sequence
protein_seq = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL"

# Get peptides
peptides = []
enzyme.digest(ms.AASequence.fromString(protein_seq), peptides)

print(f"Generated {len(peptides)} peptides")
for peptide in peptides[:5]:  # Show first 5
    print(f"  {peptide.toString()}, mass: {peptide.getMonoWeight():.2f}")
```

## Theoretical Spectrum Generation

### Fragment Ion Calculation

Generate theoretical fragment ions:

```python
# Create peptide
peptide = ms.AASequence.fromString("PEPTIDE")

# Generate b and y ions
fragments = []
ms.TheoreticalSpectrumGenerator().getSpectrum(fragments, peptide, 1, 1)

print(f"Generated {fragments.size()} fragment ions")

# Access fragments
mz, intensity = fragments.get_peaks()
for m, i in zip(mz[:10], intensity[:10]):  # Show first 10
    print(f"m/z: {m:.4f}, intensity: {i}")
```

## Complete Identification Workflow

### End-to-End Example

```python
import pyopenms as ms

def identification_workflow(spectrum_file, fasta_file, output_file):
    """
    Complete identification workflow with FDR control.

    Args:
        spectrum_file: Input mzML file
        fasta_file: Protein database (FASTA)
        output_file: Output idXML file
    """

    # Step 1: Load spectra
    exp = ms.MSExperiment()
    ms.MzMLFile().load(spectrum_file, exp)
    print(f"Loaded {exp.getNrSpectra()} spectra")

    # Step 2: Configure search parameters
    search_params = ms.SearchParameters()
    search_params.db = fasta_file
    search_params.precursor_mass_tolerance = 10.0  # ppm
    search_params.fragment_mass_tolerance = 0.5  # Da
    search_params.enzyme = "Trypsin"
    search_params.missed_cleavages = 2
    search_params.modifications = ["Oxidation (M)", "Carbamidomethyl (C)"]

    # Step 3: Run search (example with Comet adapter)
    # Note: Requires search engine to be installed
    # comet = ms.CometAdapter()
    # protein_ids, peptide_ids = comet.search(exp, search_params)

    # For this example, load pre-computed results (already PeptideIndexer-
    # annotated with target_decoy). peptide_ids must be a PeptideIdentificationList.
    protein_ids = []
    peptide_ids = ms.PeptideIdentificationList()
    ms.IdXMLFile().load("raw_identifications.idXML", protein_ids, peptide_ids)

    print(f"Initial peptide IDs: {len(peptide_ids)}")

    # Step 4: Apply FDR (scores -> q-values) and filter at 1% with IDFilter
    fdr = ms.FalseDiscoveryRate()
    fdr.apply(peptide_ids)
    ms.IDFilter().filterHitsByScore(peptide_ids, 0.01)
    ms.IDFilter().removeEmptyIdentifications(peptide_ids)

    print(f"Peptide IDs after FDR (1%): {len(peptide_ids)}")

    # Step 5: Protein inference
    inference = ms.BasicProteinInferenceAlgorithm()
    inference.run(peptide_ids, protein_ids)

    print(f"Identified proteins: {len(protein_ids)}")

    # Step 6: Save results
    ms.IdXMLFile().store(output_file, protein_ids, peptide_ids)
    print(f"Results saved to {output_file}")

    return protein_ids, peptide_ids

# Run workflow
protein_ids, peptide_ids = identification_workflow(
    "spectra.mzML",
    "database.fasta",
    "identifications_fdr.idXML"
)
```

## Spectral Library Search

### Library Matching

Load an MSP spectral library. `MSPFile.load` reads the library spectra into an
`MSExperiment` and their peptide annotations into a `PeptideIdentificationList`:

```python
# Load spectral library (spectra -> MSExperiment, annotations -> ID list)
library_ids = ms.PeptideIdentificationList()
library_spectra = ms.MSExperiment()
ms.MSPFile().load("spectral_library.msp", library_ids, library_spectra)

# Load experimental spectra
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

print(f"Library spectra: {library_spectra.getNrSpectra()}, "
      f"query MS2 spectra: {sum(s.getMSLevel() == 2 for s in exp)}")
```

For the actual spectral comparison, score pairs of `MSSpectrum` objects with a
similarity metric such as `BinnedSpectrum` + `BinnedSpectralContrastAngle`
(`SpectraSTSimilarityScore` exposes `preprocess`/`compute_F`, not a simple
`operator()` call). For metabolite/small-molecule spectral matching, prefer the
`matchms` skill, which is purpose-built for cosine/modified-cosine scoring.

## Best Practices

### Decoy Database

Use target-decoy approach for FDR calculation:

```python
# Generate decoy database.
# DecoyGenerator.reverseProtein takes/returns an AASequence (not a FASTAEntry),
# so wrap each entry's sequence and write a new FASTAEntry with a decoy prefix.
decoy_generator = ms.DecoyGenerator()

# Load target database (FASTAEntry list; plain [] is fine for FASTA)
fasta_entries = []
ms.FASTAFile().load("target.fasta", fasta_entries)

# Generate decoys
decoy_entries = []
for entry in fasta_entries:
    rev = decoy_generator.reverseProtein(ms.AASequence.fromString(entry.sequence))
    decoy = ms.FASTAEntry()
    decoy.identifier = "DECOY_" + entry.identifier
    decoy.description = entry.description
    decoy.sequence = rev.toUnmodifiedString()
    decoy_entries.append(decoy)

# Save combined target+decoy database
all_entries = list(fasta_entries) + decoy_entries
ms.FASTAFile().store("target_decoy.fasta", all_entries)
```

### Score Interpretation

Understand score types from different engines:

```python
# The search engine lives on the ProteinIdentification run, not the peptide ID.
# Map each run identifier to its engine name first.
engine_by_run = {p.getIdentifier(): p.getSearchEngine() for p in protein_ids}

for peptide_id in peptide_ids:
    engine = engine_by_run.get(peptide_id.getIdentifier(), "")
    higher_better = peptide_id.isHigherScoreBetter()

    for hit in peptide_id.getHits():
        score = hit.getScore()
        # Whether higher is better is recorded per ID; do not assume by engine
        print(f"{engine} {peptide_id.getScoreType()}={score} "
              f"(higher_better={higher_better})")
```
