#!/usr/bin/env python3
"""Data Visualizer - Create charts from marketing data."""

import click
from pathlib import Path
import csv
import json

@click.group()
def cli():
    """Data Visualizer - Marketing charts and dashboards."""
    pass

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--type', '-t', 'chart_type', default='bar',
              type=click.Choice(['bar', 'line', 'pie', 'scatter']))
@click.option('--x', '-x', required=True, help='X-axis column')
@click.option('--y', '-y', required=True, help='Y-axis column')
@click.option('--title', help='Chart title')
@click.option('--output', '-o', default='chart.html', help='Output file')
def chart(file: str, chart_type: str, x: str, y: str, title: str, output: str):
    """Create chart from CSV data."""
    click.echo("\n  Data Visualizer")
    click.echo("  " + "=" * 40)
    click.echo(f"  Data: {file}")
    click.echo(f"  Type: {chart_type}")
    click.echo(f"  X: {x}, Y: {y}")

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    x_data = [row.get(x, '') for row in data]
    y_data = [float(row.get(y, 0)) for row in data]

    chart_title = title or f"{y} by {x}"

    # Generate simple HTML chart using Chart.js
    html = generate_chartjs_html(chart_type, x_data, y_data, chart_title)

    Path(output).write_text(html)
    click.echo(f"\n  [Done] Saved: {output}")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--metrics', '-m', required=True, help='Comma-separated metrics')
@click.option('--output', '-o', default='dashboard.html', help='Output file')
def dashboard(file: str, metrics: str, output: str):
    """Create dashboard with multiple metrics."""
    click.echo("\n  Dashboard Generator")
    click.echo("  " + "=" * 40)

    metric_list = [m.strip() for m in metrics.split(',')]

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    html = generate_dashboard_html(data, metric_list)
    Path(output).write_text(html)

    click.echo(f"  Metrics: {', '.join(metric_list)}")
    click.echo(f"\n  [Done] Saved: {output}")

def generate_chartjs_html(chart_type: str, labels: list, values: list, title: str) -> str:
    """Generate HTML with Chart.js."""
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': title,
            'data': values,
            'backgroundColor': 'rgba(54, 162, 235, 0.5)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1
        }]
    }

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
        canvas {{ max-height: 500px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <canvas id="chart"></canvas>
    <script>
        new Chart(document.getElementById('chart'), {{
            type: '{chart_type}',
            data: {json.dumps(chart_data)},
            options: {{ responsive: true }}
        }});
    </script>
</body>
</html>"""

def generate_dashboard_html(data: list, metrics: list) -> str:
    """Generate dashboard HTML."""
    from datetime import datetime

    # Calculate totals/averages
    summaries = {}
    for metric in metrics:
        values = [float(row.get(metric, 0)) for row in data if row.get(metric)]
        if values:
            summaries[metric] = {
                'total': sum(values),
                'avg': sum(values) / len(values),
                'count': len(values)
            }

    cards_html = ""
    for metric, stats in summaries.items():
        cards_html += f"""
        <div class="card">
            <h3>{metric}</h3>
            <p class="value">{stats['total']:,.0f}</p>
            <p class="sub">Avg: {stats['avg']:,.1f}</p>
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Marketing Dashboard</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 1200px; margin: 40px auto; padding: 20px; }}
        .dashboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .card {{ background: #f5f5f5; padding: 20px; border-radius: 8px; text-align: center; }}
        .card h3 {{ margin: 0; color: #666; font-size: 14px; text-transform: uppercase; }}
        .card .value {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
        .card .sub {{ color: #888; margin: 0; }}
    </style>
</head>
<body>
    <h1>Marketing Dashboard</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <div class="dashboard">
        {cards_html}
    </div>
</body>
</html>"""

if __name__ == "__main__":
    cli()
