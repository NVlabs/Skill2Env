---
name: alterlab-hedgefund-monitor
description: Queries the OFR (Office of Financial Research) Hedge Fund Monitor API for time series on hedge fund size, leverage, counterparties, liquidity, complexity, and risk management, including SEC Form PF aggregated statistics, CFTC Traders in Financial Futures, FICC Sponsored Repo volumes, and FRB SCOOS dealer financing terms (no API key or registration required). Use when working with hedge fund data, systemic risk monitoring, financial stability research, hedge fund leverage or leverage ratios, counterparty concentration, Form PF statistics, repo market data, or OFR financial research data. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: No API key or registration required. Queries the open OFR Hedge Fund Monitor REST API; needs network access.
metadata:
    skill-author: AlterLab
    version: "1.1.0"
---

# OFR Hedge Fund Monitor API

Free, open REST API from the U.S. Office of Financial Research (OFR) providing aggregated hedge fund time series data. No API key or registration required.

**Base URL:** `https://data.financialresearch.gov/hf/v1`

## Quick Start

```python
import requests
import pandas as pd

BASE = "https://data.financialresearch.gov/hf/v1"

# List all available datasets
resp = requests.get(f"{BASE}/series/dataset")
datasets = resp.json()
# Returns: {"ficc": {...}, "fpf": {...}, "scoos": {...}, "tff": {...}}

# Search for series by keyword
resp = requests.get(f"{BASE}/metadata/search", params={"query": "*leverage*"})
results = resp.json()
# Each result: {mnemonic, dataset, field, value, type}

# Fetch a single time series
resp = requests.get(f"{BASE}/series/timeseries", params={
    "mnemonic": "FPF-STRATEGY_EQUITY_LEVERAGERATIO_GAVWMEAN",
    "start_date": "2015-01-01"
})
series = resp.json()  # [[date, value], ...]
df = pd.DataFrame(series, columns=["date", "value"])
df["date"] = pd.to_datetime(df["date"])
```

**Mnemonics are exact — guessing fails.** The API rejects unknown identifiers with a plain
`Invalid mnemonic` string (HTTP 200, not JSON). Always discover real mnemonics via
`/metadata/search` or `/metadata/mnemonics` before requesting data. Note in particular that
there is **no** `FPF-ALLQHF_LEVERAGERATIO_*` series: aggregate leverage is published per
gross-asset cohort (see below), while the `GAVWMEAN`/`NAVWMEAN` asset-weighted leverage means
exist only at the strategy level.

## Authentication

None required. The API is fully open and free.

## Datasets

| Key | Dataset | Update Frequency |
|-----|---------|-----------------|
| `fpf` | SEC Form PF — aggregated stats from qualifying hedge fund filings | Quarterly |
| `tff` | CFTC Traders in Financial Futures — futures market positioning | Monthly |
| `scoos` | FRB Senior Credit Officer Opinion Survey on Dealer Financing Terms | Quarterly |
| `ficc` | FICC Sponsored Repo Service Volumes | Daily |

> The `/series/dataset` index returns `long_name: "FormPF"` for every dataset (an upstream API
> label quirk); the real source names are above. Confirm a series' true cadence via
> `schedule/observation_frequency` in its metadata.

## Data Categories

The HFM organizes data into six categories (each downloadable as CSV):
- **size** — Hedge fund industry size (AUM, count of funds, net/gross assets)
- **leverage** — Leverage ratios, borrowing, gross notional exposure
- **counterparties** — Counterparty concentration, prime broker lending
- **liquidity** — Financing maturity, investor redemption terms, portfolio liquidity
- **complexity** — Open positions, strategy distribution, asset class exposure
- **risk_management** — Stress test results (CDS, equity, rates, FX scenarios)

## Core Endpoints

### Metadata

| Endpoint | Path | Description |
|----------|------|-------------|
| List mnemonics | `GET /metadata/mnemonics` | All series identifiers |
| Query series info | `GET /metadata/query?mnemonic=` | Full metadata for one series |
| Search series | `GET /metadata/search?query=` | Text search with wildcards (`*`, `?`) |

### Series Data

| Endpoint | Path | Description |
|----------|------|-------------|
| Single timeseries | `GET /series/timeseries?mnemonic=` | Date/value pairs for one series |
| Full single | `GET /series/full?mnemonic=` | Data + metadata for one series |
| Multi full | `GET /series/multifull?mnemonics=A,B` | Data + metadata for multiple series |
| Dataset | `GET /series/dataset?dataset=fpf` | All series in a dataset |
| Category CSV | `GET /categories?category=leverage` | CSV download for a category |
| Spread | `GET /calc/spread?x=MNE1&y=MNE2` | Difference between two series |

## Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `start_date` | Start date YYYY-MM-DD | `2020-01-01` |
| `end_date` | End date YYYY-MM-DD | `2024-12-31` |
| `periodicity` | Resample frequency | `Q`, `M`, `A`, `D`, `W` |
| `how` | Aggregation method | `last` (default), `first`, `mean`, `median`, `sum` |
| `remove_nulls` | Drop null values | `true` |
| `time_format` | Date format | `date` (YYYY-MM-DD) or `ms` (epoch ms) |

## Key FPF Mnemonic Patterns

Mnemonics follow the pattern `FPF-{SCOPE}_{METRIC}_{STAT}`:
- Scope: `ALLQHF` (all qualifying hedge funds), or a strategy such as `STRATEGY_CREDIT`,
  `STRATEGY_EQUITY`, `STRATEGY_MACRO`, `STRATEGY_RV` (relative value), `STRATEGY_FUTURES`, etc.
  ALLQHF leverage/cash metrics carry a gross-asset cohort segment: `GAVN10` (10 largest funds),
  `GAVN11TO50`, `GAVN51` (rest).
- Metrics: `GAV` (gross assets), `NAV` (net assets), `GNE` (gross notional exposure),
  `LEVERAGERATIO`, `CASHRATIO`, `COUNT`, plus stress-test scenarios (`CDSUP250BPS`, etc.)
- Stats: `SUM`, `AVERAGE` (equal-weighted, used for ALLQHF cohorts), `GAVWMEAN`/`NAVWMEAN`
  (asset-weighted, strategy-level only), `P5`, `P50`, `P95`, `PCTCHANGE`

```python
# Verified series examples (all return data as of 2026)
mnemonics = [
    "FPF-ALLQHF_GAVN10_LEVERAGERATIO_AVERAGE",    # 10 largest funds: leverage (equal-weighted)
    "FPF-STRATEGY_EQUITY_LEVERAGERATIO_GAVWMEAN", # Equity strategy: leverage (GAV-weighted)
    "FPF-ALLQHF_GAV_SUM",                         # All funds: gross assets (total $)
    "FPF-ALLQHF_NAV_SUM",                         # All funds: net assets (total $)
    "FPF-ALLQHF_GNE_SUM",                         # All funds: gross notional exposure
    "FICC-SPONSORED_REPO_VOL",                    # FICC: sponsored repo volume (daily)
]
```

## Reference Files

- **[references/api-overview.md](references/api-overview.md)** — Base URL, versioning, protocols, response format
- **[references/endpoints-metadata.md](references/endpoints-metadata.md)** — Mnemonics, query, and search endpoints with full parameter details
- **[references/endpoints-series-data.md](references/endpoints-series-data.md)** — Timeseries, spread, and full data endpoints
- **[references/endpoints-combined.md](references/endpoints-combined.md)** — Full, multifull, dataset, and category endpoints
- **[references/datasets.md](references/datasets.md)** — Dataset descriptions (fpf, tff, scoos, ficc) and dataset-specific notes
- **[references/parameters.md](references/parameters.md)** — Complete parameter reference with periodicity codes, how values
- **[references/examples.md](references/examples.md)** — Python examples: discovery, bulk download, spread analysis, DataFrame workflows
