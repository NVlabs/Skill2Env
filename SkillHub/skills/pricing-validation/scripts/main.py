#!/usr/bin/env python3
"""
Pricing Validation Calculator - Van Westendorp PSM & Gabor-Granger analysis.

Based on Van Westendorp (1976) Price Sensitivity Meter methodology.

Usage:
    python main.py van-westendorp data.csv
    python main.py gabor-granger --prices 49,79,99,149 --responses 80,65,45,20
    python main.py elasticity --base-price 99 --base-demand 100 --new-price 79 --new-demand 130
"""

import click
import json
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class VanWestendorpResult:
    """Van Westendorp Price Sensitivity Meter results."""
    point_of_marginal_cheapness: float  # PMC
    point_of_marginal_expensiveness: float  # PME
    optimal_price_point: float  # OPP
    indifference_price_point: float  # IPP
    acceptable_price_range: tuple[float, float]


@dataclass
class GaborGrangerResult:
    """Gabor-Granger demand curve results."""
    prices: list[float]
    demands: list[float]
    revenues: list[float]
    optimal_price: float
    optimal_revenue: float
    elasticity_estimate: float


def analyze_van_westendorp(
    too_cheap: list[float],
    cheap: list[float],
    expensive: list[float],
    too_expensive: list[float]
) -> VanWestendorpResult:
    """
    Analyze Van Westendorp PSM data.

    Arguments:
        too_cheap: "At what price would it be so cheap you'd doubt quality?"
        cheap: "At what price would it start to seem like a bargain?"
        expensive: "At what price would it start to seem expensive?"
        too_expensive: "At what price would it be too expensive to consider?"
    """
    # Sort all responses
    too_cheap = sorted(too_cheap)
    cheap = sorted(cheap)
    expensive = sorted(expensive)
    too_expensive = sorted(too_expensive)

    # Get price range for analysis
    all_prices = too_cheap + cheap + expensive + too_expensive
    min_price = min(all_prices)
    max_price = max(all_prices)

    # Calculate cumulative percentages at each price point
    def cumulative_pct(data: list[float], price: float, ascending: bool = True) -> float:
        """Calculate cumulative percentage at a price point."""
        if ascending:
            return sum(1 for p in data if p <= price) / len(data) * 100
        else:
            return sum(1 for p in data if p >= price) / len(data) * 100

    # Find intersection points
    # PMC: too_cheap (descending) crosses cheap (ascending)
    # PME: expensive (ascending) crosses too_expensive (descending)
    # OPP: too_cheap (descending) crosses too_expensive (descending)
    # IPP: cheap (ascending) crosses expensive (ascending)

    price_points = sorted(set(all_prices))
    pmc = pme = opp = ipp = None

    for i, price in enumerate(price_points[:-1]):
        next_price = price_points[i + 1]

        # Calculate cumulative percentages
        tc_pct = cumulative_pct(too_cheap, price, ascending=False)
        tc_next = cumulative_pct(too_cheap, next_price, ascending=False)
        c_pct = cumulative_pct(cheap, price, ascending=True)
        c_next = cumulative_pct(cheap, next_price, ascending=True)
        e_pct = cumulative_pct(expensive, price, ascending=True)
        e_next = cumulative_pct(expensive, next_price, ascending=True)
        te_pct = cumulative_pct(too_expensive, price, ascending=False)
        te_next = cumulative_pct(too_expensive, next_price, ascending=False)

        # Find PMC (too_cheap desc crosses cheap asc)
        if pmc is None and tc_pct >= c_pct and tc_next <= c_next:
            pmc = (price + next_price) / 2

        # Find PME (expensive asc crosses too_expensive desc)
        if pme is None and e_pct <= te_pct and e_next >= te_next:
            pme = (price + next_price) / 2

        # Find OPP (too_cheap desc crosses too_expensive desc - minimum resistance)
        if opp is None and tc_pct >= te_pct and tc_next <= te_next:
            opp = (price + next_price) / 2

        # Find IPP (cheap asc crosses expensive asc)
        if ipp is None and c_pct <= e_pct and c_next >= e_next:
            ipp = (price + next_price) / 2

    # Fallbacks if intersections not found
    pmc = pmc or min_price + (max_price - min_price) * 0.25
    pme = pme or min_price + (max_price - min_price) * 0.75
    opp = opp or (pmc + pme) / 2
    ipp = ipp or (pmc + pme) / 2

    return VanWestendorpResult(
        point_of_marginal_cheapness=pmc,
        point_of_marginal_expensiveness=pme,
        optimal_price_point=opp,
        indifference_price_point=ipp,
        acceptable_price_range=(pmc, pme)
    )


def analyze_gabor_granger(
    prices: list[float],
    demands: list[float]
) -> GaborGrangerResult:
    """
    Analyze Gabor-Granger demand curve data.

    Arguments:
        prices: List of tested price points
        demands: List of purchase intent percentages (0-100)
    """
    revenues = [p * d for p, d in zip(prices, demands)]

    max_revenue_idx = revenues.index(max(revenues))
    optimal_price = prices[max_revenue_idx]
    optimal_revenue = revenues[max_revenue_idx]

    # Calculate price elasticity using midpoint method
    if len(prices) >= 2:
        p1, p2 = prices[0], prices[-1]
        d1, d2 = demands[0], demands[-1]
        avg_d = (d1 + d2) / 2
        avg_p = (p1 + p2) / 2
        if avg_d > 0 and avg_p > 0:
            elasticity = ((d2 - d1) / avg_d) / ((p2 - p1) / avg_p)
        else:
            elasticity = 0
    else:
        elasticity = 0

    return GaborGrangerResult(
        prices=prices,
        demands=demands,
        revenues=revenues,
        optimal_price=optimal_price,
        optimal_revenue=optimal_revenue,
        elasticity_estimate=elasticity
    )


@click.group()
def cli():
    """Pricing Validation Calculator - Van Westendorp & Gabor-Granger."""
    pass


@cli.command('van-westendorp')
@click.argument('data_file', type=click.Path(exists=True), required=False)
@click.option('--too-cheap', '-tc', help='Comma-separated "too cheap" responses')
@click.option('--cheap', '-c', help='Comma-separated "bargain" responses')
@click.option('--expensive', '-e', help='Comma-separated "expensive" responses')
@click.option('--too-expensive', '-te', help='Comma-separated "too expensive" responses')
def van_westendorp(
    data_file: Optional[str],
    too_cheap: Optional[str],
    cheap: Optional[str],
    expensive: Optional[str],
    too_expensive: Optional[str]
):
    """Run Van Westendorp Price Sensitivity Meter analysis.

    Provide either a JSON/CSV file or command-line data.

    Example with CLI data:
        python main.py van-westendorp --tc "10,15,20,25" --c "30,40,50,60" --e "80,90,100,110" --te "120,150,180,200"
    """
    if data_file:
        path = Path(data_file)
        if path.suffix == '.json':
            with open(path) as f:
                data = json.load(f)
            tc_data = data.get('too_cheap', [])
            c_data = data.get('cheap', [])
            e_data = data.get('expensive', [])
            te_data = data.get('too_expensive', [])
        else:
            click.echo("Only JSON files supported currently")
            return
    elif all([too_cheap, cheap, expensive, too_expensive]):
        tc_data = [float(x.strip()) for x in too_cheap.split(',')]
        c_data = [float(x.strip()) for x in cheap.split(',')]
        e_data = [float(x.strip()) for x in expensive.split(',')]
        te_data = [float(x.strip()) for x in too_expensive.split(',')]
    else:
        click.echo("Provide either data_file or all four price response options")
        return

    result = analyze_van_westendorp(tc_data, c_data, e_data, te_data)

    click.echo("\n  Van Westendorp Price Sensitivity Meter")
    click.echo(f"  {'=' * 50}")
    click.echo("\n  Data Summary")
    click.echo(f"  {'-' * 50}")
    click.echo(f"  Responses analyzed:    {len(tc_data)} per question")
    click.echo(f"  Price range tested:    ${min(tc_data + c_data + e_data + te_data):.0f} - ${max(tc_data + c_data + e_data + te_data):.0f}")

    click.echo("\n  Key Price Points")
    click.echo(f"  {'-' * 50}")
    click.echo(f"  Point of Marginal Cheapness (PMC):     ${result.point_of_marginal_cheapness:.2f}")
    click.echo(f"  Point of Marginal Expensiveness (PME): ${result.point_of_marginal_expensiveness:.2f}")
    click.echo(f"  Optimal Price Point (OPP):             ${result.optimal_price_point:.2f}")
    click.echo(f"  Indifference Price Point (IPP):        ${result.indifference_price_point:.2f}")

    click.echo("\n  Acceptable Price Range")
    click.echo(f"  {'-' * 50}")
    click.echo(f"  Range: ${result.acceptable_price_range[0]:.2f} - ${result.acceptable_price_range[1]:.2f}")

    click.echo("\n  Interpretation")
    click.echo(f"  {'-' * 50}")
    click.echo(f"  - Price below ${result.point_of_marginal_cheapness:.0f}: Quality concerns")
    click.echo(f"  - Price above ${result.point_of_marginal_expensiveness:.0f}: Too expensive for most")
    click.echo(f"  - Optimal price: ${result.optimal_price_point:.0f} (minimal price resistance)")
    click.echo(f"  - Safe pricing zone: ${result.point_of_marginal_cheapness:.0f} - ${result.point_of_marginal_expensiveness:.0f}")


@cli.command('gabor-granger')
@click.option('--prices', '-p', required=True, help='Comma-separated price points tested')
@click.option('--responses', '-r', required=True, help='Comma-separated purchase intent % at each price')
def gabor_granger(prices: str, responses: str):
    """Run Gabor-Granger demand curve analysis.

    Example:
        python main.py gabor-granger --prices "49,79,99,149" --responses "80,65,45,20"
    """
    price_list = [float(x.strip()) for x in prices.split(',')]
    demand_list = [float(x.strip()) for x in responses.split(',')]

    if len(price_list) != len(demand_list):
        click.echo("Error: Number of prices must match number of responses")
        return

    result = analyze_gabor_granger(price_list, demand_list)

    click.echo("\n  Gabor-Granger Demand Analysis")
    click.echo(f"  {'=' * 50}")

    click.echo("\n  Demand Curve")
    click.echo(f"  {'-' * 50}")
    click.echo(f"  {'Price':>10} {'Demand %':>12} {'Revenue Index':>15}")
    click.echo(f"  {'-' * 50}")

    for i, (p, d, r) in enumerate(zip(result.prices, result.demands, result.revenues)):
        marker = " <-- optimal" if p == result.optimal_price else ""
        click.echo(f"  ${p:>9.0f} {d:>11.0f}% {r:>14.0f}{marker}")

    click.echo("\n  Analysis")
    click.echo(f"  {'-' * 50}")
    click.echo(f"  Optimal Price:        ${result.optimal_price:.0f}")
    click.echo(f"  Max Revenue Index:    {result.optimal_revenue:.0f}")
    click.echo(f"  Price Elasticity:     {result.elasticity_estimate:.2f}")

    if result.elasticity_estimate < -1:
        click.echo("\n  Elasticity Interpretation: ELASTIC")
        click.echo("  - Demand is sensitive to price changes")
        click.echo("  - Consider lower prices for higher volume")
    elif result.elasticity_estimate > -1:
        click.echo("\n  Elasticity Interpretation: INELASTIC")
        click.echo("  - Demand is less sensitive to price")
        click.echo("  - Room to increase prices")


@cli.command('elasticity')
@click.option('--base-price', '-bp', type=float, required=True, help='Original price')
@click.option('--base-demand', '-bd', type=float, required=True, help='Original demand/sales')
@click.option('--new-price', '-np', type=float, required=True, help='New price')
@click.option('--new-demand', '-nd', type=float, required=True, help='New demand/sales')
def elasticity(base_price: float, base_demand: float, new_price: float, new_demand: float):
    """Calculate price elasticity from before/after data.

    Example:
        python main.py elasticity --base-price 99 --base-demand 100 --new-price 79 --new-demand 130
    """
    # Midpoint elasticity formula
    avg_q = (base_demand + new_demand) / 2
    avg_p = (base_price + new_price) / 2

    pct_change_q = (new_demand - base_demand) / avg_q * 100
    pct_change_p = (new_price - base_price) / avg_p * 100

    if pct_change_p != 0:
        elasticity_value = pct_change_q / pct_change_p
    else:
        elasticity_value = 0

    base_revenue = base_price * base_demand
    new_revenue = new_price * new_demand
    revenue_change = new_revenue - base_revenue
    revenue_change_pct = (revenue_change / base_revenue) * 100 if base_revenue > 0 else 0

    click.echo("\n  Price Elasticity Analysis")
    click.echo(f"  {'=' * 45}")

    click.echo("\n  Before vs After")
    click.echo(f"  {'-' * 45}")
    click.echo(f"  {'':15} {'Before':>12} {'After':>12}")
    click.echo(f"  {'-' * 45}")
    click.echo(f"  {'Price':15} ${base_price:>11.0f} ${new_price:>11.0f}")
    click.echo(f"  {'Demand':15} {base_demand:>12.0f} {new_demand:>12.0f}")
    click.echo(f"  {'Revenue':15} ${base_revenue:>11.0f} ${new_revenue:>11.0f}")

    click.echo("\n  Calculations")
    click.echo(f"  {'-' * 45}")
    click.echo(f"  Price Change:       {pct_change_p:+.1f}%")
    click.echo(f"  Demand Change:      {pct_change_q:+.1f}%")
    click.echo(f"  Price Elasticity:   {elasticity_value:.2f}")
    click.echo(f"  Revenue Change:     {revenue_change_pct:+.1f}% (${revenue_change:+,.0f})")

    click.echo("\n  Interpretation")
    click.echo(f"  {'-' * 45}")

    abs_e = abs(elasticity_value)
    if abs_e > 1:
        click.echo(f"  ELASTIC (|E| = {abs_e:.2f} > 1)")
        click.echo("  - Demand is sensitive to price changes")
        click.echo("  - 1% price change leads to >{:.1f}% demand change".format(abs_e))
        if revenue_change > 0:
            click.echo("  - Price decrease increased revenue (correct direction)")
        else:
            click.echo("  - Consider: Lower price may increase revenue")
    elif abs_e < 1:
        click.echo(f"  INELASTIC (|E| = {abs_e:.2f} < 1)")
        click.echo("  - Demand is not very sensitive to price")
        click.echo("  - 1% price change leads to <{:.1f}% demand change".format(abs_e))
        if new_price > base_price and revenue_change > 0:
            click.echo("  - Price increase worked (demand held)")
        else:
            click.echo("  - Consider: Room to raise prices")
    else:
        click.echo(f"  UNIT ELASTIC (|E| = {abs_e:.2f})")
        click.echo("  - Revenue stays constant as price changes")


@cli.command('questions')
def questions():
    """Print Van Westendorp survey questions for your research."""
    click.echo("\n  Van Westendorp Survey Questions")
    click.echo(f"  {'=' * 60}")
    click.echo("\n  Use these 4 questions in your pricing research:")
    click.echo(f"  {'-' * 60}")

    click.echo("""
  Q1 - TOO CHEAP (Quality Doubt):
  "At what price would you consider [product] to be priced so low
   that you would feel the quality couldn't be very good?"

  Q2 - CHEAP (Bargain):
  "At what price would you consider [product] to be a bargain -
   a great buy for the money?"

  Q3 - EXPENSIVE (Getting Expensive):
  "At what price would you consider [product] starting to get
   expensive - not out of the question, but you'd have to think?"

  Q4 - TOO EXPENSIVE (Prohibitive):
  "At what price would you consider [product] to be so expensive
   that you wouldn't consider buying it?"
    """)

    click.echo(f"  {'-' * 60}")
    click.echo("  Collect 100-200+ responses for reliable results.")
    click.echo("  Export data as JSON with keys: too_cheap, cheap, expensive, too_expensive")


if __name__ == "__main__":
    cli()
