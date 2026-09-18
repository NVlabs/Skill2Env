# ClinPGx Rate Limiting, Error Handling, and Caching

Reusable helpers for compliant, robust ClinPGx API access. The API allows a
maximum of **2 requests per second**; exceeding it returns HTTP 429. For
substantial API use, notify the ClinPGx team at api@clinpgx.org.

**Note**: `safe_api_call` below returns the raw `{"status", "data"}` envelope.
Unwrap the records with `result["data"]` (and treat `status == "fail"` — e.g.
"No results matching criteria" — as an empty result). `scripts/query_clinpgx.py`
provides an `unwrap()` helper and query functions that do this for you.

## Rate Limit Compliance

```python
import requests
import time

def rate_limited_request(url, params=None, delay=0.5):
    """Make API request with rate limiting (2 req/sec max)"""
    response = requests.get(url, params=params)
    time.sleep(delay)  # Wait 0.5 seconds between requests
    return response

# Use in loops (resolve each gene symbol via the collection endpoint)
genes = ["CYP2D6", "CYP2C19", "CYP2C9"]
for gene in genes:
    response = rate_limited_request(
        "https://api.clinpgx.org/v1/data/gene", params={"symbol": gene}
    )
    data = response.json()
```

## Error Handling

```python
def safe_api_call(url, params=None, max_retries=3):
    """API call with error handling and retries"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Rate limit exceeded
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

## Caching Results

```python
import json
from pathlib import Path

def cached_query(cache_file, api_func, *args, **kwargs):
    """Cache API results to avoid repeated queries"""
    cache_path = Path(cache_file)

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    result = api_func(*args, **kwargs)  # must return JSON-serializable data

    if result is not None:
        with open(cache_path, 'w') as f:
            json.dump(result, f, indent=2)

    return result

# Usage (CYP2D6 = accession PA128). Pass a func that returns parsed JSON
# (e.g. safe_api_call), NOT rate_limited_request, which returns a Response.
envelope = cached_query(
    'cyp2d6_cache.json',
    safe_api_call,
    "https://api.clinpgx.org/v1/data/gene/PA128"
)
gene_data = envelope["data"] if envelope else None
```
