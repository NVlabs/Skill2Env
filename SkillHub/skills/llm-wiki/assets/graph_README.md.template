# Wiki Graph Layer

This directory holds the compiled knowledge graph derived from the markdown
wiki. **Markdown is canonical.** Everything here can be deleted and rebuilt
without losing knowledge:

```bash
python scripts/wiki_graph_extract.py wiki/ --out wiki/graph
```

## Files

| File | Purpose | Tracking |
|------|---------|----------|
| `ontology.yaml` | Declares node types and predicates the graph recognises. The contract `wiki_graph_lint.py` validates against. | **Tracked. Edit by hand.** |
| `nodes.jsonl` | One JSON object per node, sorted by id. | Generated. Track if you want graph diffs in PRs; otherwise gitignore. |
| `edges.jsonl` | One JSON object per edge, sorted by id. Includes typed semantic edges, `mentions`, `sourced_from`, and `summarizes_raw`. | Generated. Same trade-off as `nodes.jsonl`. |
| `graph.sqlite` | Queryable index used by `wiki_graph_query.py`. Schema: `nodes`, `aliases`, `edges`. | Generated. **Gitignored** — rebuild on demand. |
| `graph.graphml` | GraphML export for tools like Gephi or yEd. | Generated. Gitignored by default. |

## Workflow

1. Author or edit a wiki page. Add typed `graph.relationships` only when an explicit source supports them.
2. Run `python scripts/wiki_graph_lint.py wiki/` — catches unknown predicates, broken object references, missing evidence, alias collisions.
3. Run `python scripts/wiki_graph_extract.py wiki/ --out wiki/graph` — regenerates the artifacts above.
4. Query with `python scripts/wiki_graph_query.py wiki/ neighbors --node product:konvy` (or `edges`, `path`, `facts`).

## Anti-patterns

- **Hand-editing `nodes.jsonl` / `edges.jsonl` / `graph.sqlite`.** Edit the markdown; regenerate.
- **Treating graph rows as evidence.** They accelerate navigation. For high-stakes claims, follow the edge's `source` and `evidence` fields back to the wiki page and the raw source.
- **Adding typed edges the source doesn't support.** Use a normal `[[wikilink]]` instead — the `mentions` edge captures the connection without overclaiming.
