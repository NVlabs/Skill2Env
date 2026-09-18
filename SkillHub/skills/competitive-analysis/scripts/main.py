#!/usr/bin/env python3
"""
Competitive Analysis Toolkit - Porter's Five Forces & Competitor Profiler.

Based on Michael Porter's competitive strategy frameworks.

Usage:
    python main.py five-forces --interactive
    python main.py profile --name "Competitor" --pricing 99 --features "A,B,C"
    python main.py matrix competitors.json
"""

import click
import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FiveForces:
    """Porter's Five Forces analysis results."""
    supplier_power: int  # 1-5
    buyer_power: int  # 1-5
    threat_of_substitutes: int  # 1-5
    threat_of_new_entrants: int  # 1-5
    competitive_rivalry: int  # 1-5
    overall_attractiveness: float
    recommendations: list[str] = field(default_factory=list)


@dataclass
class CompetitorProfile:
    """Competitor profile data."""
    name: str
    positioning: str
    target_market: str
    pricing: str
    features: list[str]
    strengths: list[str]
    weaknesses: list[str]
    differentiator: str


def calculate_industry_attractiveness(forces: FiveForces) -> float:
    """Calculate overall industry attractiveness score (1-5)."""
    # Lower forces = more attractive (invert the scale)
    total = (
        (6 - forces.supplier_power) +
        (6 - forces.buyer_power) +
        (6 - forces.threat_of_substitutes) +
        (6 - forces.threat_of_new_entrants) +
        (6 - forces.competitive_rivalry)
    )
    return total / 5


def get_force_label(score: int) -> str:
    """Convert numeric score to label."""
    labels = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Very High"}
    return labels.get(score, "Unknown")


def get_attractiveness_label(score: float) -> str:
    """Get attractiveness interpretation."""
    if score >= 4:
        return "Highly Attractive"
    elif score >= 3:
        return "Moderately Attractive"
    elif score >= 2:
        return "Challenging"
    else:
        return "Unattractive"


@click.group()
def cli():
    """Competitive Analysis Toolkit - Porter's Five Forces & Profiling."""
    pass


@cli.command('five-forces')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode with prompts')
@click.option('--supplier', '-sp', type=int, help='Supplier power (1-5)')
@click.option('--buyer', '-bp', type=int, help='Buyer power (1-5)')
@click.option('--substitutes', '-sub', type=int, help='Threat of substitutes (1-5)')
@click.option('--entrants', '-ent', type=int, help='Threat of new entrants (1-5)')
@click.option('--rivalry', '-riv', type=int, help='Competitive rivalry (1-5)')
def five_forces(
    interactive: bool,
    supplier: Optional[int],
    buyer: Optional[int],
    substitutes: Optional[int],
    entrants: Optional[int],
    rivalry: Optional[int]
):
    """Run Porter's Five Forces analysis.

    Rate each force from 1 (low) to 5 (high).
    Lower forces = more attractive industry.
    """
    if interactive:
        click.echo("\n  Porter's Five Forces Analysis")
        click.echo("  " + "=" * 50)
        click.echo("\n  Rate each force from 1 (Low) to 5 (High)")
        click.echo("  Higher = stronger force = less attractive")
        click.echo("")

        # Supplier Power
        click.echo("  SUPPLIER POWER")
        click.echo("  (Ability of suppliers to raise prices or reduce quality)")
        click.echo("  Factors: # of suppliers, switching costs, uniqueness")
        supplier = click.prompt("  Score (1-5)", type=int, default=3)

        # Buyer Power
        click.echo("\n  BUYER POWER")
        click.echo("  (Ability of buyers to negotiate lower prices)")
        click.echo("  Factors: # of buyers, switching costs, price sensitivity")
        buyer = click.prompt("  Score (1-5)", type=int, default=3)

        # Threat of Substitutes
        click.echo("\n  THREAT OF SUBSTITUTES")
        click.echo("  (Availability of alternative solutions)")
        click.echo("  Factors: Alternative products, switching costs, buyer propensity")
        substitutes = click.prompt("  Score (1-5)", type=int, default=3)

        # Threat of New Entrants
        click.echo("\n  THREAT OF NEW ENTRANTS")
        click.echo("  (Ease of entering the market)")
        click.echo("  Factors: Capital requirements, regulations, brand loyalty")
        entrants = click.prompt("  Score (1-5)", type=int, default=3)

        # Competitive Rivalry
        click.echo("\n  COMPETITIVE RIVALRY")
        click.echo("  (Intensity of competition among existing firms)")
        click.echo("  Factors: # of competitors, industry growth, differentiation")
        rivalry = click.prompt("  Score (1-5)", type=int, default=3)

    # Validate inputs
    if not all([supplier, buyer, substitutes, entrants, rivalry]):
        click.echo("Error: All five forces must be provided")
        return

    for name, val in [("supplier", supplier), ("buyer", buyer),
                      ("substitutes", substitutes), ("entrants", entrants),
                      ("rivalry", rivalry)]:
        if not 1 <= val <= 5:
            click.echo(f"Error: {name} must be between 1 and 5")
            return

    forces = FiveForces(
        supplier_power=supplier,
        buyer_power=buyer,
        threat_of_substitutes=substitutes,
        threat_of_new_entrants=entrants,
        competitive_rivalry=rivalry,
        overall_attractiveness=0
    )
    forces.overall_attractiveness = calculate_industry_attractiveness(forces)

    # Generate recommendations
    recommendations = []
    if forces.supplier_power >= 4:
        recommendations.append("Diversify suppliers or develop alternatives")
    if forces.buyer_power >= 4:
        recommendations.append("Increase switching costs or differentiate")
    if forces.threat_of_substitutes >= 4:
        recommendations.append("Emphasize unique value vs. substitutes")
    if forces.threat_of_new_entrants >= 4:
        recommendations.append("Build barriers: brand, patents, scale")
    if forces.competitive_rivalry >= 4:
        recommendations.append("Differentiate or find niche positioning")

    # Display results
    click.echo("\n  " + "=" * 55)
    click.echo("  FIVE FORCES ANALYSIS RESULTS")
    click.echo("  " + "=" * 55)

    click.echo(f"\n  {'Force':<30} {'Score':<10} {'Level':<15}")
    click.echo("  " + "-" * 55)
    click.echo(f"  {'Supplier Power':<30} {forces.supplier_power:<10} {get_force_label(forces.supplier_power):<15}")
    click.echo(f"  {'Buyer Power':<30} {forces.buyer_power:<10} {get_force_label(forces.buyer_power):<15}")
    click.echo(f"  {'Threat of Substitutes':<30} {forces.threat_of_substitutes:<10} {get_force_label(forces.threat_of_substitutes):<15}")
    click.echo(f"  {'Threat of New Entrants':<30} {forces.threat_of_new_entrants:<10} {get_force_label(forces.threat_of_new_entrants):<15}")
    click.echo(f"  {'Competitive Rivalry':<30} {forces.competitive_rivalry:<10} {get_force_label(forces.competitive_rivalry):<15}")

    click.echo("\n  " + "-" * 55)
    click.echo(f"  Industry Attractiveness: {forces.overall_attractiveness:.1f}/5.0")
    click.echo(f"  Assessment: {get_attractiveness_label(forces.overall_attractiveness)}")

    if recommendations:
        click.echo("\n  Strategic Recommendations:")
        for rec in recommendations:
            click.echo(f"  - {rec}")

    # Visual representation
    click.echo("\n  Force Strength Visualization:")
    for name, val in [("Suppliers", forces.supplier_power),
                      ("Buyers", forces.buyer_power),
                      ("Substitutes", forces.threat_of_substitutes),
                      ("Entrants", forces.threat_of_new_entrants),
                      ("Rivalry", forces.competitive_rivalry)]:
        bar = "*" * val + "." * (5 - val)
        click.echo(f"  {name:<12} [{bar}] {val}/5")


@cli.command('profile')
@click.option('--name', '-n', required=True, help='Competitor name')
@click.option('--positioning', '-pos', default='', help='Positioning statement')
@click.option('--target', '-t', default='', help='Target market')
@click.option('--pricing', '-p', default='', help='Pricing info')
@click.option('--features', '-f', default='', help='Key features (comma-separated)')
@click.option('--strengths', '-s', default='', help='Strengths (comma-separated)')
@click.option('--weaknesses', '-w', default='', help='Weaknesses (comma-separated)')
@click.option('--differentiator', '-d', default='', help='Key differentiator')
@click.option('--output', '-o', type=click.Path(), help='Save to JSON file')
def profile(
    name: str,
    positioning: str,
    target: str,
    pricing: str,
    features: str,
    strengths: str,
    weaknesses: str,
    differentiator: str,
    output: Optional[str]
):
    """Create a competitor profile."""
    profile = CompetitorProfile(
        name=name,
        positioning=positioning,
        target_market=target,
        pricing=pricing,
        features=[f.strip() for f in features.split(',') if f.strip()],
        strengths=[s.strip() for s in strengths.split(',') if s.strip()],
        weaknesses=[w.strip() for w in weaknesses.split(',') if w.strip()],
        differentiator=differentiator
    )

    click.echo("\n  " + "=" * 50)
    click.echo(f"  COMPETITOR PROFILE: {profile.name.upper()}")
    click.echo("  " + "=" * 50)

    if profile.positioning:
        click.echo(f"\n  Positioning: {profile.positioning}")
    if profile.target_market:
        click.echo(f"  Target Market: {profile.target_market}")
    if profile.pricing:
        click.echo(f"  Pricing: {profile.pricing}")

    if profile.features:
        click.echo("\n  Key Features:")
        for f in profile.features:
            click.echo(f"  - {f}")

    if profile.strengths:
        click.echo("\n  Strengths:")
        for s in profile.strengths:
            click.echo(f"  + {s}")

    if profile.weaknesses:
        click.echo("\n  Weaknesses:")
        for w in profile.weaknesses:
            click.echo(f"  - {w}")

    if profile.differentiator:
        click.echo(f"\n  Key Differentiator: {profile.differentiator}")

    if output:
        data = {
            'name': profile.name,
            'positioning': profile.positioning,
            'target_market': profile.target_market,
            'pricing': profile.pricing,
            'features': profile.features,
            'strengths': profile.strengths,
            'weaknesses': profile.weaknesses,
            'differentiator': profile.differentiator
        }
        with open(output, 'w') as f:
            json.dump(data, f, indent=2)
        click.echo(f"\n  Saved to: {output}")


@cli.command('matrix')
@click.argument('competitors_file', type=click.Path(exists=True), required=False)
@click.option('--feature', '-f', multiple=True, help='Features to compare')
def matrix(competitors_file: Optional[str], feature: tuple):
    """Generate competitive comparison matrix.

    Provide a JSON file with array of competitor profiles.
    """
    if not competitors_file:
        click.echo("\n  Competitive Matrix Template")
        click.echo("  " + "=" * 50)
        click.echo("\n  Create a JSON file with this structure:")
        click.echo("""
  {
    "competitors": [
      {
        "name": "Competitor A",
        "pricing": "$99/mo",
        "features": ["Feature 1", "Feature 2"],
        "rating": 4.2
      },
      {
        "name": "Competitor B",
        "pricing": "$149/mo",
        "features": ["Feature 1", "Feature 3"],
        "rating": 4.5
      }
    ],
    "compare_features": ["Feature 1", "Feature 2", "Feature 3"]
  }
        """)
        return

    with open(competitors_file) as f:
        data = json.load(f)

    competitors = data.get('competitors', [])
    compare_features = list(feature) if feature else data.get('compare_features', [])

    if not competitors:
        click.echo("No competitors found in file")
        return

    click.echo("\n  " + "=" * 60)
    click.echo("  COMPETITIVE COMPARISON MATRIX")
    click.echo("  " + "=" * 60)

    # Header
    names = [c['name'][:15] for c in competitors]
    header = f"  {'Feature':<20}" + "".join(f"{n:<16}" for n in names)
    click.echo(f"\n{header}")
    click.echo("  " + "-" * (20 + 16 * len(competitors)))

    # Pricing row
    pricing_row = f"  {'Pricing':<20}"
    for c in competitors:
        pricing_row += f"{c.get('pricing', 'N/A'):<16}"
    click.echo(pricing_row)

    # Feature rows
    if compare_features:
        for feat in compare_features:
            row = f"  {feat[:18]:<20}"
            for c in competitors:
                has_feature = feat in c.get('features', [])
                row += f"{'Yes' if has_feature else 'No':<16}"
            click.echo(row)

    # Rating row if available
    if any('rating' in c for c in competitors):
        rating_row = f"  {'Rating':<20}"
        for c in competitors:
            rating = c.get('rating', 'N/A')
            rating_row += f"{rating:<16}"
        click.echo(rating_row)


if __name__ == "__main__":
    cli()
