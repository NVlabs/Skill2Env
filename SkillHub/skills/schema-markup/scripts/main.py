#!/usr/bin/env python3
"""Schema Markup Generator - Create JSON-LD structured data."""

import click
import json
from datetime import datetime
from pathlib import Path

TEMPLATES = {
    'article': {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': '',
        'author': {'@type': 'Person', 'name': ''},
        'datePublished': '',
        'publisher': {'@type': 'Organization', 'name': '', 'logo': {'@type': 'ImageObject', 'url': ''}}
    },
    'product': {
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': '',
        'description': '',
        'offers': {'@type': 'Offer', 'price': '', 'priceCurrency': 'USD', 'availability': 'https://schema.org/InStock'}
    },
    'organization': {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': '',
        'url': '',
        'logo': '',
        'sameAs': []
    },
    'faq': {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': []
    },
    'breadcrumb': {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': []
    }
}

@click.group()
def cli():
    """Schema Markup Generator - JSON-LD for SEO."""
    pass

@cli.command()
@click.option('--type', '-t', 'schema_type', required=True,
              type=click.Choice(['article', 'product', 'organization', 'faq', 'breadcrumb']))
@click.option('--title', help='Title/headline')
@click.option('--name', help='Name')
@click.option('--author', help='Author name')
@click.option('--price', type=float, help='Price')
@click.option('--url', help='URL')
@click.option('--description', help='Description')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def generate(schema_type: str, title: str, name: str, author: str,
             price: float, url: str, description: str, output: str):
    """Generate JSON-LD schema."""
    click.echo(f"\n  Schema Generator: {schema_type}")
    click.echo("  " + "=" * 40)

    schema = TEMPLATES[schema_type].copy()

    if schema_type == 'article':
        schema['headline'] = title or name or 'Article Title'
        schema['author']['name'] = author or 'Author Name'
        schema['datePublished'] = datetime.now().strftime('%Y-%m-%d')
        schema['publisher']['name'] = 'Publisher Name'

    elif schema_type == 'product':
        schema['name'] = name or title or 'Product Name'
        schema['description'] = description or 'Product description'
        schema['offers']['price'] = str(price) if price else '0'

    elif schema_type == 'organization':
        schema['name'] = name or 'Organization Name'
        schema['url'] = url or 'https://example.com'

    json_output = json.dumps(schema, indent=2)

    click.echo("\n  Generated Schema:")
    click.echo("  " + "-" * 40)
    click.echo(json_output)

    click.echo("\n  HTML Usage:")
    click.echo('  <script type="application/ld+json">')
    click.echo(f'  {json_output}')
    click.echo('  </script>')

    if output:
        Path(output).write_text(json_output)
        click.echo(f"\n  Saved: {output}")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def validate(file: str):
    """Validate JSON-LD schema."""
    click.echo("\n  Schema Validator")
    click.echo("  " + "=" * 40)

    try:
        content = Path(file).read_text()
        schema = json.loads(content)

        issues = []

        if '@context' not in schema:
            issues.append('Missing @context')
        if '@type' not in schema:
            issues.append('Missing @type')

        if issues:
            click.echo("  ✗ Issues found:")
            for issue in issues:
                click.echo(f"    - {issue}")
        else:
            click.echo("  ✓ Schema is valid")
            click.echo(f"  Type: {schema.get('@type')}")

    except json.JSONDecodeError as e:
        click.echo(f"  ✗ Invalid JSON: {e}")

@cli.command()
def templates():
    """Show available schema templates."""
    click.echo("\n  Available Schema Templates")
    click.echo("  " + "=" * 40)

    for name, template in TEMPLATES.items():
        click.echo(f"\n  {name}:")
        click.echo(f"    Type: {template.get('@type')}")

if __name__ == "__main__":
    cli()
