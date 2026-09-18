# Metabolomics Workflows

## Overview

PyOpenMS provides specialized tools for untargeted metabolomics analysis including feature detection optimized for small molecules, adduct grouping, compound identification, and integration with metabolomics databases.

## Untargeted Metabolomics Pipeline

### Complete Workflow

```python
import pyopenms as ms

def metabolomics_pipeline(input_files, output_dir):
    """
    Complete untargeted metabolomics workflow.

    Args:
        input_files: List of mzML file paths (one per sample)
        output_dir: Directory for output files
    """

    # Step 1: Peak picking and feature detection
    feature_maps = []

    for mzml_file in input_files:
        print(f"Processing {mzml_file}...")

        # Load data
        exp = ms.MSExperiment()
        ms.MzMLFile().load(mzml_file, exp)

        # Peak picking if the data is still in profile mode
        picker = ms.PeakPickerHiRes()
        exp_picked = ms.MSExperiment()
        picker.pickExperiment(exp, exp_picked)
        exp = exp_picked
        exp.updateRanges()

        # Feature detection via the metabolomics chain
        # (MassTraceDetection -> ElutionPeakDetection -> FeatureFindingMetabo).
        # For peptide/centroided data use FeatureFinderAlgorithmPicked instead.
        mtd = ms.MassTraceDetection()
        mtd_params = mtd.getDefaults()
        mtd_params.setValue("mass_error_ppm", 5.0)   # tight for high-res metabolites
        mtd_params.setValue("noise_threshold_int", 1000.0)
        mtd.setParameters(mtd_params)
        mass_traces = []
        mtd.run(exp, mass_traces, 0)

        epd = ms.ElutionPeakDetection()
        split_traces = []
        epd.detectPeaks(mass_traces, split_traces)

        ffm = ms.FeatureFindingMetabo()
        ffm_params = ffm.getDefaults()
        ffm_params.setValue("isotope_filtering_model", "none")
        ffm.setParameters(ffm_params)
        features = ms.FeatureMap()
        chrom_out = []
        ffm.run(split_traces, features, chrom_out)

        features.setPrimaryMSRunPath([mzml_file.encode()])
        feature_maps.append(features)

        print(f"  Detected {features.size()} features")

    # Step 2: Adduct detection and grouping.
    # Class is MetaboliteFeatureDeconvolution; potential_adducts uses the
    # "Element:charge:probability" syntax (NOT "[M+H]+"), and compute() takes
    # four maps: (fm_in, fm_out, cons_map, cons_map_pairs).
    print("Detecting adducts...")
    adduct_grouped_maps = []

    adduct_detector = ms.MetaboliteFeatureDeconvolution()
    params = adduct_detector.getParameters()
    params.setValue("potential_adducts", [b"H:+:0.6", b"Na:+:0.2",
                                          b"K:+:0.1", b"NH4:+:0.1"])
    params.setValue("charge_min", 1)
    params.setValue("charge_max", 1)
    adduct_detector.setParameters(params)

    for fm in feature_maps:
        fm_out = ms.FeatureMap()
        adduct_detector.compute(fm, fm_out, ms.ConsensusMap(), ms.ConsensusMap())
        adduct_grouped_maps.append(fm_out)

    # Step 3: RT alignment.
    # align() processes one map at a time against a fixed reference.
    print("Aligning retention times...")
    aligner = ms.MapAlignmentAlgorithmPoseClustering()

    params = aligner.getParameters()
    params.setValue("max_num_peaks_considered", 1000)
    params.setValue("pairfinder:distance_MZ:max_difference", 10.0)
    params.setValue("pairfinder:distance_MZ:unit", "ppm")
    aligner.setParameters(params)

    aligner.setReference(adduct_grouped_maps[0])
    transformer = ms.MapAlignmentTransformer()
    for fm in adduct_grouped_maps[1:]:
        trafo = ms.TransformationDescription()
        aligner.align(fm, trafo)
        transformer.transformRetentionTimes(fm, trafo, True)
    aligned_maps = adduct_grouped_maps  # transformed in place

    # Step 4: Feature linking
    print("Linking features...")
    grouper = ms.FeatureGroupingAlgorithmQT()

    params = grouper.getParameters()
    params.setValue("distance_RT:max_difference", 60.0)  # seconds
    params.setValue("distance_MZ:max_difference", 5.0)  # ppm
    params.setValue("distance_MZ:unit", "ppm")
    grouper.setParameters(params)

    consensus_map = ms.ConsensusMap()
    grouper.group(aligned_maps, consensus_map)

    print(f"Created {consensus_map.size()} consensus features")

    # Step 5: Gap filling (fill missing values)
    print("Filling gaps...")
    # Gap filling not directly available in Python API
    # Would use TOPP tool FeatureFinderMetaboIdent

    # Step 6: Export results
    consensus_file = f"{output_dir}/consensus.consensusXML"
    ms.ConsensusXMLFile().store(consensus_file, consensus_map)

    # Export to CSV for downstream analysis
    df = consensus_map.get_df()
    csv_file = f"{output_dir}/metabolite_table.csv"
    df.to_csv(csv_file, index=False)

    print(f"Results saved to {output_dir}")

    return consensus_map

# Run pipeline
input_files = ["sample1.mzML", "sample2.mzML", "sample3.mzML"]
consensus = metabolomics_pipeline(input_files, "output")
```

## Adduct Detection

### Configure Adduct Types

```python
# Create adduct detector
adduct_detector = ms.MetaboliteFeatureDeconvolution()

# Configure common adducts.
# Each entry is "Element:charge:probability" (probabilities are relative
# weights, not required to sum to 1). This is NOT the "[M+H]+" notation.
params = adduct_detector.getParameters()

# Positive mode adducts
positive_adducts = [b"H:+:0.6", b"Na:+:0.2", b"K:+:0.1", b"NH4:+:0.1"]

# Negative mode adducts (set charge_min/charge_max to negative for these)
negative_adducts = [b"H-1:-:0.8", b"Cl:-:0.2"]

# Set for positive mode
params.setValue("potential_adducts", positive_adducts)
params.setValue("charge_min", 1)
params.setValue("charge_max", 1)
params.setValue("max_neutrals", 1)
adduct_detector.setParameters(params)

# Apply adduct detection. compute() needs four maps:
# (input, output, consensus, consensus_pairs).
feature_map_out = ms.FeatureMap()
adduct_detector.compute(feature_map, feature_map_out,
                        ms.ConsensusMap(), ms.ConsensusMap())
```

### Access Adduct Information

```python
# Check adduct annotations
for feature in feature_map_out:
    # Get adduct type if annotated
    if feature.metaValueExists("adduct"):
        adduct = feature.getMetaValue("adduct")
        neutral_mass = feature.getMetaValue("neutral_mass")
        print(f"m/z: {feature.getMZ():.4f}")
        print(f"  Adduct: {adduct}")
        print(f"  Neutral mass: {neutral_mass:.4f}")
```

## Compound Identification

### Mass-Based Annotation

```python
# Annotate features with compound database
from pyopenms import MassDecomposition

# Load compound database (example structure)
# In practice, use external database like HMDB, METLIN

compound_db = [
    {"name": "Glucose", "formula": "C6H12O6", "mass": 180.0634},
    {"name": "Citric acid", "formula": "C6H8O7", "mass": 192.0270},
    # ... more compounds
]

# Annotate features
mass_tolerance = 5.0  # ppm

for feature in feature_map:
    observed_mz = feature.getMZ()

    # Calculate neutral mass (assuming [M+H]+)
    neutral_mass = observed_mz - 1.007276  # Proton mass

    # Search database
    for compound in compound_db:
        mass_error_ppm = abs(neutral_mass - compound["mass"]) / compound["mass"] * 1e6

        if mass_error_ppm <= mass_tolerance:
            print(f"Potential match: {compound['name']}")
            print(f"  Observed m/z: {observed_mz:.4f}")
            print(f"  Expected mass: {compound['mass']:.4f}")
            print(f"  Error: {mass_error_ppm:.2f} ppm")
```

### MS/MS-Based Identification

```python
# Load MS2 data
exp = ms.MSExperiment()
ms.MzMLFile().load("data_with_ms2.mzML", exp)

# Extract MS2 spectra
ms2_spectra = []
for spec in exp:
    if spec.getMSLevel() == 2:
        ms2_spectra.append(spec)

print(f"Found {len(ms2_spectra)} MS2 spectra")

# Match to spectral library
# (Requires external tool or custom implementation)
```

## Data Normalization

### Total Ion Current (TIC) Normalization

```python
import numpy as np

# Load consensus map
consensus_map = ms.ConsensusMap()
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Calculate TIC per sample
n_samples = len(consensus_map.getColumnHeaders())
tic_per_sample = np.zeros(n_samples)

for cons_feature in consensus_map:
    for handle in cons_feature.getFeatureList():
        map_idx = handle.getMapIndex()
        tic_per_sample[map_idx] += handle.getIntensity()

print("TIC per sample:", tic_per_sample)

# Normalize to median TIC
median_tic = np.median(tic_per_sample)
normalization_factors = median_tic / tic_per_sample

print("Normalization factors:", normalization_factors)

# Apply normalization
consensus_map_normalized = ms.ConsensusMap(consensus_map)
for cons_feature in consensus_map_normalized:
    feature_list = cons_feature.getFeatureList()
    for handle in feature_list:
        map_idx = handle.getMapIndex()
        normalized_intensity = handle.getIntensity() * normalization_factors[map_idx]
        handle.setIntensity(normalized_intensity)
```

## Quality Control

### Coefficient of Variation (CV) Filtering

```python
import pandas as pd
import numpy as np

# Export to pandas
df = consensus_map.get_df()

# Assume QC samples are columns with 'QC' in name
qc_cols = [col for col in df.columns if 'QC' in col]

if qc_cols:
    # Calculate CV for each feature in QC samples
    qc_data = df[qc_cols]
    cv = (qc_data.std(axis=1) / qc_data.mean(axis=1)) * 100

    # Filter features with CV < 30% in QC samples
    good_features = df[cv < 30]

    print(f"Features before CV filter: {len(df)}")
    print(f"Features after CV filter: {len(good_features)}")
```

### Blank Filtering

```python
# Remove features present in blank samples
blank_cols = [col for col in df.columns if 'Blank' in col]
sample_cols = [col for col in df.columns if 'Sample' in col]

if blank_cols and sample_cols:
    # Calculate mean intensity in blanks and samples
    blank_mean = df[blank_cols].mean(axis=1)
    sample_mean = df[sample_cols].mean(axis=1)

    # Keep features with 3x higher intensity in samples than blanks
    ratio = sample_mean / (blank_mean + 1)  # Add 1 to avoid division by zero
    filtered_df = df[ratio > 3]

    print(f"Features before blank filtering: {len(df)}")
    print(f"Features after blank filtering: {len(filtered_df)}")
```

## Missing Value Imputation

```python
import pandas as pd
import numpy as np

# Load data
df = consensus_map.get_df()

# Replace zeros with NaN
df = df.replace(0, np.nan)

# Count missing values
missing_per_feature = df.isnull().sum(axis=1)
print(f"Features with >50% missing: {sum(missing_per_feature > len(df.columns)/2)}")

# Simple imputation: replace with minimum value
for col in df.columns:
    if df[col].dtype in [np.float64, np.int64]:
        min_val = df[col].min() / 2  # Half minimum
        df[col].fillna(min_val, inplace=True)
```

## Metabolite Table Export

### Create Analysis-Ready Table

```python
import pandas as pd

def create_metabolite_table(consensus_map, output_file):
    """
    Create metabolite quantification table for statistical analysis.
    """

    # Get column headers (file descriptions)
    headers = consensus_map.getColumnHeaders()

    # Initialize data structure
    data = {
        'mz': [],
        'rt': [],
        'feature_id': []
    }

    # Add sample columns
    for map_idx, header in headers.items():
        sample_name = header.label or f"Sample_{map_idx}"
        data[sample_name] = []

    # Extract feature data
    for idx, cons_feature in enumerate(consensus_map):
        data['mz'].append(cons_feature.getMZ())
        data['rt'].append(cons_feature.getRT())
        data['feature_id'].append(f"F{idx:06d}")

        # Initialize intensities
        intensities = {map_idx: 0.0 for map_idx in headers.keys()}

        # Fill in measured intensities
        for handle in cons_feature.getFeatureList():
            map_idx = handle.getMapIndex()
            intensities[map_idx] = handle.getIntensity()

        # Add to data structure
        for map_idx, header in headers.items():
            sample_name = header.label or f"Sample_{map_idx}"
            data[sample_name].append(intensities[map_idx])

    # Create DataFrame
    df = pd.DataFrame(data)

    # Sort by RT
    df = df.sort_values('rt')

    # Save to CSV
    df.to_csv(output_file, index=False)

    print(f"Metabolite table with {len(df)} features saved to {output_file}")

    return df

# Create table
df = create_metabolite_table(consensus_map, "metabolite_table.csv")
```

## Integration with External Tools

### Export for MetaboAnalyst

```python
def export_for_metaboanalyst(df, output_file):
    """
    Format data for MetaboAnalyst input.

    Requires sample names as columns, features as rows.
    """

    # Transpose DataFrame
    # Remove metadata columns
    sample_cols = [col for col in df.columns if col not in ['mz', 'rt', 'feature_id']]

    # Extract sample data
    sample_data = df[sample_cols]

    # Transpose (samples as rows, features as columns)
    df_transposed = sample_data.T

    # Add feature identifiers as column names
    df_transposed.columns = df['feature_id']

    # Save
    df_transposed.to_csv(output_file)

    print(f"MetaboAnalyst format saved to {output_file}")

# Export
export_for_metaboanalyst(df, "for_metaboanalyst.csv")
```

## Best Practices

### Sample Size and Replicates

- Include QC samples (pooled sample) every 5-10 injections
- Run blank samples to identify contamination
- Use at least 3 biological replicates per group
- Randomize sample injection order

### Parameter Optimization

Test parameters on pooled QC sample:

```python
# Test different mass trace parameters
mz_tolerances = [3.0, 5.0, 10.0]
min_spectra_values = [3, 5, 7]

for tol in mz_tolerances:
    for min_spec in min_spectra_values:
        ff = ms.FeatureFinderAlgorithmPicked()
        params = ff.getParameters()
        params.setValue("mass_trace:mz_tolerance", tol)
        params.setValue("mass_trace:min_spectra", min_spec)
        ff.setParameters(params)

        features = ms.FeatureMap()
        ff.run(exp, features, params, ms.FeatureMap())

        print(f"tol={tol}, min_spec={min_spec}: {features.size()} features")
```

### Retention Time Windows

Adjust based on chromatographic method:

```python
# For 10-minute LC gradient
params.setValue("distance_RT:max_difference", 30.0)  # 30 seconds

# For 60-minute LC gradient
params.setValue("distance_RT:max_difference", 90.0)  # 90 seconds
```
