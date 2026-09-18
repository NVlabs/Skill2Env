---
name: redis-semantic-cache
description: Redis LangCache guidance for semantic caching of LLM responses on Redis Cloud — calling search/set via the SDK or REST API, tuning the similarity threshold, separating caches per task type, and filtering with custom attributes. Use when caching LLM completions or RAG answers to cut API cost and latency, building a cache-aside layer in front of OpenAI / Anthropic / etc., tuning hit rate vs precision, or splitting one app's LLM workloads into multiple LangCache caches.
license: MIT
metadata:
  author: Redis, Inc.
  version: "0.1.0"
---

# Redis Semantic Cache

Semantic caching for LLM responses with Redis Cloud's LangCache service. Stores prompts as embeddings; subsequent semantically-similar prompts return the cached response without re-calling the model.

> LangCache is currently in **preview** on Redis Cloud. Features and behavior may change.

## When to apply

- Wrapping an LLM call (OpenAI, Anthropic, etc.) with a cache layer to cut cost and latency.
- Caching RAG answers, classification outputs, or any deterministic LLM workload.
- Tuning the precision/hit-rate trade-off for a semantic cache.
- Splitting one application's LLM workloads across multiple cache instances.

## 1. The cache-aside flow

LangCache fits in front of any LLM call as a standard cache-aside pattern:

1. Send the user's prompt to LangCache's `search`.
2. **Cache hit** — return the stored response directly.
3. **Cache miss** — call the LLM, then `set` the response so future similar prompts hit.

```python
from langcache import LangCache
import os

lang_cache = LangCache(
    server_url=f"https://{os.getenv('HOST')}",
    cache_id=os.getenv("CACHE_ID"),
    api_key=os.getenv("API_KEY"),
)

result = lang_cache.search(prompt="What is Redis?", similarity_threshold=0.9)
if result:
    response = result[0]["response"]
else:
    response = llm.generate("What is Redis?")
    lang_cache.set(prompt="What is Redis?", response=response)
```

The same operations are available via REST (`POST /v1/caches/{cacheId}/entries/search` and `POST /v1/caches/{cacheId}/entries`) when an SDK isn't an option.

See [references/langcache-usage.md](references/langcache-usage.md) for full SDK + REST samples and attribute-based storage.

## 2. Tune the similarity threshold

The threshold controls how close (in embedding cosine distance) a new prompt must be to a cached one to count as a hit. Higher = stricter match, fewer false positives. Lower = more hits, more risk of returning an off-topic answer.

| Threshold | Behavior | Use when |
|---|---|---|
| 0.95+ | Near-exact match required | Customer-facing answers where wrong responses are costly |
| 0.9 | Balanced default | Most workloads — start here |
| 0.8 | Loose semantic match | Internal tools, exploratory queries, FAQ deduplication |

```python
# Stricter — fewer false positives
result = lang_cache.search(prompt="What is Redis?", similarity_threshold=0.95)

# Looser — higher hit rate
result = lang_cache.search(prompt="What is Redis?", similarity_threshold=0.8)
```

Adjust by watching the actual cache-hit rate and spot-checking that returned answers are still relevant.

See [references/best-practices.md](references/best-practices.md).

## 3. Separate caches per task type

Different LLM workloads should not share one cache — a "code question" prompt is semantically close to other code questions but has nothing to do with a password-reset support query, and crossing them returns garbage.

```python
support_cache = LangCache(server_url=..., cache_id="support-cache-id", api_key=...)
code_cache    = LangCache(server_url=..., cache_id="code-cache-id",    api_key=...)
```

Create distinct cache IDs in Redis Cloud per task, and route each call to the right one. As a finer-grained alternative, store and search with **custom attributes** (e.g. `{"category": "database"}`) to keep tasks in the same cache but isolated by attribute filter — useful when the same prompt format spans subtopics.

## References

- [LangCache documentation](https://redis.io/docs/latest/develop/ai/langcache/)
