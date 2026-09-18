#!/usr/bin/env python3
"""Link Checker - Find broken links on websites."""

import click
from typing import Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0)'}

def check_url(url: str, timeout: int = 10) -> tuple:
    """Check if URL is accessible."""
    try:
        response = requests.head(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return url, response.status_code, None
    except requests.RequestException as e:
        return url, 0, str(e)[:50]

def get_links(url: str) -> list:
    """Extract all links from page."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith(('http', '/')) and not href.startswith('#'):
                full_url = urljoin(url, href)
                links.append(full_url)
        return list(set(links))
    except Exception:
        return []

@click.group()
def cli():
    """Link Checker - Find broken links."""
    pass

@cli.command()
@click.argument('url')
@click.option('--depth', '-d', default=1, help='Crawl depth')
@click.option('--output', '-o', type=click.Path(), help='Output CSV file')
def check(url: str, depth: int, output: Optional[str]):
    """Check website for broken links."""
    click.echo("\n  Link Checker")
    click.echo("  " + "=" * 40)
    click.echo(f"  URL: {url}")
    click.echo(f"  Depth: {depth}")

    base_domain = urlparse(url).netloc
    all_links = set()
    checked = set()
    broken = []

    to_crawl = [url]
    current_depth = 0

    while to_crawl and current_depth <= depth:
        click.echo(f"\n  Depth {current_depth}: checking {len(to_crawl)} pages...")
        next_crawl = []

        for page_url in to_crawl:
            if page_url in checked:
                continue
            checked.add(page_url)

            links = get_links(page_url)
            for link in links:
                all_links.add((page_url, link))
                if urlparse(link).netloc == base_domain and link not in checked:
                    next_crawl.append(link)

        to_crawl = next_crawl[:50]  # Limit per depth
        current_depth += 1

    click.echo(f"\n  Found {len(all_links)} links. Checking...")

    unique_urls = list(set(link for _, link in all_links))

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_url, url): url for url in unique_urls}
        results = {}
        for future in as_completed(futures):
            url_checked, status, error = future.result()
            results[url_checked] = (status, error)
            if status >= 400 or status == 0:
                broken.append((url_checked, status, error))

    click.echo("\n  Results")
    click.echo("  " + "-" * 40)
    click.echo(f"  Total links: {len(unique_urls)}")
    click.echo(f"  Broken: {len(broken)}")

    if broken:
        click.echo("\n  Broken Links:")
        for url, status, error in broken[:20]:
            click.echo(f"  ✗ [{status}] {url[:60]}")
            if error:
                click.echo(f"      Error: {error}")

    if output:
        with open(output, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['url', 'status', 'error', 'found_on'])
            for source, link in all_links:
                status, error = results.get(link, (0, 'Not checked'))
                if status >= 400 or status == 0:
                    writer.writerow([link, status, error, source])
        click.echo(f"\n  Saved: {output}")

@cli.command()
@click.argument('url')
@click.option('--output', '-o', required=True, type=click.Path())
def report(url: str, output: str):
    """Generate broken links report."""
    ctx = click.Context(check)
    ctx.invoke(check, url=url, depth=2, output=output)

if __name__ == "__main__":
    cli()
