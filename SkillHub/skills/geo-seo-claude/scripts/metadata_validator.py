#!/usr/bin/env python3
"""
SEO/GEO Metadata Validator

Validates metadata completeness and correctness for SEO/GEO optimization.
Checks meta tags, Open Graph, Twitter Cards, schema markup, and best practices.

Usage:
    python metadata_validator.py <file_path>
    python metadata_validator.py --help

Requirements:
    Python 3.7+ (stdlib only)

Output:
    JSON with validation results, score, and recommendations
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
import re

# Import analyze_content and shared functions
import sys
from pathlib import Path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from analyze_content import analyze_file
from shared import has_schema_type, LIMITS, SCORES


def validate_meta_title(title: str) -> Dict:
    """Validate meta title"""
    issues = []
    recommendations = []
    score = 100

    if not title:
        issues.append("CRITICAL: Missing meta title")
        score = 0
    else:
        length = len(title)

        if length < 30:
            issues.append(f"Meta title too short ({length} chars, should be 50-60)")
            score -= 30
        elif length > 60:
            issues.append(f"Meta title too long ({length} chars, will be truncated at ~60)")
            score -= 20
        elif 50 <= length <= 60:
            recommendations.append(f"✅ Perfect title length ({length} chars)")
            score += 10

        # Check for brand name
        if '|' not in title and '-' not in title:
            recommendations.append("Consider adding brand name separator (| or -)")

        # Check for keyword stuffing
        words = title.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 3:
                word_counts[word] = word_counts.get(word, 0) + 1

        repeated = [word for word, count in word_counts.items() if count > 1]
        if repeated:
            issues.append(f"Potential keyword stuffing: {', '.join(repeated)}")
            score -= 10

    return {
        'title': title,
        'length': len(title) if title else 0,
        'score': max(0, min(100, score)),
        'issues': issues,
        'recommendations': recommendations
    }


def validate_meta_description(description: str) -> Dict:
    """Validate meta description"""
    issues = []
    recommendations = []
    score = 100

    if not description:
        issues.append("CRITICAL: Missing meta description")
        score = 0
    else:
        length = len(description)

        if length < 100:
            issues.append(f"Meta description too short ({length} chars, should be 150-160)")
            score -= 30
        elif length > 160:
            issues.append(f"Meta description too long ({length} chars, will be truncated)")
            score -= 20
        elif 150 <= length <= 160:
            recommendations.append(f"✅ Perfect description length ({length} chars)")
            score += 10

        # Check for call-to-action
        cta_words = ['learn', 'discover', 'get', 'find', 'explore', 'read', 'see']
        has_cta = any(word in description.lower() for word in cta_words)
        if has_cta:
            recommendations.append("✅ Contains call-to-action")
        else:
            recommendations.append("Consider adding call-to-action (Learn, Discover, Get)")

    return {
        'description': description,
        'length': len(description) if description else 0,
        'score': max(0, min(100, score)),
        'issues': issues,
        'recommendations': recommendations
    }


def validate_open_graph(og: Dict) -> Dict:
    """Validate Open Graph tags"""
    issues = []
    recommendations = []
    score = 100

    required = ['title', 'description', 'image', 'url', 'type']
    missing = [field for field in required if not og.get(field)]

    if missing:
        issues.append(f"Missing required OG tags: {', '.join(missing)}")
        score -= 20 * len(missing)

    # Validate og:title
    if og.get('title'):
        if len(og['title']) > 90:
            issues.append(f"og:title too long ({len(og['title'])} chars, max ~88)")
            score -= 10

    # Validate og:description
    if og.get('description'):
        if len(og['description']) > 200:
            issues.append(f"og:description too long ({len(og['description'])} chars, max ~200)")
            score -= 10

    # Validate og:image
    if og.get('image'):
        if not og['image'].startswith('http'):
            issues.append("og:image must be absolute URL (https://example.com/image.jpg)")
            score -= 15
        recommendations.append("✅ og:image present")
        recommendations.append("Verify image is 1200×630px for optimal display (Facebook, LinkedIn, WhatsApp)")
        recommendations.append("Instagram: OG tags only work in Stories link stickers (not feed posts)")
    else:
        issues.append("CRITICAL: Missing og:image (no Facebook/LinkedIn/WhatsApp/Instagram Stories preview)")
        score -= 30

    # Validate og:url
    if og.get('url'):
        if not og['url'].startswith('http'):
            issues.append("og:url must be absolute URL")
            score -= 10

    # Validate og:type
    if og.get('type'):
        valid_types = ['website', 'article', 'video.movie', 'video.episode', 'music.song']
        if og['type'] not in valid_types:
            recommendations.append(f"og:type '{og['type']}' is valid but uncommon")

    # Check for optional but useful tags
    if not og.get('site_name'):
        recommendations.append("Consider adding og:site_name for branding")

    if og.get('type') == 'article':
        if not og.get('article:published_time'):
            recommendations.append("Add article:published_time for article type")
        if not og.get('article:author'):
            recommendations.append("Add article:author for E-E-A-T")

    return {
        'tags': og,
        'score': max(0, min(100, score)),
        'issues': issues,
        'recommendations': recommendations
    }


def validate_twitter_cards(twitter: Dict) -> Dict:
    """Validate Twitter Card tags"""
    issues = []
    recommendations = []
    score = 100

    required = ['card', 'title', 'description', 'image']
    missing = [field for field in required if not twitter.get(field)]

    if missing:
        issues.append(f"Missing Twitter Card tags: {', '.join(missing)}")
        score -= 20 * len(missing)

    # Validate card type
    if twitter.get('card'):
        valid_cards = ['summary', 'summary_large_image', 'app', 'player']
        if twitter['card'] not in valid_cards:
            issues.append(f"Invalid twitter:card value: {twitter['card']}")
            score -= 15
        elif twitter['card'] == 'summary':
            recommendations.append("Consider using 'summary_large_image' for better engagement")
        elif twitter['card'] == 'summary_large_image':
            recommendations.append("✅ Using summary_large_image (recommended)")

    # Validate image
    if twitter.get('image'):
        if not twitter['image'].startswith('http'):
            issues.append("twitter:image must be absolute URL")
            score -= 15
        recommendations.append("Verify image is 1200×628px for large card")
    else:
        issues.append("CRITICAL: Missing twitter:image (no Twitter/X preview)")
        score -= 30

    # Check for creator/site
    if not twitter.get('site') and not twitter.get('creator'):
        recommendations.append("Add twitter:site or twitter:creator for attribution")

    if twitter.get('site'):
        if not twitter['site'].startswith('@'):
            issues.append("twitter:site should include @ (e.g., @username)")
            score -= 5
        else:
            recommendations.append(f"✅ Twitter site attributed: {twitter['site']}")

    return {
        'tags': twitter,
        'score': max(0, min(100, score)),
        'issues': issues,
        'recommendations': recommendations
    }


def validate_schema_markup(schemas: List) -> Dict:
    """Validate JSON-LD schema markup"""
    issues = []
    recommendations = []
    score = 100

    if not schemas:
        issues.append("No JSON-LD schema found")
        recommendations.append("Add FAQ schema (highest AI citation probability)")
        recommendations.append("Add Article schema for E-E-A-T signals")
        score = 0
    else:
        # Check for FAQ schema
        if has_schema_type(schemas, 'FAQPage'):
            recommendations.append("✅ FAQ schema present (highest citation probability)")
        else:
            recommendations.append("Add FAQ schema for Q&A content (35% citation boost)")

        # Check for Article schema
        if has_schema_type(schemas, 'Article'):
            recommendations.append("✅ Article schema present")

            # Check for E-E-A-T signals
            for schema in schemas:
                if isinstance(schema, dict) and schema.get('@type') == 'Article':
                    if schema.get('author'):
                        author = schema['author']
                        if isinstance(author, dict):
                            if author.get('honorificSuffix'):
                                recommendations.append("✅ Author credentials present (40% citation boost)")
                            else:
                                recommendations.append("Add author honorificSuffix (MD, PhD) for 40% boost")

                            if author.get('affiliation'):
                                recommendations.append("✅ Author affiliation present")
                            else:
                                recommendations.append("Add author affiliation for E-E-A-T")

                    if schema.get('dateModified'):
                        recommendations.append("✅ dateModified present (critical for Perplexity)")
                    else:
                        recommendations.append("Add dateModified for freshness signals")

                    if schema.get('speakable'):
                        recommendations.append("✅ Speakable schema present (voice search optimized)")
                    else:
                        recommendations.append("Add Speakable schema for voice search optimization")
        else:
            recommendations.append("Add Article schema with E-E-A-T signals")

        # Check for HowTo schema (if applicable)
        if has_schema_type(schemas, 'HowTo'):
            recommendations.append("✅ HowTo schema present (voice search friendly)")

        # Validate JSON structure
        for i, schema in enumerate(schemas):
            if isinstance(schema, dict):
                if not schema.get('@context'):
                    issues.append(f"Schema #{i+1}: Missing @context")
                    score -= 10
                if not schema.get('@type'):
                    issues.append(f"Schema #{i+1}: Missing @type")
                    score -= 10

    return {
        'schema_count': len(schemas),
        'schemas': schemas,
        'score': max(0, min(100, score)),
        'issues': issues,
        'recommendations': recommendations
    }


def validate_content_structure(content: Dict) -> Dict:
    """Validate content structure for AI optimization"""
    issues = []
    recommendations = []
    score = 100

    # TL;DR check
    if not content.get('has_tldr'):
        issues.append("Missing TL;DR in first 60 words (35% citation boost)")
        score -= 25
        recommendations.append("Add TL;DR: direct answer in first 40-60 words")
    else:
        recommendations.append("✅ TL;DR present (35% citation boost)")

    # Heading structure
    h1_count = content.get('h1_count', 0)
    if h1_count == 0:
        issues.append("CRITICAL: No H1 heading found")
        score -= 30
    elif h1_count > 1:
        issues.append(f"Multiple H1 headings ({h1_count}), should have exactly 1")
        score -= 15
    else:
        recommendations.append("✅ Single H1 heading (correct structure)")

    h2_count = content.get('h2_count', 0)
    if h2_count < 2:
        issues.append(f"Too few H2 headings ({h2_count}), need at least 2-3 for structure")
        score -= 15
    elif h2_count >= 3:
        recommendations.append(f"✅ Good H2 structure ({h2_count} headings)")

    # FAQ check
    if not content.get('has_faq'):
        recommendations.append("Consider adding FAQ section for voice search")
    else:
        recommendations.append("✅ FAQ section present (voice search ready)")

    # Author attribution
    if not content.get('has_author'):
        issues.append("No author attribution found (40% citation boost with credentials)")
        score -= 20
        recommendations.append("Add author byline with full name and credentials")
    else:
        if not content.get('has_credentials'):
            recommendations.append("Author found but no credentials (MD, PhD) - add for 40% boost")
        else:
            recommendations.append("✅ Author with credentials (40% citation boost)")

    # Word count
    word_count = content.get('word_count', 0)
    if word_count < 300:
        issues.append(f"Content too short ({word_count} words, minimum 300 recommended)")
        score -= 20
    elif word_count >= 800:
        recommendations.append(f"✅ Comprehensive content ({word_count} words)")

    return {
        'word_count': word_count,
        'structure': {
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': content.get('h3_count', 0),
            'has_tldr': content.get('has_tldr', False),
            'has_faq': content.get('has_faq', False),
            'has_author': content.get('has_author', False),
            'has_credentials': content.get('has_credentials', False)
        },
        'score': max(0, min(100, score)),
        'issues': issues,
        'recommendations': recommendations
    }


def calculate_overall_score(validation_results: Dict) -> int:
    """Calculate weighted overall score"""

    weights = {
        'meta_title': 0.15,
        'meta_description': 0.15,
        'open_graph': 0.20,
        'twitter_cards': 0.15,
        'schema': 0.20,
        'content_structure': 0.15
    }

    weighted_score = 0
    for key, weight in weights.items():
        if key in validation_results:
            weighted_score += validation_results[key]['score'] * weight

    return int(weighted_score)


def get_score_grade(score: int) -> str:
    """Convert score to letter grade"""
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Good"
    elif score >= 70:
        return "Fair"
    elif score >= 60:
        return "Poor"
    else:
        return "Critical"


def validate_metadata(file_path: str) -> Dict:
    """Main validation function"""

    # First analyze file with analyze_content
    analysis = analyze_file(file_path)

    if 'error' in analysis:
        return analysis

    # Run detailed validations
    validation_results = {
        'file': file_path,
        'file_type': analysis.get('file_type'),
        'meta_title': validate_meta_title(analysis['meta'].get('title')),
        'meta_description': validate_meta_description(analysis['meta'].get('description')),
        'open_graph': validate_open_graph(analysis['open_graph']),
        'twitter_cards': validate_twitter_cards(analysis['twitter_cards']),
        'schema': validate_schema_markup(analysis['schema']),
        'content_structure': validate_content_structure(analysis['content'])
    }

    # Calculate overall score
    overall_score = calculate_overall_score(validation_results)
    grade = get_score_grade(overall_score)

    # Collect all issues and recommendations
    all_issues = []
    all_recommendations = []

    for key, result in validation_results.items():
        if key not in ['file', 'file_type']:
            all_issues.extend(result.get('issues', []))
            all_recommendations.extend(result.get('recommendations', []))

    # Priority categorization
    critical_issues = [i for i in all_issues if 'CRITICAL' in i]
    regular_issues = [i for i in all_issues if 'CRITICAL' not in i]

    validation_results['summary'] = {
        'overall_score': overall_score,
        'grade': grade,
        'critical_issues': len(critical_issues),
        'total_issues': len(all_issues),
        'recommendations': len(all_recommendations)
    }

    validation_results['issues'] = {
        'critical': critical_issues,
        'regular': regular_issues
    }

    validation_results['recommendations'] = all_recommendations

    return validation_results


def main():
    """Main entry point"""

    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print(__doc__)
        print("\nExamples:")
        print("  python metadata_validator.py ~/project/about.html")
        print("  python metadata_validator.py ~/blog/post.md")
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    file_path = sys.argv[1]

    try:
        validation = validate_metadata(file_path)

        # Pretty print JSON
        print(json.dumps(validation, indent=2, ensure_ascii=False))

        # Exit code based on score
        if 'error' in validation:
            sys.exit(1)
        elif validation['summary']['overall_score'] < 60:
            sys.exit(2)  # Poor SEO
        else:
            sys.exit(0)  # Good SEO

    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'file': file_path
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
