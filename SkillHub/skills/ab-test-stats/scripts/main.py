#!/usr/bin/env python3
"""
A/B Test Statistics Calculator - Statistical significance for experiments.

Usage:
    python main.py significance --control 1000,50 --variant 1000,65
    python main.py sample-size --baseline 0.05 --mde 0.02
    python main.py duration --traffic 1000 --baseline 0.05 --mde 0.02
"""

import click
import math
from typing import Tuple


def parse_data(data_str: str) -> Tuple[int, int]:
    """Parse 'visitors,conversions' format."""
    parts = data_str.split(',')
    return int(parts[0]), int(parts[1])


def z_score(p1: float, p2: float, n1: int, n2: int) -> float:
    """Calculate z-score for two proportions."""
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    if se == 0:
        return 0
    return (p2 - p1) / se


def p_value_from_z(z: float) -> float:
    """Calculate two-tailed p-value from z-score."""
    # Approximation of normal CDF
    def norm_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    return 2 * (1 - norm_cdf(abs(z)))


def z_value_for_confidence(confidence: float) -> float:
    """Get z-value for given confidence level."""
    # Common values
    z_values = {
        0.80: 1.282,
        0.85: 1.440,
        0.90: 1.645,
        0.95: 1.960,
        0.99: 2.576,
    }
    return z_values.get(confidence, 1.960)


def calculate_sample_size(baseline: float, mde: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """Calculate required sample size per variant."""
    p1 = baseline
    p2 = baseline + mde

    # Z-values
    z_alpha = z_value_for_confidence(1 - alpha)
    z_beta = z_value_for_confidence(power)

    # Sample size formula for two proportions
    p_avg = (p1 + p2) / 2
    numerator = 2 * p_avg * (1 - p_avg) * ((z_alpha + z_beta) ** 2)
    denominator = (p2 - p1) ** 2

    if denominator == 0:
        return float('inf')

    return int(math.ceil(numerator / denominator))


@click.group()
def cli():
    """A/B Test Statistics Calculator."""
    pass


@cli.command()
@click.option('--control', '-c', required=True, help='Control: visitors,conversions')
@click.option('--variant', '-v', required=True, help='Variant: visitors,conversions')
@click.option('--confidence', default=0.95, help='Required confidence level')
def significance(control: str, variant: str, confidence: float):
    """Check if A/B test results are statistically significant."""
    n_control, conv_control = parse_data(control)
    n_variant, conv_variant = parse_data(variant)

    rate_control = conv_control / n_control
    rate_variant = conv_variant / n_variant
    lift = (rate_variant - rate_control) / rate_control if rate_control > 0 else 0

    click.echo("\n  A/B Test Results")
    click.echo("  " + "=" * 35)
    click.echo(f"  Control:  {rate_control*100:.2f}% ({conv_control}/{n_control})")
    click.echo(f"  Variant:  {rate_variant*100:.2f}% ({conv_variant}/{n_variant})")
    click.echo(f"  Lift:     {lift*100:+.1f}%")

    # Calculate significance
    z = z_score(rate_control, rate_variant, n_control, n_variant)
    p = p_value_from_z(z)
    conf = 1 - p

    click.echo("\n  Statistical Analysis")
    click.echo("  " + "-" * 35)
    click.echo(f"  Z-score:    {z:.3f}")
    click.echo(f"  p-value:    {p:.4f}")
    click.echo(f"  Confidence: {conf*100:.1f}%")

    # Verdict
    if conf >= confidence:
        winner = "Variant" if lift > 0 else "Control"
        click.echo("\n  Result: ✓ SIGNIFICANT")
        click.echo(f"  Winner: {winner}")

        # Practical impact
        if abs(lift) >= 0.1:
            click.echo(f"  Impact: Strong ({abs(lift)*100:.0f}% lift)")
        elif abs(lift) >= 0.05:
            click.echo(f"  Impact: Moderate ({abs(lift)*100:.0f}% lift)")
        else:
            click.echo(f"  Impact: Small ({abs(lift)*100:.1f}% lift)")
    else:
        click.echo("\n  Result: ✗ NOT SIGNIFICANT")
        click.echo(f"  Need {confidence*100:.0f}% confidence, have {conf*100:.1f}%")
        click.echo("  Recommendation: Continue test or increase sample")

        # Estimate additional sample needed
        if rate_control != rate_variant:
            needed = calculate_sample_size(rate_control, abs(rate_variant - rate_control))
            additional = max(0, needed - min(n_control, n_variant))
            if additional > 0:
                click.echo(f"  Additional needed: ~{additional:,} per variant")


@cli.command('sample-size')
@click.option('--baseline', '-b', required=True, type=float, help='Baseline conversion rate (e.g., 0.05)')
@click.option('--mde', '-m', required=True, type=float, help='Minimum detectable effect (absolute)')
@click.option('--power', '-p', default=0.80, type=float, help='Statistical power')
@click.option('--confidence', '-c', default=0.95, type=float, help='Confidence level')
def sample_size(baseline: float, mde: float, power: float, confidence: float):
    """Calculate required sample size for A/B test."""
    target = baseline + mde
    relative_lift = mde / baseline if baseline > 0 else 0

    click.echo("\n  Sample Size Calculator")
    click.echo("  " + "=" * 40)
    click.echo(f"  Baseline conversion: {baseline*100:.1f}%")
    click.echo(f"  MDE (absolute): {mde*100:.1f}%")
    click.echo(f"  MDE (relative): {relative_lift*100:.0f}%")
    click.echo(f"  Target conversion: {target*100:.1f}%")
    click.echo(f"  Power: {power*100:.0f}%")
    click.echo(f"  Confidence: {confidence*100:.0f}%")

    alpha = 1 - confidence
    n = calculate_sample_size(baseline, mde, alpha, power)

    click.echo("\n  Results")
    click.echo("  " + "-" * 40)
    click.echo(f"  Required per variant: {n:,}")
    click.echo(f"  Total required: {n*2:,}")

    # Show duration estimates
    click.echo("\n  Duration Estimates")
    click.echo("  " + "-" * 40)
    for daily in [100, 500, 1000, 5000, 10000]:
        days = math.ceil(n * 2 / daily)
        click.echo(f"  At {daily:,}/day: {days} days")


@cli.command()
@click.option('--traffic', '-t', required=True, type=int, help='Daily traffic')
@click.option('--baseline', '-b', required=True, type=float, help='Baseline conversion rate')
@click.option('--mde', '-m', required=True, type=float, help='Minimum detectable effect')
@click.option('--power', '-p', default=0.80, type=float, help='Statistical power')
def duration(traffic: int, baseline: float, mde: float, power: float):
    """Estimate test duration."""
    click.echo("\n  Test Duration Estimator")
    click.echo("  " + "=" * 40)
    click.echo(f"  Daily traffic: {traffic:,}")
    click.echo(f"  Baseline: {baseline*100:.1f}%")
    click.echo(f"  MDE: {mde*100:.1f}%")

    n = calculate_sample_size(baseline, mde, 0.05, power)
    total_needed = n * 2
    days = math.ceil(total_needed / traffic)

    click.echo("\n  Results")
    click.echo("  " + "-" * 40)
    click.echo(f"  Sample needed: {total_needed:,}")
    click.echo(f"  Estimated duration: {days} days")
    click.echo(f"  Weeks: {days/7:.1f}")

    if days > 30:
        click.echo("\n  ⚠ Warning: Test may be too long")
        click.echo("  Consider:")
        click.echo("    - Increasing MDE (accept smaller lift detection)")
        click.echo("    - Reducing power (accept more false negatives)")
        click.echo("    - Increasing traffic to test")


@cli.command()
@click.option('--conversions', '-c', required=True, type=int, help='Number of conversions')
@click.option('--visitors', '-v', required=True, type=int, help='Number of visitors')
@click.option('--confidence', default=0.95, type=float, help='Confidence level')
def rate_ci(conversions: int, visitors: int, confidence: float):
    """Calculate confidence interval for conversion rate."""
    rate = conversions / visitors
    z = z_value_for_confidence(confidence)
    se = math.sqrt(rate * (1 - rate) / visitors)

    lower = max(0, rate - z * se)
    upper = min(1, rate + z * se)

    click.echo("\n  Conversion Rate Confidence Interval")
    click.echo("  " + "=" * 40)
    click.echo(f"  Conversions: {conversions}")
    click.echo(f"  Visitors: {visitors}")
    click.echo(f"  Rate: {rate*100:.2f}%")
    click.echo(f"  {confidence*100:.0f}% CI: [{lower*100:.2f}%, {upper*100:.2f}%]")
    click.echo(f"  Margin of error: ±{z*se*100:.2f}%")


if __name__ == "__main__":
    cli()
