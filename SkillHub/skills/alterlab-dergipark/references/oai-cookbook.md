# OAI-PMH Cookbook — Harvesting DergiPark

Recipes for the three scripts, with the exact commands and the gotchas that bite.
The interactive search page (`/tr/search`) is **gated behind a human-verification
challenge**, so none of this uses search — OAI harvesting plus direct article-page
fetches are the only robust, reproducible paths. Run everything with `uv run`.

## 1. Find a journal's slug

The slug is the `setSpec`. List every journal set:

```bash
uv run python scripts/dergipark_oai.py list-journals --tsv | head
# mulkiye   Mülkiye Dergisi
# yerblm    Cumhuriyet Yerbilimleri Dergisi
# ...
```

Filter locally for the title you want (the list is large; pipe to `rg`/`grep`).
The slug also appears in any article URL: `/en/pub/{slug}/article/{id}`.

## 2. Harvest a whole journal's metadata

```bash
uv run python scripts/dergipark_oai.py harvest mulkiye --prefix oai_dc --out mulkiye.json
```

- Follows `<resumptionToken>` automatically until the set is exhausted.
- `--max N` caps the harvest (useful for a quick look).
- `--prefix` accepts `oai_dc | oai_etdms | oai_marc | oai_mods`. For anything other
  than `oai_dc` the script returns the raw record XML (`{"raw_xml": "..."}`) so you
  can parse the richer schema yourself; `oai_dc` is parsed into clean fields.

### Filter by publication year — the right way

The OAI `<datestamp>` is the **re-index** time, not publication date, so you cannot
get a publication-year slice from `from`/`until`. Harvest, then filter on `dc:date`:

```bash
uv run python scripts/dergipark_oai.py harvest mulkiye --out mulkiye.json
uv run python - <<'PY'
import json
recs = json.load(open("mulkiye.json"))
y2012 = [r for r in recs if r["date"].startswith("2012")]
print(len(y2012), "articles published in 2012")
PY
```

## 3. One article → structured record / BibTeX / RIS

```bash
uv run python scripts/dergipark_oai.py get 10 --prefix oai_dc        # OAI oai_dc record
uv run python scripts/article_meta.py /en/pub/mulkiye/article/10 --format bibtex
uv run python scripts/article_meta.py /en/pub/mulkiye/article/10 --format ris
```

`article_meta.py` parses the page's `citation_*` / `DC.*` meta tags and formats
BibTeX/RIS **locally** — it does not call any on-site export backend. It also
returns `pdf_url` (resolved from `citation_pdf_url`); see the PDF gotcha below.

## 4. Download the full-text PDF

Take the PDF link from the page's `citation_pdf_url` meta tag — **do not build it
from the article id.** On article `/10` the PDF was `/en/download/article-file/9`
(file id 9 ≠ article id 10).

```bash
PDF=$(uv run python scripts/article_meta.py /en/pub/mulkiye/article/10 --format json \
      | uv run python -c "import sys,json;print(json.load(sys.stdin)['pdf_url'])")
curl -L -o article.pdf "$PDF"      # content-type: application/pdf
```

## 5. Journal scope + (self-declared) indexing

```bash
uv run python scripts/journal_info.py mulkiye --lang en
```

Returns aim-and-scope text and the `/indexes` page text, the latter stamped with a
`DISCLAIMER` (self-declared, unverified) plus cross-check pointers to TR Dizin and
DOAJ. **Never report the `/indexes` list as confirmed indexing** — see
`indexing.md` and route TR Dizin status questions to **alterlab-trdizin**.

## Live keyword search (when OAI set-harvest is not enough)

`/tr/search` is human-verification-gated, so plain HTTP scraping of it is
unreliable — **never claim a plain-HTTP search endpoint exists.** Two options:

1. **Preferred / reproducible:** OAI set-harvest + local filtering (recipe 2).
2. **Live keyword search:** drive a real browser via the Playwright MCP against
   `https://dergipark.org.tr/tr/search` with `q`, `section=article`, `page`,
   `sortBy`, `filter[article_type][]`, `filter[publication_year][]`. Result cards
   are `div.card.article-card.dp-card-outline`; titles `h5.card-title > a`. (Card
   selectors are from prior art — verify against the live DOM before depending on
   them.)

## Polite-harvesting notes

- The scripts send a descriptive `User-Agent` and retry with backoff. Keep harvests
  to what you need; the endpoint advertises `gzip`/`deflate` compression.
- No API key is required for any of these paths.
- Bulk Turkish-language cleanup of a harvested set (dedup, advisor-name
  normalization, TR↔EN synonym expansion) is a good fit to offload to a local LLM
  rather than burning API calls.
