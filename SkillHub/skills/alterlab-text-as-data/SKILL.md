---
name: alterlab-text-as-data
description: "Analyzes text as social-science data — topic modeling (BERTopic with embeddings + class-based TF-IDF, LDA/NMF via scikit-learn or gensim), document embeddings (sentence-transformers), dictionary/lexicon methods, and supervised text classification — choosing the method that matches the inferential goal (discovery vs measurement vs prediction) and validating topic reliability rather than trusting one stochastic run. It uses the verified stack (BERTopic, scikit-learn, gensim CoherenceModel, spaCy, sentence-transformers) with pinned patterns. Use when the request mentions topic modeling, text as data, computational text analysis, document embeddings, dictionary/sentiment lexicons, or classifying a corpus. For training or fine-tuning transformer models prefer alterlab-transformers; for humanities close-reading corpora prefer alterlab-digital-humanities. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires (declare in-session, no runtime install on Anthropic API): bertopic>=0.16, scikit-learn>=1.3, gensim>=4.3, spacy>=3.7 (+ a model like en_core_web_sm), sentence-transformers>=2.2 (pip). Runs locally via `uv run python`; no API key."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-ssci-design-gate, alterlab-transformers (model training), alterlab-digital-humanities; audited by alterlab-ssci-inference-gate"
---

# Text-as-Data — Match the Method to the Inferential Goal

**Skill type: ANALYSIS MODULE.** Turns a corpus into measurements. The discipline is choosing by
*goal* — **discovery** (what themes exist?), **measurement** (how much of concept X?), or
**prediction** (label new documents) — and validating that a topic solution is **reliable**, not a
single lucky stochastic run.

## Core Mission

```
PICK BY GOAL: DISCOVERY vs MEASUREMENT vs PREDICTION. THEN VALIDATE THE TOPICS — ONE RUN IS NOT A RESULT.
```

## When to Use This Skill

- "Run topic modeling on my corpus (BERTopic / LDA)."
- "Measure how much each document expresses concept X (dictionary/lexicon)."
- "Embed my documents and cluster / compare them."
- "Classify these texts into categories."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Training / fine-tuning a transformer model | `alterlab-transformers` | Model training, not corpus measurement. |
| Humanities close-reading / annotation of texts | `alterlab-digital-humanities` | Interpretive, not quantitative text-as-data. |
| Whether a text method fits the question at all | `alterlab-ssci-design-gate` | Design routing, upstream. |
| Plain tabular statistics | `alterlab-statistical-analysis` | No text. |

## Method by goal (verified stack, pinned)

| Goal | Method | Verified call |
|------|--------|---------------|
| **Discovery** (emergent themes, contextual) | **BERTopic** (v0.17) | `from bertopic import BERTopic; topics, probs = BERTopic().fit_transform(docs)`; `get_topic_info()`, `get_topic(0)`. Plug embeddings via `embedding_model=SentenceTransformer("all-MiniLM-L6-v2")`, a `vectorizer_model=CountVectorizer(min_df=10)`. |
| Discovery (bag-of-words, classic) | **LDA / NMF** | sklearn: `LatentDirichletAllocation(n_components=k).fit(CountVectorizer().fit_transform(docs))`; or gensim `LdaModel(corpus, num_topics=k, id2word=dictionary)`. |
| Topic quality | **coherence** | gensim `CoherenceModel(model=lda, texts=tok, dictionary=d, coherence="c_v").get_coherence()`. |
| **Measurement** (how much of concept X) | **dictionary / lexicon** | count validated lexicon terms; report reliability and validate against hand-coding. |
| Embeddings / similarity | **sentence-transformers** (v5) | `SentenceTransformer("all-MiniLM-L6-v2").encode(texts)` → cluster / cosine-compare. |
| **Prediction** (label documents) | **supervised** | `TfidfVectorizer()` → a sklearn classifier; report held-out F1, not in-sample fit. |
| Linguistic features (POS, entities) | **spaCy** (v3) | `nlp = spacy.load("en_core_web_sm"); doc = nlp(text)`. |

Method-selection helper (stdlib): `scripts/text_method_router.py`. Full patterns, preprocessing,
and the topic-reliability procedure: `references/text_stack.md`.

## The reliability discipline (topic models are stochastic)

LDA (and, to a lesser degree, BERTopic via UMAP) gives different topics on different runs. A single
run is not a result. Required:

1. **Replicate** across seeds/runs; align topics across runs (e.g. Hungarian matching) and score
   stability (top-word overlap, RBO); report a **prototype** (most-representative) solution.
2. **Coherence, not just perplexity** — choose K by `c_v` coherence and human readability, not
   log-likelihood alone.
3. **Determinism where possible** — fix `random_state` (sklearn LDA) and UMAP's `random_state`
   (BERTopic) for reproducibility; still report stability across *different* seeds.
4. **Validate measurement** — a dictionary/topic used as a *measure* of a concept needs validation
   against human coding (precision/recall or correlation), exactly like any other instrument.

## Output Template

```
GOAL:         discovery | measurement | prediction
METHOD:       <BERTopic / LDA / dictionary / embeddings / supervised> + why it matches the goal
MODEL:        <call + K selection by coherence; embedding/vectorizer choices>
RELIABILITY:  <seeds run; topic stability; coherence c_v; determinism settings>
VALIDATION:   <if used as a measure: agreement with human coding>
CLAIM SCOPE:  descriptive/measurement of the corpus; generalization scoped to the corpus/sampling
```

## References

- `references/text_stack.md` — BERTopic/LDA/gensim/spaCy/embeddings patterns, preprocessing, topic-reliability procedure.
- `scripts/text_method_router.py` — stdlib router from goal + corpus features to the right method.

Part of the AlterLab Academic Skills suite.
