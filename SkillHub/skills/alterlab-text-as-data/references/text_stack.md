# Text-as-Data Stack — Patterns and Topic Reliability

Loaded on demand from the text-as-data SKILL.md. Verified against current docs: BERTopic v0.17,
scikit-learn, gensim v4.4, spaCy v3.8, sentence-transformers v5.

## BERTopic (discovery, contextual)

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

topic_model = BERTopic(
    embedding_model=SentenceTransformer("all-MiniLM-L6-v2"),
    vectorizer_model=CountVectorizer(min_df=10, stop_words="english"),
    calculate_probabilities=True,
)
topics, probs = topic_model.fit_transform(docs)
topic_model.get_topic_info()      # topics + sizes
topic_model.get_topic(0)          # top terms for topic 0
topic_model.visualize_topics()    # interactive map
```

For reproducibility, pass a UMAP with a fixed `random_state` (BERTopic is stochastic through UMAP):

```python
from umap import UMAP
BERTopic(umap_model=UMAP(random_state=42))
```

## LDA / NMF (discovery, bag-of-words)

sklearn:

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
dtm = CountVectorizer(min_df=5, stop_words="english").fit_transform(docs)
lda = LatentDirichletAllocation(n_components=10, random_state=0).fit(dtm)
lda.components_          # topic-term weights
lda.transform(dtm)       # doc-topic distribution
```

gensim (with coherence for choosing K):

```python
from gensim.corpora import Dictionary
from gensim.models import LdaModel, CoherenceModel
d = Dictionary(tokenized_docs); corpus = [d.doc2bow(t) for t in tokenized_docs]
lda = LdaModel(corpus, num_topics=10, id2word=d, random_state=0)
cm = CoherenceModel(model=lda, texts=tokenized_docs, dictionary=d, coherence="c_v")
cm.get_coherence()       # compare across K; c_v needs tokenized `texts`
```

## Embeddings and dictionary methods

```python
from sentence_transformers import SentenceTransformer
emb = SentenceTransformer("all-MiniLM-L6-v2").encode(texts)   # np.ndarray, cluster or cosine
```

Dictionary/lexicon measurement: count validated term lists per document, normalize by length, and
**validate** the score against human coding — a lexicon is an instrument and needs reliability and
validity evidence like any scale (see `alterlab-ssci-measurement-gate`).

## spaCy (linguistic features)

```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
[(t.text, t.pos_, t.lemma_) for t in doc]
[(e.text, e.label_) for e in doc.ents]
```

## Preprocessing notes

- Match preprocessing to the method: BERTopic works on **raw** documents (embeddings capture
  context) — do NOT aggressively stem/stopword before embedding; apply stopword removal in the
  `vectorizer_model` for the topic representation instead. Classic LDA benefits from lowercasing,
  stopword removal, and sometimes lemmatization.
- Keep the unit of analysis explicit (sentence vs paragraph vs document) — it changes topics.

## Topic reliability procedure (topic models are stochastic)

LDA can reproduce fewer than half its topics across runs at large K. Do not report one run.

1. Run the model **R times** with different seeds.
2. Align topics across runs — Hungarian algorithm on a top-word similarity (cosine/Jaccard) or RBO.
3. Score stability; keep topics that recur above a threshold (e.g. overlap > 0.7).
4. Report the **prototype** run (most representative / medoid) and the stability statistics — see
   the LDAPrototype approach and the reliability-of-topic-models literature (arXiv 2410.23186).
5. Choose K by coherence (`c_v`) plus human interpretability, not perplexity/log-likelihood alone.

## References

- Grimmer & Stewart (2013), Text as Data. *Political Analysis.*
- Grootendorst (2022), BERTopic.
- Blei, Ng & Jordan (2003), Latent Dirichlet Allocation.
- Rieger et al. (LDAPrototype); reliability of topic modeling (arXiv 2410.23186).
