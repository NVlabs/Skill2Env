# Graph Workflow

The graph layer is the optional **compiled index** over the markdown wiki. It does not replace the wiki — it sits alongside it under `wiki/graph/` and is reproducible from the markdown at any time. The point is to make typed, provenance-backed relationships machine-queryable while keeping markdown canonical.

If `wiki/graph/ontology.yaml` is absent, the wiki is pre-graph: don't run extract/lint/query and don't fabricate ontology files. Either propose adding the layer, or proceed without it.

## What the graph captures

Three classes of edge come out of an extract:

1. **Typed semantic edges** declared in a page's `graph.relationships[]` frontmatter. Examples: `founded`, `proposed`, `depends_on`. Each one carries an explicit `source` (a source-page slug), an `evidence` quote, a `confidence` (high/medium/low), and a `status` (current/historical/proposed/disputed/superseded). The extractor never invents these.
2. **`mentions` edges** — one per body `[[wikilink]]` (deduplicated per page). Confidence is `low`; they accelerate navigation but should not be cited as evidence of a typed relationship.
3. **`sourced_from`** edges — one per slug in a non-source page's frontmatter `sources:` list, pointing at the source page. **`summarizes_raw`** edges — one per source page's `raw:` field, with the raw file path as the (string-literal) object.

## Frontmatter schema

```yaml
graph:
  node_id: person:praney-behl       # optional; default <node_type>:<slug>
  node_type: person                  # optional; default mapped from type/kind via ontology
  canonical: true                    # mark canonical when multiple slugs alias the same entity
  aliases: [Praney, praney@example.com]
  relationships:
    - predicate: founded
      object: company:seedblocks
      source: praney-founder-context-dump
      evidence: "Solo technical founder and sole director..."
      confidence: high
      status: current
      # optional:
      # valid_from: 2025-01-15
      # valid_to: 2026-03-01
      # notes: "..."
      # raw_ref: "raw/founder-dump.md#L42"
      # contradicts: <node-id-or-edge-id>
      # supersedes: <node-id-or-edge-id>
```

Required relationship fields: `predicate`, `object`, `source`, `evidence`, `confidence`, `status`.

`node_id` format is `<node_type>:<slug>`. The default is derived from the page's `type`/`kind` via the ontology's `maps_from` block. `decision`, `claim`, and `raw` are explicit-only — they don't have wiki pages, so they only show up as edge objects. If a typed edge points at one of these, the `wiki_graph_lint.py` flag for "broken object reference" will fire until either (a) you create a page for it, or (b) you add it to the ontology with `explicit_only: true` and accept that lint will continue to flag the reference.

## The ontology

`wiki/graph/ontology.yaml` is the contract. It declares:

- `node_types[*].maps_from` — how page `type`/`kind` projects onto a node type.
- `predicates[*]` — the allowed predicates, each with `subject_types`, `object_types`, and `requires_evidence`. `"*"` is a wildcard for either side.

Edit the ontology when you need a new domain predicate. Re-run `wiki_graph_lint.py` to validate; existing typed edges will be caught if they no longer match.

## When to add a typed edge vs a plain `[[wikilink]]`

Add a typed edge when:

- A specific source explicitly states the relationship.
- You can quote a snippet of evidence.
- The predicate is meaningful for downstream queries ("who founded what", "what did Stephanie propose").

Use a plain `[[wikilink]]` when:

- The relationship is implicit, atmospheric, or you're hedging.
- You cannot pin the claim to a single source quote.
- The predicate would be `mentions` anyway.

When in doubt, write the wikilink and skip the typed edge. The lint surfaces missing evidence; it does not punish under-claiming.

## Extract / lint / query loop

```bash
# Validate the typed metadata first; lint is conservative, never edits.
python scripts/wiki_graph_lint.py wiki/

# Compile to nodes.jsonl, edges.jsonl, graph.sqlite, graph.graphml.
python scripts/wiki_graph_extract.py wiki/

# Navigate.
python scripts/wiki_graph_query.py wiki/ neighbors --node product:konvy
python scripts/wiki_graph_query.py wiki/ edges    --subject person:stephanie-emmanouel
python scripts/wiki_graph_query.py wiki/ path     --from person:praney-behl --to product:konvy
python scripts/wiki_graph_query.py wiki/ facts    --about product:konvy
```

`--json` works on both lint and query commands.

## Ingest workflow integration

After Step 6 of the standard ingest workflow (after surgical updates and source page creation), run:

1. If new typed edges were added on the page being ingested, run `wiki_graph_lint.py`. Triage findings with the user before extract.
2. Run `wiki_graph_extract.py` to refresh the compiled artifacts.
3. Append a sub-line under the ingest's `log.md` entry:
   `   graph: +N nodes, +M typed edges (predicates: founded, contains_product, ...)`

Skip both if the page being ingested has no `graph.relationships[]` and no new pages were created — the graph layer is unchanged.

## Query workflow integration

When the user asks a question that smells relational ("what's connected to X", "who proposed Y", "trace the path from A to B"):

1. Read the index as usual.
2. If `wiki/graph/graph.sqlite` exists and is fresher than the latest log entry, query it for typed edges around the candidate pages — `neighbors`, `edges`, `facts` are the most useful.
3. Read the wiki pages behind the relevant nodes/edges. Don't answer from graph rows alone for high-stakes claims; the `evidence` field is a hint, not the source of truth.
4. Cite with `[[wikilinks]]` to wiki pages, not graph rows.

If `graph.sqlite` is stale (older than the most recent ingest in `log.md`), regenerate first, then query.

## Generated artifact policy

| File | Canonical? | Default tracking |
|------|-----------|------------------|
| `wiki/graph/ontology.yaml` | Yes — edit by hand | Tracked |
| `wiki/graph/nodes.jsonl` | Generated | Optional — `wiki/graph/.gitignore` does not ignore it; track if you want graph diffs in PRs |
| `wiki/graph/edges.jsonl` | Generated | Same as above |
| `wiki/graph/graph.sqlite` | Generated | **Gitignored** by default (large, binary) |
| `wiki/graph/graph.graphml` | Generated | **Gitignored** by default |

The bootstrapped `wiki/graph/.gitignore` ignores `graph.sqlite` and `graph.graphml`. Edit it if your team prefers different policy.

## Anti-patterns

- **Typed edges without evidence.** Defeats the entire point. Lint will flag them; do not silence.
- **Editing `nodes.jsonl` / `edges.jsonl` / `graph.sqlite` by hand.** Edit the markdown; regenerate.
- **Inventing ontology entries to make a typed edge "fit".** The ontology should reflect domain reality, not paper over a too-eager edge. Either add the predicate with proper `subject_types`/`object_types`, or use `mentions`.
- **Treating graph rows as evidence in answers.** Always cite the wiki page; the graph just told you which wiki page to read.
- **Forgetting to regenerate after an ingest.** The graph diverges silently. Tie extract to ingest in muscle memory.
