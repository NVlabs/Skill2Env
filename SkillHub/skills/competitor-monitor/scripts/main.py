#!/usr/bin/env python3
"""
Competitor Monitor - Track competitor websites for changes.

Usage:
    python main.py watch https://competitor.com/pricing
    python main.py diff https://competitor.com/pricing --baseline cache.html
    python main.py pricing https://competitor.com/pricing
    python main.py batch competitors.txt --output changes/
"""

import click
from pathlib import Path
from typing import Optional
import requests
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
import re
import json


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; CompetitorMonitor/1.0)'
}


def fetch_page(url: str, selector: Optional[str] = None) -> tuple:
    """Fetch page and optionally extract specific content."""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    if selector:
        elements = soup.select(selector)
        content = '\n'.join(el.get_text(strip=True) for el in elements)
    else:
        content = soup.get_text(separator='\n', strip=True)

    return response.text, content


def content_hash(content: str) -> str:
    """Generate hash of content for change detection."""
    return hashlib.md5(content.encode()).hexdigest()


def extract_prices(html: str) -> list:
    """Extract price patterns from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    # Common price patterns
    patterns = [
        r'\$\d+(?:,\d{3})*(?:\.\d{2})?(?:/mo(?:nth)?)?',  # $99/mo
        r'€\d+(?:,\d{3})*(?:\.\d{2})?(?:/mo(?:nth)?)?',   # €99/mo
        r'£\d+(?:,\d{3})*(?:\.\d{2})?(?:/mo(?:nth)?)?',   # £99/mo
    ]

    prices = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        prices.extend(matches)

    return list(set(prices))


def simple_diff(old_text: str, new_text: str) -> list:
    """Simple line-by-line diff."""
    old_lines = set(old_text.split('\n'))
    new_lines = set(new_text.split('\n'))

    removed = old_lines - new_lines
    added = new_lines - old_lines

    changes = []
    for line in removed:
        if line.strip():
            changes.append(('removed', line.strip()[:100]))
    for line in added:
        if line.strip():
            changes.append(('added', line.strip()[:100]))

    return changes


@click.group()
def cli():
    """Competitor Monitor - Track competitor website changes."""
    pass


@cli.command()
@click.argument('url')
@click.option('--selector', '-s', help='CSS selector to monitor')
@click.option('--save', type=click.Path(), help='Save snapshot to file')
def watch(url: str, selector: Optional[str], save: Optional[str]):
    """Watch a URL and capture snapshot."""
    click.echo("\n  Competitor Watch")
    click.echo("  " + "=" * 40)
    click.echo(f"  URL: {url}")
    if selector:
        click.echo(f"  Selector: {selector}")

    click.echo("  Fetching...")
    html, content = fetch_page(url, selector)

    hash_val = content_hash(content)
    word_count = len(content.split())

    click.echo("\n  Snapshot")
    click.echo("  " + "-" * 40)
    click.echo(f"  Hash: {hash_val[:12]}...")
    click.echo(f"  Words: {word_count}")
    click.echo(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Extract prices if found
    prices = extract_prices(html)
    if prices:
        click.echo("\n  Prices found:")
        for price in prices[:10]:
            click.echo(f"    • {price}")

    # Preview content
    click.echo("\n  Preview:")
    click.echo("  " + "-" * 40)
    preview = content[:500].replace('\n', '\n  ')
    click.echo(f"  {preview}...")

    # Save if requested
    if save:
        save_path = Path(save)
        save_path.write_text(html)

        # Also save metadata
        meta_path = save_path.with_suffix('.json')
        meta = {
            'url': url,
            'hash': hash_val,
            'timestamp': datetime.now().isoformat(),
            'prices': prices
        }
        meta_path.write_text(json.dumps(meta, indent=2))

        click.echo(f"\n  Saved: {save_path}")
        click.echo(f"  Meta: {meta_path}")


@cli.command()
@click.argument('url')
@click.option('--baseline', '-b', required=True, type=click.Path(exists=True),
              help='Baseline HTML file')
@click.option('--selector', '-s', help='CSS selector to compare')
def diff(url: str, baseline: str, selector: Optional[str]):
    """Compare current page with baseline."""
    click.echo("\n  Competitor Diff")
    click.echo("  " + "=" * 40)
    click.echo(f"  URL: {url}")
    click.echo(f"  Baseline: {baseline}")

    # Load baseline
    baseline_path = Path(baseline)
    baseline_html = baseline_path.read_text()
    baseline_soup = BeautifulSoup(baseline_html, 'html.parser')

    if selector:
        baseline_elements = baseline_soup.select(selector)
        baseline_text = '\n'.join(el.get_text(strip=True) for el in baseline_elements)
    else:
        baseline_text = baseline_soup.get_text(separator='\n', strip=True)

    # Fetch current
    click.echo("  Fetching current...")
    current_html, current_text = fetch_page(url, selector)

    # Compare hashes
    baseline_hash = content_hash(baseline_text)
    current_hash = content_hash(current_text)

    click.echo("\n  Comparison")
    click.echo("  " + "-" * 40)
    click.echo(f"  Baseline hash: {baseline_hash[:12]}...")
    click.echo(f"  Current hash:  {current_hash[:12]}...")

    if baseline_hash == current_hash:
        click.echo("\n  ✓ No changes detected")
        return

    click.echo("\n  ✗ CHANGES DETECTED")

    # Show diff
    changes = simple_diff(baseline_text, current_text)

    if changes:
        click.echo("\n  Changes:")
        click.echo("  " + "-" * 40)

        removed = [c for c in changes if c[0] == 'removed']
        added = [c for c in changes if c[0] == 'added']

        if removed:
            click.echo("\n  Removed:")
            for _, text in removed[:10]:
                click.echo(f"  - {text}")

        if added:
            click.echo("\n  Added:")
            for _, text in added[:10]:
                click.echo(f"  + {text}")

    # Compare prices
    baseline_prices = extract_prices(baseline_html)
    current_prices = extract_prices(current_html)

    if baseline_prices != current_prices:
        click.echo("\n  Price changes:")
        old_prices = set(baseline_prices)
        new_prices = set(current_prices)

        for p in old_prices - new_prices:
            click.echo(f"  - Removed: {p}")
        for p in new_prices - old_prices:
            click.echo(f"  + Added: {p}")


@cli.command()
@click.argument('url')
@click.option('--output', '-o', type=click.Path(), help='Save prices to file')
def pricing(url: str, output: Optional[str]):
    """Extract and monitor pricing information."""
    click.echo("\n  Pricing Monitor")
    click.echo("  " + "=" * 40)
    click.echo(f"  URL: {url}")

    click.echo("  Fetching...")
    html, _ = fetch_page(url)

    prices = extract_prices(html)

    click.echo(f"\n  Prices Found: {len(prices)}")
    click.echo("  " + "-" * 40)

    for price in prices:
        click.echo(f"  • {price}")

    # Try to find pricing context
    soup = BeautifulSoup(html, 'html.parser')
    pricing_sections = soup.find_all(class_=re.compile(r'pric', re.I))

    if pricing_sections:
        click.echo("\n  Pricing sections:")
        for section in pricing_sections[:3]:
            text = section.get_text(strip=True)[:200]
            click.echo(f"  • {text}")

    if output:
        data = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'prices': prices
        }
        Path(output).write_text(json.dumps(data, indent=2))
        click.echo(f"\n  Saved: {output}")


@cli.command()
@click.argument('urls_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), default='./snapshots',
              help='Output directory')
def batch(urls_file: str, output: str):
    """Batch monitor multiple URLs."""
    urls_path = Path(urls_file)
    urls = [line.strip() for line in urls_path.read_text().splitlines() if line.strip()]

    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')

    click.echo("\n  Batch Competitor Monitor")
    click.echo("  " + "=" * 40)
    click.echo(f"  URLs: {len(urls)}")
    click.echo(f"  Output: {output_dir}")

    results = []

    for url in urls:
        click.echo(f"\n  Fetching: {url[:50]}...")
        try:
            html, content = fetch_page(url)
            hash_val = content_hash(content)
            prices = extract_prices(html)

            # Create filename from URL
            url_slug = re.sub(r'[^a-z0-9]', '_', url.lower())[:50]
            snapshot_file = output_dir / f"{url_slug}_{timestamp}.html"
            snapshot_file.write_text(html)

            results.append({
                'url': url,
                'hash': hash_val,
                'prices': prices,
                'file': str(snapshot_file)
            })

            click.echo(f"  -> {snapshot_file.name} (hash: {hash_val[:8]})")

        except Exception as e:
            click.echo(f"  [Error] {e}")
            results.append({
                'url': url,
                'error': str(e)
            })

    # Save summary
    summary_file = output_dir / f"summary_{timestamp}.json"
    summary_file.write_text(json.dumps(results, indent=2))

    click.echo(f"\n  [Done] Monitored {len(urls)} URLs")
    click.echo(f"  Summary: {summary_file}")


if __name__ == "__main__":
    cli()
