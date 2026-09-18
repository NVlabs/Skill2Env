#!/usr/bin/env python3
"""Route a text-as-data task to the right method by inferential goal (stdlib only).

It does NOT run any model — it names the method that matches your GOAL (discovery / measurement /
prediction) and corpus features, with the verified call and the reliability check you must run.

    python text_method_router.py --goal discovery --corpus-size 5000
    python text_method_router.py --goal measurement --have-lexicon yes
    python text_method_router.py --goal prediction --labeled yes
"""
from __future__ import annotations

import argparse

_REC = {
    "discovery": {
        "default": (
            "BERTopic (embeddings + class-based TF-IDF)",
            "from bertopic import BERTopic; topics, probs = BERTopic().fit_transform(docs)",
            "replicate across seeds; fix UMAP random_state; pick K by human readability + coherence",
        ),
        "small": (
            "LDA (gensim/sklearn) — BERTopic needs enough docs for good embeddings clustering",
            "LatentDirichletAllocation(n_components=k, random_state=0).fit(CountVectorizer().fit_transform(docs))",
            "choose K by gensim CoherenceModel c_v; replicate across seeds; report a prototype run",
        ),
    },
    "measurement": (
        "Dictionary / lexicon method (validated word lists)",
        "count validated lexicon terms per doc; normalize by length",
        "VALIDATE against human coding (precision/recall or correlation) — a dictionary is an instrument",
    ),
    "prediction": (
        "Supervised classification",
        "TfidfVectorizer() -> a sklearn classifier (or fine-tune via alterlab-transformers)",
        "report held-out F1 / cross-validated performance, never in-sample fit",
    ),
    "similarity": (
        "Sentence embeddings",
        'SentenceTransformer("all-MiniLM-L6-v2").encode(texts) -> cosine / clustering',
        "check that the embedding model suits the domain/language",
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--goal", required=True,
                    choices=["discovery", "measurement", "prediction", "similarity"])
    ap.add_argument("--corpus-size", type=int, default=None, help="number of documents")
    ap.add_argument("--have-lexicon", choices=["yes", "no"], default=None)
    ap.add_argument("--labeled", choices=["yes", "no"], default=None)
    args = ap.parse_args()

    if args.goal == "discovery":
        branch = "small" if (args.corpus_size is not None and args.corpus_size < 1000) else "default"
        method, call, reliability = _REC["discovery"][branch]
    else:
        method, call, reliability = _REC[args.goal]

    notes = []
    if args.goal == "measurement" and args.have_lexicon == "no":
        notes.append("No lexicon yet: build/adopt a validated word list before measuring.")
    if args.goal == "prediction" and args.labeled == "no":
        notes.append("No labels: you need labeled examples, or reframe as discovery (topic modeling).")

    print(f"GOAL:        {args.goal}")
    print(f"METHOD:      {method}")
    print(f"CALL:        {call}")
    print(f"RELIABILITY: {reliability}")
    for n in notes:
        print(f"NOTE:        {n}")
    print("Scope the claim to the corpus; a single stochastic topic run is not a result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
