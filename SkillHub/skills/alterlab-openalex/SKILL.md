---
name: alterlab-openalex
description: Query and analyze scholarly literature using the OpenAlex API across 240M+ works, retrieving papers, authors, institutions, citations, and open access status. Use when searching academic papers, tracking citations, finding works by author or institution, analyzing research trends, discovering open access publications, or running bibliometric analysis. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: OpenAlex REST API at api.openalex.org. Works keyless ($0.01/day credit); a free API key (openalex.org/settings/api) raises the free allowance to $1/day.
metadata:
    skill-author: AlterLab
    version: "1.1.0"
---

# OpenAlex Database

## Overview

OpenAlex is a comprehensive open catalog of 240M+ scholarly works, authors, institutions, topics, sources, publishers, and funders. This skill provides tools and workflows for querying the OpenAlex API to search literature, analyze research output, track citations, and conduct bibliometric studies.

## Quick Start

### Basic Setup

OpenAlex now runs on a credit model (see "Rate Limits & Cost" below). It still works with no credentials, but a **free API key** raises the daily free allowance from $0.01 to $1 — get one at `openalex.org/settings/api` and pass it to the client:

```python
from scripts.openalex_client import OpenAlexClient

# Recommended: free API key (raises free allowance to $1/day)
client = OpenAlexClient(api_key="YOUR_KEY")

# Keyless still works (lower $0.01/day allowance); mailto is optional/harmless
client = OpenAlexClient(email="your-email@example.edu")
```

### Installation Requirements

Install required package using uv:

```bash
uv pip install requests
```

## Core Capabilities

### 1. Search for Papers

**Use for**: Finding papers by title, abstract, or topic

```python
# Simple search
results = client.search_works(
    search="machine learning",
    per_page=100
)

# Search with filters
results = client.search_works(
    search="CRISPR gene editing",
    filter_params={
        "publication_year": ">2020",
        "is_oa": "true"
    },
    sort="cited_by_count:desc"
)
```

### 2. Find Works by Author

**Use for**: Getting all publications by a specific researcher

Use the two-step pattern (entity name → ID → works):

```python
from scripts.query_helpers import find_author_works

works = find_author_works(
    author_name="Jennifer Doudna",
    client=client,
    limit=100
)
```

**Manual two-step approach**:
```python
# Step 1: Get author ID
author_response = client._make_request(
    '/authors',
    params={'search': 'Jennifer Doudna', 'per-page': 1}
)
author_id = author_response['results'][0]['id'].split('/')[-1]

# Step 2: Get works
works = client.search_works(
    filter_params={"authorships.author.id": author_id}
)
```

### 3. Find Works from Institution

**Use for**: Analyzing research output from universities or organizations

```python
from scripts.query_helpers import find_institution_works

works = find_institution_works(
    institution_name="Stanford University",
    client=client,
    limit=200
)
```

### 4. Highly Cited Papers

**Use for**: Finding influential papers in a field

```python
from scripts.query_helpers import find_highly_cited_recent_papers

papers = find_highly_cited_recent_papers(
    topic="quantum computing",
    years=">2020",
    client=client,
    limit=100
)
```

### 5. Open Access Papers

**Use for**: Finding freely available research

```python
from scripts.query_helpers import get_open_access_papers

papers = get_open_access_papers(
    search_term="climate change",
    client=client,
    oa_status="any",  # or "gold", "green", "hybrid", "bronze"
    limit=200
)
```

### 6. Publication Trends Analysis

**Use for**: Tracking research output over time

```python
from scripts.query_helpers import get_publication_trends

trends = get_publication_trends(
    search_term="artificial intelligence",
    filter_params={"is_oa": "true"},
    client=client
)

# Sort and display
for trend in sorted(trends, key=lambda x: x['key'])[-10:]:
    print(f"{trend['key']}: {trend['count']} publications")
```

### 7. Research Output Analysis

**Use for**: Comprehensive analysis of author or institution research

```python
from scripts.query_helpers import analyze_research_output

analysis = analyze_research_output(
    entity_type='institution',  # or 'author'
    entity_name='MIT',
    client=client,
    years='>2020'
)

print(f"Total works: {analysis['total_works']}")
print(f"Open access: {analysis['open_access_percentage']}%")
print(f"Top topics: {analysis['top_topics'][:5]}")
```

### 8. Batch Lookups

**Use for**: Getting information for multiple DOIs, ORCIDs, or IDs efficiently

```python
dois = [
    "https://doi.org/10.1038/s41586-021-03819-2",
    "https://doi.org/10.1126/science.abc1234",
    # ... up to 50 DOIs
]

works = client.batch_lookup(
    entity_type='works',
    ids=dois,
    id_field='doi'
)
```

### 9. Random Sampling

**Use for**: Getting representative samples for analysis

```python
# Small sample
works = client.sample_works(
    sample_size=100,
    seed=42,  # For reproducibility
    filter_params={"publication_year": "2023"}
)

# Large sample (>10k) - automatically handles multiple requests
works = client.sample_works(
    sample_size=25000,
    seed=42,
    filter_params={"is_oa": "true"}
)
```

### 10. Citation Analysis

**Use for**: Finding papers that cite a specific work

```python
# Get the work
work = client.get_entity('works', 'https://doi.org/10.1038/s41586-021-03819-2')

# Get citing papers using cited_by_api_url
import requests
citing_response = requests.get(
    work['cited_by_api_url'],
    params={**client.auth_params(), 'per-page': 200}
)
citing_works = citing_response.json()['results']
```

### 11. Topic and Subject Analysis

**Use for**: Understanding research focus areas

```python
# Get top topics for an institution
topics = client.group_by(
    entity_type='works',
    group_field='topics.id',
    filter_params={
        "authorships.institutions.id": "I136199984",  # MIT
        "publication_year": ">2020"
    }
)

for topic in topics[:10]:
    print(f"{topic['key_display_name']}: {topic['count']} works")
```

### 12. Large-Scale Data Extraction

**Use for**: Downloading large datasets for analysis

```python
# Paginate through all results
all_papers = client.paginate_all(
    endpoint='/works',
    params={
        'search': 'synthetic biology',
        'filter': 'publication_year:2020-2024'
    },
    max_results=10000
)

# Export to CSV
import csv
with open('papers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Year', 'Citations', 'DOI', 'OA Status'])

    for paper in all_papers:
        writer.writerow([
            paper.get('title', 'N/A'),
            paper.get('publication_year', 'N/A'),
            paper.get('cited_by_count', 0),
            paper.get('doi', 'N/A'),
            paper.get('open_access', {}).get('oa_status', 'closed')
        ])
```

## Critical Best Practices

### Use a Free API Key to Raise the Daily Allowance
Without credentials you get a $0.01/day free credit; a free API key raises it to $1/day. Pass the key to the client:
```python
client = OpenAlexClient(api_key="YOUR_KEY")  # free at openalex.org/settings/api
```

### Use Two-Step Pattern for Entity Lookups
Never filter by entity names directly - always get ID first:
```python
# ✅ Correct
# 1. Search for entity → get ID
# 2. Filter by ID

# ❌ Wrong
# filter=author_name:Einstein  # This doesn't work!
```

### Use Maximum Page Size
Always use `per-page=200` for efficient data retrieval:
```python
results = client.search_works(search="topic", per_page=200)
```

### Batch Multiple IDs
Use batch_lookup() for multiple IDs instead of individual requests:
```python
# ✅ Correct - 1 request for 50 DOIs
works = client.batch_lookup('works', doi_list, 'doi')

# ❌ Wrong - 50 separate requests
for doi in doi_list:
    work = client.get_entity('works', doi)
```

### Use Sample Parameter for Random Data
Use `sample_works()` with seed for reproducible random sampling:
```python
# ✅ Correct
works = client.sample_works(sample_size=100, seed=42)

# ❌ Wrong - random page numbers bias results
# Using random page numbers doesn't give true random sample
```

### Select Only Needed Fields
Reduce response size by selecting specific fields:
```python
results = client.search_works(
    search="topic",
    select=['id', 'title', 'publication_year', 'cited_by_count']
)
```

## Common Filter Patterns

### Date Ranges
```python
# Single year
filter_params={"publication_year": "2023"}

# After year
filter_params={"publication_year": ">2020"}

# Range
filter_params={"publication_year": "2020-2024"}
```

### Multiple Filters (AND)
```python
# All conditions must match
filter_params={
    "publication_year": ">2020",
    "is_oa": "true",
    "cited_by_count": ">100"
}
```

### Multiple Values (OR)
```python
# Any institution matches
filter_params={
    "authorships.institutions.id": "I136199984|I27837315"  # MIT or Harvard
}
```

### Collaboration (AND within attribute)
```python
# Papers with authors from BOTH institutions
filter_params={
    "authorships.institutions.id": "I136199984+I27837315"  # MIT AND Harvard
}
```

### Negation
```python
# Exclude type
filter_params={
    "type": "!paratext"
}
```

## Entity Types

OpenAlex provides these entity types:
- **works** - Scholarly documents (articles, books, datasets)
- **authors** - Researchers with disambiguated identities
- **institutions** - Universities and research organizations
- **sources** - Journals, repositories, conferences
- **topics** - Subject classifications
- **publishers** - Publishing organizations
- **funders** - Funding agencies

Access any entity type using consistent patterns:
```python
client.search_works(...)
client.get_entity('authors', author_id)
client.group_by('works', 'topics.id', filter_params={...})
```

## External IDs

Use external identifiers directly:
```python
# DOI for works
work = client.get_entity('works', 'https://doi.org/10.7717/peerj.4375')

# ORCID for authors
author = client.get_entity('authors', 'https://orcid.org/0000-0003-1613-5981')

# ROR for institutions
institution = client.get_entity('institutions', 'https://ror.org/02y3ad647')

# ISSN for sources
source = client.get_entity('sources', 'issn:0028-0836')
```

## Reference Documentation

### Detailed API Reference
See `references/api_guide.md` for:
- Complete filter syntax
- All available endpoints
- Response structures
- Error handling
- Performance optimization
- Rate limiting details

### Common Query Examples
See `references/common_queries.md` for:
- Complete working examples
- Real-world use cases
- Complex query patterns
- Data export workflows
- Multi-step analysis procedures

## Scripts

### openalex_client.py
Main API client with:
- Automatic rate limiting
- Exponential backoff retry logic
- Pagination support
- Batch operations
- Error handling

Use for direct API access with full control.

### query_helpers.py
High-level helper functions for common operations:
- `find_author_works()` - Get papers by author
- `find_institution_works()` - Get papers from institution
- `find_highly_cited_recent_papers()` - Get influential papers
- `get_open_access_papers()` - Find OA publications
- `get_publication_trends()` - Analyze trends over time
- `analyze_research_output()` - Comprehensive analysis

Use for common research queries with simplified interfaces.

## Troubleshooting

### Daily Limit / Throttling (429)
If encountering 429 (Too Many Requests) errors:
1. Add a free API key to raise the daily allowance from $0.01 to $1 (`OpenAlexClient(api_key=...)`)
2. Reduce cost: prefer single-entity and list+filter calls over `search=` (search costs more credits per call); use `select=` to keep responses cheap
3. Client automatically backs off and retries on 429/403/5xx
4. Inspect the `x-ratelimit-remaining-usd` / `x-ratelimit-cost-usd` response headers to see remaining budget

### Empty Results
If searches return no results:
1. Check filter syntax (see `references/api_guide.md`)
2. Use two-step pattern for entity lookups (don't filter by names)
3. Verify entity IDs are correct format

### Timeout Errors
For large queries:
1. Use pagination with `per-page=200`
2. Use `select=` to limit returned fields
3. Break into smaller queries if needed

## Rate Limits & Cost

OpenAlex uses a daily cost (credit) model, not a fixed requests/second limit. Each call has a small USD cost; you get a free daily budget and pay only past it.

- **Keyless**: $0.01/day free budget.
- **With a free API key** (`openalex.org/settings/api`): $1/day free budget. Recommended.
- **Approximate costs per $1** (the bulk of the work): single-entity lookups are effectively free/unlimited; ~10,000 list+filter calls; ~1,000 `search=` calls; ~100 PDF/content downloads. So `search=` is ~10x more expensive than list+filter — filter when you can.
- Live budget is reported in response headers: `x-ratelimit-limit-usd`, `x-ratelimit-remaining-usd`, `x-ratelimit-cost-usd` (and the response `meta.cost_usd`).
- Exhausting the daily budget returns **429 Too Many Requests** (403 also signals "slow down"). The client backs off and retries on these.

## Notes

- All data is open and free; the daily budget is generous for typical research workloads.
- A free API key is recommended for any non-trivial workflow; keyless is fine for one-off lookups.
- Costs/limits apply per credential (per key, or per IP when keyless), not per request type alone — minimize `search=` and use `select=` to stretch the budget.
- Use LitLLM with OpenRouter if LLM-based analysis is needed (don't use Perplexity API directly).
- Client handles pagination, retries, and backoff automatically.

