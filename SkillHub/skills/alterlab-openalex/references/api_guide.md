# OpenAlex API Complete Guide

## Base Information

**Base URL:** `https://api.openalex.org`
**Authentication:** Optional but recommended. A free API key (from `openalex.org/settings/api`) is passed as `?api_key=YOUR_KEY`.
**Rate Limits (daily cost/credit model):**
- Keyless: $0.01/day free budget
- With a free API key: $1/day free budget
- Per-call cost varies by operation (see "Cost Model" below); past the free budget you pay for what you use.

## Critical Best Practices

### ✅ DO: Use `?sample` parameter for random sampling
```
https://api.openalex.org/works?sample=20&seed=123
```
For large samples (10k+), use multiple seeds and deduplicate.

### ❌ DON'T: Use random page numbers for sampling
Incorrect: `?page=5`, `?page=17` - This biases results!

### ✅ DO: Use two-step lookup for entity filtering
```
1. Find entity ID: /authors?search=einstein
2. Use ID: /works?filter=authorships.author.id:A5023888391
```

### ❌ DON'T: Filter by entity names directly
Incorrect: `/works?filter=author_name:Einstein` - Names are ambiguous!

### ✅ DO: Use maximum page size for bulk extraction
```
?per-page=200
```
This is 8x faster than default (25).

### ❌ DON'T: Use default page sizes
Default is only 25 results per page.

### ✅ DO: Use OR filter (pipe |) for batch lookups
```
/works?filter=doi:10.1/abc|10.2/def|10.3/ghi
```
Up to 50 values per filter.

### ❌ DON'T: Make sequential API calls for lists
Making 100 separate calls when you can batch them is inefficient.

### ✅ DO: Implement exponential backoff for retries
```python
for attempt in range(max_retries):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except:
        wait_time = 2 ** attempt
        time.sleep(wait_time)
```

### ✅ DO: Add a free API key to raise the daily budget
```
?api_key=YOUR_KEY
```
Raises the free daily budget from $0.01 (keyless) to $1. Get a key free at `openalex.org/settings/api`.

### ✅ DO: Prefer filter over search to spend less budget
`search=` calls cost roughly 10x a list+filter call. Filter by IDs/fields where possible and use `select=` to keep responses lean.

## Entity Endpoints

- `/works` - 240M+ scholarly documents
- `/authors` - Researcher profiles
- `/sources` - Journals, repositories, conferences
- `/institutions` - Universities, research organizations
- `/topics` - Subject classifications (3-level hierarchy)
- `/publishers` - Publishing organizations
- `/funders` - Funding agencies
- `/text` - Tag your own text with topics/keywords (POST)

## Essential Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `filter=` | Filter results | `?filter=publication_year:2020` |
| `search=` | Full-text search | `?search=machine+learning` |
| `sort=` | Sort results | `?sort=cited_by_count:desc` |
| `per-page=` | Results per page (max 200) | `?per-page=200` |
| `page=` | Page number | `?page=2` |
| `sample=` | Random results | `?sample=50&seed=42` |
| `select=` | Limit fields | `?select=id,title` |
| `group_by=` | Aggregate by field | `?group_by=publication_year` |
| `api_key=` | Free API key (raises daily budget to $1) | `?api_key=YOUR_KEY` |
| `mailto=` | Optional contact email (harmless; no longer changes limits) | `?mailto=you@example.edu` |

## Filter Syntax

### Basic Filtering
```
Single filter:     ?filter=publication_year:2020
Multiple (AND):    ?filter=publication_year:2020,is_oa:true
Values (OR):       ?filter=type:journal-article|book
Negation:          ?filter=type:!journal-article
```

### Comparison Operators
```
Greater than:      ?filter=cited_by_count:>100
Less than:         ?filter=publication_year:<2020
Range:             ?filter=publication_year:2020-2023
```

### Multiple Values in Same Attribute
```
Repeat filter:     ?filter=institutions.country_code:us,institutions.country_code:gb
Use + symbol:      ?filter=institutions.country_code:us+gb
```
Both mean: "works with author from US AND author from GB"

### OR Queries
```
Any of these:      ?filter=institutions.country_code:us|gb|ca
Batch IDs:         ?filter=doi:10.1/abc|10.2/def
```
Up to 50 values with pipes.

## Common Query Patterns

### Get Random Sample
```bash
# Small sample
https://api.openalex.org/works?sample=20&seed=42

# Large sample (10k+) - make multiple requests
https://api.openalex.org/works?sample=1000&seed=1
https://api.openalex.org/works?sample=1000&seed=2
# Then deduplicate by ID
```

### Search Works
```bash
# Simple search
https://api.openalex.org/works?search=machine+learning

# Search specific field
https://api.openalex.org/works?filter=title.search:CRISPR

# Search + filter
https://api.openalex.org/works?search=climate&filter=publication_year:2023
```

### Find Works by Author (Two-Step)
```bash
# Step 1: Get author ID
https://api.openalex.org/authors?search=Heather+Piwowar
# Returns: "id": "https://openalex.org/A5023888391"

# Step 2: Get their works
https://api.openalex.org/works?filter=authorships.author.id:A5023888391
```

### Find Works by Institution (Two-Step)
```bash
# Step 1: Get institution ID
https://api.openalex.org/institutions?search=MIT
# Returns: "id": "https://openalex.org/I136199984"

# Step 2: Get their works
https://api.openalex.org/works?filter=authorships.institutions.id:I136199984
```

### Highly Cited Recent Papers
```bash
https://api.openalex.org/works?filter=publication_year:>2020&sort=cited_by_count:desc&per-page=200
```

### Open Access Works
```bash
# All OA
https://api.openalex.org/works?filter=is_oa:true

# Gold OA only
https://api.openalex.org/works?filter=open_access.oa_status:gold
```

### Multiple Criteria
```bash
# Recent OA works about COVID from top institutions
https://api.openalex.org/works?filter=publication_year:2022,is_oa:true,title.search:covid,authorships.institutions.id:I136199984|I27837315
```

### Bulk DOI Lookup
```bash
# Get specific works by DOI (up to 50 per request)
https://api.openalex.org/works?filter=doi:https://doi.org/10.1371/journal.pone.0266781|https://doi.org/10.1371/journal.pone.0267149&per-page=50
```

### Aggregate Data
```bash
# Top topics
https://api.openalex.org/works?group_by=topics.id

# Papers per year
https://api.openalex.org/works?group_by=publication_year

# Most prolific institutions
https://api.openalex.org/works?group_by=authorships.institutions.id
```

### Pagination
```bash
# First page
https://api.openalex.org/works?filter=publication_year:2023&per-page=200

# Next pages
https://api.openalex.org/works?filter=publication_year:2023&per-page=200&page=2
```

## Response Structure

### List Endpoints
```json
{
  "meta": {
    "count": 240523418,
    "db_response_time_ms": 42,
    "page": 1,
    "per_page": 25
  },
  "results": [
    { /* entity object */ }
  ]
}
```

### Single Entity
```
https://api.openalex.org/works/W2741809807
→ Returns Work object directly (no meta/results wrapper)
```

### Group By
```json
{
  "meta": { "count": 100 },
  "group_by": [
    {
      "key": "https://openalex.org/T10001",
      "key_display_name": "Artificial Intelligence",
      "count": 15234
    }
  ]
}
```

## Works Filters (Most Common)

| Filter | Description | Example |
|--------|-------------|---------|
| `authorships.author.id` | Author's OpenAlex ID | `A5023888391` |
| `authorships.institutions.id` | Institution's ID | `I136199984` |
| `cited_by_count` | Citation count | `>100` |
| `is_oa` | Is open access | `true/false` |
| `publication_year` | Year published | `2020`, `>2020`, `2018-2022` |
| `primary_location.source.id` | Source (journal) ID | `S137773608` |
| `topics.id` | Topic ID | `T10001` |
| `type` | Document type | `article`, `book`, `dataset` |
| `has_doi` | Has DOI | `true/false` |
| `has_fulltext` | Has fulltext | `true/false` |

## Authors Filters

| Filter | Description |
|--------|-------------|
| `last_known_institution.id` | Current/last institution |
| `works_count` | Number of works |
| `cited_by_count` | Total citations |
| `orcid` | ORCID identifier |

## External ID Support

### Works
```
DOI:  /works/https://doi.org/10.7717/peerj.4375
PMID: /works/pmid:29844763
```

### Authors
```
ORCID: /authors/https://orcid.org/0000-0003-1613-5981
```

### Institutions
```
ROR: /institutions/https://ror.org/02y3ad647
```

### Sources
```
ISSN: /sources/issn:0028-0836
```

## Performance Tips

1. **Use maximum page size**: `?per-page=200` (8x fewer calls)
2. **Batch ID lookups**: Use pipe operator for up to 50 IDs
3. **Select only needed fields**: `?select=id,title,publication_year`
4. **Prefer filter over search**: list+filter calls cost ~10x less than `search=` calls
5. **Add an API key**: `?api_key=YOUR_KEY` raises the free daily budget from $0.01 to $1

## Error Handling

### HTTP Status Codes
- `200` - Success
- `400` - Bad request (check filter syntax)
- `403` - Forbidden ("slow down"; back off)
- `404` - Entity doesn't exist
- `429` - Too Many Requests / daily budget exhausted (back off; add an API key to raise the budget)
- `500` - Server error (retry with backoff)

### Exponential Backoff
```python
def fetch_with_retry(url, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code in [403, 500, 502, 503, 504]:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                response.raise_for_status()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")
```

## Cost Model & Rate Limiting

OpenAlex uses a daily USD cost budget rather than a fixed requests/second cap.

### Daily Free Budget
- **Keyless**: $0.01/day
- **With a free API key** (`openalex.org/settings/api`): $1/day — recommended

### Approximate operation cost (what $1/day buys)
- Single-entity lookups (`/works/W...`): effectively free / unlimited
- List + filter calls (e.g. `/works?filter=...`): ~10,000 calls (~1M results)
- `search=` calls: ~1,000 calls (~100k results) — ~10x the cost of a filter call
- Content/PDF downloads: ~100

Implication: resolve and filter by IDs; reserve `search=` for genuine free-text needs; use `select=` to keep responses cheap.

### Reading the budget from responses
Every response includes cost headers and `meta.cost_usd`:
```
x-ratelimit-limit-usd: 1
x-ratelimit-remaining-usd: 0.9999
x-ratelimit-cost-usd: 0.0001
```

### Strategy when the budget runs low
1. Add an API key (raises budget 100x vs keyless)
2. Replace `search=` with `filter=` where possible
3. Back off and retry on 429/403
4. Spread heavy bulk jobs across days, or top up the account

## Common Mistakes to Avoid

1. ❌ Using page numbers for sampling → ✅ Use `?sample=`
2. ❌ Filtering by entity names → ✅ Get IDs first
3. ❌ Default page size → ✅ Use `per-page=200`
4. ❌ Sequential ID lookups → ✅ Batch with pipe operator
5. ❌ No error handling → ✅ Implement retry with backoff on 429/403/5xx
6. ❌ Burning budget on `search=` → ✅ Filter by IDs/fields; reserve `search=` for free text
7. ❌ Running keyless for bulk jobs → ✅ Add a free `api_key=` (raises budget 100x)
8. ❌ Fetching all fields → ✅ Use `select=`

## Additional Resources

- Full documentation: https://developers.openalex.org (docs.openalex.org now redirects here)
- Authentication & pricing: https://developers.openalex.org/guides/authentication
- Get a free API key: https://openalex.org/settings/api
- LLM quick reference: https://developers.openalex.org/guides/llm-quick-reference
- User group: https://groups.google.com/g/openalex-users
