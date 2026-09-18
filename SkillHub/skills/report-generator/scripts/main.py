#!/usr/bin/env python3
"""Report Generator - Create reports from templates and data."""

import click
from pathlib import Path
import json
import csv
from datetime import datetime

@click.group()
def cli():
    """Report Generator - Automated marketing reports."""
    pass

@cli.command()
@click.option('--data', '-d', type=click.Path(exists=True), help='Data file (JSON/CSV)')
@click.option('--title', '-t', default='Marketing Report', help='Report title')
@click.option('--output', '-o', default='report.html', help='Output file')
def generate(data: str, title: str, output: str):
    """Generate report from data."""
    click.echo("\n  Report Generator")
    click.echo("  " + "=" * 40)

    # Load data
    report_data = {}
    if data:
        data_path = Path(data)
        if data_path.suffix == '.json':
            report_data = json.loads(data_path.read_text())
        elif data_path.suffix == '.csv':
            with open(data_path, 'r') as f:
                reader = csv.DictReader(f)
                report_data['rows'] = list(reader)

    html = generate_report_html(title, report_data)
    Path(output).write_text(html)

    click.echo(f"  Title: {title}")
    click.echo(f"\n  [Done] Saved: {output}")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', default='weekly-report.html', help='Output file')
def weekly(file: str, output: str):
    """Generate weekly metrics report."""
    click.echo("\n  Weekly Report Generator")
    click.echo("  " + "=" * 40)

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Calculate metrics
    metrics = {}
    for row in data:
        for key, value in row.items():
            if key not in metrics:
                metrics[key] = []
            try:
                metrics[key].append(float(value))
            except (ValueError, TypeError):
                pass

    summaries = {k: {'total': sum(v), 'avg': sum(v)/len(v) if v else 0}
                 for k, v in metrics.items() if v}

    html = generate_weekly_html(summaries, data)
    Path(output).write_text(html)

    click.echo(f"\n  [Done] Saved: {output}")

def generate_report_html(title: str, data: dict) -> str:
    """Generate basic report HTML."""
    rows_html = ""
    if 'rows' in data:
        if data['rows']:
            headers = data['rows'][0].keys()
            rows_html = "<table><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>"
            for row in data['rows'][:50]:
                rows_html += "<tr>" + "".join(f"<td>{v}</td>" for v in row.values()) + "</tr>"
            rows_html += "</table>"

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f5f5f5; }}
        .meta {{ color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    {rows_html}
</body>
</html>"""

def generate_weekly_html(summaries: dict, data: list) -> str:
    """Generate weekly report HTML."""
    cards_html = ""
    for metric, stats in summaries.items():
        cards_html += f"""
        <div class="metric">
            <h3>{metric}</h3>
            <p class="value">{stats['total']:,.0f}</p>
            <p class="avg">Avg: {stats['avg']:,.1f}</p>
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Weekly Performance Report</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .metric {{ background: #f5f5f5; padding: 15px; border-radius: 8px; text-align: center; }}
        .metric h3 {{ margin: 0; font-size: 12px; color: #666; text-transform: uppercase; }}
        .metric .value {{ font-size: 28px; font-weight: bold; margin: 10px 0 5px; }}
        .metric .avg {{ margin: 0; color: #888; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>Weekly Performance Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <p>Data points: {len(data)}</p>

    <h2>Summary</h2>
    <div class="metrics">
        {cards_html}
    </div>
</body>
</html>"""

if __name__ == "__main__":
    cli()
