#!/usr/bin/env python3
"""
Startup Metrics Calculator - Unit economics & cohort analysis.

Based on A16Z and YC frameworks for measuring startup progress.

Usage:
    python main.py unit-economics 50000 100 500 --churn 0.05
    python main.py benchmark --arr 1200000 --growth 180 --nrr 108 --ltv-cac 4.5
    python main.py quick-ratio 10000 5000 3000 1000
"""

import click
from dataclasses import dataclass
from typing import Optional


@dataclass
class UnitEconomics:
    """Unit economics calculation results."""
    mrr: float
    customers: int
    cac: float
    churn_rate: float
    arpu: float
    ltv: float
    ltv_cac: float
    payback_months: float
    customer_lifespan_months: float


def calculate_unit_economics(
    mrr: float,
    customers: int,
    cac: float,
    churn_rate: float = 0.05,
    gross_margin: float = 0.80
) -> UnitEconomics:
    """Calculate core SaaS unit economics."""
    arpu = mrr / customers if customers > 0 else 0
    customer_lifespan = 1 / churn_rate if churn_rate > 0 else 100
    ltv = arpu * gross_margin * customer_lifespan
    ltv_cac = ltv / cac if cac > 0 else 0
    payback = cac / (arpu * gross_margin) if arpu > 0 else 0

    return UnitEconomics(
        mrr=mrr,
        customers=customers,
        cac=cac,
        churn_rate=churn_rate,
        arpu=arpu,
        ltv=ltv,
        ltv_cac=ltv_cac,
        payback_months=payback,
        customer_lifespan_months=customer_lifespan
    )


def get_benchmark_status(value: float, good: float, great: float, higher_is_better: bool = True) -> str:
    """Return status emoji based on benchmark."""
    if higher_is_better:
        if value >= great:
            return "excellent"
        elif value >= good:
            return "good"
        else:
            return "needs work"
    else:
        if value <= great:
            return "excellent"
        elif value <= good:
            return "good"
        else:
            return "needs work"


@click.group()
def cli():
    """Startup Metrics Calculator - A16Z/YC frameworks."""
    pass


@cli.command()
@click.argument('mrr', type=float)
@click.argument('customers', type=int)
@click.argument('cac', type=float)
@click.option('--churn', '-c', default=0.05, help='Monthly churn rate (default: 0.05)')
@click.option('--margin', '-m', default=0.80, help='Gross margin (default: 0.80)')
def unit_economics(mrr: float, customers: int, cac: float, churn: float, margin: float):
    """Calculate unit economics (LTV, LTV/CAC, payback).

    Arguments:
        MRR: Monthly Recurring Revenue
        CUSTOMERS: Number of customers
        CAC: Customer Acquisition Cost
    """
    result = calculate_unit_economics(mrr, customers, cac, churn, margin)

    # Status indicators
    ltv_cac_status = get_benchmark_status(result.ltv_cac, 3, 5)
    payback_status = get_benchmark_status(result.payback_months, 18, 12, higher_is_better=False)
    get_benchmark_status(result.churn_rate * 100, 5, 2, higher_is_better=False)

    click.echo("\n  Unit Economics Report")
    click.echo(f"  {'=' * 45}")
    click.echo("\n  Input Data")
    click.echo(f"  {'-' * 45}")
    click.echo(f"  MRR:                ${result.mrr:,.2f}")
    click.echo(f"  Customers:          {result.customers:,}")
    click.echo(f"  CAC:                ${result.cac:,.2f}")
    click.echo(f"  Monthly Churn:      {result.churn_rate * 100:.1f}%")
    click.echo(f"  Gross Margin:       {margin * 100:.0f}%")

    click.echo("\n  Calculated Metrics")
    click.echo(f"  {'-' * 45}")
    click.echo(f"  ARPU:               ${result.arpu:,.2f}/month")
    click.echo(f"  Customer Lifespan:  {result.customer_lifespan_months:.1f} months")
    click.echo(f"  LTV:                ${result.ltv:,.2f}")
    click.echo(f"  LTV/CAC:            {result.ltv_cac:.1f}x [{ltv_cac_status}]")
    click.echo(f"  CAC Payback:        {result.payback_months:.1f} months [{payback_status}]")

    click.echo("\n  Analysis")
    click.echo(f"  {'-' * 45}")

    if result.ltv_cac >= 3:
        click.echo("  [+] LTV/CAC ratio is healthy (>3x)")
    else:
        click.echo(f"  [-] LTV/CAC ({result.ltv_cac:.1f}x) below 3x threshold")
        click.echo("      Consider: Reduce CAC, increase prices, or reduce churn")

    if result.payback_months <= 18:
        click.echo("  [+] CAC payback is within acceptable range (<18mo)")
    else:
        click.echo(f"  [-] CAC payback ({result.payback_months:.1f}mo) exceeds 18 months")
        click.echo("      Consider: Lower CAC or increase ARPU")

    if result.churn_rate <= 0.03:
        click.echo("  [+] Monthly churn is low (<3%)")
    elif result.churn_rate <= 0.05:
        click.echo("  [~] Monthly churn is acceptable but improvable (3-5%)")
    else:
        click.echo(f"  [-] Monthly churn ({result.churn_rate * 100:.1f}%) is high (>5%)")
        click.echo("      Annual churn would be ~{:.0f}%".format((1 - (1 - result.churn_rate) ** 12) * 100))

    # ARR projection
    arr = result.mrr * 12
    click.echo("\n  Projections")
    click.echo(f"  {'-' * 45}")
    click.echo(f"  Current ARR:        ${arr:,.0f}")
    click.echo(f"  Implied Annual Churn: {(1 - (1 - result.churn_rate) ** 12) * 100:.0f}%")

    # Break-even customers
    if result.ltv_cac < 1:
        click.echo("  [!] Warning: LTV < CAC - losing money on each customer")
    else:
        break_even_cust = result.cac / (result.arpu * margin)
        click.echo(f"  Break-even:         {break_even_cust:.1f} months of revenue")


@cli.command()
@click.argument('new_mrr', type=float)
@click.argument('expansion_mrr', type=float)
@click.argument('churned_mrr', type=float)
@click.argument('contraction_mrr', type=float)
def quick_ratio(new_mrr: float, expansion_mrr: float, churned_mrr: float, contraction_mrr: float):
    """Calculate Quick Ratio for growth quality.

    Quick Ratio = (New + Expansion) / (Churn + Contraction)
    >4 = Excellent, 2-4 = Good, <2 = Concerning
    """
    additions = new_mrr + expansion_mrr
    losses = churned_mrr + contraction_mrr

    if losses > 0:
        ratio = additions / losses
    else:
        ratio = float('inf')

    net_new = additions - losses

    click.echo("\n  Quick Ratio Analysis")
    click.echo(f"  {'=' * 40}")
    click.echo("\n  MRR Components")
    click.echo(f"  {'-' * 40}")
    click.echo(f"  New MRR:          +${new_mrr:,.0f}")
    click.echo(f"  Expansion MRR:    +${expansion_mrr:,.0f}")
    click.echo(f"  Churned MRR:      -${churned_mrr:,.0f}")
    click.echo(f"  Contraction MRR:  -${contraction_mrr:,.0f}")
    click.echo(f"  {'-' * 40}")
    click.echo(f"  Net New MRR:       ${net_new:,.0f}")

    click.echo("\n  Quick Ratio")
    click.echo(f"  {'-' * 40}")

    if ratio == float('inf'):
        click.echo("  Quick Ratio:      Infinite (no losses)")
    else:
        status = get_benchmark_status(ratio, 2, 4)
        click.echo(f"  Quick Ratio:      {ratio:.2f} [{status}]")

    click.echo("\n  Benchmarks")
    click.echo("  >4  = Excellent growth quality")
    click.echo("  2-4 = Good, sustainable")
    click.echo("  <2  = Leaky bucket, churn eating growth")

    if ratio < 2:
        click.echo("\n  [!] Warning: Growth quality is poor")
        click.echo("      For every $1 lost, only adding ${:.2f}".format(ratio))


@cli.command()
@click.option('--arr', type=float, help='Annual Recurring Revenue')
@click.option('--growth', type=float, help='YoY Growth Rate (%)')
@click.option('--nrr', type=float, help='Net Revenue Retention (%)')
@click.option('--ltv-cac', type=float, help='LTV/CAC Ratio')
@click.option('--payback', type=float, help='CAC Payback (months)')
@click.option('--margin', type=float, help='Gross Margin (%)')
@click.option('--magic', type=float, help='Magic Number')
def benchmark(
    arr: Optional[float],
    growth: Optional[float],
    nrr: Optional[float],
    ltv_cac: Optional[float],
    payback: Optional[float],
    margin: Optional[float],
    magic: Optional[float]
):
    """Benchmark your metrics against Series A standards."""
    click.echo("\n  Series A Readiness Benchmark")
    click.echo(f"  {'=' * 50}")

    # Benchmarks: (value, good, great, unit, higher_is_better)
    benchmarks = {
        'ARR': (arr, 1_000_000, 2_000_000, '$', True),
        'YoY Growth': (growth, 100, 200, '%', True),
        'NRR': (nrr, 100, 120, '%', True),
        'LTV/CAC': (ltv_cac, 3, 5, 'x', True),
        'CAC Payback': (payback, 18, 12, 'mo', False),
        'Gross Margin': (margin, 70, 80, '%', True),
        'Magic Number': (magic, 0.75, 1.0, '', True),
    }

    passed = 0
    total = 0

    click.echo(f"\n  {'Metric':<15} {'Value':>12} {'Series A':>12} {'Status':>12}")
    click.echo(f"  {'-' * 51}")

    for name, (value, good, great, unit, higher_is_better) in benchmarks.items():
        if value is not None:
            total += 1
            status = get_benchmark_status(value, good, great, higher_is_better)

            if unit == '$':
                val_str = f"${value / 1_000_000:.1f}M"
                bar_str = f"${good / 1_000_000:.0f}M+"
            elif unit == '%':
                val_str = f"{value:.0f}%"
                bar_str = f">{good:.0f}%"
            elif unit == 'x':
                val_str = f"{value:.1f}x"
                bar_str = f">{good:.0f}x"
            elif unit == 'mo':
                val_str = f"{value:.0f}mo"
                bar_str = f"<{good:.0f}mo"
            else:
                val_str = f"{value:.2f}"
                bar_str = f">{good:.2f}"

            if status in ['excellent', 'good']:
                passed += 1
                status_str = f"[{status}]"
            else:
                status_str = f"[{status}]"

            click.echo(f"  {name:<15} {val_str:>12} {bar_str:>12} {status_str:>12}")

    click.echo("\n  Summary")
    click.echo(f"  {'-' * 51}")
    click.echo(f"  Metrics passing: {passed}/{total}")

    if total > 0:
        pct = (passed / total) * 100
        if pct >= 80:
            click.echo("  Overall: Strong Series A candidate")
        elif pct >= 60:
            click.echo("  Overall: Approaching Series A readiness")
        else:
            click.echo("  Overall: Need improvement before Series A")


@cli.command()
@click.argument('growth_rate', type=float)
@click.argument('profit_margin', type=float)
def rule_of_40(growth_rate: float, profit_margin: float):
    """Calculate Rule of 40 score.

    Rule of 40 = Growth Rate + Profit Margin
    Should be >40% for healthy SaaS at scale.

    Arguments:
        GROWTH_RATE: YoY revenue growth (%)
        PROFIT_MARGIN: Operating profit margin (%)
    """
    score = growth_rate + profit_margin

    click.echo("\n  Rule of 40 Analysis")
    click.echo(f"  {'=' * 40}")
    click.echo("\n  Inputs")
    click.echo(f"  {'-' * 40}")
    click.echo(f"  Growth Rate:     {growth_rate:.0f}%")
    click.echo(f"  Profit Margin:   {profit_margin:.0f}%")
    click.echo(f"  {'-' * 40}")
    click.echo(f"  Rule of 40:      {score:.0f}%")

    if score >= 40:
        click.echo("\n  [+] Passing Rule of 40")
        click.echo("      Healthy balance of growth and profitability")
    else:
        gap = 40 - score
        click.echo(f"\n  [-] Below Rule of 40 by {gap:.0f} points")
        click.echo("      Options to reach 40:")
        click.echo(f"      - Increase growth to {40 - profit_margin:.0f}% (current: {growth_rate:.0f}%)")
        click.echo(f"      - Increase margin to {40 - growth_rate:.0f}% (current: {profit_margin:.0f}%)")


@cli.command()
@click.argument('net_burn', type=float)
@click.argument('net_new_arr', type=float)
def burn_multiple(net_burn: float, net_new_arr: float):
    """Calculate Burn Multiple for cash efficiency.

    Burn Multiple = Net Burn / Net New ARR
    <1x = Excellent, 1-2x = Good, >2x = Concerning
    """
    if net_new_arr > 0:
        multiple = net_burn / net_new_arr
    else:
        multiple = float('inf')

    click.echo("\n  Burn Multiple Analysis")
    click.echo(f"  {'=' * 40}")
    click.echo("\n  Inputs")
    click.echo(f"  {'-' * 40}")
    click.echo(f"  Net Burn:        ${net_burn:,.0f}")
    click.echo(f"  Net New ARR:     ${net_new_arr:,.0f}")
    click.echo(f"  {'-' * 40}")

    if multiple == float('inf'):
        click.echo("  Burn Multiple:   Infinite (no new ARR)")
        click.echo("\n  [!] Critical: Spending but not growing")
    else:
        status = get_benchmark_status(multiple, 2, 1, higher_is_better=False)
        click.echo(f"  Burn Multiple:   {multiple:.1f}x [{status}]")

        click.echo("\n  Interpretation")
        click.echo(f"  Spending ${multiple:.2f} for every $1 of new ARR")

        if multiple < 1:
            click.echo("  [+] Excellent cash efficiency")
        elif multiple < 2:
            click.echo("  [~] Acceptable, but monitor closely")
        else:
            click.echo("  [-] Poor cash efficiency")
            click.echo("      Consider: Reduce spend or improve sales efficiency")


if __name__ == "__main__":
    cli()
