# Data Formats Reference

## Supported Input Formats

### JSON Format

The primary format for structured simulation data.

**Field Data Structure:**
```json
{
    "timestep": 100,
    "time": 0.5,
    "phi": [[0.0, 0.1, ...], [0.2, 0.3, ...], ...],
    "concentration": [[0.5, 0.5, ...], [0.5, 0.5, ...], ...],
    "dx": 0.01,
    "dy": 0.01,
    "Lx": 1.0,
    "Ly": 1.0
}
```

**Time Series Structure:**
```json
{
    "history": {
        "time": [0.0, 0.01, 0.02, ...],
        "energy": [1.0, 0.99, 0.98, ...],
        "residual": [1e-2, 1e-3, 1e-4, ...],
        "mass": [1.0, 1.0, 1.0, ...]
    }
}
```

**Profile Data Structure:**
```json
{
    "coordinates": [0.0, 0.1, 0.2, ...],
    "values": [0.0, 0.5, 1.0, ...],
    "field": "phi",
    "axis": "x",
    "slice_position": 0.5
}
```

### CSV Format

Tabular data with header row.

**Time Series Example:**
```csv
time,energy,residual,mass
0.0,1.0,1e-2,1.0
0.01,0.99,1e-3,1.0
0.02,0.98,1e-4,1.0
```

**Profile Example:**
```csv
x,phi,concentration
0.0,0.0,0.5
0.1,0.25,0.5
0.2,0.5,0.5
```

## Output Formats

All scripts support `--json` flag for machine-readable output.

### JSON Output Structure

Output envelopes are **not uniform** across scripts. Most scripts emit a flat
top-level object that includes a `source_file` key plus script-specific result
keys (field statistics such as `min`/`max`/`mean`/`count` appear at the top
level, not nested under a `data` object). For example, `field_extractor.py`:

```json
{
    "field": "phi",
    "found": true,
    "shape": [10, 10],
    "min": 0.0,
    "max": 1.0,
    "mean": 0.33,
    "count": 100,
    "source_file": "results/field_0100.json",
    "timestep_info": {"timestep": 100, "time": 0.5}
}
```

Exceptions:

- `derived_quantities.py` wraps its payload in an
  `{ "inputs": {...}, "results": {...} }` envelope.
- `report_generator.py` emits top-level `report_version` and `generator`
  keys plus the requested report sections.

No script emits top-level `script`, `version`, or `input_file` keys.

### CSV Export

For tabular results, use `--export-csv` where available:
- Comma-separated values
- Header row with field names
- Numeric precision: 6 significant figures

## Field Naming Conventions

| Convention | Example | Description |
|------------|---------|-------------|
| Snake case | `phi_field` | Preferred for field names |
| Timestep suffix | `field_0100.json` | For sequential output |
| History files | `history.json` | Time series data |
| Config files | `config.json` | Simulation parameters |

## Grid Information

Scripts attempt to extract grid information from:

1. **Explicit fields:** `dx`, `dy`, `dz` (these take precedence)
2. **Domain fields:** `Lx`, `Ly`, `Lz` — used only to *derive* a spacing when
   the corresponding explicit `dx`/`dy`/`dz` is absent
   (node-centered: `dx = Lx / (nx - 1)`)
3. **Default:** `dx = dy = dz = 1.0` if not found

When both an explicit spacing and a domain size are present but inconsistent
under both the cell-centered (`dx*nx == Lx`) and node-centered
(`dx*(nx-1) == Lx`) conventions, `derived_quantities.py` keeps the explicit
spacing and prints a warning to stderr.

## Data Validation

Scripts validate:
- File exists and is readable
- JSON is well-formed
- Requested fields exist
- Numeric data is present
- No unexpected NaN/Inf values (where applicable)
