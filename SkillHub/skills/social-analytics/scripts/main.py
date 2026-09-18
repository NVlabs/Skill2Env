#!/usr/bin/env python3
"""
Social Analytics - Analyze social media profiles and engagement.

Usage:
    python main.py analyze @profile --platform twitter
    python main.py engagement @profile --platform twitter --days 30
    python main.py top-posts @profile --platform twitter --count 10
    python main.py compare @brand1 @brand2 --platform twitter
"""

import click
from typing import Optional
import json
from datetime import datetime
import csv
from pathlib import Path


# Simulated data for demo (in production, use APIs)
def get_profile_data(handle: str, platform: str) -> dict:
    """Get profile data (simulated for demo)."""
    import random
    random.seed(hash(handle + platform))

    followers = random.randint(5000, 500000)

    return {
        'handle': handle,
        'platform': platform,
        'followers': followers,
        'following': random.randint(100, 5000),
        'posts': random.randint(500, 10000),
        'avg_likes': random.randint(50, int(followers * 0.05)),
        'avg_comments': random.randint(5, int(followers * 0.01)),
        'avg_shares': random.randint(10, int(followers * 0.02)),
        'engagement_rate': random.uniform(0.5, 5.0),
        'posts_per_day': random.uniform(0.5, 5.0),
        'top_hashtags': random.sample([
            '#marketing', '#growth', '#startup', '#tech', '#business',
            '#entrepreneur', '#success', '#mindset', '#leadership', '#innovation'
        ], 5)
    }


def get_posts_data(handle: str, platform: str, count: int = 50) -> list:
    """Get recent posts data (simulated for demo)."""
    import random
    random.seed(hash(handle + platform))

    posts = []
    post_types = ['single', 'thread', 'image', 'video', 'poll']
    times = ['Monday 9am', 'Tuesday 8am', 'Wednesday 12pm', 'Thursday 6pm', 'Friday 10am']

    for i in range(count):
        followers = random.randint(5000, 500000)
        likes = random.randint(10, int(followers * 0.1))
        comments = random.randint(1, int(likes * 0.1))
        shares = random.randint(1, int(likes * 0.3))

        posts.append({
            'id': f'post_{i}',
            'text': f'Sample post content {i}...',
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'engagement': (likes + comments + shares) / followers * 100,
            'type': random.choice(post_types),
            'time': random.choice(times),
            'date': f'2024-01-{random.randint(1, 28):02d}'
        })

    return sorted(posts, key=lambda x: x['engagement'], reverse=True)


def format_number(n: int) -> str:
    """Format number with K/M suffix."""
    if n >= 1000000:
        return f"{n/1000000:.1f}M"
    elif n >= 1000:
        return f"{n/1000:.1f}K"
    return str(n)


@click.group()
def cli():
    """Social Analytics - Profile and engagement analysis."""
    pass


@cli.command()
@click.argument('handle')
@click.option('--platform', '-p', required=True,
              type=click.Choice(['twitter', 'instagram', 'linkedin', 'tiktok']))
def analyze(handle: str, platform: str):
    """Analyze a social media profile."""
    handle = handle.lstrip('@')

    click.echo(f"\n  Profile Analysis: @{handle}")
    click.echo("  " + "=" * 40)

    data = get_profile_data(handle, platform)

    click.echo(f"  Platform:       {platform.title()}")
    click.echo(f"  Followers:      {format_number(data['followers'])}")
    click.echo(f"  Following:      {format_number(data['following'])}")
    click.echo(f"  Total Posts:    {format_number(data['posts'])}")
    click.echo(f"  Avg Likes:      {format_number(data['avg_likes'])}")
    click.echo(f"  Avg Comments:   {format_number(data['avg_comments'])}")
    click.echo(f"  Avg Shares:     {format_number(data['avg_shares'])}")
    click.echo(f"  Engagement:     {data['engagement_rate']:.1f}%")
    click.echo(f"  Post Frequency: {data['posts_per_day']:.1f}/day")
    click.echo(f"  Top Hashtags:   {', '.join(data['top_hashtags'][:5])}")

    # Engagement assessment
    if data['engagement_rate'] > 3:
        assessment = "Excellent"
    elif data['engagement_rate'] > 1.5:
        assessment = "Good"
    elif data['engagement_rate'] > 0.5:
        assessment = "Average"
    else:
        assessment = "Below Average"

    click.echo("\n  " + "-" * 40)
    click.echo(f"  Assessment: {assessment} engagement for {platform}")


@cli.command()
@click.argument('handle')
@click.option('--platform', '-p', required=True,
              type=click.Choice(['twitter', 'instagram', 'linkedin', 'tiktok']))
@click.option('--days', '-d', default=30, help='Days to analyze')
@click.option('--posts', '-n', default=50, help='Number of posts to analyze')
def engagement(handle: str, platform: str, days: int, posts: int):
    """Calculate engagement metrics."""
    handle = handle.lstrip('@')

    click.echo(f"\n  Engagement Analysis: @{handle}")
    click.echo("  " + "=" * 40)
    click.echo(f"  Period: Last {days} days ({posts} posts)")

    data = get_profile_data(handle, platform)
    posts_data = get_posts_data(handle, platform, posts)

    # Calculate metrics
    total_likes = sum(p['likes'] for p in posts_data)
    total_comments = sum(p['comments'] for p in posts_data)
    total_shares = sum(p['shares'] for p in posts_data)
    total_engagement = total_likes + total_comments + total_shares

    eng_rate = (total_engagement / posts) / data['followers'] * 100
    amplification = (total_shares / posts) / data['followers'] * 100
    conversation = (total_comments / posts) / data['followers'] * 100
    applause = (total_likes / posts) / data['followers'] * 100

    click.echo("\n  Engagement Metrics")
    click.echo("  " + "-" * 40)
    click.echo(f"  Overall Engagement:  {eng_rate:.2f}%")
    click.echo(f"  Amplification Rate:  {amplification:.3f}%")
    click.echo(f"  Conversation Rate:   {conversation:.3f}%")
    click.echo(f"  Applause Rate:       {applause:.2f}%")

    click.echo("\n  Averages per Post")
    click.echo("  " + "-" * 40)
    click.echo(f"  Likes:    {total_likes // posts:,}")
    click.echo(f"  Comments: {total_comments // posts:,}")
    click.echo(f"  Shares:   {total_shares // posts:,}")


@cli.command('top-posts')
@click.argument('handle')
@click.option('--platform', '-p', required=True,
              type=click.Choice(['twitter', 'instagram', 'linkedin', 'tiktok']))
@click.option('--count', '-c', default=10, help='Number of posts')
@click.option('--metric', '-m', default='engagement',
              type=click.Choice(['engagement', 'likes', 'comments', 'shares']))
def top_posts(handle: str, platform: str, count: int, metric: str):
    """Find top performing posts."""
    handle = handle.lstrip('@')

    click.echo(f"\n  Top {count} Posts: @{handle}")
    click.echo("  " + "=" * 40)
    click.echo(f"  Sorted by: {metric}")

    posts_data = get_posts_data(handle, platform, 100)

    # Sort by metric
    posts_data.sort(key=lambda x: x[metric], reverse=True)
    top = posts_data[:count]

    for i, post in enumerate(top, 1):
        click.echo(f"\n  {i}. \"{post['text'][:50]}...\"")
        click.echo(f"     Likes: {post['likes']:,}  Comments: {post['comments']}  Shares: {post['shares']}")
        click.echo(f"     Eng: {post['engagement']:.1f}%  Type: {post['type']}  Time: {post['time']}")


@cli.command()
@click.argument('handles', nargs=-1, required=True)
@click.option('--platform', '-p', required=True,
              type=click.Choice(['twitter', 'instagram', 'linkedin', 'tiktok']))
def compare(handles: tuple, platform: str):
    """Compare multiple profiles."""
    handles = [h.lstrip('@') for h in handles]

    click.echo("\n  Profile Comparison")
    click.echo("  " + "=" * 50)

    # Header
    click.echo(f"  {'Profile':<15} {'Followers':>12} {'Eng.Rate':>10} {'Posts/Day':>10}")
    click.echo("  " + "-" * 50)

    profiles = []
    for handle in handles:
        data = get_profile_data(handle, platform)
        profiles.append(data)
        click.echo(f"  @{handle:<14} {format_number(data['followers']):>12} "
                   f"{data['engagement_rate']:>9.1f}% {data['posts_per_day']:>9.1f}")

    # Find winner
    best = max(profiles, key=lambda x: x['engagement_rate'])
    click.echo("\n  " + "-" * 50)
    click.echo(f"  Winner: @{best['handle']} (highest engagement rate)")


@cli.command()
@click.argument('handle')
@click.option('--platform', '-p', required=True,
              type=click.Choice(['twitter', 'instagram', 'linkedin', 'tiktok']))
@click.option('--format', '-f', 'output_format', default='csv',
              type=click.Choice(['csv', 'json', 'md']))
@click.option('--output', '-o', type=click.Path(), help='Output file')
def export(handle: str, platform: str, output_format: str, output: Optional[str]):
    """Export profile data."""
    handle = handle.lstrip('@')

    click.echo(f"\n  Exporting: @{handle}")
    click.echo("  " + "=" * 40)

    data = get_profile_data(handle, platform)
    posts = get_posts_data(handle, platform, 100)

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = Path(f"{handle}_{platform}_export.{output_format}")

    if output_format == 'json':
        export_data = {
            'profile': data,
            'posts': posts,
            'exported_at': datetime.now().isoformat()
        }
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

    elif output_format == 'csv':
        with open(output_path, 'w', newline='') as f:
            if posts:
                writer = csv.DictWriter(f, fieldnames=posts[0].keys())
                writer.writeheader()
                writer.writerows(posts)

    elif output_format == 'md':
        with open(output_path, 'w') as f:
            f.write(f"# Social Analytics Report: @{handle}\n\n")
            f.write(f"**Platform:** {platform.title()}\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("## Profile Metrics\n\n")
            f.write("| Metric | Value |\n|--------|-------|\n")
            f.write(f"| Followers | {format_number(data['followers'])} |\n")
            f.write(f"| Engagement | {data['engagement_rate']:.1f}% |\n")
            f.write(f"| Posts/Day | {data['posts_per_day']:.1f} |\n")

    click.echo(f"  [Done] Exported to {output_path}")


if __name__ == "__main__":
    cli()
