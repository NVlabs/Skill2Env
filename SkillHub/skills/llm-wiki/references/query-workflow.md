# Query Workflow

The user is asking a question against the wiki. The job is to answer it from the wiki, with citations, scaling navigation to the wiki's size, and to file the answer back as a synthesis page when warranted.

## Step 0: Check the schema

Read `wiki/SCHEMA.md` if you haven't this session. Some wikis declare query-specific conventions (e.g. "always answer with a comparison table when the question is comparative", "answers go in `wiki/synthesis/qa/` not `wiki/synthesis/`"). Schema overrides defaults.

## Step 1: Read the index

Always start at `wiki/index.md`. If the index has been sharded into `wiki/indexes/`, read the top-level `index.md` first to identify which shard(s) are relevant, then read those.

The index is engineered for this — one line per page with a tight summary. You should be able to identify candidate pages from the index alone in most cases. If a query touches multiple shards (e.g. "compare the methodologies in papers A and B"), read all relevant shards.

## Step 2: Identify candidate pages

From the index, build a short list of pages that look relevant to the query. Be selective — reading 30 pages to answer a question is a sign you've fallen back to brute-force search, which doesn't scale. If the index summaries don't disambiguate well, that's a signal that the index entries are too terse — note it for the next lint pass.

If the index doesn't surface good candidates (the query uses fuzzy or domain-specific language that doesn't match the index summaries), fall back to the search script:

```bash
python scripts/wiki_search.py "your query terms" --top 10
```

This returns the top-N pages by BM25 score, with optional filters on frontmatter (`--type concept`, `--tag llms`, `--since 2026-01-01`). Use the search script *as a fallback*, not as the default — index-first is cheaper and produces more interpretable results when it works.

## Step 2b: Graph-assisted lookup (only if `wiki/graph/graph.sqlite` exists)

For relational questions ("what's connected to X", "who proposed Y", "trace the path from A to B"), query the compiled graph after the index pass and before reading pages:

```bash
python scripts/wiki_graph_query.py wiki/ neighbors --node <node-id>
python scripts/wiki_graph_query.py wiki/ facts    --about <node-id>
```

Use the structured neighbors/facts to pick the right wiki pages to read — but never answer from graph rows alone for high-stakes claims. The graph accelerates navigation; the wiki page and its raw source remain the evidence. If `graph.sqlite` is older than the most recent `## [YYYY-MM-DD] ingest |` entry in `log.md`, regenerate first with `wiki_graph_extract.py`. Full reference: `references/graph-workflow.md`.

## Step 3: Read the candidate pages

Read each candidate page in full. While reading, note any `[[wikilinks]]` to other pages that look relevant — those are pre-curated leads. Follow the most promising ones, but don't recursively chase every link or you'll exhaust your context window on tangentially-relevant pages.

If a page references a source-summary page in its frontmatter and the answer hinges on what that source actually said, read the source-summary page too. Avoid going all the way back to the raw source unless the wiki summaries are clearly insufficient — the whole point of the wiki is that the synthesis is already done.

## Step 4: Find backlinks if needed

If the query is "what does my wiki say about X" or "where is X mentioned", and X has its own page, the inbound links are often more interesting than the page itself. Find them with:

```bash
grep -rl "\[\[<page-slug>\]\]" wiki/
```

This is faster than reading pages to look for mentions. Note that the bundled `wiki_search.py` has a `--backlinks <slug>` mode that does this and returns ranked results.

## Step 5: Synthesize the answer

Write the answer in your own words, with `[[wikilink]]` citations to the wiki pages you used and (where helpful) `raw/<file>` references to specific raw sources. The citations matter — they let the user verify the answer and follow up.

If the wiki contains contradicting claims, surface the contradiction explicitly rather than picking one and presenting it as settled. The wiki's value is partly in tracking what's known versus what's contested.

If the wiki has no relevant content for the query, say so plainly. Do not confabulate — that's the surest way to corrupt the wiki when the answer gets filed back. Instead, suggest sources the user could ingest to fill the gap.

## Step 6: Offer to file the answer back

If the synthesized answer represents new connection-making — a comparison the wiki didn't already contain, an analysis that pulls together threads from multiple pages, an answer to a recurring question — offer to file it as a synthesis page. The user will say no for trivial answers and yes for substantive ones. Default to offering.

The file-back creates `wiki/synthesis/<answer-slug>.md` with frontmatter:

```yaml
---
type: synthesis
question: "the original question, verbatim or lightly cleaned"
asked: 2026-04-15
sources_consulted: [page-1, page-2, page-3]
tags: [...]
---
```

Body: the answer as you gave it to the user, possibly lightly edited for the wiki's voice. Add the new synthesis page to the relevant index. Append to `log.md` with prefix `## [YYYY-MM-DD] query | <question-summary>`.

A filed synthesis page is itself queryable — the next time the user asks an adjacent question, the synthesis page may be the most relevant candidate. This is how exploration compounds.

## Special query types

**"What's missing on topic X?"** — Read existing pages on X, identify open questions or unstated assumptions, and propose ingest candidates. This is essentially a per-topic micro-lint.

**"Compare X and Y"** — Read both pages, look for explicit comparison pages already in `synthesis/`, generate a comparison table or contrast prose. Strong file-back candidate.

**"Show me the timeline of X"** — Use `log.md` to reconstruct chronology of ingests touching X, supplement with `created`/`updated` frontmatter on relevant pages.

**"What did source X say about Y?"** — Read `wiki/sources/<x>.md` for the source's summary; if it doesn't directly answer, read `raw/<x>` (chunk-read if large).

**"Lint check on this answer"** — Before filing back, ask the user to verify a key claim by pointing to its raw source. Especially valuable for high-stakes wikis (medical, legal, financial).

## Anti-patterns to avoid

**Reading every page in the wiki to be safe.** This doesn't scale and produces vague answers. Trust the index; if the index fails, fix the index, don't bypass it.

**Citing the wiki without citing the underlying sources for hard claims.** The wiki page is a paraphrase; for any claim the user might need to verify, the citation should chain back to the raw source.

**Filing back trivial answers.** Not every Q&A is worth a permanent page. If the answer is a one-line lookup or restates an existing page, don't pollute synthesis/. The threshold is "would I want to find this when I ask a similar question in three months?"

**Confabulating when the wiki is silent.** Better to say "the wiki doesn't cover this" than to invent an answer that gets filed back as authoritative.
