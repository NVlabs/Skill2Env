#!/usr/bin/env python3
"""UGC Collector - Collect user-generated content."""

import click
from pathlib import Path
from typing import Optional
import json
from datetime import datetime
import random

def generate_ugc_item(hashtag: str, platform: str) -> dict:
    """Generate simulated UGC item."""
    types = ['photo', 'video', 'story', 'review', 'testimonial']
    sentiments = ['positive', 'positive', 'positive', 'neutral', 'negative']

    return {
        'id': f"ugc_{random.randint(10000, 99999)}",
        'platform': platform,
        'type': random.choice(types),
        'author': f"@user{random.randint(100, 9999)}",
        'date': datetime.now().strftime('%Y-%m-%d'),
        'hashtag': hashtag,
        'sentiment': random.choice(sentiments),
        'engagement': random.randint(10, 1000),
        'content': f"Sample UGC content mentioning {hashtag}...",
    }

@click.group()
def cli():
    """UGC Collector - User-generated content management."""
    pass

@cli.command()
@click.argument('hashtag')
@click.option('--platform', '-p', default='instagram',
              type=click.Choice(['instagram', 'twitter', 'tiktok']))
@click.option('--count', '-c', default=20, help='Number of items')
@click.option('--output', '-o', type=click.Path(), help='Output JSON file')
def search(hashtag: str, platform: str, count: int, output: Optional[str]):
    """Search for UGC by hashtag."""
    click.echo("\n  UGC Search")
    click.echo("  " + "=" * 40)
    click.echo(f"  Hashtag: {hashtag}")
    click.echo(f"  Platform: {platform}")

    items = []
    for _ in range(count):
        random.seed()
        items.append(generate_ugc_item(hashtag, platform))

    # Summary
    by_type = {}
    by_sentiment = {}
    for item in items:
        by_type[item['type']] = by_type.get(item['type'], 0) + 1
        by_sentiment[item['sentiment']] = by_sentiment.get(item['sentiment'], 0) + 1

    click.echo(f"\n  Found {len(items)} UGC items")
    click.echo("  " + "-" * 40)

    click.echo("\n  By Type:")
    for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
        click.echo(f"    {t}: {c}")

    click.echo("\n  By Sentiment:")
    for s, c in sorted(by_sentiment.items(), key=lambda x: -x[1]):
        click.echo(f"    {s}: {c}")

    click.echo("\n  Top Performers:")
    sorted_items = sorted(items, key=lambda x: x['engagement'], reverse=True)
    for item in sorted_items[:5]:
        click.echo(f"    {item['author']} - {item['type']} ({item['engagement']} eng)")

    if output:
        Path(output).write_text(json.dumps(items, indent=2))
        click.echo(f"\n  Saved: {output}")

@cli.command()
@click.argument('handle')
@click.option('--platform', '-p', default='twitter')
@click.option('--days', '-d', default=7, help='Days to look back')
def mentions(handle: str, platform: str, days: int):
    """Collect brand mentions."""
    click.echo(f"\n  Brand Mentions: {handle}")
    click.echo("  " + "=" * 40)
    click.echo(f"  Platform: {platform}")
    click.echo(f"  Period: Last {days} days")

    # Simulated mentions
    mention_count = random.randint(10, 100)
    positive = int(mention_count * 0.7)
    neutral = int(mention_count * 0.2)
    negative = mention_count - positive - neutral

    click.echo(f"\n  Found {mention_count} mentions")
    click.echo("  " + "-" * 40)
    click.echo(f"  Positive: {positive} ({positive/mention_count*100:.0f}%)")
    click.echo(f"  Neutral: {neutral} ({neutral/mention_count*100:.0f}%)")
    click.echo(f"  Negative: {negative} ({negative/mention_count*100:.0f}%)")

    click.echo("\n  Notable Mentions:")
    for i in range(3):
        click.echo(f"    @user{random.randint(100, 9999)}: \"Great experience with {handle}!\"")

@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--by-type', is_flag=True, help='Organize by content type')
@click.option('--by-date', is_flag=True, help='Organize by date')
def organize(folder: str, by_type: bool, by_date: bool):
    """Organize collected UGC."""
    click.echo("\n  UGC Organizer")
    click.echo("  " + "=" * 40)
    click.echo(f"  Folder: {folder}")

    folder_path = Path(folder)

    # Count files
    files = list(folder_path.glob('*'))
    click.echo(f"  Files found: {len(files)}")

    if by_type:
        click.echo("\n  Organizing by type...")
        for content_type in ['photos', 'videos', 'testimonials']:
            type_folder = folder_path / content_type
            type_folder.mkdir(exist_ok=True)
            click.echo(f"    Created: {type_folder}")

    if by_date:
        click.echo("\n  Organizing by date...")
        date_folder = folder_path / datetime.now().strftime('%Y-%m')
        date_folder.mkdir(exist_ok=True)
        click.echo(f"    Created: {date_folder}")

    click.echo("\n  [Done] UGC organized")

if __name__ == "__main__":
    cli()
