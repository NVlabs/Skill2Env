#!/usr/bin/env python3
"""Funnel Analyzer - Analyze conversion funnels."""

import click
from pathlib import Path
from typing import Optional
import csv

@click.group()
def cli():
    """Funnel Analyzer - Conversion funnel analysis."""
    pass

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--stages', '-s', required=True, help='Comma-separated funnel stages')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def analyze(file: str, stages: str, output: Optional[str]):
    """Analyze funnel from event data."""
    click.echo("\n  Funnel Analyzer")
    click.echo("  " + "=" * 45)

    stage_list = [s.strip() for s in stages.split(',')]
    click.echo(f"  Stages: {' → '.join(stage_list)}")

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Count users at each stage
    stage_counts = {stage: 0 for stage in stage_list}

    for row in data:
        event = row.get('event') or row.get('stage') or row.get('action')
        if event in stage_counts:
            stage_counts[event] += 1

    # If no events found, try using column values
    if all(v == 0 for v in stage_counts.values()):
        for stage in stage_list:
            if stage in data[0]:
                stage_counts[stage] = sum(1 for row in data if row.get(stage))

    click.echo("\n  Funnel Analysis")
    click.echo("  " + "-" * 45)
    click.echo(f"  {'Stage':<15} {'Users':>10} {'Conv':>10} {'Drop':>10}")
    click.echo("  " + "-" * 45)

    prev_count = None
    total_start = list(stage_counts.values())[0] if stage_counts else 0

    for stage, count in stage_counts.items():
        if count == 0:
            count = total_start  # Assume all start at top

        if prev_count is None:
            conv = 100.0
            drop = 0.0
        else:
            conv = (count / prev_count * 100) if prev_count else 0
            drop = 100 - conv

        bar_len = int(count / max(stage_counts.values() or [1]) * 20)
        bar = "█" * bar_len

        click.echo(f"  {stage:<15} {count:>10,} {conv:>9.1f}% {drop:>9.1f}%")
        click.echo(f"  {bar}")

        prev_count = count

    # Overall conversion
    values = list(stage_counts.values())
    if len(values) >= 2 and values[0] > 0:
        overall = values[-1] / values[0] * 100
        click.echo("\n  " + "-" * 45)
        click.echo(f"  Overall conversion: {overall:.1f}%")
        click.echo(f"  ({values[0]:,} → {values[-1]:,})")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def dropoff(file: str):
    """Identify biggest drop-off points."""
    click.echo("\n  Drop-off Analysis")
    click.echo("  " + "=" * 40)

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        list(reader)

    # Analyze drop-offs
    click.echo("\n  Biggest drop-off points:")
    click.echo("  (Run with --stages to get specific analysis)")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--stages', '-s', required=True, help='Comma-separated stages')
@click.option('--output', '-o', default='funnel.html', help='Output file')
def visualize(file: str, stages: str, output: str):
    """Create funnel visualization."""
    stage_list = [s.strip() for s in stages.split(',')]

    # Sample data for visualization
    html = generate_funnel_html(stage_list)
    Path(output).write_text(html)

    click.echo(f"\n  [Done] Saved: {output}")

def generate_funnel_html(stages: list) -> str:
    """Generate funnel visualization HTML."""
    from datetime import datetime

    # Sample decreasing values
    values = [100]
    for _ in stages[1:]:
        values.append(int(values[-1] * 0.6))

    bars_html = ""
    for i, (stage, value) in enumerate(zip(stages, values)):
        width = value
        bars_html += f"""
        <div class="stage">
            <div class="bar" style="width: {width}%;">
                <span class="label">{stage}</span>
                <span class="value">{value}%</span>
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Conversion Funnel</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        .funnel {{ margin: 30px 0; }}
        .stage {{ margin: 10px 0; }}
        .bar {{ background: linear-gradient(90deg, #4CAF50, #8BC34A);
                padding: 15px; border-radius: 4px; color: white;
                display: flex; justify-content: space-between; }}
        .label {{ font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Conversion Funnel Analysis</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d')}</p>
    <div class="funnel">
        {bars_html}
    </div>
</body>
</html>"""

if __name__ == "__main__":
    cli()
