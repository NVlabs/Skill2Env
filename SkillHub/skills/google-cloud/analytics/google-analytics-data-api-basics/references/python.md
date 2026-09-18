# Google Analytics Data API Python Client Library Installation

This guide provides specific instructions for installing and setting up the
Google Analytics Data API (v1beta) client library for Python.

## Prerequisites

*   **Python:** Version 3.8 or higher.
*   **Package Manager:** `pip`
*   **Authentication:** Application Default Credentials (ADC) configured via
    `gcloud auth application-default login`.

## Installation

Install the official Google Analytics Data client library within a virtual
environment.

> [!NOTE] For complete documentation, see the
> [Python Analytics Data README](https://github.com/googleapis/google-cloud-python/blob/main/packages/google-analytics-data/README.rst#installation).

### 1. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install the Client Library

```bash
pip install google-analytics-data
```

If `pip` is not available, prompt the user to install Python and `pip` before
installing the client library.

*Why: Installing `google-analytics-data` in a clean virtual environment ensures
repeatable builds and prevents dependency conflicts.*

## Quickstart / Usage

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

def run_report(property_id: str):
    # Initialize the client. Uses ADC from environment.
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="city")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="2026-05-01", end_date="today")],
    )
    response = client.run_report(request)

    for row in response.rows:
        print(f"City: {row.dimension_values[0].value}, Users: {row.metric_values[0].value}")

if __name__ == "__main__":
    run_report("1234567")
```
