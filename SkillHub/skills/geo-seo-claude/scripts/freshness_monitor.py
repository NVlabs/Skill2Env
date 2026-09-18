#!/usr/bin/env python3
"""
Content Freshness Monitor

Analyzes content age and freshness signals for SEO/GEO optimization.
Perplexity AI prioritizes recent content - stale content sees 3.2x fewer citations.

Key checks:
- dateModified schema analysis
- Year/date mentions in content
- Stale statistics detection
- Technology reference age
- Update frequency recommendations

Usage:
    python freshness_monitor.py <file_path>
    python freshness_monitor.py <file_path> --json
    python freshness_monitor.py --help

Requirements:
    Python 3.7+ (stdlib only)

Output:
    JSON with freshness score, issues, and update recommendations
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

# Import shared utilities
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from shared import PATTERNS, FRESHNESS


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse various date formats.

    Args:
        date_str: Date string in various formats

    Returns:
        datetime object or None if parsing fails
    """
    formats = [
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S%z',
        '%B %d, %Y',
        '%b %d, %Y',
        '%d %B %Y',
        '%d %b %Y',
    ]

    # Handle ISO format with timezone
    date_str_clean = date_str.replace('Z', '+00:00')

    for fmt in formats:
        try:
            return datetime.strptime(date_str_clean, fmt)
        except ValueError:
            continue

    # Try ISO format parser
    try:
        return datetime.fromisoformat(date_str_clean.replace('Z', '+00:00')).replace(tzinfo=None)
    except ValueError:
        return None


def extract_dates_from_html(html: str) -> Dict:
    """
    Extract date signals from HTML content.

    Args:
        html: HTML content

    Returns:
        Dict with extracted dates and metadata
    """
    dates = {
        'date_modified': None,
        'date_published': None,
        'last_updated_text': None,
        'year_mentions': []
    }

    # Extract dateModified from JSON-LD
    date_modified_match = PATTERNS['date_modified'].search(html)
    if date_modified_match:
        dates['date_modified'] = date_modified_match.group(1)

    # Extract datePublished from JSON-LD
    date_published_match = re.search(r'"datePublished":\s*"([^"]+)"', html)
    if date_published_match:
        dates['date_published'] = date_published_match.group(1)

    # Extract "Last updated" text patterns
    last_updated_patterns = [
        r'(?:Last\s+)?(?:updated|modified|revised)(?:\s+on)?:\s*([A-Za-z0-9,\s]+\d{4})',
        r'(?:As\s+of)\s+([A-Za-z0-9,\s]+\d{4})',
    ]
    for pattern in last_updated_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            dates['last_updated_text'] = match.group(1).strip()
            break

    # Extract year mentions
    year_matches = PATTERNS['year'].findall(html)
    dates['year_mentions'] = list(set(year_matches))

    return dates


def detect_stale_statistics(html: str) -> List[Dict]:
    """
    Detect potentially stale statistics in content.

    Looks for patterns like "2020 study shows", "According to 2021 data".

    Args:
        html: HTML content

    Returns:
        List of stale statistic findings
    """
    current_year = datetime.now().year
    stale_threshold = current_year - FRESHNESS['stale_year_threshold']
    stale_stats = []

    # Patterns for dated statistics
    patterns = [
        (r'(\d{4})\s+(?:study|research|report|survey|data|statistics)\s+(?:shows?|reveals?|indicates?|found)', 'study/research'),
        (r'(?:according\s+to|based\s+on)\s+(?:a\s+)?(\d{4})\s+(?:study|report|survey|data)', 'citation'),
        (r'(?:in|from|since)\s+(\d{4}),?\s+(?:we|the|our|this|there)', 'temporal reference'),
        (r'(\d{4})\s+(?:edition|version|update)', 'versioned content'),
    ]

    for pattern, stat_type in patterns:
        matches = re.finditer(pattern, html, re.IGNORECASE)
        for match in matches:
            year = int(match.group(1))
            if year < stale_threshold:
                context_start = max(0, match.start() - 30)
                context_end = min(len(html), match.end() + 30)
                context = html[context_start:context_end].strip()

                stale_stats.append({
                    'year': year,
                    'type': stat_type,
                    'context': re.sub(r'<[^>]+>', '', context)[:80],
                    'years_old': current_year - year
                })

    return stale_stats


def detect_outdated_technology(html: str) -> List[Dict]:
    """
    Detect references to outdated technology.

    Args:
        html: HTML content

    Returns:
        List of outdated technology references
    """
    # Technology terms with approximate obsolescence years
    outdated_tech = {
        'Internet Explorer': 2022,
        'IE11': 2022,
        'Flash': 2020,
        'jQuery 1.': 2016,
        'jQuery 2.': 2017,
        'Python 2': 2020,
        'PHP 5': 2018,
        'AngularJS': 2021,  # Angular 1.x
        'Windows 7': 2020,
        'Windows 8': 2023,
        'iOS 12': 2021,
        'iOS 13': 2022,
        'Android 8': 2021,
        'Android 9': 2022,
    }

    findings = []
    html_lower = html.lower()

    for tech, obsolete_year in outdated_tech.items():
        if tech.lower() in html_lower:
            current_year = datetime.now().year
            if current_year >= obsolete_year:
                findings.append({
                    'technology': tech,
                    'obsolete_since': obsolete_year,
                    'years_outdated': current_year - obsolete_year
                })

    return findings


def calculate_freshness_score(
    date_modified: Optional[str],
    stale_stats: List[Dict],
    outdated_tech: List[Dict],
    year_mentions: List[str]
) -> Tuple[int, List[str]]:
    """
    Calculate overall freshness score.

    Args:
        date_modified: dateModified value from schema
        stale_stats: List of stale statistics
        outdated_tech: List of outdated technology references
        year_mentions: List of years mentioned in content

    Returns:
        Tuple of (score, list of issues)
    """
    score = 100
    issues = []
    current_year = datetime.now().year

    # Check dateModified
    if date_modified:
        parsed_date = parse_date(date_modified)
        if parsed_date:
            days_old = (datetime.now() - parsed_date).days
            if days_old > FRESHNESS['max_days_optimal']:
                penalty = min(30, (days_old // 30) * 5)
                score -= penalty
                issues.append(
                    f"Content is {days_old} days old "
                    f"(>30 days = {FRESHNESS['citation_penalty_multiplier']}x fewer citations)"
                )
        else:
            issues.append(f"Invalid dateModified format: {date_modified}")
            score -= 10
    else:
        issues.append("Missing dateModified schema (critical for Perplexity)")
        score -= 20

    # Check stale statistics
    if stale_stats:
        penalty = min(25, len(stale_stats) * 5)
        score -= penalty
        oldest = min(s['year'] for s in stale_stats)
        issues.append(f"{len(stale_stats)} stale statistics found (oldest: {oldest})")

    # Check outdated technology
    if outdated_tech:
        penalty = min(20, len(outdated_tech) * 10)
        score -= penalty
        tech_list = ', '.join(t['technology'] for t in outdated_tech[:3])
        issues.append(f"Outdated technology references: {tech_list}")

    # Check year mentions
    old_years = [int(y) for y in year_mentions if int(y) < current_year - 1]
    if old_years:
        issues.append(f"Contains references to past years: {', '.join(map(str, sorted(old_years)[:5]))}")
        score -= min(10, len(old_years) * 2)

    return max(0, min(100, score)), issues


def generate_recommendations(
    score: int,
    date_modified: Optional[str],
    stale_stats: List[Dict],
    outdated_tech: List[Dict]
) -> List[str]:
    """
    Generate update recommendations based on analysis.

    Args:
        score: Freshness score
        date_modified: dateModified value
        stale_stats: List of stale statistics
        outdated_tech: List of outdated technology

    Returns:
        List of recommendations
    """
    recommendations = []

    if not date_modified:
        recommendations.append("Add dateModified to Article schema (critical for Perplexity AI)")

    if score < 70:
        recommendations.append(
            f"Update content every {FRESHNESS['update_frequency_days']} days for optimal Perplexity visibility"
        )

    if stale_stats:
        recommendations.append(
            f"Update {len(stale_stats)} dated statistics with current data"
        )
        for stat in stale_stats[:3]:
            recommendations.append(f"  → Replace {stat['year']} {stat['type']}: \"{stat['context'][:40]}...\"")

    if outdated_tech:
        for tech in outdated_tech[:3]:
            recommendations.append(
                f"Remove or update reference to {tech['technology']} "
                f"(obsolete since {tech['obsolete_since']})"
            )

    if score >= 90:
        recommendations.append("Content freshness is excellent - maintain regular updates")

    return recommendations


def analyze_freshness(file_path: str) -> Dict:
    """
    Main freshness analysis function.

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

    # Extract dates
    dates = extract_dates_from_html(html)

    # Detect stale content
    stale_stats = detect_stale_statistics(html)
    outdated_tech = detect_outdated_technology(html)

    # Calculate score
    score, issues = calculate_freshness_score(
        dates['date_modified'],
        stale_stats,
        outdated_tech,
        dates['year_mentions']
    )

    # Generate recommendations
    recommendations = generate_recommendations(
        score,
        dates['date_modified'],
        stale_stats,
        outdated_tech
    )

    return {
        'success': True,
        'file': file_path,
        'freshness_score': score,
        'dates': {
            'date_modified': dates['date_modified'],
            'date_published': dates['date_published'],
            'last_updated_text': dates['last_updated_text'],
        },
        'year_mentions': sorted(dates['year_mentions'], reverse=True),
        'stale_statistics': stale_stats,
        'outdated_technology': outdated_tech,
        'issues': issues,
        'recommendations': recommendations,
        'timestamp': datetime.now().isoformat()
    }


def main():
    """Main entry point"""

    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print(__doc__)
        print("\nExamples:")
        print("  python freshness_monitor.py page.html")
        print("  python freshness_monitor.py page.html --json")
        sys.exit(0 if '--help' in sys.argv else 1)

    file_path = sys.argv[1]
    json_output = '--json' in sys.argv or len(sys.argv) == 2

    try:
        result = analyze_freshness(file_path)

        if json_output:
            print(json.dumps(result, indent=2))
        else:
            if result['success']:
                print(f"Freshness Analysis: {file_path}")
                print(f"{'=' * 50}")
                print(f"Score: {result['freshness_score']}/100")

                if result['dates']['date_modified']:
                    print(f"Last Modified: {result['dates']['date_modified']}")

                if result['issues']:
                    print("\nIssues:")
                    for issue in result['issues']:
                        print(f"  - {issue}")

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
