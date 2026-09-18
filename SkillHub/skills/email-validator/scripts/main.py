#!/usr/bin/env python3
"""Email Validator - Validate and clean email lists."""

import click
from pathlib import Path
from typing import Optional
import re
import csv
import dns.resolver

DISPOSABLE_DOMAINS = {
    'tempmail.com', 'throwaway.email', 'guerrillamail.com', '10minutemail.com',
    'mailinator.com', 'yopmail.com', 'temp-mail.org', 'fakeinbox.com'
}

def validate_email_format(email: str) -> tuple:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, None
    return False, "Invalid format"

def check_mx_record(domain: str) -> bool:
    """Check if domain has MX records."""
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except Exception:
        return False

def is_disposable(email: str) -> bool:
    """Check if email is from disposable domain."""
    domain = email.split('@')[-1].lower()
    return domain in DISPOSABLE_DOMAINS

def validate_email(email: str, check_mx: bool = True) -> dict:
    """Full email validation."""
    email = email.strip().lower()
    result = {'email': email, 'valid': False, 'issues': []}

    # Format check
    valid, error = validate_email_format(email)
    if not valid:
        result['issues'].append(error)
        return result

    domain = email.split('@')[-1]

    # Disposable check
    if is_disposable(email):
        result['issues'].append("Disposable domain")

    # MX record check
    if check_mx and not check_mx_record(domain):
        result['issues'].append("No MX records")

    result['valid'] = len(result['issues']) == 0
    return result

@click.group()
def cli():
    """Email Validator - Clean and validate email lists."""
    pass

@cli.command()
@click.argument('email')
@click.option('--check-mx/--no-check-mx', default=True, help='Check MX records')
def validate(email: str, check_mx: bool):
    """Validate a single email address."""
    click.echo("\n  Email Validator")
    click.echo("  " + "=" * 40)
    click.echo(f"  Email: {email}")

    result = validate_email(email, check_mx)

    if result['valid']:
        click.echo("\n  ✓ Valid email address")
    else:
        click.echo("\n  ✗ Invalid email address")
        for issue in result['issues']:
            click.echo(f"    - {issue}")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--column', '-c', default='email', help='Email column name')
@click.option('--output', '-o', type=click.Path(), help='Output file')
@click.option('--check-mx/--no-check-mx', default=False, help='Check MX records')
def batch(file: str, column: str, output: Optional[str], check_mx: bool):
    """Batch validate emails from CSV."""
    click.echo("\n  Batch Email Validation")
    click.echo("  " + "=" * 40)

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    click.echo(f"  Emails: {len(rows)}")
    click.echo("  Validating...")

    valid_count = 0
    invalid_count = 0
    results = []

    for row in rows:
        email = row.get(column, '').strip()
        if email:
            result = validate_email(email, check_mx)
            row['valid'] = result['valid']
            row['issues'] = '; '.join(result['issues'])
            if result['valid']:
                valid_count += 1
            else:
                invalid_count += 1
            results.append(row)

    click.echo("\n  Results")
    click.echo("  " + "-" * 40)
    click.echo(f"  Valid: {valid_count}")
    click.echo(f"  Invalid: {invalid_count}")
    click.echo(f"  Rate: {valid_count/(valid_count+invalid_count)*100:.1f}%")

    if output:
        with open(output, 'w', newline='') as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
        click.echo(f"\n  Saved: {output}")

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--remove-disposable', is_flag=True, help='Remove disposable emails')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def clean(file: str, remove_disposable: bool, output: Optional[str]):
    """Clean email list (remove invalid/duplicates)."""
    click.echo("\n  Email List Cleaner")
    click.echo("  " + "=" * 40)

    emails = [line.strip().lower() for line in Path(file).read_text().splitlines() if line.strip()]
    original_count = len(emails)

    # Remove duplicates
    emails = list(set(emails))
    after_dedup = len(emails)

    # Validate format
    valid_emails = [e for e in emails if validate_email_format(e)[0]]
    after_format = len(valid_emails)

    # Remove disposable
    if remove_disposable:
        valid_emails = [e for e in valid_emails if not is_disposable(e)]

    final_count = len(valid_emails)

    click.echo("\n  Cleaning Results")
    click.echo("  " + "-" * 40)
    click.echo(f"  Original: {original_count}")
    click.echo(f"  After dedup: {after_dedup} (-{original_count - after_dedup})")
    click.echo(f"  After format check: {after_format} (-{after_dedup - after_format})")
    if remove_disposable:
        click.echo(f"  After disposable removal: {final_count} (-{after_format - final_count})")
    click.echo(f"  Final: {final_count}")

    output_path = Path(output) if output else Path(file).with_stem(f"{Path(file).stem}_clean")
    output_path.write_text('\n'.join(valid_emails))
    click.echo(f"\n  Saved: {output_path}")

if __name__ == "__main__":
    cli()
