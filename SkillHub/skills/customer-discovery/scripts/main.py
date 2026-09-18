#!/usr/bin/env python3
"""
Customer Discovery Tracker - Steve Blank methodology.

Track interview progress, synthesize learnings, generate validation scorecards.

Usage:
    python main.py add-interview --type problem --notes "..."
    python main.py hypothesis --statement "..." --evidence 3
    python main.py scorecard
"""

import click
import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("customer_discovery.json")


def load_data() -> dict:
    """Load existing data or create new."""
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {
        "hypotheses": [],
        "interviews": [],
        "created": datetime.now().isoformat()
    }


def save_data(data: dict):
    """Save data to file."""
    data["updated"] = datetime.now().isoformat()
    DATA_FILE.write_text(json.dumps(data, indent=2))


@click.group()
def cli():
    """Customer Discovery Tracker - Steve Blank methodology."""
    pass


@cli.command('hypothesis')
@click.option('--statement', '-s', required=True, help='Hypothesis statement')
@click.option('--category', '-c', type=click.Choice(['customer', 'problem', 'solution', 'channel', 'revenue']),
              default='problem', help='Hypothesis category')
@click.option('--evidence', '-e', type=int, default=0, help='Supporting interviews (0-10)')
@click.option('--status', type=click.Choice(['testing', 'validated', 'invalidated']),
              default='testing', help='Validation status')
def hypothesis(statement: str, category: str, evidence: int, status: str):
    """Add or update a business hypothesis."""
    data = load_data()

    h = {
        "id": len(data["hypotheses"]) + 1,
        "statement": statement,
        "category": category,
        "evidence_count": evidence,
        "status": status,
        "created": datetime.now().isoformat()
    }
    data["hypotheses"].append(h)
    save_data(data)

    click.echo(f"\nHypothesis #{h['id']} added:")
    click.echo(f"  Category: {category}")
    click.echo(f"  Statement: {statement}")
    click.echo(f"  Status: {status} ({evidence} supporting interviews)")


@cli.command('add-interview')
@click.option('--type', '-t', 'interview_type',
              type=click.Choice(['problem', 'solution', 'usability']),
              required=True, help='Interview type')
@click.option('--segment', '-s', default='General', help='Customer segment')
@click.option('--notes', '-n', required=True, help='Key findings/notes')
@click.option('--pain-level', '-p', type=int, default=0, help='Pain intensity (1-10)')
def add_interview(interview_type: str, segment: str, notes: str, pain_level: int):
    """Log a customer interview."""
    data = load_data()

    interview = {
        "id": len(data["interviews"]) + 1,
        "type": interview_type,
        "segment": segment,
        "notes": notes,
        "pain_level": pain_level,
        "date": datetime.now().isoformat()
    }
    data["interviews"].append(interview)
    save_data(data)

    click.echo(f"\nInterview #{interview['id']} logged:")
    click.echo(f"  Type: {interview_type}")
    click.echo(f"  Segment: {segment}")
    click.echo(f"  Pain Level: {pain_level}/10")
    click.echo(f"  Notes: {notes[:100]}...")

    # Show progress
    count = len(data["interviews"])
    click.echo(f"\nTotal interviews: {count}")
    if count < 10:
        click.echo(f"  Recommendation: Continue to {10 - count} more for initial validation")


@cli.command('scorecard')
def scorecard():
    """Generate Customer Discovery validation scorecard."""
    data = load_data()

    interviews = data.get("interviews", [])
    hypotheses = data.get("hypotheses", [])

    click.echo("\n" + "=" * 50)
    click.echo("  CUSTOMER DISCOVERY SCORECARD")
    click.echo("=" * 50)

    # Interview summary
    click.echo("\n  Interview Summary")
    click.echo("  " + "-" * 45)
    total = len(interviews)
    by_type = {}
    for i in interviews:
        t = i.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    click.echo(f"  Total Interviews: {total}")
    for t, count in by_type.items():
        click.echo(f"    - {t}: {count}")

    # Pain levels
    if interviews:
        pains = [i.get("pain_level", 0) for i in interviews if i.get("pain_level")]
        if pains:
            avg_pain = sum(pains) / len(pains)
            click.echo(f"  Average Pain Level: {avg_pain:.1f}/10")
            if avg_pain >= 7:
                click.echo("    [STRONG] - Significant pain identified")
            elif avg_pain >= 5:
                click.echo("    [MODERATE] - Pain exists but may not be urgent")
            else:
                click.echo("    [WEAK] - Pain may not drive purchasing")

    # Hypothesis status
    if hypotheses:
        click.echo("\n  Hypothesis Status")
        click.echo("  " + "-" * 45)
        for h in hypotheses:
            status_marker = {"validated": "[+]", "invalidated": "[-]", "testing": "[?]"}
            marker = status_marker.get(h.get("status", "testing"), "[?]")
            click.echo(f"  {marker} {h.get('category', 'unknown').upper()}: {h.get('statement', '')[:50]}...")
            click.echo(f"      Evidence: {h.get('evidence_count', 0)} interviews")

    # Recommendations
    click.echo("\n  Recommendations")
    click.echo("  " + "-" * 45)

    if total < 10:
        click.echo(f"  - Need {10 - total} more interviews for initial validation")
    elif total < 20:
        click.echo("  - Good progress. Target 20+ for strong validation")
    else:
        click.echo("  - Strong interview base. Focus on synthesis")

    problem_interviews = by_type.get("problem", 0)
    solution_interviews = by_type.get("solution", 0)

    if problem_interviews < 10:
        click.echo("  - Focus on problem interviews before solution testing")
    elif solution_interviews < 5 and problem_interviews >= 10:
        click.echo("  - Ready to start solution interviews")


@cli.command('export')
@click.option('--format', '-f', 'fmt', type=click.Choice(['json', 'md']), default='md')
def export(fmt: str):
    """Export discovery data."""
    data = load_data()

    if fmt == 'json':
        click.echo(json.dumps(data, indent=2))
    else:
        click.echo("# Customer Discovery Report")
        click.echo(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d')}")
        click.echo(f"\n## Interviews ({len(data.get('interviews', []))} total)")
        for i in data.get("interviews", []):
            click.echo(f"\n### Interview #{i['id']} ({i.get('type', 'unknown')})")
            click.echo(f"- Segment: {i.get('segment', 'N/A')}")
            click.echo(f"- Pain: {i.get('pain_level', 'N/A')}/10")
            click.echo(f"- Notes: {i.get('notes', 'N/A')}")


if __name__ == "__main__":
    cli()
