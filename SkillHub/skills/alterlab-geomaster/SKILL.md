---
name: alterlab-geomaster
description: Covers geospatial science across remote sensing, GIS, spatial analysis, and machine learning for earth observation — satellite imagery processing (Sentinel, Landsat, MODIS, SAR, hyperspectral), raster and DEM operations, spectral indices (NDVI/EVI/NDWI), spatial statistics, point cloud processing, network analysis, and cloud-native workflows (STAC, COG, Planetary Computer), with examples across Python, R, Julia, JavaScript, C++, Java, Go, and Rust. Use for remote sensing workflows, satellite/raster image classification, terrain/slope/hillshade analysis, spatial ML on earth-observation data, hydrological modeling, marine spatial analysis, or atmospheric science. For pure tabular vector work with no raster/EO aspect (plain GeoPandas sjoin, buffer, overlay, dissolve, choropleths) prefer the geopandas skill; for celestial-sphere astronomy coordinates (ICRS/galactic, FITS, WCS) prefer the astropy skill. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(uv:*) Bash(python:*)
compatibility: No API key required for local geospatial work. Runs via `uv run python`; cloud-native STAC/Planetary Computer workflows need network access (and provider credentials where applicable).
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# GeoMaster

Comprehensive geospatial science skill covering GIS, remote sensing, spatial analysis, and ML for Earth observation across 70+ topics with 500+ code examples in 8 programming languages.

## Installation

Pick ONE package manager for the GDAL-backed stack. Modern pip wheels for
rasterio/fiona/pyproj/shapely bundle their own GDAL/GEOS/PROJ, so a pure-pip
(uv) env covers the core libs without a system GDAL. Do NOT mix conda-GDAL
with pip rasterio/fiona in the same env — the two ship different GDAL binaries
and the ABI mismatch segfaults. The standalone `gdal` Python bindings do NOT
bundle binaries (they need a matching system/conda libgdal); PDAL and rsgislib
likewise have no reliable pip wheels — get those via conda (Option B).

```bash
# Option A — uv/pip env (recommended here): wheels bundle GDAL/GEOS/PROJ.
# rasterio/fiona cover most GDAL needs; standalone `gdal` -> use Option B.
uv pip install rasterio fiona shapely pyproj geopandas
uv pip install torchgeo earthengine-api
uv pip install scikit-learn xgboost torch-geometric
uv pip install osmnx networkx folium keplergl
uv pip install cartopy contextily mapclassify
uv pip install xarray rioxarray dask-geopandas
uv pip install pystac-client planetary-computer odc-stac rio-cogeo
uv pip install laspy[lazrs] open3d        # PDAL: use conda (no pip wheel)

# Option B — conda env (best for PDAL / rsgislib / system GDAL tooling)
conda install -c conda-forge gdal rasterio fiona shapely pyproj geopandas \
    rsgislib pdal python-pdal postgis libspatialite
```

## Quick Start

### NDVI from Sentinel-2

```python
import rasterio
import numpy as np

with rasterio.open('sentinel2.tif') as src:
    red = src.read(4).astype(float)   # B04
    nir = src.read(8).astype(float)   # B08
    ndvi = (nir - red) / (nir + red + 1e-8)
    ndvi = np.nan_to_num(ndvi, nan=0)

    profile = src.profile
    profile.update(count=1, dtype=rasterio.float32)

    with rasterio.open('ndvi.tif', 'w', **profile) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)
```

### Spatial Analysis with GeoPandas

```python
import geopandas as gpd

# Load and ensure same CRS
zones = gpd.read_file('zones.geojson')
points = gpd.read_file('points.geojson')

if zones.crs != points.crs:
    points = points.to_crs(zones.crs)

# Spatial join and statistics
joined = gpd.sjoin(points, zones, how='inner', predicate='within')
stats = joined.groupby('zone_id').agg({
    'value': ['count', 'mean', 'std', 'min', 'max']
}).round(2)
```

### Google Earth Engine Time Series

```python
import ee
import pandas as pd

ee.Initialize(project='your-project')
roi = ee.Geometry.Point([-122.4, 37.7]).buffer(10000)

s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
      .filterBounds(roi)
      .filterDate('2020-01-01', '2023-12-31')
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))

def add_ndvi(img):
    return img.addBands(img.normalizedDifference(['B8', 'B4']).rename('NDVI'))

s2_ndvi = s2.map(add_ndvi)

def extract_series(image):
    stats = image.reduceRegion(ee.Reducer.mean(), roi.centroid(), scale=10, maxPixels=1e9)
    return ee.Feature(None, {'date': image.date().format('YYYY-MM-dd'), 'ndvi': stats.get('NDVI')})

series = s2_ndvi.map(extract_series).getInfo()
df = pd.DataFrame([f['properties'] for f in series['features']])
df['date'] = pd.to_datetime(df['date'])
```

## Core Concepts

### Data Types

| Type | Examples | Libraries |
|------|----------|-----------|
| Vector | Shapefile, GeoJSON, GeoPackage | GeoPandas, Fiona, GDAL |
| Raster | GeoTIFF, NetCDF, COG | Rasterio, Xarray, GDAL |
| Point Cloud | LAS, LAZ | Laspy, PDAL, Open3D |

### Coordinate Systems

- **EPSG:4326** (WGS 84) - Geographic, lat/lon, use for storage
- **EPSG:3857** (Web Mercator) - Web maps only (don't use for area/distance!)
- **EPSG:326xx/327xx** (UTM) - Metric calculations, <1% distortion per zone
- Use `gdf.estimate_utm_crs()` for automatic UTM detection

```python
# Always check CRS before operations
assert gdf1.crs == gdf2.crs, "CRS mismatch!"

# For area/distance calculations, use projected CRS
gdf_metric = gdf.to_crs(gdf.estimate_utm_crs())
area_sqm = gdf_metric.geometry.area
```

### OGC Standards

- **WMS**: Web Map Service - raster maps
- **WFS**: Web Feature Service - vector data
- **WCS**: Web Coverage Service - raster coverage
- **STAC**: Spatiotemporal Asset Catalog - modern metadata

## Common Operations

### Spectral Indices

```python
def calculate_indices(image_path, bands=(2, 3, 4, 8, 11)):
    """NDVI, EVI, SAVI, NDWI from Sentinel-2.

    `bands` maps (B02, B03, B04, B08, B11) to the 1-based band indices in
    your file. EVI's constants (6, 7.5, +1) assume surface reflectance in
    [0, 1]; raw L2A DN are scaled by 10000, so divide first or EVI is wrong.
    """
    with rasterio.open(image_path) as src:
        B02, B03, B04, B08, B11 = (src.read(b).astype(float) for b in bands)

    ndvi = (B08 - B04) / (B08 + B04 + 1e-8)
    evi = 2.5 * (B08 - B04) / (B08 + 6*B04 - 7.5*B02 + 1 + 1e-8)
    savi = ((B08 - B04) / (B08 + B04 + 0.5)) * 1.5
    ndwi = (B03 - B08) / (B03 + B08 + 1e-8)

    return {'NDVI': ndvi, 'EVI': evi, 'SAVI': savi, 'NDWI': ndwi}
```

### Vector Operations

```python
# Buffer (use projected CRS! 1000 = metres in UTM).
# Keep the result in the projected frame; don't bolt projected geometry
# back onto a geographic gdf or you silently mix CRS in one column.
gdf_proj = gdf.to_crs(gdf.estimate_utm_crs())
gdf_proj['buffer_1km'] = gdf_proj.geometry.buffer(1000)

# Spatial relationships
intersects = gdf[gdf.geometry.intersects(other_geometry)]
contains = gdf[gdf.geometry.contains(point_geometry)]

# Geometric operations
gdf['centroid'] = gdf.geometry.centroid
gdf['simplified'] = gdf.geometry.simplify(tolerance=0.001)

# Overlay operations
intersection = gpd.overlay(gdf1, gdf2, how='intersection')
union = gpd.overlay(gdf1, gdf2, how='union')
```

### Terrain Analysis

```python
def terrain_metrics(dem_path):
    """Calculate slope, aspect, hillshade from DEM."""
    with rasterio.open(dem_path) as src:
        dem = src.read(1)

    dy, dx = np.gradient(dem)
    slope = np.arctan(np.sqrt(dx**2 + dy**2)) * 180 / np.pi
    aspect = (90 - np.arctan2(-dy, dx) * 180 / np.pi) % 360

    # Hillshade
    az_rad, alt_rad = np.radians(315), np.radians(45)
    hillshade = (np.sin(alt_rad) * np.sin(np.radians(slope)) +
                 np.cos(alt_rad) * np.cos(np.radians(slope)) *
                 np.cos(np.radians(aspect) - az_rad))

    return slope, aspect, hillshade
```

### Network Analysis

```python
import osmnx as ox
import networkx as nx

# Download and analyze street network
G = ox.graph_from_place('San Francisco, CA', network_type='drive')
G = ox.add_edge_speeds(G).add_edge_travel_times(G)

# Shortest path
orig = ox.distance.nearest_nodes(G, -122.4, 37.7)
dest = ox.distance.nearest_nodes(G, -122.3, 37.8)
route = nx.shortest_path(G, orig, dest, weight='travel_time')
```

## Image Classification

```python
from sklearn.ensemble import RandomForestClassifier
import rasterio
from rasterio.features import rasterize

def classify_imagery(raster_path, training_gdf, output_path):
    """Train RF and classify imagery."""
    with rasterio.open(raster_path) as src:
        image = src.read()
        profile = src.profile
        transform = src.transform

    # Extract training data
    X_train, y_train = [], []
    for _, row in training_gdf.iterrows():
        mask = rasterize([(row.geometry, 1)],
                        out_shape=(profile['height'], profile['width']),
                        transform=transform, fill=0, dtype=np.uint8)
        pixels = image[:, mask > 0].T
        X_train.extend(pixels)
        y_train.extend([row['class_id']] * len(pixels))

    # Train and predict
    rf = RandomForestClassifier(n_estimators=100, max_depth=20, n_jobs=-1)
    rf.fit(X_train, y_train)

    prediction = rf.predict(image.reshape(image.shape[0], -1).T)
    prediction = prediction.reshape(profile['height'], profile['width'])

    profile.update(dtype=rasterio.uint8, count=1)
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(prediction.astype(rasterio.uint8), 1)

    return rf
```

## Modern Cloud-Native Workflows

### STAC + Planetary Computer

```python
import pystac_client
import planetary_computer
import odc.stac

# Search Sentinel-2 via STAC
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=[-122.5, 37.7, -122.3, 37.9],
    datetime="2023-01-01/2023-12-31",
    query={"eo:cloud_cover": {"lt": 20}},
)

# Load as xarray (cloud-native!)
# pystac-client >= 0.7: use search.items() (get_items() is deprecated).
items = list(search.items())[:5]
data = odc.stac.load(
    items,
    bands=["B02", "B03", "B04", "B08"],
    crs="EPSG:32610",
    resolution=10,
)

# Calculate NDVI on xarray
ndvi = (data.B08 - data.B04) / (data.B08 + data.B04)
```

### Cloud-Optimized GeoTIFF (COG)

```python
import rasterio
from rasterio.session import AWSSession

# Read COG directly from cloud (partial reads)
session = AWSSession(aws_access_key_id=..., aws_secret_access_key=...)
with rasterio.open('s3://bucket/path.tif', session=session) as src:
    # Read only window of interest
    window = ((1000, 2000), (1000, 2000))
    subset = src.read(1, window=window)

# Write COG
with rasterio.open('output.tif', 'w', **profile,
                   tiled=True, blockxsize=256, blockysize=256,
                   compress='DEFLATE', predictor=2) as dst:
    dst.write(data)

# Validate COG
from rio_cogeo.cogeo import cog_validate
cog_validate('output.tif')
```

## Performance Tips

```python
# 1. Spatial indexing (10-100x faster queries)
gdf.sindex  # Auto-created by GeoPandas

# 2. Chunk large rasters
with rasterio.open('large.tif') as src:
    for i, window in src.block_windows(1):
        block = src.read(1, window=window)

# 3. Dask for big data (lazy, chunked, dask-backed DataArray)
import rioxarray
da_raster = rioxarray.open_rasterio('large.tif', chunks=(1, 1024, 1024))
# .data is the underlying dask.array if you need the raw chunked array:
# dask_array = da_raster.data

# 4. Use Arrow for I/O
gdf.to_file('output.gpkg', use_arrow=True)

# 5. GDAL caching
from osgeo import gdal
gdal.SetCacheMax(2**30)  # 1GB cache

# 6. Parallel processing
rf = RandomForestClassifier(n_jobs=-1)  # All cores
```

## Best Practices

1. **Always check CRS** before spatial operations
2. **Use projected CRS** for area/distance calculations
3. **Validate geometries**: `gdf = gdf[gdf.is_valid]` (repair with `gdf.geometry.make_valid()`)
4. **Drop missing geometries**: `gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty]` (`fillna(None)` does NOT work on a geometry column)
5. **Use efficient formats**: GeoPackage > Shapefile, Parquet for large data
6. **Apply cloud masking** to optical imagery
7. **Preserve lineage** for reproducible research
8. **Use appropriate resolution** for your analysis scale

## Detailed Documentation

- **[Coordinate Systems](references/coordinate-systems.md)** - CRS fundamentals, UTM, transformations
- **[Core Libraries](references/core-libraries.md)** - GDAL, Rasterio, GeoPandas, Shapely
- **[Remote Sensing](references/remote-sensing.md)** - Satellite missions, spectral indices, SAR
- **[Machine Learning](references/machine-learning.md)** - Deep learning, CNNs, GNNs for RS
- **[GIS Software](references/gis-software.md)** - QGIS, ArcGIS, GRASS integration
- **[Scientific Domains](references/scientific-domains.md)** - Marine, hydrology, agriculture, forestry
- **[Advanced GIS](references/advanced-gis.md)** - 3D GIS, spatiotemporal, topology
- **[Big Data](references/big-data.md)** - Distributed processing, GPU acceleration
- **[Industry Applications](references/industry-applications.md)** - Urban planning, disaster management
- **[Programming Languages](references/programming-languages.md)** - Python, R, Julia, JS, C++, Java, Go, Rust
- **[Data Sources](references/data-sources.md)** - Satellite catalogs, APIs
- **[Troubleshooting](references/troubleshooting.md)** - Common issues, debugging, error reference
- **[Code Examples](references/code-examples.md)** - 500+ examples

---

**GeoMaster covers everything from basic GIS operations to advanced remote sensing and machine learning.**
