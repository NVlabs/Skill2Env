---
name: paper-search
description: Search for academic papers by keyword, or look up a specific paper by DOI or OpenAlex ID. Powered by OpenAlex (250M+ works, free, no API key).
---

Search for academic papers and get details including title, authors, citation count, DOI, abstract, and open access links.

Steps:
1. Find the scripts directory: `find ~/.claude -name "search.sh" -path "*/paper-search/*" 2>/dev/null | sort -V | tail -1`
   - This finds the script whether installed via plugin or manual setup
   - The `paper.sh` script is in the same directory
2. To search for papers by keyword:
   ```
   <scripts-dir>/search.sh "your search query" [limit] [sort] [page]
   ```
   - `limit`: number of results per page (default: 10, max: 200)
   - `sort`: `relevance` (default), `cites`, or `date`
   - `page`: page number for pagination (default: 1)
3. To look up a specific paper by DOI or OpenAlex ID:
   ```
   <scripts-dir>/paper.sh <DOI_URL or OpenAlex_ID>
   ```
   - Accepts full DOI URLs like `https://doi.org/10.3390/brainsci8020020`
   - Or OpenAlex IDs like `W2789811475`
   - Returns full details: authors, abstract, concepts, open access PDF link, related works

Tips:
- Use `relevance` sort (default) for topical searches. Use `cites` when you want landmark papers.
- Be specific with queries — "bilingual cognitive advantages executive function" beats "bilingualism brain".
- Use `paper.sh` to get the full abstract when search results show "Abstract: N/A".
- The `related_works` IDs from `paper.sh` can be fed back into `paper.sh` to explore the citation graph.
- When the user asks for scientific backing: search broadly first, pick the most relevant/cited papers, then use `paper.sh` for full details and cite as (Author, Year, Journal).
