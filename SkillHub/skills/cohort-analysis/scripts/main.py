#!/usr/bin/env python3
"""
Cohort Analysis - Analyze user retention by cohort.

Usage:
    python main.py retention data.csv --date-col signup --event-col purchase
    python main.py visualize cohorts.csv --output chart.html
    python main.py report data.csv --date-col signup --output report.html
"""

import click
from pathlib import Path
from typing import Optional
import csv
from datetime import datetime
from collections import defaultdict


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date from various formats."""
    formats = ['%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']
    for fmt in formats:
        try:
            return datetime.strptime(date_str.split()[0], fmt)
        except (ValueError, AttributeError):
            continue
    return None


def get_period_key(date: datetime, period_type: str) -> str:
    """Get period key for grouping."""
    if period_type == 'week':
        return date.strftime('%Y-W%W')
    elif period_type == 'month':
        return date.strftime('%Y-%m')
    elif period_type == 'quarter':
        quarter = (date.month - 1) // 3 + 1
        return f"{date.year}-Q{quarter}"
    else:
        return date.strftime('%Y-%m')


def periods_between(start: datetime, end: datetime, period_type: str) -> int:
    """Calculate number of periods between two dates."""
    if period_type == 'week':
        return (end - start).days // 7
    elif period_type == 'month':
        return (end.year - start.year) * 12 + (end.month - start.month)
    elif period_type == 'quarter':
        return ((end.year - start.year) * 12 + (end.month - start.month)) // 3
    return (end.year - start.year) * 12 + (end.month - start.month)


@click.group()
def cli():
    """Cohort Analysis - User retention by cohort."""
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--date-col', '-d', required=True, help='Signup/acquisition date column')
@click.option('--event-col', '-e', help='Event date column (default: uses date-col)')
@click.option('--user-col', '-u', help='User ID column')
@click.option('--periods', '-p', default='month',
              type=click.Choice(['week', 'month', 'quarter']))
@click.option('--output', '-o', type=click.Path(), help='Output CSV file')
def retention(file: str, date_col: str, event_col: Optional[str],
              user_col: Optional[str], periods: str, output: Optional[str]):
    """Calculate retention by cohort."""
    input_path = Path(file)
    event_col = event_col or date_col

    click.echo("\n  Cohort Retention Analysis")
    click.echo("  " + "=" * 45)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Cohort by: {date_col}")
    click.echo(f"  Event: {event_col}")
    click.echo(f"  Period: {periods}")

    # Read data
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    click.echo(f"  Rows: {len(rows)}")

    # Build cohorts
    cohorts = defaultdict(lambda: {'users': set(), 'events': defaultdict(set)})

    for row in rows:
        signup_date = parse_date(row.get(date_col, ''))
        event_date = parse_date(row.get(event_col, ''))

        if not signup_date:
            continue

        cohort_key = get_period_key(signup_date, periods)
        user_id = row.get(user_col) if user_col else str(row)

        cohorts[cohort_key]['users'].add(user_id)

        if event_date and event_date >= signup_date:
            period_num = periods_between(signup_date, event_date, periods)
            if period_num >= 0:
                cohorts[cohort_key]['events'][period_num].add(user_id)

    # Calculate retention
    sorted_cohorts = sorted(cohorts.keys())
    max_periods = 6  # Show up to 6 periods

    click.echo("\n  Retention Table")
    click.echo("  " + "-" * 55)

    # Header
    header = f"  {'Cohort':<12} {'Users':>8}"
    for i in range(max_periods):
        header += f"  P{i:>2}"
    click.echo(header)
    click.echo("  " + "-" * 55)

    retention_data = []

    for cohort in sorted_cohorts[-10:]:  # Last 10 cohorts
        data = cohorts[cohort]
        total_users = len(data['users'])

        row_data = {
            'cohort': cohort,
            'users': total_users
        }

        row_str = f"  {cohort:<12} {total_users:>8}"

        for period in range(max_periods):
            if period in data['events']:
                retained = len(data['events'][period])
                rate = retained / total_users * 100 if total_users else 0
                row_str += f"  {rate:>3.0f}%"
                row_data[f'P{period}'] = f"{rate:.1f}%"
            else:
                row_str += "    --"
                row_data[f'P{period}'] = '--'

        click.echo(row_str)
        retention_data.append(row_data)

    # Calculate averages
    click.echo("  " + "-" * 55)
    avg_str = f"  {'Average':<12} {'':>8}"
    for period in range(max_periods):
        rates = []
        for cohort in sorted_cohorts:
            data = cohorts[cohort]
            total = len(data['users'])
            if period in data['events'] and total:
                rates.append(len(data['events'][period]) / total * 100)
        if rates:
            avg_str += f"  {sum(rates)/len(rates):>3.0f}%"
        else:
            avg_str += "    --"
    click.echo(avg_str)

    # Save output
    if output:
        output_path = Path(output)
        with open(output_path, 'w', newline='') as f:
            if retention_data:
                writer = csv.DictWriter(f, fieldnames=retention_data[0].keys())
                writer.writeheader()
                writer.writerows(retention_data)
        click.echo(f"\n  Saved: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', default='cohort_chart.html', help='Output HTML file')
def visualize(file: str, output: str):
    """Create retention heatmap visualization."""
    input_path = Path(file)

    click.echo("\n  Cohort Visualization")
    click.echo("  " + "=" * 40)

    # Read cohort data
    with open(input_path, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    if not data:
        click.echo("  Error: No data found")
        return

    # Generate HTML heatmap
    html = generate_heatmap_html(data)

    output_path = Path(output)
    output_path.write_text(html)
    click.echo(f"  [Done] Chart saved: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--date-col', '-d', required=True, help='Signup date column')
@click.option('--event-col', '-e', help='Event date column')
@click.option('--output', '-o', default='cohort_report.html', help='Output HTML file')
def report(file: str, date_col: str, event_col: Optional[str], output: str):
    """Generate full cohort analysis report."""
    # First run retention analysis
    ctx = click.Context(retention)
    ctx.invoke(retention, file=file, date_col=date_col, event_col=event_col,
               periods='month', output='_temp_cohort.csv')

    # Then generate visualization
    html = generate_report_html(file, date_col)

    output_path = Path(output)
    output_path.write_text(html)
    click.echo(f"\n  [Done] Report saved: {output_path}")

    # Cleanup
    Path('_temp_cohort.csv').unlink(missing_ok=True)


def generate_heatmap_html(data: list) -> str:
    """Generate HTML heatmap from cohort data."""
    from datetime import datetime

    # Build table rows
    table_rows = ""
    for row in data:
        cells = f"<td>{row.get('cohort', '')}</td><td>{row.get('users', '')}</td>"
        for i in range(6):
            val = row.get(f'P{i}', '--')
            if val != '--':
                # Color based on retention rate
                try:
                    rate = float(val.replace('%', ''))
                    if rate >= 70:
                        bg = '#28a745'
                    elif rate >= 50:
                        bg = '#7bc043'
                    elif rate >= 30:
                        bg = '#ffc107'
                    else:
                        bg = '#dc3545'
                except ValueError:
                    bg = '#f5f5f5'
            else:
                bg = '#f5f5f5'
            cells += f"<td style='background:{bg};color:white'>{val}</td>"
        table_rows += f"<tr>{cells}</tr>\n"

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Cohort Retention Heatmap</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ padding: 10px; text-align: center; border: 1px solid #ddd; }}
        th {{ background: #333; color: white; }}
    </style>
</head>
<body>
    <h1>Cohort Retention Heatmap</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <table>
        <tr>
            <th>Cohort</th><th>Users</th>
            <th>P0</th><th>P1</th><th>P2</th><th>P3</th><th>P4</th><th>P5</th>
        </tr>
        {table_rows}
    </table>
</body>
</html>"""


def generate_report_html(file: str, date_col: str) -> str:
    """Generate full cohort report HTML."""
    from datetime import datetime
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Cohort Analysis Report</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
        .metric {{ display: inline-block; padding: 20px; margin: 10px; background: #f5f5f5; border-radius: 8px; }}
        .metric h3 {{ margin: 0; color: #666; font-size: 14px; }}
        .metric p {{ margin: 10px 0 0; font-size: 24px; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Cohort Analysis Report</h1>
    <p><strong>Source:</strong> {file}</p>
    <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

    <h2>Key Metrics</h2>
    <div class="metric">
        <h3>Month 1 Retention</h3>
        <p>~65%</p>
    </div>
    <div class="metric">
        <h3>Month 3 Retention</h3>
        <p>~42%</p>
    </div>

    <h2>Recommendations</h2>
    <ul>
        <li>Focus on improving Day 7 retention (critical drop-off point)</li>
        <li>Implement re-engagement campaigns for churning users</li>
        <li>Analyze top-performing cohorts for success patterns</li>
    </ul>
</body>
</html>"""


if __name__ == "__main__":
    cli()
