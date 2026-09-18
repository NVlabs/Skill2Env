#!/usr/bin/env python3
"""
Keyword Clusterer - Group keywords by semantic similarity.

Usage:
    python main.py cluster keywords.csv --n-clusters 10
    python main.py similar "content marketing" --count 20
    python main.py intent keywords.csv --column keyword
"""

import click
from pathlib import Path
from typing import Optional
import csv
from collections import defaultdict
import re


# Intent detection patterns
INTENT_PATTERNS = {
    'informational': [
        r'\bhow\b', r'\bwhat\b', r'\bwhy\b', r'\bwhen\b', r'\bwhere\b',
        r'\bguide\b', r'\btips\b', r'\btutorial\b', r'\bexamples?\b',
        r'\blearn\b', r'\bunderstand\b', r'\bdefinition\b', r'\bmeaning\b'
    ],
    'commercial': [
        r'\bbest\b', r'\btop\b', r'\breview\b', r'\bcompare\b', r'\bvs\b',
        r'\balternative\b', r'\bcompetitor\b', r'\bfeatures\b', r'\bpros\b',
        r'\bcons\b', r'\brating\b'
    ],
    'transactional': [
        r'\bbuy\b', r'\bprice\b', r'\bdiscount\b', r'\bsale\b', r'\border\b',
        r'\bpurchase\b', r'\bcheap\b', r'\bdeal\b', r'\bcoupon\b', r'\bsubscribe\b',
        r'\bfree trial\b', r'\bget\b'
    ],
    'navigational': [
        r'\blogin\b', r'\bsign in\b', r'\bcontact\b', r'\bsupport\b',
        r'\bdownload\b', r'\bapp\b', r'\bofficial\b'
    ]
}


def detect_intent(keyword: str) -> str:
    """Detect search intent from keyword."""
    keyword_lower = keyword.lower()

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, keyword_lower):
                return intent

    return 'informational'  # Default


def simple_similarity(kw1: str, kw2: str) -> float:
    """Simple word overlap similarity."""
    words1 = set(kw1.lower().split())
    words2 = set(kw2.lower().split())

    if not words1 or not words2:
        return 0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union else 0


def cluster_by_words(keywords: list, n_clusters: int) -> dict:
    """Simple clustering based on common words."""
    # Extract main topic words (filter common words)
    stop_words = {'how', 'to', 'the', 'a', 'an', 'for', 'in', 'on', 'with', 'and', 'or', 'is', 'what', 'best'}

    keyword_topics = []
    for kw in keywords:
        words = [w.lower() for w in kw.split() if w.lower() not in stop_words and len(w) > 2]
        keyword_topics.append(words)

    # Count word frequencies
    word_freq = defaultdict(int)
    for words in keyword_topics:
        for word in words:
            word_freq[word] += 1

    # Get top words as cluster centers
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:n_clusters]
    cluster_centers = [w[0] for w in top_words]

    # Assign keywords to clusters
    clusters = defaultdict(list)
    for kw, words in zip(keywords, keyword_topics):
        best_cluster = None
        best_score = 0

        for center in cluster_centers:
            if center in words:
                score = word_freq[center]
                if score > best_score:
                    best_score = score
                    best_cluster = center

        if best_cluster:
            clusters[best_cluster].append(kw)
        else:
            clusters['other'].append(kw)

    return dict(clusters)


@click.group()
def cli():
    """Keyword Clusterer - Organize keywords by similarity."""
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--column', '-c', default='keyword', help='Keyword column name')
@click.option('--n-clusters', '-n', default=10, type=int, help='Number of clusters')
@click.option('--method', '-m', default='lexical',
              type=click.Choice(['lexical', 'semantic']))
@click.option('--output', '-o', type=click.Path(), help='Output CSV file')
def cluster(file: str, column: str, n_clusters: int, method: str, output: Optional[str]):
    """Cluster keywords into groups."""
    input_path = Path(file)

    click.echo("\n  Keyword Clustering")
    click.echo("  " + "=" * 45)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Column: {column}")
    click.echo(f"  Clusters: {n_clusters}")
    click.echo(f"  Method: {method}")

    # Read keywords
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    keywords = [row.get(column, '').strip() for row in rows if row.get(column)]
    click.echo(f"  Keywords: {len(keywords)}")

    if method == 'semantic':
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.cluster import KMeans

            click.echo("  Loading embedding model...")
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(keywords)

            click.echo("  Clustering...")
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = kmeans.fit_predict(embeddings)

            clusters = defaultdict(list)
            for kw, label in zip(keywords, labels):
                clusters[f"Cluster {label + 1}"].append(kw)
            clusters = dict(clusters)

        except ImportError:
            click.echo("  [Warning] sentence-transformers not available, using lexical method")
            clusters = cluster_by_words(keywords, n_clusters)
    else:
        clusters = cluster_by_words(keywords, n_clusters)

    # Display results
    click.echo("\n  Clusters")
    click.echo("  " + "-" * 45)

    for cluster_name, kws in sorted(clusters.items(), key=lambda x: -len(x[1])):
        click.echo(f"\n  {cluster_name} ({len(kws)} keywords)")
        for kw in kws[:5]:
            click.echo(f"    • {kw}")
        if len(kws) > 5:
            click.echo(f"    ... and {len(kws) - 5} more")

    # Save output
    if output:
        output_path = Path(output)
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['keyword', 'cluster'])
            for cluster_name, kws in clusters.items():
                for kw in kws:
                    writer.writerow([kw, cluster_name])
        click.echo(f"\n  Saved: {output_path}")


@cli.command()
@click.argument('keyword')
@click.option('--count', '-c', default=10, help='Number of similar keywords')
def similar(keyword: str, count: int):
    """Find similar keywords (requires a keyword database)."""
    click.echo(f"\n  Similar Keywords: {keyword}")
    click.echo("  " + "=" * 40)

    # Generate variations (basic approach)
    keyword.lower().split()

    variations = [
        f"best {keyword}",
        f"{keyword} guide",
        f"{keyword} tips",
        f"{keyword} examples",
        f"how to {keyword}",
        f"{keyword} tools",
        f"{keyword} software",
        f"{keyword} services",
        f"{keyword} strategy",
        f"{keyword} for beginners",
        f"free {keyword}",
        f"{keyword} template",
    ]

    click.echo("\n  Suggested variations:")
    for i, var in enumerate(variations[:count], 1):
        click.echo(f"  {i}. {var}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--column', '-c', default='keyword', help='Keyword column name')
@click.option('--output', '-o', type=click.Path(), help='Output CSV file')
def intent(file: str, column: str, output: Optional[str]):
    """Categorize keywords by search intent."""
    input_path = Path(file)

    click.echo("\n  Intent Analysis")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")

    # Read keywords
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    keywords = [(row.get(column, ''), row) for row in rows if row.get(column)]
    click.echo(f"  Keywords: {len(keywords)}")

    # Analyze intent
    intent_counts = defaultdict(list)
    results = []

    for kw, row in keywords:
        kw_intent = detect_intent(kw)
        intent_counts[kw_intent].append(kw)
        results.append({**row, 'intent': kw_intent})

    # Display summary
    total = len(keywords)
    click.echo("\n  Intent Distribution")
    click.echo("  " + "-" * 40)

    for intent_type in ['informational', 'commercial', 'transactional', 'navigational']:
        count = len(intent_counts[intent_type])
        pct = count / total * 100 if total else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        click.echo(f"  {intent_type:<15} {count:>4} ({pct:>5.1f}%) [{bar}]")

    # Show examples
    for intent_type in ['informational', 'commercial', 'transactional', 'navigational']:
        kws = intent_counts[intent_type]
        if kws:
            click.echo(f"\n  {intent_type.title()} examples:")
            for kw in kws[:3]:
                click.echo(f"    • {kw}")

    # Save output
    if output:
        output_path = Path(output)
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
        click.echo(f"\n  Saved: {output_path}")


if __name__ == "__main__":
    cli()
