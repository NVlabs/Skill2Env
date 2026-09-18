#!/usr/bin/env python3
"""
Image Batch Processing - Resize, compress, remove backgrounds, watermark.

Usage:
    python main.py resize ./images/ --width 1200
    python main.py compress ./images/ --quality 80
    python main.py remove-bg photo.jpg
    python main.py watermark ./images/ --logo logo.png
    python main.py convert ./images/ --format webp
"""

import click
from pathlib import Path
from typing import Optional
from PIL import Image
import io


SOCIAL_FORMATS = {
    'instagram': (1080, 1080),
    'instagram-story': (1080, 1920),
    'linkedin': (1200, 627),
    'linkedin-post': (1200, 1200),
    'twitter': (1200, 675),
    'facebook': (1200, 630),
    'pinterest': (1000, 1500),
    'youtube': (1280, 720),
}

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff'}


def get_images(path: Path) -> list:
    """Get list of image files from path (file or directory)."""
    if path.is_file():
        return [path] if path.suffix.lower() in IMAGE_EXTENSIONS else []
    return [f for f in path.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS]


def resize_image(img: Image.Image, width: int, height: int, fit: str = 'cover') -> Image.Image:
    """Resize image with specified fit mode."""
    if fit == 'stretch':
        return img.resize((width, height), Image.Resampling.LANCZOS)

    elif fit == 'contain':
        img.thumbnail((width, height), Image.Resampling.LANCZOS)
        # Create new image with padding
        new_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        x = (width - img.width) // 2
        y = (height - img.height) // 2
        new_img.paste(img, (x, y))
        return new_img

    else:  # cover (default)
        # Calculate crop dimensions
        img_ratio = img.width / img.height
        target_ratio = width / height

        if img_ratio > target_ratio:
            # Image is wider, crop sides
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            # Image is taller, crop top/bottom
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))

        return img.resize((width, height), Image.Resampling.LANCZOS)


@click.group()
def cli():
    """Image Batch Processing - Marketing image automation."""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--width', '-w', type=int, help='Target width')
@click.option('--height', '-h', 'height_val', type=int, help='Target height')
@click.option('--format', '-f', 'social_format', type=click.Choice(list(SOCIAL_FORMATS.keys())),
              help='Social media preset')
@click.option('--fit', type=click.Choice(['cover', 'contain', 'stretch']), default='cover')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def resize(path: str, width: Optional[int], height_val: Optional[int],
           social_format: Optional[str], fit: str, output: Optional[str]):
    """Resize images to specified dimensions."""
    input_path = Path(path)
    images = get_images(input_path)

    if not images:
        click.echo("No images found")
        return

    if social_format:
        width, height_val = SOCIAL_FORMATS[social_format]
    elif not (width and height_val):
        if width:
            height_val = width  # Square if only width specified
        else:
            click.echo("Error: Specify --width/--height or --format")
            return

    output_dir = Path(output) if output else input_path if input_path.is_dir() else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    click.echo("\n  Image Resize")
    click.echo("  " + "=" * 40)
    click.echo(f"  Images: {len(images)}")
    click.echo(f"  Target: {width}x{height_val}")
    click.echo(f"  Fit: {fit}")

    for img_path in images:
        img = Image.open(img_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        resized = resize_image(img, width, height_val, fit)

        # Determine output path
        if social_format:
            output_name = f"{img_path.stem}_{social_format}{img_path.suffix}"
        else:
            output_name = f"{img_path.stem}_{width}x{height_val}{img_path.suffix}"

        output_path = output_dir / output_name
        resized.save(output_path)
        click.echo(f"  -> {output_name}")

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Resized {len(images)} images")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--quality', '-q', type=int, default=80, help='Quality (1-100)')
@click.option('--max-size', type=int, help='Maximum file size in KB')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def compress(path: str, quality: int, max_size: Optional[int], output: Optional[str]):
    """Compress images to reduce file size."""
    input_path = Path(path)
    images = get_images(input_path)

    if not images:
        click.echo("No images found")
        return

    output_dir = Path(output) if output else input_path if input_path.is_dir() else input_path.parent

    click.echo("\n  Image Compression")
    click.echo("  " + "=" * 40)
    click.echo(f"  Images: {len(images)}")
    click.echo(f"  Quality: {quality}")
    if max_size:
        click.echo(f"  Max size: {max_size}KB")

    total_before = 0
    total_after = 0

    for img_path in images:
        original_size = img_path.stat().st_size
        total_before += original_size

        img = Image.open(img_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        output_path = output_dir / img_path.name
        current_quality = quality

        if max_size:
            # Iteratively reduce quality to meet size target
            while current_quality > 10:
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=current_quality, optimize=True)
                if buffer.tell() <= max_size * 1024:
                    break
                current_quality -= 5

            buffer.seek(0)
            with open(output_path, 'wb') as f:
                f.write(buffer.read())
        else:
            img.save(output_path, quality=quality, optimize=True)

        new_size = output_path.stat().st_size
        total_after += new_size
        reduction = (1 - new_size / original_size) * 100

        click.echo(f"  {img_path.name}: {original_size//1024}KB -> {new_size//1024}KB ({reduction:.0f}% smaller)")

    overall_reduction = (1 - total_after / total_before) * 100 if total_before else 0
    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Total: {total_before//1024}KB -> {total_after//1024}KB ({overall_reduction:.0f}% reduction)")


@cli.command('remove-bg')
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def remove_bg(path: str, output: Optional[str]):
    """Remove background from images."""
    try:
        from rembg import remove
    except ImportError:
        click.echo("Error: rembg not installed")
        click.echo("Run: pip install rembg")
        return

    input_path = Path(path)
    images = get_images(input_path)

    if not images:
        click.echo("No images found")
        return

    output_dir = Path(output) if output else input_path.parent / 'transparent'
    output_dir.mkdir(parents=True, exist_ok=True)

    click.echo("\n  Background Removal")
    click.echo("  " + "=" * 40)
    click.echo(f"  Images: {len(images)}")

    for img_path in images:
        click.echo(f"  Processing {img_path.name}...")

        with open(img_path, 'rb') as f:
            input_data = f.read()

        output_data = remove(input_data)

        output_path = output_dir / f"{img_path.stem}_nobg.png"
        with open(output_path, 'wb') as f:
            f.write(output_data)

        click.echo(f"  -> {output_path.name}")

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Processed {len(images)} images")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--logo', '-l', type=click.Path(exists=True), help='Logo image file')
@click.option('--text', '-t', help='Watermark text')
@click.option('--position', '-p', default='bottom-right',
              type=click.Choice(['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']))
@click.option('--opacity', default=0.5, type=float, help='Watermark opacity (0-1)')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def watermark(path: str, logo: Optional[str], text: Optional[str],
              position: str, opacity: float, output: Optional[str]):
    """Add watermark to images."""
    if not logo and not text:
        click.echo("Error: Specify --logo or --text")
        return

    input_path = Path(path)
    images = get_images(input_path)

    if not images:
        click.echo("No images found")
        return

    output_dir = Path(output) if output else input_path.parent / 'watermarked'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load watermark
    if logo:
        watermark_img = Image.open(logo).convert('RGBA')
        # Apply opacity
        alpha = watermark_img.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        watermark_img.putalpha(alpha)

    click.echo("\n  Watermark Application")
    click.echo("  " + "=" * 40)
    click.echo(f"  Images: {len(images)}")
    click.echo(f"  Position: {position}")
    click.echo(f"  Opacity: {opacity}")

    for img_path in images:
        img = Image.open(img_path).convert('RGBA')

        if logo:
            # Scale watermark to 20% of image width
            scale = (img.width * 0.2) / watermark_img.width
            wm_size = (int(watermark_img.width * scale), int(watermark_img.height * scale))
            wm = watermark_img.resize(wm_size, Image.Resampling.LANCZOS)

            # Calculate position
            padding = 20
            if position == 'top-left':
                pos = (padding, padding)
            elif position == 'top-right':
                pos = (img.width - wm.width - padding, padding)
            elif position == 'bottom-left':
                pos = (padding, img.height - wm.height - padding)
            elif position == 'bottom-right':
                pos = (img.width - wm.width - padding, img.height - wm.height - padding)
            else:  # center
                pos = ((img.width - wm.width) // 2, (img.height - wm.height) // 2)

            img.paste(wm, pos, wm)

        output_path = output_dir / img_path.name
        img.save(output_path)
        click.echo(f"  -> {img_path.name}")

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Watermarked {len(images)} images")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--format', '-f', 'target_format', required=True,
              type=click.Choice(['webp', 'avif', 'jpg', 'png']))
@click.option('--quality', '-q', type=int, default=80, help='Quality (1-100)')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def convert(path: str, target_format: str, quality: int, output: Optional[str]):
    """Convert images to different format."""
    input_path = Path(path)
    images = get_images(input_path)

    if not images:
        click.echo("No images found")
        return

    output_dir = Path(output) if output else input_path if input_path.is_dir() else input_path.parent

    click.echo("\n  Format Conversion")
    click.echo("  " + "=" * 40)
    click.echo(f"  Images: {len(images)}")
    click.echo(f"  Target: {target_format.upper()}")
    click.echo(f"  Quality: {quality}")

    total_before = 0
    total_after = 0

    for img_path in images:
        original_size = img_path.stat().st_size
        total_before += original_size

        img = Image.open(img_path)

        # Handle transparency
        if target_format in ['jpg', 'jpeg'] and img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif target_format == 'png' and img.mode != 'RGBA':
            img = img.convert('RGBA')

        output_path = output_dir / f"{img_path.stem}.{target_format}"

        if target_format == 'webp':
            img.save(output_path, 'WEBP', quality=quality)
        elif target_format == 'avif':
            img.save(output_path, 'AVIF', quality=quality)
        elif target_format in ['jpg', 'jpeg']:
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        else:
            img.save(output_path, 'PNG', optimize=True)

        new_size = output_path.stat().st_size
        total_after += new_size
        reduction = (1 - new_size / original_size) * 100

        click.echo(f"  {img_path.name} -> {output_path.name} ({reduction:+.0f}%)")

    overall_change = (1 - total_after / total_before) * 100 if total_before else 0
    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] {overall_change:.0f}% size {'reduction' if overall_change > 0 else 'increase'}")


if __name__ == "__main__":
    cli()
