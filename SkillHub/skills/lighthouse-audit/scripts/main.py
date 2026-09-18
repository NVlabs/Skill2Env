#!/usr/bin/env python3
"""
Lighthouse Audit - Automated Core Web Vitals and SEO audits.

Usage:
    python main.py audit https://example.com --categories performance,seo
    python main.py batch urls.txt --output results/
    python main.py compare https://example.com --baseline scores.json
"""

import click
from pathlib import Path
from typing import Optional
import subprocess
import json
from datetime import datetime
import csv


def check_lighthouse():
    """Check if lighthouse CLI is installed."""
    try:
        result = subprocess.run(['lighthouse', '--version'],
                                capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def run_lighthouse(url: str, categories: list, output_path: Optional[Path] = None) -> dict:
    """Run lighthouse audit on URL."""
    cmd = [
        'lighthouse', url,
        '--output=json',
        '--quiet',
        '--chrome-flags="--headless"'
    ]

    if categories:
        cmd.append(f'--only-categories={",".join(categories)}')

    if output_path:
        cmd.append(f'--output-path={output_path}')

    result = subprocess.run(cmd, capture_output=True, text=True)

    if output_path and output_path.exists():
        return json.loads(output_path.read_text())
    else:
        # Parse from stdout if no output file
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {}


def extract_scores(report: dict) -> dict:
    """Extract key scores from lighthouse report."""
    categories = report.get('categories', {})
    audits = report.get('audits', {})

    scores = {
        'performance': int(categories.get('performance', {}).get('score', 0) * 100),
        'seo': int(categories.get('seo', {}).get('score', 0) * 100),
        'accessibility': int(categories.get('accessibility', {}).get('score', 0) * 100),
        'best_practices': int(categories.get('best-practices', {}).get('score', 0) * 100),
    }

    # Core Web Vitals
    if 'largest-contentful-paint' in audits:
        scores['lcp'] = audits['largest-contentful-paint'].get('numericValue', 0) / 1000
    if 'total-blocking-time' in audits:
        scores['tbt'] = audits['total-blocking-time'].get('numericValue', 0)
    if 'cumulative-layout-shift' in audits:
        scores['cls'] = audits['cumulative-layout-shift'].get('numericValue', 0)
    if 'speed-index' in audits:
        scores['speed_index'] = audits['speed-index'].get('numericValue', 0) / 1000

    return scores


def score_indicator(score: int) -> str:
    """Get color indicator for score."""
    if score >= 90:
        return "✓"
    elif score >= 50:
        return "~"
    else:
        return "✗"


CATEGORIES = ['performance', 'seo', 'accessibility', 'best-practices', 'pwa']


@click.group()
def cli():
    """Lighthouse Audit - Core Web Vitals and SEO automation."""
    if not check_lighthouse():
        click.echo("Warning: lighthouse CLI not found")
        click.echo("Install with: npm install -g lighthouse")
        click.echo("Or results will be simulated for demo")


@cli.command()
@click.argument('url')
@click.option('--categories', '-c', default='performance,seo',
              help='Comma-separated categories')
@click.option('--format', '-f', 'output_format', default='json',
              type=click.Choice(['json', 'csv', 'html', 'md']))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def audit(url: str, categories: str, output_format: str, output: Optional[str]):
    """Run Lighthouse audit on a single URL."""
    category_list = [c.strip() for c in categories.split(',')]

    click.echo("\n  Lighthouse Audit")
    click.echo("  " + "=" * 40)
    click.echo(f"  URL: {url}")
    click.echo(f"  Categories: {', '.join(category_list)}")

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        url_slug = url.replace('https://', '').replace('http://', '').replace('/', '_')[:50]
        output_path = Path(f"lighthouse_{url_slug}.{output_format}")

    click.echo("  Running audit...")

    if check_lighthouse():
        # Real lighthouse run
        json_output = output_path.with_suffix('.json')
        report = run_lighthouse(url, category_list, json_output)
    else:
        # Simulated results for demo
        report = simulate_lighthouse(url, category_list)

    scores = extract_scores(report)

    # Display results
    click.echo("\n  Results")
    click.echo("  " + "-" * 40)

    if 'performance' in category_list:
        click.echo(f"  Performance:     {scores.get('performance', 0):>3} {score_indicator(scores.get('performance', 0))}")
    if 'seo' in category_list:
        click.echo(f"  SEO:             {scores.get('seo', 0):>3} {score_indicator(scores.get('seo', 0))}")
    if 'accessibility' in category_list:
        click.echo(f"  Accessibility:   {scores.get('accessibility', 0):>3} {score_indicator(scores.get('accessibility', 0))}")
    if 'best-practices' in category_list:
        click.echo(f"  Best Practices:  {scores.get('best_practices', 0):>3} {score_indicator(scores.get('best_practices', 0))}")

    if 'lcp' in scores:
        click.echo("\n  Core Web Vitals")
        click.echo(f"  LCP:  {scores['lcp']:.2f}s {'✓' if scores['lcp'] <= 2.5 else '✗'}")
    if 'cls' in scores:
        click.echo(f"  CLS:  {scores['cls']:.3f} {'✓' if scores['cls'] <= 0.1 else '✗'}")
    if 'tbt' in scores:
        click.echo(f"  TBT:  {scores['tbt']:.0f}ms")

    # Write output
    if output_format == 'json':
        output_path.write_text(json.dumps(report, indent=2))
    elif output_format == 'csv':
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['url'] + list(scores.keys()))
            writer.writeheader()
            writer.writerow({'url': url, **scores})
    elif output_format == 'md':
        md_content = generate_markdown_report(url, scores, report)
        output_path.write_text(md_content)

    click.echo("\n  " + "-" * 40)
    click.echo("  [Done] Audit complete")
    click.echo(f"  Output: {output_path}")


@cli.command()
@click.argument('urls_file', type=click.Path(exists=True))
@click.option('--categories', '-c', default='performance,seo')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def batch(urls_file: str, categories: str, output: Optional[str]):
    """Batch audit multiple URLs from file."""
    urls_path = Path(urls_file)
    urls = [line.strip() for line in urls_path.read_text().splitlines() if line.strip()]

    category_list = [c.strip() for c in categories.split(',')]

    # Create output directory
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    output_dir = Path(output) if output else Path(f"audit_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    click.echo("\n  Batch Lighthouse Audit")
    click.echo("  " + "=" * 40)
    click.echo(f"  URLs: {len(urls)}")
    click.echo(f"  Categories: {', '.join(category_list)}")
    click.echo(f"  Output: {output_dir}")

    results = []

    for i, url in enumerate(urls, 1):
        click.echo(f"\n  [{i}/{len(urls)}] {url}")

        if check_lighthouse():
            url_slug = url.replace('https://', '').replace('http://', '').replace('/', '_')[:50]
            json_output = output_dir / f"{url_slug}.json"
            report = run_lighthouse(url, category_list, json_output)
        else:
            report = simulate_lighthouse(url, category_list)

        scores = extract_scores(report)
        scores['url'] = url
        results.append(scores)

        perf = scores.get('performance', 0)
        click.echo(f"    Performance: {perf} {score_indicator(perf)}")

    # Write summary CSV
    summary_path = output_dir / 'summary.csv'
    with open(summary_path, 'w', newline='') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Audited {len(urls)} URLs")
    click.echo(f"  Summary: {summary_path}")


@cli.command()
@click.argument('url')
@click.option('--baseline', '-b', type=click.Path(exists=True), required=True,
              help='Baseline JSON file')
def compare(url: str, baseline: str):
    """Compare current audit with baseline."""
    baseline_path = Path(baseline)
    baseline_report = json.loads(baseline_path.read_text())
    baseline_scores = extract_scores(baseline_report)

    click.echo("\n  Lighthouse Comparison")
    click.echo("  " + "=" * 40)
    click.echo(f"  URL: {url}")
    click.echo(f"  Baseline: {baseline_path.name}")

    click.echo("  Running current audit...")

    if check_lighthouse():
        current_report = run_lighthouse(url, CATEGORIES[:4], None)
    else:
        current_report = simulate_lighthouse(url, CATEGORIES[:4])

    current_scores = extract_scores(current_report)

    click.echo("\n  Comparison Results")
    click.echo("  " + "-" * 40)
    click.echo(f"  {'Metric':<15} {'Before':>8} {'After':>8} {'Change':>10}")
    click.echo("  " + "-" * 40)

    for key in ['performance', 'seo', 'accessibility', 'best_practices']:
        before = baseline_scores.get(key, 0)
        after = current_scores.get(key, 0)
        change = after - before
        indicator = "✓" if change > 0 else ("✗" if change < 0 else "=")
        click.echo(f"  {key:<15} {before:>8} {after:>8} {change:>+9} {indicator}")

    # Core Web Vitals comparison
    if 'lcp' in baseline_scores and 'lcp' in current_scores:
        click.echo("\n  Core Web Vitals")
        for metric, unit in [('lcp', 's'), ('cls', ''), ('tbt', 'ms')]:
            if metric in baseline_scores and metric in current_scores:
                before = baseline_scores[metric]
                after = current_scores[metric]
                pct_change = ((after - before) / before * 100) if before else 0
                indicator = "✓" if pct_change < 0 else "✗"
                click.echo(f"  {metric.upper():<6} {before:>8.2f}{unit} {after:>8.2f}{unit} {pct_change:>+8.0f}% {indicator}")


def simulate_lighthouse(url: str, categories: list) -> dict:
    """Simulate lighthouse results for demo when CLI not available."""
    import random
    random.seed(hash(url))

    return {
        'categories': {
            'performance': {'score': random.uniform(0.5, 0.95)},
            'seo': {'score': random.uniform(0.7, 0.98)},
            'accessibility': {'score': random.uniform(0.6, 0.95)},
            'best-practices': {'score': random.uniform(0.7, 0.95)},
        },
        'audits': {
            'largest-contentful-paint': {'numericValue': random.uniform(1500, 4000)},
            'total-blocking-time': {'numericValue': random.uniform(50, 300)},
            'cumulative-layout-shift': {'numericValue': random.uniform(0.01, 0.3)},
            'speed-index': {'numericValue': random.uniform(2000, 5000)},
        }
    }


def generate_markdown_report(url: str, scores: dict, report: dict) -> str:
    """Generate markdown report."""
    return f"""# Lighthouse Audit Report

**URL:** {url}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Scores

| Category | Score |
|----------|-------|
| Performance | {scores.get('performance', 0)} |
| SEO | {scores.get('seo', 0)} |
| Accessibility | {scores.get('accessibility', 0)} |
| Best Practices | {scores.get('best_practices', 0)} |

## Core Web Vitals

| Metric | Value | Status |
|--------|-------|--------|
| LCP | {scores.get('lcp', 0):.2f}s | {'Good' if scores.get('lcp', 999) <= 2.5 else 'Needs Work'} |
| CLS | {scores.get('cls', 0):.3f} | {'Good' if scores.get('cls', 999) <= 0.1 else 'Needs Work'} |
| TBT | {scores.get('tbt', 0):.0f}ms | - |

## Recommendations

Based on the audit results, prioritize:

1. {'Optimize images and reduce LCP' if scores.get('lcp', 0) > 2.5 else 'LCP is good'}
2. {'Fix layout shifts to reduce CLS' if scores.get('cls', 0) > 0.1 else 'CLS is good'}
3. {'Review blocking JavaScript' if scores.get('tbt', 0) > 200 else 'TBT is acceptable'}
"""


if __name__ == "__main__":
    cli()
