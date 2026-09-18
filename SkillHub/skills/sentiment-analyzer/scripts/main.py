#!/usr/bin/env python3
"""
Sentiment Analyzer - Analyze sentiment in text using ML models.

Usage:
    python main.py analyze "Your text here"
    python main.py batch reviews.csv --column text
    python main.py report reviews.csv --column text --output report.html
"""

import click
from pathlib import Path
from typing import Optional
import csv
from datetime import datetime


def get_sentiment_simple(text: str) -> dict:
    """Get sentiment using simple rule-based approach."""
    text_lower = text.lower()

    # Simple word lists
    positive_words = {'love', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                      'best', 'awesome', 'perfect', 'happy', 'good', 'nice', 'enjoy',
                      'recommend', 'impressed', 'outstanding', 'superb', 'brilliant'}
    negative_words = {'hate', 'terrible', 'awful', 'worst', 'horrible', 'bad', 'poor',
                      'disappointing', 'useless', 'waste', 'broken', 'angry', 'frustrated',
                      'annoying', 'slow', 'expensive', 'never', 'refund'}

    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    total = pos_count + neg_count
    if total == 0:
        score = 0.5
    else:
        score = pos_count / total

    return {
        'score': score,
        'sentiment': 'positive' if score > 0.6 else ('negative' if score < 0.4 else 'neutral'),
        'label': get_label(score)
    }


def get_sentiment_vader(text: str) -> dict:
    """Get sentiment using VADER (if available)."""
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        compound = (scores['compound'] + 1) / 2  # Normalize to 0-1

        return {
            'score': compound,
            'sentiment': 'positive' if compound > 0.6 else ('negative' if compound < 0.4 else 'neutral'),
            'label': get_label(compound),
            'details': scores
        }
    except ImportError:
        return get_sentiment_simple(text)


def get_sentiment_transformer(text: str) -> dict:
    """Get sentiment using transformers (if available)."""
    try:
        from transformers import pipeline
        classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        result = classifier(text[:512])[0]  # Limit text length

        score = result['score'] if result['label'] == 'POSITIVE' else 1 - result['score']

        return {
            'score': score,
            'sentiment': 'positive' if score > 0.6 else ('negative' if score < 0.4 else 'neutral'),
            'label': get_label(score),
            'model': 'distilbert'
        }
    except ImportError:
        return get_sentiment_vader(text)


def get_label(score: float) -> str:
    """Convert score to human-readable label."""
    if score >= 0.8:
        return "Very Positive"
    elif score >= 0.6:
        return "Positive"
    elif score >= 0.4:
        return "Neutral"
    elif score >= 0.2:
        return "Negative"
    else:
        return "Very Negative"


@click.group()
def cli():
    """Sentiment Analyzer - ML-powered text sentiment analysis."""
    pass


@cli.command()
@click.argument('text')
@click.option('--model', '-m', default='vader',
              type=click.Choice(['simple', 'vader', 'transformer']))
def analyze(text: str, model: str):
    """Analyze sentiment of a single text."""
    click.echo("\n  Sentiment Analysis")
    click.echo("  " + "=" * 40)
    click.echo(f"  Text: \"{text[:100]}{'...' if len(text) > 100 else ''}\"")
    click.echo(f"  Model: {model}")

    if model == 'simple':
        result = get_sentiment_simple(text)
    elif model == 'vader':
        result = get_sentiment_vader(text)
    else:
        result = get_sentiment_transformer(text)

    click.echo("\n  Results")
    click.echo("  " + "-" * 40)
    click.echo(f"  Sentiment: {result['sentiment'].upper()}")
    click.echo(f"  Score: {result['score']:.2f}")
    click.echo(f"  Label: {result['label']}")

    # Visual indicator
    bar_length = int(result['score'] * 20)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    click.echo(f"  [{bar}]")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--column', '-c', required=True, help='Column containing text')
@click.option('--model', '-m', default='vader',
              type=click.Choice(['simple', 'vader', 'transformer']))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def batch(file: str, column: str, model: str, output: Optional[str]):
    """Batch analyze sentiment from CSV file."""
    input_path = Path(file)

    click.echo("\n  Batch Sentiment Analysis")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Column: {column}")
    click.echo(f"  Model: {model}")

    # Read CSV
    rows = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    click.echo(f"  Rows: {len(rows)}")
    click.echo("  Processing...")

    # Analyze each row
    results = []
    pos_count = neg_count = neu_count = 0

    for row in rows:
        text = row.get(column, '')
        if not text:
            continue

        if model == 'simple':
            result = get_sentiment_simple(text)
        elif model == 'vader':
            result = get_sentiment_vader(text)
        else:
            result = get_sentiment_transformer(text)

        row['sentiment'] = result['sentiment']
        row['sentiment_score'] = f"{result['score']:.2f}"
        row['sentiment_label'] = result['label']
        results.append(row)

        if result['sentiment'] == 'positive':
            pos_count += 1
        elif result['sentiment'] == 'negative':
            neg_count += 1
        else:
            neu_count += 1

    # Write output
    output_path = Path(output) if output else input_path.with_stem(f"{input_path.stem}_sentiment")
    output_path = output_path.with_suffix('.csv')

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    total = len(results)
    click.echo("\n  Summary")
    click.echo("  " + "-" * 40)
    click.echo(f"  Positive: {pos_count} ({pos_count/total*100:.1f}%)")
    click.echo(f"  Neutral:  {neu_count} ({neu_count/total*100:.1f}%)")
    click.echo(f"  Negative: {neg_count} ({neg_count/total*100:.1f}%)")
    click.echo(f"\n  [Done] Output: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--column', '-c', required=True, help='Column containing text')
@click.option('--output', '-o', type=click.Path(), help='Output HTML report')
def report(file: str, column: str, output: Optional[str]):
    """Generate sentiment analysis report."""
    input_path = Path(file)

    click.echo("\n  Generating Sentiment Report")
    click.echo("  " + "=" * 40)

    # Read and analyze
    rows = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    results = {'positive': [], 'neutral': [], 'negative': []}

    for row in rows:
        text = row.get(column, '')
        if text:
            result = get_sentiment_vader(text)
            results[result['sentiment']].append({
                'text': text[:200],
                'score': result['score']
            })

    total = sum(len(v) for v in results.values())

    # Generate HTML report
    output_path = Path(output) if output else input_path.with_suffix('.html')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Sentiment Analysis Report</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ padding: 20px; border-radius: 8px; flex: 1; }}
        .positive {{ background: #d4edda; color: #155724; }}
        .neutral {{ background: #fff3cd; color: #856404; }}
        .negative {{ background: #f8d7da; color: #721c24; }}
        .sample {{ margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 4px; }}
        .score {{ float: right; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Sentiment Analysis Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <p>Source: {input_path.name} ({total} entries)</p>

    <div class="summary">
        <div class="card positive">
            <h3>Positive</h3>
            <p style="font-size: 2em">{len(results['positive'])} ({len(results['positive'])/total*100:.1f}%)</p>
        </div>
        <div class="card neutral">
            <h3>Neutral</h3>
            <p style="font-size: 2em">{len(results['neutral'])} ({len(results['neutral'])/total*100:.1f}%)</p>
        </div>
        <div class="card negative">
            <h3>Negative</h3>
            <p style="font-size: 2em">{len(results['negative'])} ({len(results['negative'])/total*100:.1f}%)</p>
        </div>
    </div>

    <h2>Sample Positive Feedback</h2>
    {''.join(f'<div class="sample"><span class="score">{r["score"]:.2f}</span>{r["text"]}</div>' for r in results['positive'][:5])}

    <h2>Sample Negative Feedback</h2>
    {''.join(f'<div class="sample"><span class="score">{r["score"]:.2f}</span>{r["text"]}</div>' for r in results['negative'][:5])}
</body>
</html>"""

    output_path.write_text(html)
    click.echo(f"  [Done] Report: {output_path}")


if __name__ == "__main__":
    cli()
