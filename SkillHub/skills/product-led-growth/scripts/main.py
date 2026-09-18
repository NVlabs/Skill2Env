#!/usr/bin/env python3
"""
Product-Led Growth Metrics - PQL scoring & activation analysis.

Calculate product-qualified lead scores and track activation metrics.

Usage:
    python main.py pql-score --logins 15 --features 5 --time 45 --invites 2
    python main.py activation --signups 1000 --activated 320 --benchmark 0.3
    python main.py churn-risk --days-inactive 14 --feature-depth 2
"""

import click


@click.group()
def cli():
    """Product-Led Growth Metrics Calculator."""
    pass


@cli.command('pql-score')
@click.option('--logins', '-l', type=int, required=True, help='Login count in period')
@click.option('--features', '-f', type=int, required=True, help='Features used')
@click.option('--time', '-t', type=int, required=True, help='Time in product (minutes)')
@click.option('--invites', '-i', type=int, default=0, help='Team invites sent')
@click.option('--integrations', type=int, default=0, help='Integrations connected')
def pql_score(logins: int, features: int, time: int, invites: int, integrations: int):
    """Calculate Product-Qualified Lead score.

    PQL Score components:
    - Login frequency (25%)
    - Feature breadth (25%)
    - Time engagement (25%)
    - Collaboration signals (25%)
    """
    # Normalize scores (0-100 scale for each)
    login_score = min(logins / 20 * 100, 100)  # 20+ logins = max
    feature_score = min(features / 10 * 100, 100)  # 10+ features = max
    time_score = min(time / 120 * 100, 100)  # 120+ min = max
    collab_score = min((invites + integrations * 2) / 5 * 100, 100)  # 5 points = max

    # Weighted average
    total_score = (login_score * 0.25 +
                   feature_score * 0.25 +
                   time_score * 0.25 +
                   collab_score * 0.25)

    click.echo("\n  Product-Qualified Lead Score")
    click.echo("  " + "=" * 45)

    click.echo("\n  Input Metrics")
    click.echo("  " + "-" * 45)
    click.echo(f"  Logins:         {logins}")
    click.echo(f"  Features Used:  {features}")
    click.echo(f"  Time (min):     {time}")
    click.echo(f"  Invites:        {invites}")
    click.echo(f"  Integrations:   {integrations}")

    click.echo("\n  Score Breakdown")
    click.echo("  " + "-" * 45)
    click.echo(f"  Login Score:    {login_score:.0f}/100 (25%)")
    click.echo(f"  Feature Score:  {feature_score:.0f}/100 (25%)")
    click.echo(f"  Time Score:     {time_score:.0f}/100 (25%)")
    click.echo(f"  Collab Score:   {collab_score:.0f}/100 (25%)")

    click.echo("\n  " + "-" * 45)
    click.echo(f"  PQL SCORE:      {total_score:.0f}/100")

    if total_score >= 70:
        click.echo("\n  Classification: HIGH INTENT")
        click.echo("  Recommendation: Prioritize for sales outreach")
    elif total_score >= 40:
        click.echo("\n  Classification: MEDIUM INTENT")
        click.echo("  Recommendation: Nurture with targeted content")
    else:
        click.echo("\n  Classification: LOW INTENT")
        click.echo("  Recommendation: Focus on product education")


@cli.command('activation')
@click.option('--signups', '-s', type=int, required=True, help='Total signups')
@click.option('--activated', '-a', type=int, required=True, help='Users who activated')
@click.option('--benchmark', '-b', type=float, default=0.3, help='Target activation rate')
def activation(signups: int, activated: int, benchmark: float):
    """Calculate activation rate and compare to benchmark."""
    rate = activated / signups * 100 if signups > 0 else 0

    click.echo("\n  Activation Analysis")
    click.echo("  " + "=" * 40)

    click.echo("\n  Metrics")
    click.echo("  " + "-" * 40)
    click.echo(f"  Total Signups:      {signups:,}")
    click.echo(f"  Activated Users:    {activated:,}")
    click.echo(f"  Activation Rate:    {rate:.1f}%")
    click.echo(f"  Benchmark:          {benchmark * 100:.0f}%")

    gap = rate - (benchmark * 100)
    click.echo("\n  Analysis")
    click.echo("  " + "-" * 40)

    if gap >= 0:
        click.echo(f"  [+] Above benchmark by {gap:.1f}pp")
    else:
        click.echo(f"  [-] Below benchmark by {abs(gap):.1f}pp")
        click.echo(f"      Need {int(abs(gap) / 100 * signups)} more activations")

    # Activation rate benchmarks
    click.echo("\n  Industry Benchmarks")
    click.echo("  B2B SaaS:     20-30%")
    click.echo("  Consumer:     40-60%")
    click.echo("  Freemium:     2-5% to paid")


@cli.command('churn-risk')
@click.option('--days-inactive', '-d', type=int, required=True, help='Days since last login')
@click.option('--feature-depth', '-f', type=int, required=True, help='Features used (1-10)')
@click.option('--support-tickets', '-s', type=int, default=0, help='Recent support tickets')
def churn_risk(days_inactive: int, feature_depth: int, support_tickets: int):
    """Calculate churn risk score for a user."""
    # Risk factors (higher = more risk)
    inactivity_risk = min(days_inactive / 30 * 100, 100)  # 30+ days = max risk
    depth_risk = max(0, (10 - feature_depth) / 10 * 100)  # Low depth = high risk
    support_risk = min(support_tickets * 15, 45)  # Tickets add risk

    total_risk = (inactivity_risk * 0.5 +
                  depth_risk * 0.3 +
                  support_risk * 0.2)

    click.echo("\n  Churn Risk Assessment")
    click.echo("  " + "=" * 40)

    click.echo("\n  Risk Factors")
    click.echo("  " + "-" * 40)
    click.echo(f"  Days Inactive:    {days_inactive} days ({inactivity_risk:.0f}% risk)")
    click.echo(f"  Feature Depth:    {feature_depth}/10 ({depth_risk:.0f}% risk)")
    click.echo(f"  Support Tickets:  {support_tickets} ({support_risk:.0f}% risk)")

    click.echo("\n  " + "-" * 40)
    click.echo(f"  CHURN RISK:       {total_risk:.0f}%")

    if total_risk >= 70:
        click.echo("\n  Status: HIGH RISK")
        click.echo("  Action: Immediate intervention required")
        click.echo("  - Personal outreach from CSM")
        click.echo("  - Offer training/onboarding session")
    elif total_risk >= 40:
        click.echo("\n  Status: MEDIUM RISK")
        click.echo("  Action: Proactive engagement")
        click.echo("  - Automated re-engagement email")
        click.echo("  - Feature discovery nudges")
    else:
        click.echo("\n  Status: LOW RISK")
        click.echo("  Action: Monitor and nurture")


if __name__ == "__main__":
    cli()
