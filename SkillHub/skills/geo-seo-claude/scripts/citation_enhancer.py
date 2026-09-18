#!/usr/bin/env python3
"""
Citation Enhancer

Identifies opportunities to add statistics and quotations for improved AI citations.
Research shows: Statistics Addition (+41%), Quotation Addition (+28%).

Key checks:
- Paragraphs without quantified data
- Missing expert quotations
- Unsupported claims detection
- Evidence gap analysis
- Citation placement suggestions

Usage:
    python citation_enhancer.py <file_path>
    python citation_enhancer.py <file_path> --json
    python citation_enhancer.py --help

Requirements:
    Python 3.7+ (stdlib only)

Output:
    JSON with citation opportunities and recommendations
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Import shared utilities
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from shared import PATTERNS, SCORES, count_words, clean_html_text


# Claim indicator words that often need supporting evidence
CLAIM_INDICATORS = [
    'best', 'worst', 'most', 'least', 'always', 'never', 'everyone', 'nobody',
    'proven', 'guaranteed', 'scientifically', 'research shows', 'studies show',
    'experts agree', 'doctors recommend', 'effective', 'safe', 'dangerous',
    'revolutionary', 'breakthrough', 'leading', 'top-rated', 'award-winning',
    'increases', 'decreases', 'improves', 'reduces', 'prevents', 'causes',
    'significant', 'dramatically', 'substantially', 'considerably',
]

# Patterns that indicate existing evidence
EVIDENCE_PATTERNS = [
    r'\d+(?:\.\d+)?%',                    # Percentages
    r'\d{1,3}(?:,\d{3})+',                # Large numbers with commas
    r'\$\d+(?:,\d{3})*(?:\.\d{2})?',      # Currency
    r'\d+(?:\.\d+)?x\s',                  # Multipliers (e.g., "3x faster")
    r'according to',                       # Attribution
    r'study (?:shows?|found|reveals?)',    # Study references
    r'research (?:shows?|indicates?)',     # Research references
    r'"[^"]{20,}"',                        # Quotations
    r'\[\d+\]',                            # Citation references
]


def extract_paragraphs(html: str) -> List[Dict]:
    """
    Extract paragraphs with metadata.

    Args:
        html: HTML content

    Returns:
        List of paragraph dicts with text and analysis
    """
    paragraphs = []

    # Extract paragraph content
    p_matches = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)

    for i, p_html in enumerate(p_matches):
        # Clean HTML tags
        text = clean_html_text(p_html)

        if not text or len(text) < 20:
            continue

        word_count = count_words(text)

        # Check for existing evidence
        has_numbers = bool(re.search(r'\d+', text))
        has_percentage = bool(re.search(r'\d+(?:\.\d+)?%', text))
        has_quotation = bool(re.search(r'"[^"]{15,}"', text))
        has_citation = bool(re.search(r'\[\d+\]', text))
        has_attribution = bool(re.search(r'according to|research shows?|study shows?', text, re.IGNORECASE))

        evidence_score = sum([
            has_numbers * 20,
            has_percentage * 30,
            has_quotation * 25,
            has_citation * 30,
            has_attribution * 20,
        ])

        paragraphs.append({
            'index': i + 1,
            'text': text[:200] + ('...' if len(text) > 200 else ''),
            'word_count': word_count,
            'has_numbers': has_numbers,
            'has_percentage': has_percentage,
            'has_quotation': has_quotation,
            'has_citation': has_citation,
            'has_attribution': has_attribution,
            'evidence_score': min(100, evidence_score)
        })

    return paragraphs


def detect_unsupported_claims(paragraphs: List[Dict]) -> List[Dict]:
    """
    Detect claims that lack supporting evidence.

    Args:
        paragraphs: List of paragraph dicts

    Returns:
        List of unsupported claim findings
    """
    claims = []

    for para in paragraphs:
        text_lower = para['text'].lower()

        # Check for claim indicators
        found_claims = []
        for indicator in CLAIM_INDICATORS:
            if indicator in text_lower:
                found_claims.append(indicator)

        # If claims found but low evidence score
        if found_claims and para['evidence_score'] < 30:
            claims.append({
                'paragraph': para['index'],
                'claim_indicators': found_claims[:3],
                'evidence_score': para['evidence_score'],
                'text_preview': para['text'][:100],
                'suggestion': 'Add quantified data or expert citation to support claims'
            })

    return claims


def identify_statistic_opportunities(paragraphs: List[Dict]) -> List[Dict]:
    """
    Identify paragraphs that would benefit from statistics.

    Research shows statistics addition improves citations by 41%.

    Args:
        paragraphs: List of paragraph dicts

    Returns:
        List of statistic opportunity findings
    """
    opportunities = []

    for para in paragraphs:
        # Skip short paragraphs or those with numbers
        if para['word_count'] < 20 or para['has_numbers']:
            continue

        # Check if paragraph makes claims without numbers
        text_lower = para['text'].lower()

        claim_patterns = [
            (r'\b(?:many|most|some|few|several)\s+(?:people|users|customers|patients)', 'quantify audience'),
            (r'\b(?:increase|decrease|improve|reduce|grow|decline)', 'add percentage or number'),
            (r'\b(?:fast|slow|quick|efficient|effective)', 'add time or efficiency metric'),
            (r'\b(?:save|cost|spend|invest|earn)', 'add monetary value'),
            (r'\b(?:more|less|better|worse)\s+than', 'add comparative statistic'),
        ]

        for pattern, suggestion in claim_patterns:
            if re.search(pattern, text_lower):
                opportunities.append({
                    'paragraph': para['index'],
                    'type': 'statistic',
                    'suggestion': f'Add quantified data: {suggestion}',
                    'text_preview': para['text'][:100],
                    'impact': f'+{SCORES["citation_boosts"]["statistics"]}% citation improvement'
                })
                break

    return opportunities


def identify_quotation_opportunities(html: str, paragraphs: List[Dict]) -> List[Dict]:
    """
    Identify opportunities to add expert quotations.

    Research shows quotation addition improves citations by 28%.

    Args:
        html: Original HTML content
        paragraphs: List of paragraph dicts

    Returns:
        List of quotation opportunity findings
    """
    opportunities = []

    # Check if content has any blockquotes
    has_blockquotes = '<blockquote' in html.lower()

    # Check if content has any quotations
    has_any_quotes = bool(re.search(r'"[^"]{20,}"', html))

    # Content should have at least one quotation
    if not has_blockquotes and not has_any_quotes and len(paragraphs) > 3:
        opportunities.append({
            'type': 'quotation',
            'location': 'main content',
            'suggestion': 'Add expert quotation from authority figure',
            'examples': [
                '"According to Dr. [Name], [Specialty], \'[Quote].\'"',
                '"As [Expert Name] explains, \'[Quote].\'"',
                '<blockquote>"[Quote]" - [Expert], [Title]</blockquote>'
            ],
            'impact': f'+{SCORES["citation_boosts"]["quotations"]}% citation improvement'
        })

    # Check for specific sections that benefit from quotes
    sections_needing_quotes = [
        ('about', 'founder or CEO quote'),
        ('services', 'client testimonial'),
        ('treatment', 'physician quote'),
        ('product', 'expert review quote'),
    ]

    html_lower = html.lower()
    for section, quote_type in sections_needing_quotes:
        if section in html_lower and not has_any_quotes:
            opportunities.append({
                'type': 'quotation',
                'location': f'{section} section',
                'suggestion': f'Add {quote_type} for credibility',
                'impact': f'+{SCORES["citation_boosts"]["quotations"]}% citation improvement'
            })
            break

    return opportunities


def analyze_evidence_gaps(paragraphs: List[Dict]) -> Dict:
    """
    Analyze overall evidence coverage.

    Args:
        paragraphs: List of paragraph dicts

    Returns:
        Evidence gap analysis dict
    """
    if not paragraphs:
        return {
            'total_paragraphs': 0,
            'paragraphs_with_evidence': 0,
            'evidence_coverage': 0,
            'average_evidence_score': 0
        }

    with_evidence = len([p for p in paragraphs if p['evidence_score'] >= 30])
    total = len(paragraphs)
    avg_score = sum(p['evidence_score'] for p in paragraphs) / total

    return {
        'total_paragraphs': total,
        'paragraphs_with_evidence': with_evidence,
        'evidence_coverage': round((with_evidence / total) * 100, 1),
        'average_evidence_score': round(avg_score, 1),
        'paragraphs_needing_evidence': [
            p['index'] for p in paragraphs if p['evidence_score'] < 30 and p['word_count'] >= 20
        ][:5]
    }


def calculate_citation_score(
    paragraphs: List[Dict],
    unsupported_claims: List[Dict],
    stat_opportunities: List[Dict],
    quote_opportunities: List[Dict]
) -> int:
    """
    Calculate overall citation readiness score.

    Args:
        paragraphs: List of paragraph dicts
        unsupported_claims: List of unsupported claims
        stat_opportunities: List of statistic opportunities
        quote_opportunities: List of quotation opportunities

    Returns:
        Score 0-100
    """
    if not paragraphs:
        return 0

    score = 100

    # Deduct for unsupported claims
    score -= min(30, len(unsupported_claims) * 5)

    # Deduct for missing statistics
    score -= min(25, len(stat_opportunities) * 3)

    # Deduct for missing quotations
    score -= min(15, len(quote_opportunities) * 5)

    # Bonus for high evidence coverage
    with_evidence = len([p for p in paragraphs if p['evidence_score'] >= 30])
    coverage = with_evidence / len(paragraphs)
    if coverage >= 0.7:
        score += 10

    return max(0, min(100, score))


def analyze_citations(file_path: str) -> Dict:
    """
    Main citation analysis function.

    Args:
        file_path: Path to HTML file

    Returns:
        Analysis results dict
    """
    path = Path(file_path)

    if not path.exists():
        return {
            'success': False,
            'error': f'File not found: {file_path}'
        }

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Extract and analyze paragraphs
    paragraphs = extract_paragraphs(html)

    # Find opportunities
    unsupported_claims = detect_unsupported_claims(paragraphs)
    stat_opportunities = identify_statistic_opportunities(paragraphs)
    quote_opportunities = identify_quotation_opportunities(html, paragraphs)

    # Analyze evidence gaps
    evidence_gaps = analyze_evidence_gaps(paragraphs)

    # Calculate score
    score = calculate_citation_score(
        paragraphs,
        unsupported_claims,
        stat_opportunities,
        quote_opportunities
    )

    # Compile all opportunities
    all_opportunities = []
    for opp in stat_opportunities[:5]:
        all_opportunities.append(opp)
    for opp in quote_opportunities[:3]:
        all_opportunities.append(opp)

    return {
        'success': True,
        'file': file_path,
        'citation_score': score,
        'opportunities_count': len(all_opportunities),
        'opportunities': all_opportunities,
        'unsupported_claims': unsupported_claims[:5],
        'evidence_analysis': evidence_gaps,
        'recommendations': generate_recommendations(
            score, unsupported_claims, stat_opportunities, quote_opportunities
        ),
        'note': 'User must provide real statistics and quotes (no fabrication)',
        'timestamp': datetime.now().isoformat()
    }


def generate_recommendations(
    score: int,
    unsupported_claims: List[Dict],
    stat_opportunities: List[Dict],
    quote_opportunities: List[Dict]
) -> List[str]:
    """
    Generate citation recommendations.

    Args:
        score: Citation score
        unsupported_claims: List of unsupported claims
        stat_opportunities: List of statistic opportunities
        quote_opportunities: List of quotation opportunities

    Returns:
        List of recommendations
    """
    recommendations = []

    if unsupported_claims:
        recommendations.append(
            f"Add evidence to {len(unsupported_claims)} paragraphs with unsupported claims"
        )

    if stat_opportunities:
        recommendations.append(
            f"Add statistics to {len(stat_opportunities)} paragraphs "
            f"(+{SCORES['citation_boosts']['statistics']}% citation boost)"
        )

    if quote_opportunities:
        recommendations.append(
            f"Add {len(quote_opportunities)} expert quotations "
            f"(+{SCORES['citation_boosts']['quotations']}% citation boost)"
        )

    if score >= 80:
        recommendations.append("Citation coverage is good - consider adding case studies")
    elif score >= 60:
        recommendations.append("Moderate citation coverage - prioritize adding statistics")
    else:
        recommendations.append("Low citation coverage - significant improvement opportunity")

    return recommendations


def main():
    """Main entry point"""

    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print(__doc__)
        print("\nExamples:")
        print("  python citation_enhancer.py page.html")
        print("  python citation_enhancer.py page.html --json")
        sys.exit(0 if '--help' in sys.argv else 1)

    file_path = sys.argv[1]
    json_output = '--json' in sys.argv or len(sys.argv) == 2

    try:
        result = analyze_citations(file_path)

        if json_output:
            print(json.dumps(result, indent=2))
        else:
            if result['success']:
                print(f"Citation Analysis: {file_path}")
                print(f"{'=' * 50}")
                print(f"Score: {result['citation_score']}/100")
                print(f"Opportunities: {result['opportunities_count']}")

                if result['opportunities']:
                    print("\nTop Opportunities:")
                    for opp in result['opportunities'][:5]:
                        print(f"  - [{opp['type'].upper()}] {opp['suggestion']}")
                        print(f"    Impact: {opp.get('impact', 'N/A')}")

                if result['recommendations']:
                    print("\nRecommendations:")
                    for rec in result['recommendations']:
                        print(f"  {rec}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)

        sys.exit(0 if result['success'] else 1)

    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
