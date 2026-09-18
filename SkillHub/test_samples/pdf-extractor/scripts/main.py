#!/usr/bin/env python3
"""
PDF Extractor - Extract text, tables, and images from PDFs.

Usage:
    python main.py text document.pdf
    python main.py tables report.pdf --output tables.csv
    python main.py images presentation.pdf --output ./images/
    python main.py merge doc1.pdf doc2.pdf --output combined.pdf
"""

import click
from pathlib import Path
from typing import Optional
import csv


def parse_page_range(pages_str: str, max_pages: int) -> list:
    """Parse page range string like '1,3-5,10' into list of page numbers."""
    pages = []
    for part in pages_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start), min(int(end) + 1, max_pages + 1)))
        else:
            page = int(part)
            if page <= max_pages:
                pages.append(page)
    return sorted(set(pages))


@click.group()
def cli():
    """PDF Extractor - Text, tables, and images from PDFs."""
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--pages', '-p', help='Page range (e.g., 1-5,10)')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def text(file: str, pages: Optional[str], output: Optional[str]):
    """Extract text from PDF."""
    try:
        import pdfplumber
    except ImportError:
        click.echo("Error: pdfplumber not installed")
        click.echo("Run: pip install pdfplumber")
        return

    input_path = Path(file)

    click.echo("\n  PDF Text Extraction")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")

    with pdfplumber.open(input_path) as pdf:
        total_pages = len(pdf.pages)
        click.echo(f"  Pages: {total_pages}")

        if pages:
            page_list = parse_page_range(pages, total_pages)
            click.echo(f"  Extracting: pages {page_list}")
        else:
            page_list = list(range(1, total_pages + 1))

        all_text = []
        for page_num in page_list:
            page = pdf.pages[page_num - 1]  # 0-indexed
            page_text = page.extract_text() or ''
            all_text.append(f"--- Page {page_num} ---\n{page_text}")

    full_text = '\n\n'.join(all_text)

    # Word count
    word_count = len(full_text.split())
    click.echo(f"  Words: {word_count:,}")

    # Output
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.with_suffix('.txt')

    output_path.write_text(full_text)
    click.echo(f"\n  [Done] Saved: {output_path}")

    # Preview
    click.echo("\n  Preview:")
    click.echo("  " + "-" * 40)
    click.echo("  " + full_text[:500].replace('\n', '\n  ') + "...")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--page', '-p', type=int, help='Specific page number')
@click.option('--output', '-o', type=click.Path(), help='Output CSV file')
def tables(file: str, page: Optional[int], output: Optional[str]):
    """Extract tables from PDF."""
    try:
        import pdfplumber
    except ImportError:
        click.echo("Error: pdfplumber not installed")
        return

    input_path = Path(file)

    click.echo("\n  PDF Table Extraction")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")

    all_tables = []

    with pdfplumber.open(input_path) as pdf:
        pages_to_process = [pdf.pages[page - 1]] if page else pdf.pages

        for i, pg in enumerate(pages_to_process, start=page or 1):
            page_tables = pg.extract_tables()
            for j, table in enumerate(page_tables):
                if table and len(table) > 0:
                    all_tables.append({
                        'page': i,
                        'table_num': j + 1,
                        'data': table
                    })

    click.echo(f"  Found: {len(all_tables)} tables")

    if not all_tables:
        click.echo("  No tables found in document")
        return

    # Output directory
    output_dir = Path(output).parent if output else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save each table
    for t in all_tables:
        table_file = output_dir / f"table_page{t['page']}_{t['table_num']}.csv"
        with open(table_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in t['data']:
                writer.writerow(row)
        click.echo(f"  -> {table_file.name} ({len(t['data'])} rows)")

    # Combined output if specified
    if output:
        combined_data = []
        for t in all_tables:
            for row in t['data']:
                combined_data.append([t['page'], t['table_num']] + row)

        with open(output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['page', 'table'] + [f'col{i}' for i in range(len(combined_data[0]) - 2)])
            writer.writerows(combined_data)
        click.echo(f"\n  Combined: {output}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), default='./pdf_images',
              help='Output directory')
def images(file: str, output: str):
    """Extract images from PDF."""
    try:
        import pdfplumber
    except ImportError:
        click.echo("Error: pdfplumber required")
        click.echo("Run: pip install pdfplumber")
        return

    input_path = Path(file)
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

    click.echo("\n  PDF Image Extraction")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Output: {output_dir}")

    image_count = 0

    with pdfplumber.open(input_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            page_images = page.images
            for img_num, img in enumerate(page_images, 1):
                # Extract image data if available
                try:
                    # pdfplumber images are metadata; for actual extraction
                    # we need to use the underlying PDF structure
                    image_count += 1
                    click.echo(f"  Found image on page {page_num}")
                except Exception:
                    pass

    # Alternative: render pages as images
    click.echo("\n  Rendering pages as images...")
    with pdfplumber.open(input_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            img = page.to_image(resolution=150)
            img_path = output_dir / f"page_{page_num:03d}.png"
            img.save(img_path)
            click.echo(f"  -> {img_path.name}")
            image_count += 1

    click.echo(f"\n  [Done] Saved {image_count} images to {output_dir}")


@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--output', '-o', required=True, type=click.Path(), help='Output file')
def merge(files: tuple, output: str):
    """Merge multiple PDFs into one."""
    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        click.echo("Error: pypdf not installed")
        click.echo("Run: pip install pypdf")
        return

    if len(files) < 2:
        click.echo("Error: Need at least 2 PDFs to merge")
        return

    click.echo("\n  PDF Merge")
    click.echo("  " + "=" * 40)

    writer = PdfWriter()
    total_pages = 0

    for file_path in files:
        click.echo(f"  Adding: {Path(file_path).name}")
        reader = PdfReader(file_path)
        for page in reader.pages:
            writer.add_page(page)
            total_pages += 1

    output_path = Path(output)
    with open(output_path, 'wb') as f:
        writer.write(f)

    click.echo(f"\n  [Done] Merged {len(files)} files ({total_pages} pages)")
    click.echo(f"  Output: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
def info(file: str):
    """Display PDF information."""
    try:
        from pypdf import PdfReader
    except ImportError:
        click.echo("Error: pypdf not installed")
        return

    input_path = Path(file)
    reader = PdfReader(input_path)

    click.echo("\n  PDF Information")
    click.echo("  " + "=" * 40)
    click.echo(f"  File: {input_path.name}")
    click.echo(f"  Size: {input_path.stat().st_size / 1024:.1f} KB")
    click.echo(f"  Pages: {len(reader.pages)}")

    # Metadata
    meta = reader.metadata
    if meta:
        click.echo("\n  Metadata")
        click.echo("  " + "-" * 40)
        if meta.title:
            click.echo(f"  Title: {meta.title}")
        if meta.author:
            click.echo(f"  Author: {meta.author}")
        if meta.creator:
            click.echo(f"  Creator: {meta.creator}")
        if meta.creation_date:
            click.echo(f"  Created: {meta.creation_date}")


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def batch(folder: str, output: Optional[str]):
    """Batch convert all PDFs in folder to text."""
    try:
        import pdfplumber
    except ImportError:
        click.echo("Error: pdfplumber not installed")
        return

    input_dir = Path(folder)
    output_dir = Path(output) if output else input_dir / 'text_output'
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = list(input_dir.glob('*.pdf'))

    click.echo("\n  Batch PDF Conversion")
    click.echo("  " + "=" * 40)
    click.echo(f"  Found: {len(pdfs)} PDFs")
    click.echo(f"  Output: {output_dir}")

    for pdf_path in pdfs:
        click.echo(f"\n  Processing: {pdf_path.name}")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_text = []
                for page in pdf.pages:
                    text = page.extract_text() or ''
                    all_text.append(text)

                output_path = output_dir / pdf_path.with_suffix('.txt').name
                output_path.write_text('\n\n'.join(all_text))
                click.echo(f"  -> {output_path.name}")
        except Exception as e:
            click.echo(f"  Error: {e}")

    click.echo(f"\n  [Done] Converted {len(pdfs)} PDFs")


if __name__ == "__main__":
    cli()
