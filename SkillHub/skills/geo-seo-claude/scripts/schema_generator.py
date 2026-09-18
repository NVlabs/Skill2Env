#!/usr/bin/env python3
"""
JSON-LD Schema Generator

Generates valid JSON-LD schema markup for SEO/GEO optimization.
Supports: FAQ, Article, HowTo, BreadcrumbList, Organization, Person, Speakable

Usage:
    python schema_generator.py faq --questions "Q1:A1" "Q2:A2"
    python schema_generator.py article --title "..." --author "..." --date "2025-01-15"
    python schema_generator.py --help

Requirements:
    Python 3.7+ (stdlib only)

Output:
    Valid JSON-LD schema ready to embed in <script type="application/ld+json">
"""

import json
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Optional


def generate_faq_schema(questions: List[Dict[str, str]]) -> str:
    """
    Generate FAQPage schema (highest AI citation probability)

    Args:
        questions: List of {'question': str, 'answer': str}

    Returns:
        JSON-LD string

    Example:
        >>> questions = [
        ...     {'question': 'What is SEO?', 'answer': 'Search Engine Optimization...'},
        ...     {'question': 'What is GEO?', 'answer': 'Generative Engine Optimization...'}
        ... ]
        >>> print(generate_faq_schema(questions))
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q['question'],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": q['answer']
                }
            }
            for q in questions
        ]
    }

    return json.dumps(schema, indent=2, ensure_ascii=False)


def generate_article_schema(
    headline: str,
    description: str,
    date_published: str,
    date_modified: Optional[str] = None,
    author_name: Optional[str] = None,
    author_job_title: Optional[str] = None,
    author_credentials: Optional[str] = None,
    author_url: Optional[str] = None,
    organization_name: Optional[str] = None,
    organization_url: Optional[str] = None,
    article_url: Optional[str] = None,
    image_url: Optional[str] = None,
    word_count: Optional[int] = None,
    keywords: Optional[List[str]] = None
) -> str:
    """
    Generate Article schema with E-E-A-T signals (40% citation boost with credentials)

    Args:
        headline: Article title
        description: Brief description
        date_published: ISO 8601 date (e.g., "2025-01-15")
        date_modified: ISO 8601 date (optional, defaults to date_published)
        author_name: Author full name
        author_job_title: e.g., "Board-Certified Physician"
        author_credentials: e.g., "MD, PhD, FAAD"
        author_url: Author profile URL
        organization_name: Publisher name
        organization_url: Publisher URL
        article_url: Article canonical URL
        image_url: Article image URL
        word_count: Article word count
        keywords: List of keywords

    Returns:
        JSON-LD string
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "datePublished": date_published,
        "dateModified": date_modified or date_published
    }

    # Author (E-E-A-T signal)
    if author_name:
        schema["author"] = {
            "@type": "Person",
            "name": author_name
        }
        if author_job_title:
            schema["author"]["jobTitle"] = author_job_title
        if author_credentials:
            schema["author"]["honorificSuffix"] = author_credentials
        if author_url:
            schema["author"]["url"] = author_url

    # Publisher (required for Article)
    if organization_name and organization_url:
        schema["publisher"] = {
            "@type": "Organization",
            "name": organization_name,
            "url": organization_url
        }

    # Main entity (canonical URL)
    if article_url:
        schema["mainEntityOfPage"] = {
            "@type": "WebPage",
            "@id": article_url
        }

    # Speakable (voice search optimization)
    schema["speakable"] = {
        "@type": "SpeakableSpecification",
        "cssSelector": [".article-summary", ".article-intro", "h1", "h2"]
    }

    # Optional metadata
    if image_url:
        schema["image"] = {
            "@type": "ImageObject",
            "url": image_url
        }

    if word_count:
        schema["wordCount"] = word_count

    if keywords:
        schema["keywords"] = ", ".join(keywords)

    return json.dumps(schema, indent=2, ensure_ascii=False)


def generate_howto_schema(
    name: str,
    description: str,
    estimated_time: str,
    steps: List[Dict[str, str]]
) -> str:
    """
    Generate HowTo schema (voice search optimized)

    Args:
        name: Title of the how-to
        description: Brief description
        estimated_time: ISO 8601 duration (e.g., "PT5M" for 5 minutes, "PT1H" for 1 hour)
        steps: List of {'name': str, 'text': str}

    Returns:
        JSON-LD string

    Example:
        >>> steps = [
        ...     {'name': 'Step 1: Prepare', 'text': 'Gather all materials needed...'},
        ...     {'name': 'Step 2: Execute', 'text': 'Follow the process carefully...'}
        ... ]
        >>> print(generate_howto_schema('How to Optimize SEO', 'Guide...', 'PT15M', steps))
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "totalTime": estimated_time,
        "step": [
            {
                "@type": "HowToStep",
                "name": step['name'],
                "text": step['text']
            }
            for step in steps
        ]
    }

    return json.dumps(schema, indent=2, ensure_ascii=False)


def generate_breadcrumb_schema(items: List[Dict[str, str]]) -> str:
    """
    Generate BreadcrumbList schema (site hierarchy for search engines)

    Args:
        items: List of {'name': str, 'url': str}

    Returns:
        JSON-LD string

    Example:
        >>> items = [
        ...     {'name': 'Home', 'url': 'https://example.com/'},
        ...     {'name': 'Blog', 'url': 'https://example.com/blog'},
        ...     {'name': 'Article', 'url': 'https://example.com/blog/article'}
        ... ]
        >>> print(generate_breadcrumb_schema(items))
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item['name'],
                "item": item['url']
            }
            for i, item in enumerate(items)
        ]
    }

    return json.dumps(schema, indent=2, ensure_ascii=False)


def generate_organization_schema(
    name: str,
    org_type: str,
    url: str,
    logo: Optional[str] = None,
    description: Optional[str] = None,
    address_street: Optional[str] = None,
    address_city: Optional[str] = None,
    address_state: Optional[str] = None,
    address_zip: Optional[str] = None,
    address_country: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None
) -> str:
    """
    Generate Organization/LocalBusiness schema (entity recognition, Knowledge Graph)

    Args:
        name: Organization name
        org_type: Type (e.g., "Organization", "MedicalBusiness", "ProfessionalService")
        url: Organization website URL
        logo: Logo image URL
        description: Organization description
        address_*: Address components
        phone: Phone number
        email: Email address

    Returns:
        JSON-LD string
    """
    schema = {
        "@context": "https://schema.org",
        "@type": org_type,
        "name": name,
        "url": url
    }

    if logo:
        schema["logo"] = logo

    if description:
        schema["description"] = description

    # Address
    if any([address_street, address_city, address_state, address_zip, address_country]):
        schema["address"] = {
            "@type": "PostalAddress"
        }
        if address_street:
            schema["address"]["streetAddress"] = address_street
        if address_city:
            schema["address"]["addressLocality"] = address_city
        if address_state:
            schema["address"]["addressRegion"] = address_state
        if address_zip:
            schema["address"]["postalCode"] = address_zip
        if address_country:
            schema["address"]["addressCountry"] = address_country

    # Contact
    if phone:
        schema["telephone"] = phone
    if email:
        schema["email"] = email

    return json.dumps(schema, indent=2, ensure_ascii=False)


def generate_person_schema(
    name: str,
    job_title: Optional[str] = None,
    credentials: Optional[str] = None,
    url: Optional[str] = None,
    image: Optional[str] = None,
    description: Optional[str] = None,
    organization_name: Optional[str] = None
) -> str:
    """
    Generate Person schema (author profiles, E-E-A-T)

    Args:
        name: Person full name
        job_title: e.g., "Board-Certified Physician"
        credentials: e.g., "MD, PhD, FAAD"
        url: Profile URL
        image: Profile image URL
        description: Bio description
        organization_name: Affiliated organization

    Returns:
        JSON-LD string
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": name
    }

    if job_title:
        schema["jobTitle"] = job_title

    if credentials:
        schema["honorificSuffix"] = credentials

    if url:
        schema["url"] = url

    if image:
        schema["image"] = image

    if description:
        schema["description"] = description

    if organization_name:
        schema["worksFor"] = {
            "@type": "Organization",
            "name": organization_name
        }

    return json.dumps(schema, indent=2, ensure_ascii=False)


def main():
    """Main entry point with CLI"""

    parser = argparse.ArgumentParser(
        description='Generate JSON-LD schema markup for SEO/GEO optimization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # FAQ Schema
  python schema_generator.py faq --questions "What is SEO?:SEO is..." "What is GEO?:GEO is..."

  # Article Schema
  python schema_generator.py article \\
    --title "Complete SEO Guide" \\
    --description "Learn SEO basics..." \\
    --date "2025-01-15" \\
    --author "Dr. John Smith" \\
    --author-credentials "MD, PhD" \\
    --author-title "Medical Director" \\
    --org-name "Health Clinic" \\
    --org-url "https://example.com" \\
    --article-url "https://example.com/blog/seo-guide"

  # HowTo Schema
  python schema_generator.py howto \\
    --name "How to Optimize for Voice Search" \\
    --description "Step by step guide..." \\
    --time "PT15M" \\
    --steps "Prepare:Gather materials..." "Execute:Follow process..."

  # Organization Schema
  python schema_generator.py organization \\
    --name "Medical Clinic" \\
    --type "MedicalBusiness" \\
    --url "https://example.com" \\
    --city "San Francisco" \\
    --state "CA"
""")

    subparsers = parser.add_subparsers(dest='schema_type', help='Schema type to generate')

    # FAQ Schema
    faq_parser = subparsers.add_parser('faq', help='Generate FAQ schema')
    faq_parser.add_argument('--questions', nargs='+', required=True,
                            help='Question:Answer pairs (e.g., "What is SEO?:SEO is...")')

    # Article Schema
    article_parser = subparsers.add_parser('article', help='Generate Article schema')
    article_parser.add_argument('--title', required=True, help='Article title')
    article_parser.add_argument('--description', required=True, help='Article description')
    article_parser.add_argument('--date', required=True, help='Publication date (YYYY-MM-DD)')
    article_parser.add_argument('--date-modified', help='Last modified date (YYYY-MM-DD)')
    article_parser.add_argument('--author', help='Author name')
    article_parser.add_argument('--author-title', help='Author job title')
    article_parser.add_argument('--author-credentials', help='Author credentials (MD, PhD)')
    article_parser.add_argument('--author-url', help='Author profile URL')
    article_parser.add_argument('--org-name', help='Organization name')
    article_parser.add_argument('--org-url', help='Organization URL')
    article_parser.add_argument('--article-url', help='Article canonical URL')
    article_parser.add_argument('--image', help='Article image URL')
    article_parser.add_argument('--word-count', type=int, help='Word count')
    article_parser.add_argument('--keywords', nargs='+', help='Keywords')

    # HowTo Schema
    howto_parser = subparsers.add_parser('howto', help='Generate HowTo schema')
    howto_parser.add_argument('--name', required=True, help='HowTo title')
    howto_parser.add_argument('--description', required=True, help='HowTo description')
    howto_parser.add_argument('--time', required=True, help='Estimated time (ISO 8601, e.g., PT15M)')
    howto_parser.add_argument('--steps', nargs='+', required=True,
                              help='Steps as Name:Text pairs')

    # Breadcrumb Schema
    breadcrumb_parser = subparsers.add_parser('breadcrumb', help='Generate Breadcrumb schema')
    breadcrumb_parser.add_argument('--items', nargs='+', required=True,
                                   help='Items as Name:URL pairs')

    # Organization Schema
    org_parser = subparsers.add_parser('organization', help='Generate Organization schema')
    org_parser.add_argument('--name', required=True, help='Organization name')
    org_parser.add_argument('--type', default='Organization', help='Organization type')
    org_parser.add_argument('--url', required=True, help='Organization URL')
    org_parser.add_argument('--logo', help='Logo URL')
    org_parser.add_argument('--description', help='Description')
    org_parser.add_argument('--street', help='Street address')
    org_parser.add_argument('--city', help='City')
    org_parser.add_argument('--state', help='State/Region')
    org_parser.add_argument('--zip', help='ZIP/Postal code')
    org_parser.add_argument('--country', help='Country')
    org_parser.add_argument('--phone', help='Phone number')
    org_parser.add_argument('--email', help='Email address')

    # Person Schema
    person_parser = subparsers.add_parser('person', help='Generate Person schema')
    person_parser.add_argument('--name', required=True, help='Person name')
    person_parser.add_argument('--title', help='Job title')
    person_parser.add_argument('--credentials', help='Credentials (MD, PhD)')
    person_parser.add_argument('--url', help='Profile URL')
    person_parser.add_argument('--image', help='Profile image URL')
    person_parser.add_argument('--description', help='Bio description')
    person_parser.add_argument('--org', help='Organization name')

    args = parser.parse_args()

    if not args.schema_type:
        parser.print_help()
        sys.exit(1)

    try:
        if args.schema_type == 'faq':
            questions = []
            for q in args.questions:
                if ':' in q:
                    question, answer = q.split(':', 1)
                    questions.append({'question': question.strip(), 'answer': answer.strip()})
            schema = generate_faq_schema(questions)

        elif args.schema_type == 'article':
            schema = generate_article_schema(
                headline=args.title,
                description=args.description,
                date_published=args.date,
                date_modified=args.date_modified,
                author_name=args.author,
                author_job_title=args.author_title,
                author_credentials=args.author_credentials,
                author_url=args.author_url,
                organization_name=args.org_name,
                organization_url=args.org_url,
                article_url=args.article_url,
                image_url=args.image,
                word_count=args.word_count,
                keywords=args.keywords
            )

        elif args.schema_type == 'howto':
            steps = []
            for s in args.steps:
                if ':' in s:
                    name, text = s.split(':', 1)
                    steps.append({'name': name.strip(), 'text': text.strip()})
            schema = generate_howto_schema(
                name=args.name,
                description=args.description,
                estimated_time=args.time,
                steps=steps
            )

        elif args.schema_type == 'breadcrumb':
            items = []
            for item in args.items:
                if ':' in item:
                    name, url = item.split(':', 1)
                    items.append({'name': name.strip(), 'url': url.strip()})
            schema = generate_breadcrumb_schema(items)

        elif args.schema_type == 'organization':
            schema = generate_organization_schema(
                name=args.name,
                org_type=args.type,
                url=args.url,
                logo=args.logo,
                description=args.description,
                address_street=args.street,
                address_city=args.city,
                address_state=args.state,
                address_zip=args.zip,
                address_country=args.country,
                phone=args.phone,
                email=args.email
            )

        elif args.schema_type == 'person':
            schema = generate_person_schema(
                name=args.name,
                job_title=args.title,
                credentials=args.credentials,
                url=args.url,
                image=args.image,
                description=args.description,
                organization_name=args.org
            )

        else:
            print(f"Unknown schema type: {args.schema_type}", file=sys.stderr)
            sys.exit(1)

        print(schema)
        sys.exit(0)

    except Exception as e:
        print(f"Error generating schema: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
