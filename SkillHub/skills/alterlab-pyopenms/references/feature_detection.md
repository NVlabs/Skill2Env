# Feature Detection and Linking

## Overview

Feature detection identifies persistent signals (chromatographic peaks) in LC-MS data. Feature linking combines features across multiple samples for quantitative comparison.

## Feature Detection Basics

A feature represents a chromatographic peak characterized by:
- m/z value (mass-to-charge ratio)
- Retention time (RT)
- Intensity
- Quality score
- Convex hull (spatial extent in RT-m/z space)

## Feature Finding

> pyOpenMS 3.x note: the old `FeatureFinder` facade (`ff.run("centroided", ...)`)
> was removed. The former `"centroided"` algorithm is now the standalone class
> `FeatureFinderAlgorithmPicked`; its `run(input_map, output, params, seeds)`
> takes the param object directly (no algorithm-name string). The
> `mass_trace:*` and `isotopic_pattern:*` parameter names are unchanged.
> For small molecules, prefer the metabolomics chain below
> (`MassTraceDetection` → `ElutionPeakDetection` → `FeatureFindingMetabo`).

### FeatureFinderAlgorithmPicked (peptide / centroided data)

Standard algorithm for feature detection in centroided data:

```python
import pyopenms as ms

# Load centroided data
exp = ms.MSExperiment()
ms.MzMLFile().load("centroided.mzML", exp)
exp.updateRanges()

# Create feature finder (former "centroided" algorithm)
ff = ms.FeatureFinderAlgorithmPicked()

# Get default parameters
params = ff.getParameters()

# Modify key parameters
params.setValue("mass_trace:mz_tolerance", 10.0)  # ppm
params.setValue("mass_trace:min_spectra", 7)  # Min scans per feature
params.setValue("isotopic_pattern:charge_low", 1)
params.setValue("isotopic_pattern:charge_high", 4)
ff.setParameters(params)

# Run feature detection (empty seeds = de novo)
features = ms.FeatureMap()
seeds = ms.FeatureMap()
ff.run(exp, features, params, seeds)

print(f"Detected {features.size()} features")

# Save features
ms.FeatureXMLFile().store("features.featureXML", features)
```

### FeatureFindingMetabo (small molecules)

The dedicated metabolomics workflow runs mass-trace detection, elution-peak
splitting, then assembles features:

```python
# Load centroided data
exp = ms.MSExperiment()
ms.MzMLFile().load("centroided.mzML", exp)
exp.updateRanges()

# 1. Detect mass traces
mtd = ms.MassTraceDetection()
mtd_params = mtd.getDefaults()
mtd_params.setValue("mass_error_ppm", 5.0)       # tight for high-res metabolomics
mtd_params.setValue("noise_threshold_int", 1000.0)
mtd.setParameters(mtd_params)
mass_traces = []
mtd.run(exp, mass_traces, 0)  # 0 = no limit on number of traces

# 2. Split traces into elution peaks
epd = ms.ElutionPeakDetection()
epd_params = epd.getDefaults()
epd_params.setValue("width_filtering", "fixed")
epd.setParameters(epd_params)
split_traces = []
epd.detectPeaks(mass_traces, split_traces)

# 3. Assemble features
ffm = ms.FeatureFindingMetabo()
ffm_params = ffm.getDefaults()
ffm_params.setValue("isotope_filtering_model", "none")
ffm.setParameters(ffm_params)
features = ms.FeatureMap()
chrom_out = []
ffm.run(split_traces, features, chrom_out)

print(f"Detected {features.size()} features")
```

## Accessing Feature Data

### Iterate Through Features

```python
# Load features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Access individual features
for feature in feature_map:
    print(f"m/z: {feature.getMZ():.4f}")
    print(f"RT: {feature.getRT():.2f}")
    print(f"Intensity: {feature.getIntensity():.0f}")
    print(f"Charge: {feature.getCharge()}")
    print(f"Quality: {feature.getOverallQuality():.3f}")
    print(f"Width (RT): {feature.getWidth():.2f}")

    # Get convex hull
    hull = feature.getConvexHull()
    print(f"Hull points: {hull.getHullPoints().size()}")
```

### Feature Subordinates (Isotope Pattern)

```python
# Access isotopic pattern
for feature in feature_map:
    # Get subordinate features (isotopes)
    subordinates = feature.getSubordinates()

    if subordinates:
        print(f"Main feature m/z: {feature.getMZ():.4f}")
        for sub in subordinates:
            print(f"  Isotope m/z: {sub.getMZ():.4f}")
            print(f"  Isotope intensity: {sub.getIntensity():.0f}")
```

### Export to Pandas

```python
import pandas as pd

# Convert to DataFrame
df = feature_map.get_df()

print(df.columns)
# Typical columns: RT, mz, intensity, charge, quality

# Analyze features
print(f"Mean intensity: {df['intensity'].mean()}")
print(f"RT range: {df['RT'].min():.1f} - {df['RT'].max():.1f}")
```

## Feature Linking

### Map Alignment

Align retention times before linking:

```python
# Load multiple feature maps
fm1 = ms.FeatureMap()
fm2 = ms.FeatureMap()
ms.FeatureXMLFile().load("sample1.featureXML", fm1)
ms.FeatureXMLFile().load("sample2.featureXML", fm2)

# Create aligner
aligner = ms.MapAlignmentAlgorithmPoseClustering()

# align() works on ONE map against a reference (it does NOT take a list).
# Pick a reference map, then align every other map to it.
aligner.setReference(fm1)  # fm1 is the reference; leave it unchanged

trafo = ms.TransformationDescription()
aligner.align(fm2, trafo)  # fills `trafo`; fm2 itself is not modified yet

# Apply the transformation to fm2's retention times
transformer = ms.MapAlignmentTransformer()
transformer.transformRetentionTimes(fm2, trafo, True)
```

### Feature Linking Algorithm

Link features across samples:

```python
# Create feature grouping algorithm
grouper = ms.FeatureGroupingAlgorithmQT()

# Configure parameters
params = grouper.getParameters()
params.setValue("distance_RT:max_difference", 30.0)  # Max RT difference (s)
params.setValue("distance_MZ:max_difference", 10.0)  # Max m/z difference (ppm)
params.setValue("distance_MZ:unit", "ppm")
grouper.setParameters(params)

# Prepare feature maps
feature_maps = [fm1, fm2, fm3]

# Create consensus map
consensus_map = ms.ConsensusMap()

# Link features
grouper.group(feature_maps, consensus_map)

print(f"Created {consensus_map.size()} consensus features")

# Save consensus map
ms.ConsensusXMLFile().store("consensus.consensusXML", consensus_map)
```

## Consensus Features

### Access Consensus Data

```python
# Load consensus map
consensus_map = ms.ConsensusMap()
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Iterate through consensus features
for cons_feature in consensus_map:
    print(f"Consensus m/z: {cons_feature.getMZ():.4f}")
    print(f"Consensus RT: {cons_feature.getRT():.2f}")

    # Get features from individual maps
    for handle in cons_feature.getFeatureList():
        map_idx = handle.getMapIndex()
        intensity = handle.getIntensity()
        print(f"  Sample {map_idx}: intensity {intensity:.0f}")
```

### Consensus Map Metadata

```python
# Access file descriptions (map metadata)
file_descriptions = consensus_map.getColumnHeaders()

for map_idx, description in file_descriptions.items():
    print(f"Map {map_idx}:")
    print(f"  Filename: {description.filename}")
    print(f"  Label: {description.label}")
    print(f"  Size: {description.size}")
```

## Adduct Detection

Identify different ionization forms of the same molecule:

```python
# Create adduct detector (class: MetaboliteFeatureDeconvolution)
adduct_detector = ms.MetaboliteFeatureDeconvolution()

# Configure parameters. Adducts use "Element:charge:probability" syntax,
# NOT "[M+H]+". Set one polarity at a time via charge_min/charge_max.
params = adduct_detector.getParameters()
params.setValue("potential_adducts", [b"H:+:0.7", b"Na:+:0.2", b"K:+:0.1"])
params.setValue("charge_min", 1)
params.setValue("charge_max", 1)
params.setValue("max_neutrals", 1)
adduct_detector.setParameters(params)

# Detect adducts. compute() takes four maps:
# (input, output, consensus, consensus_pairs).
feature_map_out = ms.FeatureMap()
adduct_detector.compute(feature_map, feature_map_out,
                        ms.ConsensusMap(), ms.ConsensusMap())
```

## Complete Feature Detection Workflow

### End-to-End Example

```python
import pyopenms as ms

def feature_detection_workflow(input_files, output_consensus):
    """
    Complete workflow: feature detection and linking across samples.

    Args:
        input_files: List of mzML file paths
        output_consensus: Output consensusXML file path
    """

    feature_maps = []

    # Step 1: Detect features in each file
    for mzml_file in input_files:
        print(f"Processing {mzml_file}...")

        # Load experiment
        exp = ms.MSExperiment()
        ms.MzMLFile().load(mzml_file, exp)

        exp.updateRanges()

        # Find features
        ff = ms.FeatureFinderAlgorithmPicked()
        params = ff.getParameters()
        params.setValue("mass_trace:mz_tolerance", 10.0)
        params.setValue("mass_trace:min_spectra", 7)
        ff.setParameters(params)

        features = ms.FeatureMap()
        ff.run(exp, features, params, ms.FeatureMap())

        # Store filename in feature map
        features.setPrimaryMSRunPath([mzml_file.encode()])

        feature_maps.append(features)
        print(f"  Found {features.size()} features")

    # Step 2: Align retention times.
    # align() takes one map at a time; use the first map as the reference.
    print("Aligning retention times...")
    aligner = ms.MapAlignmentAlgorithmPoseClustering()
    aligner.setReference(feature_maps[0])
    transformer = ms.MapAlignmentTransformer()
    for fm in feature_maps[1:]:
        trafo = ms.TransformationDescription()
        aligner.align(fm, trafo)
        transformer.transformRetentionTimes(fm, trafo, True)
    aligned_maps = feature_maps  # transformed in place

    # Step 3: Link features
    print("Linking features across samples...")
    grouper = ms.FeatureGroupingAlgorithmQT()
    params = grouper.getParameters()
    params.setValue("distance_RT:max_difference", 30.0)
    params.setValue("distance_MZ:max_difference", 10.0)
    params.setValue("distance_MZ:unit", "ppm")
    grouper.setParameters(params)

    consensus_map = ms.ConsensusMap()
    grouper.group(aligned_maps, consensus_map)

    # Save results
    ms.ConsensusXMLFile().store(output_consensus, consensus_map)

    print(f"Created {consensus_map.size()} consensus features")
    print(f"Results saved to {output_consensus}")

    return consensus_map

# Run workflow
input_files = ["sample1.mzML", "sample2.mzML", "sample3.mzML"]
consensus = feature_detection_workflow(input_files, "consensus.consensusXML")
```

## Feature Filtering

### Filter by Quality

```python
# Filter features by quality score
filtered_features = ms.FeatureMap()

for feature in feature_map:
    if feature.getOverallQuality() > 0.5:  # Quality threshold
        filtered_features.push_back(feature)

print(f"Kept {filtered_features.size()} high-quality features")
```

### Filter by Intensity

```python
# Keep only intense features
min_intensity = 10000

filtered_features = ms.FeatureMap()
for feature in feature_map:
    if feature.getIntensity() >= min_intensity:
        filtered_features.push_back(feature)
```

### Filter by m/z Range

```python
# Extract features in specific m/z range
mz_min = 200.0
mz_max = 800.0

filtered_features = ms.FeatureMap()
for feature in feature_map:
    mz = feature.getMZ()
    if mz_min <= mz <= mz_max:
        filtered_features.push_back(feature)
```

## Feature Annotation

### Add Identification Information

```python
# Annotate features with peptide identifications
# Load identifications (peptide list must be a PeptideIdentificationList)
protein_ids = []
peptide_ids = ms.PeptideIdentificationList()
ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Create ID mapper
mapper = ms.IDMapper()

# Map IDs to features
mapper.annotate(feature_map, peptide_ids, protein_ids)

# Check annotations
for feature in feature_map:
    peptide_ids_for_feature = feature.getPeptideIdentifications()
    if peptide_ids_for_feature:
        print(f"Feature at {feature.getMZ():.4f} m/z identified")
```

## Best Practices

### Parameter Optimization

Optimize parameters for your data type:

```python
# Test different tolerance values
mz_tolerances = [5.0, 10.0, 20.0]  # ppm

for tol in mz_tolerances:
    ff = ms.FeatureFinderAlgorithmPicked()
    params = ff.getParameters()
    params.setValue("mass_trace:mz_tolerance", tol)
    ff.setParameters(params)

    features = ms.FeatureMap()
    ff.run(exp, features, params, ms.FeatureMap())

    print(f"Tolerance {tol} ppm: {features.size()} features")
```

### Visual Inspection

Export features for visualization:

```python
# Convert to DataFrame for plotting
df = feature_map.get_df()

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(df['RT'], df['mz'], s=df['intensity']/1000, alpha=0.5)
plt.xlabel('Retention Time (s)')
plt.ylabel('m/z')
plt.title('Feature Map')
plt.colorbar(label='Intensity (scaled)')
plt.show()
```
