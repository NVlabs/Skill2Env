#!/usr/bin/env python3
"""Influencer Finder - Find and analyze influencers."""

import click
from typing import Optional
import random
import csv

def generate_influencer(niche: str, tier: str) -> dict:
    """Generate simulated influencer data."""
    tiers = {
        'nano': (1000, 10000),
        'micro': (10000, 100000),
        'mid': (100000, 500000),
        'macro': (500000, 1000000),
        'mega': (1000000, 10000000),
    }

    min_f, max_f = tiers.get(tier, (10000, 100000))
    followers = random.randint(min_f, max_f)

    # Higher engagement for smaller accounts
    if tier in ['nano', 'micro']:
        eng_rate = random.uniform(3, 8)
    elif tier == 'mid':
        eng_rate = random.uniform(2, 5)
    else:
        eng_rate = random.uniform(1, 3)

    names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Quinn', 'Avery']
    suffixes = ['_official', 'daily', 'hub', '_co', 'life', 'tips', 'pro', '']

    return {
        'handle': f"@{random.choice(names).lower()}{niche[:4]}{random.choice(suffixes)}",
        'followers': followers,
        'engagement': eng_rate,
        'tier': tier,
        'niche': niche,
        'avg_likes': int(followers * eng_rate / 100),
        'est_cpm': random.randint(10, 50) if tier in ['nano', 'micro'] else random.randint(30, 100),
    }

@click.group()
def cli():
    """Influencer Finder - Research influencer partnerships."""
    pass

@cli.command()
@click.argument('niche')
@click.option('--platform', '-p', default='instagram',
              type=click.Choice(['instagram', 'tiktok', 'youtube', 'twitter']))
@click.option('--tier', '-t', default='micro',
              type=click.Choice(['nano', 'micro', 'mid', 'macro', 'mega']))
@click.option('--count', '-c', default=10, help='Number of results')
@click.option('--output', '-o', type=click.Path(), help='Output CSV')
def search(niche: str, platform: str, tier: str, count: int, output: Optional[str]):
    """Search for influencers in a niche."""
    click.echo("\n  Influencer Search")
    click.echo("  " + "=" * 45)
    click.echo(f"  Niche: {niche}")
    click.echo(f"  Platform: {platform}")
    click.echo(f"  Tier: {tier}")

    influencers = []
    for _ in range(count):
        random.seed()  # Reset seed for variety
        influencers.append(generate_influencer(niche, tier))

    click.echo(f"\n  Found {len(influencers)} influencers")
    click.echo("  " + "-" * 45)
    click.echo(f"  {'Handle':<20} {'Followers':>12} {'Eng%':>8} {'CPM':>8}")
    click.echo("  " + "-" * 45)

    for inf in influencers:
        click.echo(f"  {inf['handle']:<20} {inf['followers']:>12,} {inf['engagement']:>7.1f}% ${inf['est_cpm']:>6}")

    if output:
        with open(output, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=influencers[0].keys())
            writer.writeheader()
            writer.writerows(influencers)
        click.echo(f"\n  Saved: {output}")

@cli.command()
@click.argument('handle')
@click.option('--platform', '-p', default='instagram')
def analyze(handle: str, platform: str):
    """Analyze an influencer profile."""
    click.echo(f"\n  Influencer Analysis: {handle}")
    click.echo("  " + "=" * 40)

    # Simulated analysis
    random.seed(hash(handle))
    followers = random.randint(10000, 500000)
    eng_rate = random.uniform(1.5, 6.0)

    click.echo("\n  Profile Metrics")
    click.echo("  " + "-" * 40)
    click.echo(f"  Followers: {followers:,}")
    click.echo(f"  Engagement Rate: {eng_rate:.2f}%")
    click.echo(f"  Avg Likes: {int(followers * eng_rate / 100):,}")
    click.echo(f"  Avg Comments: {int(followers * eng_rate / 100 * 0.1):,}")
    click.echo(f"  Posting Frequency: {random.randint(3, 14)} posts/week")

    # Assessment
    if eng_rate >= 3.5:
        assessment = "Excellent engagement - highly recommended"
    elif eng_rate >= 2.0:
        assessment = "Good engagement - worth considering"
    else:
        assessment = "Below average engagement - evaluate carefully"

    click.echo(f"\n  Assessment: {assessment}")

    # Estimated rates
    click.echo("\n  Estimated Rates")
    click.echo("  " + "-" * 40)
    click.echo(f"  Story mention: ${followers // 1000 * 5}-${followers // 1000 * 10}")
    click.echo(f"  Feed post: ${followers // 1000 * 20}-${followers // 1000 * 50}")
    click.echo(f"  Reel/Video: ${followers // 1000 * 50}-${followers // 1000 * 100}")

if __name__ == "__main__":
    cli()
