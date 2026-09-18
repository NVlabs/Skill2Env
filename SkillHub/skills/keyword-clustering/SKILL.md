---
name: keyword-clustering
description: >
  Cluster a list of keywords into topical groups with search intent labels, validated search volume, KD, and CPC data. Use this skill whenever a user provides a list of keywords (pasted, uploaded as CSV/Excel, or via Google Sheet URL) and asks to cluster, group, map, organize, or categorize them. Also trigger when a user says "keyword cluster", "cluster my keywords", "group these keywords", "keyword map", "keyword strategy from this list", "organize keywords by topic", or pastes or uploads a list of keywords and wants structure from it. Always use this skill — do not attempt keyword clustering manually without following this workflow.
---

# Keyword Clustering Skill

Turn a raw keyword list into a structured, validated cluster map delivered as a downloadable Excel file.

---

## What This Skill Does

1. **Accepts** keywords from any input format
2. **Validates** each keyword via DataForSEO — fetches search volume, KD, CPC
3. **Filters** out keywords with 0 or null search volume (dead keywords)
4. **Clusters** the validated keywords by topic + search intent
5. **Outputs** a formatted, downloadable Excel file

---

## Step 1: Input Handling

Detect which input format the user provided and extract the keyword list.

### Pasted list
If the user pasted keywords directly in chat (one per line, comma-separated, or numbered), extract each keyword into a clean array. Strip numbers, bullets, extra whitespace.

### CSV or Excel upload
The file will be at `/mnt/user-data/uploads/`. Read it with pandas:
```python
import pandas as pd

# CSV
df = pd.read_csv('/mnt/user-data/uploads/filename.csv')

# Excel
df = pd.read_excel('/mnt/user-data/uploads/filename.xlsx')

# Identify keyword column: look for columns named 'keyword', 'keywords', 'query', 'term', 'search term'
# If ambiguous, pick the first text column or ask the user
keyword_candidates = ['keyword', 'keywords', 'query', 'term', 'search term']
keyword_col = next((col for col in df.columns if col.lower() in keyword_candidates), df.columns[0])
keywords = df[keyword_col].dropna().tolist()
```

### Google Sheet URL
Use `web_fetch` to fetch the sheet as CSV (append `/export?format=csv` to the base URL). Parse with pandas.

**Cap at 500 keywords per run.** If input exceeds 500, tell the user and process the first 500, or ask which subset to use.

---

## Step 2: DataForSEO Validation

Use the `dataforseo_labs_google_keyword_overview` tool to validate all keywords and fetch metrics. Batch in groups of 100 to stay within API limits.

**Required fields to extract per keyword:**
- `search_volume` — monthly searches (Google)
- `keyword_difficulty` — KD score (0–100)

**Filter rule:** Drop any keyword where `search_volume` is `0`, `null`, or missing. These are dead keywords.

Tell the user upfront: "Validating [N] keywords via DataForSEO. This may take a moment..."

After validation, report:
- Total keywords submitted
- Keywords that passed (have search volume)
- Keywords that were dropped (zero/null volume) — list them so the user can see what was removed

**If DataForSEO is unavailable or returns an error:** Tell the user "DataForSEO validation failed — I'll cluster the full list but cannot validate search volume or provide KD/CPC data." Then proceed with the full unvalidated list and skip the volume/KD/CPC columns in the output.

---

## Step 3: Clustering

Cluster the **validated keywords only** using a two-axis approach:

### Axis 1: Topical Cluster
Group keywords by shared topic/theme. Use the root concept to name the cluster.

Rules:
- Each cluster should have a **2–5 word descriptive name** (e.g., "Email Marketing Tools", "Python Data Analysis")
- Aim for clusters of **3–8 keywords**. Prefer more clusters over fewer — if a topic can reasonably be split into two distinct subtopics, split it
- Do NOT over-merge: keywords that target different angles, audiences, or content types should be in separate clusters even if they share a root word
- If a topic is very broad, always create sub-clusters (use a parent + child naming convention, e.g., "SEO – On-Page", "SEO – Technical")
- Assign each cluster a numeric `Cluster ID` (1, 2, 3…)

### Axis 2: Search Intent
For each keyword, assign one of the four standard intent labels:

| Label | Meaning | Signal words |
|---|---|---|
| `Informational` | User wants to learn | what is, how to, guide, tutorial, definition, examples |
| `Navigational` | User wants a specific site/brand | brand name + login/sign in/pricing |
| `Commercial` | User is comparing options | best, top, vs, review, alternative, comparison |
| `Transactional` | User wants to act/buy | buy, download, get, free trial, sign up, hire |

When intent is ambiguous, pick the most likely based on the full keyword phrase. Do not leave intent blank.

### Clustering Logic
Use your understanding of keyword semantics. Group keywords that:
- Share the same core topic or product area
- Would logically appear in the same content piece or site section
- Target the same audience stage

Do NOT group purely by shared word (e.g., don't put "best email marketing software" and "email marketing statistics" in the same cluster just because they share "email marketing" — one is Commercial, one is Informational, and they serve different pages).

---

## Step 4: Build the Excel Output

Read the xlsx SKILL first if available. Use `openpyxl` for formatting.

### Sheet 1: "Keyword Clusters" (main output)

Columns in order:
| Column | Description |
|---|---|
| Cluster ID | Numeric cluster number |
| Cluster Name | Descriptive topic name |
| Keyword | The validated keyword |
| Search Volume | Monthly search volume from DataForSEO |
| KD | Keyword difficulty (0–100) |
| Intent | Informational / Navigational / Commercial / Transactional |

**Sorting:** Sort by Cluster ID ascending, then by Search Volume descending within each cluster.

**Formatting:**
- Row 1: Bold header, dark background (#1F2D40), white text, center-aligned
- Alternate cluster groups with light row shading to visually separate clusters (#F2F2F2 every other cluster group)
- Freeze top row
- Auto-fit column widths (min 15, max 40)
- Number format for Search Volume: `#,##0`
- KD: plain integer

### Sheet 2: "Cluster Summary"

One row per cluster:
| Column | Description |
|---|---|
| Cluster ID | Number |
| Cluster Name | Name |
| # Keywords | Count of keywords in cluster |
| Avg Search Volume | Average volume across cluster |
| Avg KD | Average KD |
| Dominant Intent | Most common intent label in cluster |
| Top Keyword | Highest-volume keyword in cluster |

**Sort by Avg Search Volume descending** — highest-opportunity clusters first.

### Sheet 3: "Dropped Keywords"

List all keywords removed at the validation step:
| Column | Description |
|---|---|
| Keyword | The dropped keyword |
| Reason | "Zero search volume" or "No data returned" |

If no keywords were dropped, add a single row: "No keywords were dropped."

---

## Step 5: Save and Deliver

```python
# Save the workbook
output_path = '/mnt/user-data/outputs/keyword_clusters.xlsx'
wb.save(output_path)
```

Then run recalc if formulas are used:
```bash
python scripts/recalc.py /mnt/user-data/outputs/keyword_clusters.xlsx
```

Use `present_files` to deliver the file to the user.

After presenting the file, give a short summary in chat:
- Total keywords clustered
- Number of clusters created
- Number of keywords dropped
- Top 3 clusters by average search volume

---

## Edge Cases

- **Duplicate keywords:** Deduplicate before validation. If duplicates exist, mention it.
- **Non-English keywords:** DataForSEO supports multi-language. Cluster by semantic meaning. Note the language.
- **All keywords dropped:** Tell the user all keywords had zero volume. Offer to cluster them anyway without validation.
- **Single keyword input:** Tell the user clustering requires at least 10 keywords to be meaningful.
- **Very large input (200+ keywords):** Warn that DataForSEO batching may take 2–3 minutes. Proceed automatically.