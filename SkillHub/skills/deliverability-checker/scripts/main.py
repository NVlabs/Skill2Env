#!/usr/bin/env python3
"""
Email Deliverability Checker - Check SPF, DKIM, DMARC, and MX records.

Usage:
    python main.py audit example.com
    python main.py spf example.com
    python main.py dkim example.com --selector google
    python main.py dmarc example.com
"""

import click
from typing import Optional
import dns.resolver


def check_dns_record(domain: str, record_type: str) -> list:
    """Query DNS records."""
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        return []
    except Exception:
        return []


def check_mx(domain: str) -> dict:
    """Check MX records."""
    records = check_dns_record(domain, 'MX')

    provider = "Unknown"
    if records:
        mx_str = ' '.join(records).lower()
        if 'google' in mx_str or 'gmail' in mx_str:
            provider = "Google Workspace"
        elif 'outlook' in mx_str or 'microsoft' in mx_str:
            provider = "Microsoft 365"
        elif 'zoho' in mx_str:
            provider = "Zoho Mail"
        elif 'protonmail' in mx_str:
            provider = "ProtonMail"

    return {
        'valid': len(records) > 0,
        'records': records,
        'provider': provider
    }


def check_spf(domain: str) -> dict:
    """Check SPF record."""
    txt_records = check_dns_record(domain, 'TXT')

    spf_record = None
    for record in txt_records:
        if 'v=spf1' in record:
            spf_record = record.strip('"')
            break

    if not spf_record:
        return {'valid': False, 'record': None, 'issues': ['No SPF record found']}

    issues = []
    includes = []

    # Parse includes
    parts = spf_record.split()
    for part in parts:
        if part.startswith('include:'):
            includes.append(part.replace('include:', ''))

    # Check policy
    if '~all' in spf_record:
        policy = 'softfail'
        issues.append('Using ~all (softfail) - consider -all for stricter policy')
    elif '-all' in spf_record:
        policy = 'hardfail'
    elif '+all' in spf_record:
        policy = 'pass'
        issues.append('CRITICAL: +all allows anyone to send - very insecure')
    elif '?all' in spf_record:
        policy = 'neutral'
        issues.append('Using ?all (neutral) - provides no protection')
    else:
        policy = 'unknown'

    return {
        'valid': True,
        'record': spf_record,
        'includes': includes,
        'policy': policy,
        'issues': issues
    }


def check_dkim(domain: str, selector: str) -> dict:
    """Check DKIM record."""
    dkim_domain = f"{selector}._domainkey.{domain}"
    txt_records = check_dns_record(dkim_domain, 'TXT')

    if not txt_records:
        return {
            'valid': False,
            'selector': selector,
            'record': None,
            'issues': [f'No DKIM record found for selector "{selector}"']
        }

    record = ' '.join(txt_records).replace('" "', '').strip('"')

    issues = []
    if 'p=' not in record:
        issues.append('Missing public key (p=)')

    return {
        'valid': 'p=' in record,
        'selector': selector,
        'record': record[:100] + '...' if len(record) > 100 else record,
        'issues': issues
    }


def check_dmarc(domain: str) -> dict:
    """Check DMARC record."""
    dmarc_domain = f"_dmarc.{domain}"
    txt_records = check_dns_record(dmarc_domain, 'TXT')

    dmarc_record = None
    for record in txt_records:
        if 'v=DMARC1' in record:
            dmarc_record = record.strip('"')
            break

    if not dmarc_record:
        return {
            'valid': False,
            'record': None,
            'policy': None,
            'issues': ['No DMARC record found'],
            'suggested': f'v=DMARC1; p=none; rua=mailto:dmarc@{domain}'
        }

    # Parse policy
    policy = 'none'
    if 'p=reject' in dmarc_record:
        policy = 'reject'
    elif 'p=quarantine' in dmarc_record:
        policy = 'quarantine'
    elif 'p=none' in dmarc_record:
        policy = 'none'

    issues = []
    if policy == 'none':
        issues.append('Policy is "none" - consider "quarantine" or "reject" for enforcement')
    if 'rua=' not in dmarc_record:
        issues.append('No aggregate report address (rua=) configured')

    return {
        'valid': True,
        'record': dmarc_record,
        'policy': policy,
        'issues': issues
    }


def calculate_score(mx: dict, spf: dict, dkim: dict, dmarc: dict) -> int:
    """Calculate deliverability score."""
    score = 0

    if mx['valid']:
        score += 20
    if spf['valid']:
        score += 25
        if spf.get('policy') == 'hardfail':
            score += 5
    if dkim['valid']:
        score += 25
    if dmarc['valid']:
        score += 25
        if dmarc.get('policy') in ['quarantine', 'reject']:
            score += 5

    return min(score, 100)


@click.group()
def cli():
    """Email Deliverability Checker - SPF, DKIM, DMARC, MX."""
    pass


@cli.command()
@click.argument('domain')
@click.option('--selector', '-s', default='google', help='DKIM selector')
@click.option('--output', '-o', type=click.Path(), help='Output HTML report')
def audit(domain: str, selector: str, output: Optional[str]):
    """Full email deliverability audit."""
    click.echo(f"\n  Email Deliverability Audit: {domain}")
    click.echo("  " + "=" * 45)

    # Run checks
    mx = check_mx(domain)
    spf = check_spf(domain)
    dkim = check_dkim(domain, selector)
    dmarc = check_dmarc(domain)

    score = calculate_score(mx, spf, dkim, dmarc)

    # Display results
    click.echo(f"  MX Records:      {'✓' if mx['valid'] else '✗'} {'Found (' + mx['provider'] + ')' if mx['valid'] else 'Missing'}")
    click.echo(f"  SPF:             {'✓' if spf['valid'] else '✗'} {'Valid' if spf['valid'] else 'Missing'}")
    click.echo(f"  DKIM ({selector}): {'✓' if dkim['valid'] else '✗'} {'Valid' if dkim['valid'] else 'Missing'}")
    click.echo(f"  DMARC:           {'✓' if dmarc['valid'] else '✗'} {'Valid' if dmarc['valid'] else 'Missing'}")

    click.echo(f"\n  Score: {score}/100")

    # Collect issues
    all_issues = []
    if not mx['valid']:
        all_issues.append(('CRITICAL', 'No MX records found - domain cannot receive email'))
    if not spf['valid']:
        all_issues.append(('HIGH', 'No SPF record - emails may be rejected'))
    else:
        for issue in spf.get('issues', []):
            all_issues.append(('MEDIUM', f'SPF: {issue}'))
    if not dkim['valid']:
        all_issues.append(('HIGH', f'No DKIM for selector "{selector}" - try different selector'))
    if not dmarc['valid']:
        all_issues.append(('CRITICAL', 'No DMARC record - enables spoofing'))
        all_issues.append(('FIX', f'Add: {dmarc.get("suggested", "")}'))
    else:
        for issue in dmarc.get('issues', []):
            all_issues.append(('MEDIUM', f'DMARC: {issue}'))

    if all_issues:
        click.echo("\n  Issues Found:")
        for severity, issue in all_issues:
            click.echo(f"  [{severity}] {issue}")

    if output:
        # Generate HTML report
        html = generate_html_report(domain, mx, spf, dkim, dmarc, score, all_issues)
        with open(output, 'w') as f:
            f.write(html)
        click.echo(f"\n  Report saved: {output}")


@cli.command()
@click.argument('domain')
def spf(domain: str):
    """Check SPF record."""
    click.echo(f"\n  SPF Analysis: {domain}")
    click.echo("  " + "=" * 40)

    result = check_spf(domain)

    if result['valid']:
        click.echo("  Status: ✓ Valid")
        click.echo(f"  Record: {result['record']}")
        click.echo(f"  Policy: {result['policy']}")

        if result['includes']:
            click.echo("\n  Authorized Senders:")
            for inc in result['includes']:
                click.echo(f"    - {inc}")

        if result['issues']:
            click.echo("\n  Warnings:")
            for issue in result['issues']:
                click.echo(f"    ⚠ {issue}")
    else:
        click.echo("  Status: ✗ Missing")
        click.echo("  Suggested: v=spf1 include:_spf.google.com ~all")


@cli.command()
@click.argument('domain')
@click.option('--selector', '-s', default='google', help='DKIM selector')
def dkim(domain: str, selector: str):
    """Check DKIM record."""
    click.echo(f"\n  DKIM Analysis: {domain}")
    click.echo("  " + "=" * 40)
    click.echo(f"  Selector: {selector}")

    result = check_dkim(domain, selector)

    if result['valid']:
        click.echo("  Status: ✓ Valid")
        click.echo(f"  Record: {result['record']}")
    else:
        click.echo("  Status: ✗ Not Found")
        click.echo("\n  Common selectors to try:")
        for sel in ['google', 'selector1', 'selector2', 's1', 's2', 'default', 'k1']:
            click.echo(f"    - {sel}")


@cli.command()
@click.argument('domain')
def dmarc(domain: str):
    """Check DMARC record."""
    click.echo(f"\n  DMARC Analysis: {domain}")
    click.echo("  " + "=" * 40)

    result = check_dmarc(domain)

    if result['valid']:
        click.echo("  Status: ✓ Valid")
        click.echo(f"  Record: {result['record']}")
        click.echo(f"  Policy: {result['policy']}")

        if result['issues']:
            click.echo("\n  Recommendations:")
            for issue in result['issues']:
                click.echo(f"    ⚠ {issue}")
    else:
        click.echo("  Status: ✗ Missing")
        click.echo("\n  Suggested record:")
        click.echo(f"  {result['suggested']}")


@cli.command()
@click.argument('domain')
def mx(domain: str):
    """Check MX records."""
    click.echo(f"\n  MX Records: {domain}")
    click.echo("  " + "=" * 40)

    result = check_mx(domain)

    if result['valid']:
        click.echo("  Status: ✓ Found")
        click.echo(f"  Provider: {result['provider']}")
        click.echo("\n  Records:")
        for record in result['records']:
            click.echo(f"    {record}")
    else:
        click.echo("  Status: ✗ No MX records found")


def generate_html_report(domain, mx, spf, dkim, dmarc, score, issues):
    """Generate HTML audit report."""
    from datetime import datetime
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Email Deliverability Report - {domain}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        .score {{ font-size: 3em; text-align: center; color: {'#28a745' if score >= 80 else '#ffc107' if score >= 50 else '#dc3545'}; }}
        .check {{ margin: 15px 0; padding: 15px; background: #f5f5f5; border-radius: 8px; }}
        .valid {{ border-left: 4px solid #28a745; }}
        .invalid {{ border-left: 4px solid #dc3545; }}
        .issue {{ padding: 10px; margin: 5px 0; background: #fff3cd; border-radius: 4px; }}
        .critical {{ background: #f8d7da; }}
    </style>
</head>
<body>
    <h1>Email Deliverability Report</h1>
    <p><strong>Domain:</strong> {domain}</p>
    <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

    <div class="score">{score}/100</div>

    <div class="check {'valid' if mx['valid'] else 'invalid'}">
        <h3>{'✓' if mx['valid'] else '✗'} MX Records</h3>
        <p>Provider: {mx['provider']}</p>
    </div>

    <div class="check {'valid' if spf['valid'] else 'invalid'}">
        <h3>{'✓' if spf['valid'] else '✗'} SPF</h3>
        <p>{spf.get('record', 'Not configured')}</p>
    </div>

    <div class="check {'valid' if dkim['valid'] else 'invalid'}">
        <h3>{'✓' if dkim['valid'] else '✗'} DKIM</h3>
        <p>Selector: {dkim['selector']}</p>
    </div>

    <div class="check {'valid' if dmarc['valid'] else 'invalid'}">
        <h3>{'✓' if dmarc['valid'] else '✗'} DMARC</h3>
        <p>{dmarc.get('record', 'Not configured')}</p>
    </div>

    <h2>Issues</h2>
    {''.join(f'<div class="issue {("critical" if s=="CRITICAL" else "")}">[{s}] {i}</div>' for s, i in issues)}
</body>
</html>"""


if __name__ == "__main__":
    cli()
