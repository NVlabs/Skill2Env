#!/usr/bin/env python3
"""Sitemap Generator - Create XML sitemaps."""

import click
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree as ET

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; SitemapBot/1.0)'}

def crawl_site(start_url: str, depth: int = 2) -> set:
    """Crawl site to discover URLs."""
    base_domain = urlparse(start_url).netloc
    found_urls = set()
    to_crawl = [start_url]
    crawled = set()
    current_depth = 0

    while to_crawl and current_depth <= depth:
        next_crawl = []
        for url in to_crawl:
            if url in crawled:
                continue
            crawled.add(url)
            found_urls.add(url)

            try:
                response = requests.get(url, headers=HEADERS, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                for a in soup.find_all('a', href=True):
                    href = a['href']
                    full_url = urljoin(url, href)
                    parsed = urlparse(full_url)

                    if (parsed.netloc == base_domain and
                        full_url not in crawled and
                        not any(x in full_url for x in ['#', '?', '.pdf', '.jpg', '.png'])):
                        next_crawl.append(full_url)
            except Exception:
                pass

        to_crawl = list(set(next_crawl))[:100]
        current_depth += 1

    return found_urls

def generate_sitemap_xml(urls: list, output_path: Path):
    """Generate sitemap XML."""
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    for url in sorted(urls):
        url_elem = ET.SubElement(root, 'url')
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = url
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = 'weekly'
        priority = ET.SubElement(url_elem, 'priority')
        priority.text = '0.8' if '/' == urlparse(url).path else '0.5'

    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

@click.group()
def cli():
    """Sitemap Generator - XML sitemaps for SEO."""
    pass

@cli.command()
@click.argument('url')
@click.option('--depth', '-d', default=2, help='Crawl depth')
@click.option('--output', '-o', default='sitemap.xml', help='Output file')
def generate(url: str, depth: int, output: str):
    """Generate sitemap by crawling website."""
    click.echo("\n  Sitemap Generator")
    click.echo("  " + "=" * 40)
    click.echo(f"  URL: {url}")
    click.echo(f"  Depth: {depth}")

    click.echo("  Crawling...")
    urls = crawl_site(url, depth)

    click.echo(f"  Found: {len(urls)} URLs")

    output_path = Path(output)
    generate_sitemap_xml(list(urls), output_path)

    click.echo(f"\n  [Done] Saved: {output_path}")
    click.echo("\n  Sample URLs:")
    for u in list(urls)[:10]:
        click.echo(f"    • {u}")

@cli.command('from-urls')
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', default='sitemap.xml', help='Output file')
def from_urls(file: str, output: str):
    """Generate sitemap from URL list."""
    urls = [line.strip() for line in Path(file).read_text().splitlines() if line.strip()]

    click.echo(f"\n  Creating sitemap from {len(urls)} URLs")

    output_path = Path(output)
    generate_sitemap_xml(urls, output_path)

    click.echo(f"  [Done] Saved: {output_path}")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def validate(file: str):
    """Validate sitemap XML."""
    click.echo("\n  Sitemap Validator")
    click.echo("  " + "=" * 40)

    try:
        tree = ET.parse(file)
        root = tree.getroot()

        # Count URLs
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('.//sm:url', ns) or root.findall('.//url')

        click.echo("  ✓ Valid XML")
        click.echo(f"  URLs: {len(urls)}")

        # Check for issues
        for url_elem in urls[:5]:
            loc = url_elem.find('sm:loc', ns) or url_elem.find('loc')
            if loc is not None:
                click.echo(f"    • {loc.text}")

    except ET.ParseError as e:
        click.echo(f"  ✗ Invalid XML: {e}")

if __name__ == "__main__":
    cli()
