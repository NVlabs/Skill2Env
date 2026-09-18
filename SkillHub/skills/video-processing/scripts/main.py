#!/usr/bin/env python3
"""
Video Processing - FFmpeg automation for marketing video tasks.

Usage:
    python main.py compress video.mp4 --target-mb 10
    python main.py extract-audio video.mp4 --format mp3
    python main.py resize video.mp4 --format instagram
    python main.py clip video.mp4 --start 00:30 --end 01:45
    python main.py concat video1.mp4 video2.mp4 --output merged.mp4
"""

import click
from pathlib import Path
from typing import Optional
import subprocess
import json
import re


def check_ffmpeg():
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_video_info(file_path: str) -> dict:
    """Get video metadata using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)


def parse_time(time_str: str) -> float:
    """Parse time string (HH:MM:SS or MM:SS or seconds) to seconds."""
    if ':' in time_str:
        parts = time_str.split(':')
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + float(s)
        elif len(parts) == 2:
            m, s = parts
            return int(m) * 60 + float(s)
    return float(time_str)


def format_time(seconds: float) -> str:
    """Format seconds to HH:MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"


SOCIAL_FORMATS = {
    'instagram': (1080, 1920),      # 9:16 portrait
    'instagram-feed': (1080, 1080), # 1:1 square
    'tiktok': (1080, 1920),         # 9:16 portrait
    'youtube': (1920, 1080),        # 16:9 landscape
    'youtube-shorts': (1080, 1920), # 9:16 portrait
    'linkedin': (1920, 1080),       # 16:9 landscape
    'twitter': (1920, 1080),        # 16:9 landscape
    'square': (1080, 1080),         # 1:1
    'portrait': (1080, 1920),       # 9:16
    'landscape': (1920, 1080),      # 16:9
}


@click.group()
def cli():
    """Video Processing - FFmpeg automation for marketing."""
    if not check_ffmpeg():
        click.echo("Error: ffmpeg not installed")
        click.echo("macOS: brew install ffmpeg")
        click.echo("Ubuntu: sudo apt install ffmpeg")
        raise SystemExit(1)


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--target-mb', '-t', type=float, help='Target file size in MB')
@click.option('--crf', '-c', type=int, default=23, help='Quality (18-28, lower=better)')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def compress(file: str, target_mb: Optional[float], crf: int, output: Optional[str]):
    """Compress video file."""
    input_path = Path(file)
    output_path = Path(output) if output else input_path.with_stem(f"{input_path.stem}_compressed")

    click.echo("\n  Video Compression")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")

    # Get original size
    original_size = input_path.stat().st_size / (1024 * 1024)
    click.echo(f"  Original size: {original_size:.1f} MB")

    if target_mb:
        # Calculate bitrate for target size
        info = get_video_info(str(input_path))
        duration = float(info['format']['duration'])
        target_bitrate = int((target_mb * 8 * 1024) / duration)  # kbps
        click.echo(f"  Target: {target_mb} MB ({target_bitrate} kbps)")

        cmd = [
            'ffmpeg', '-i', str(input_path),
            '-c:v', 'libx264', '-b:v', f'{target_bitrate}k',
            '-c:a', 'aac', '-b:a', '128k',
            '-y', str(output_path)
        ]
    else:
        click.echo(f"  CRF: {crf}")
        cmd = [
            'ffmpeg', '-i', str(input_path),
            '-c:v', 'libx264', '-crf', str(crf),
            '-c:a', 'aac', '-b:a', '128k',
            '-y', str(output_path)
        ]

    click.echo("  Compressing...")
    subprocess.run(cmd, capture_output=True)

    new_size = output_path.stat().st_size / (1024 * 1024)
    reduction = (1 - new_size / original_size) * 100

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Compressed to {new_size:.1f} MB ({reduction:.0f}% reduction)")
    click.echo(f"  Output: {output_path}")


@cli.command('extract-audio')
@click.argument('file', type=click.Path(exists=True))
@click.option('--format', '-f', 'audio_format', default='mp3',
              type=click.Choice(['mp3', 'wav', 'aac', 'm4a', 'flac']))
@click.option('--bitrate', '-b', default='192k', help='Audio bitrate')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def extract_audio(file: str, audio_format: str, bitrate: str, output: Optional[str]):
    """Extract audio track from video."""
    input_path = Path(file)
    output_path = Path(output) if output else input_path.with_suffix(f'.{audio_format}')

    click.echo("\n  Audio Extraction")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Format: {audio_format}")
    click.echo(f"  Bitrate: {bitrate}")

    if audio_format == 'mp3':
        codec = 'libmp3lame'
    elif audio_format == 'aac' or audio_format == 'm4a':
        codec = 'aac'
    elif audio_format == 'flac':
        codec = 'flac'
    else:
        codec = 'pcm_s16le'

    cmd = [
        'ffmpeg', '-i', str(input_path),
        '-vn',  # No video
        '-acodec', codec,
        '-ab', bitrate,
        '-y', str(output_path)
    ]

    click.echo("  Extracting...")
    subprocess.run(cmd, capture_output=True)

    click.echo("\n  " + "-" * 40)
    click.echo("  [Done] Extracted audio")
    click.echo(f"  Output: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--format', '-f', 'social_format',
              type=click.Choice(list(SOCIAL_FORMATS.keys())),
              help='Social media format preset')
@click.option('--width', '-w', type=int, help='Custom width')
@click.option('--height', '-h', 'height_val', type=int, help='Custom height')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def resize(file: str, social_format: Optional[str], width: Optional[int],
           height_val: Optional[int], output: Optional[str]):
    """Resize video for different platforms."""
    input_path = Path(file)

    if social_format:
        width, height_val = SOCIAL_FORMATS[social_format]
        suffix = f"_{social_format}"
    elif width and height_val:
        suffix = f"_{width}x{height_val}"
    else:
        click.echo("Error: Specify --format or --width/--height")
        raise SystemExit(1)

    output_path = Path(output) if output else input_path.with_stem(f"{input_path.stem}{suffix}")

    click.echo("\n  Video Resize")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Target: {width}x{height_val}")

    # Scale and pad to fit
    filter_str = f"scale={width}:{height_val}:force_original_aspect_ratio=decrease,pad={width}:{height_val}:(ow-iw)/2:(oh-ih)/2"

    cmd = [
        'ffmpeg', '-i', str(input_path),
        '-vf', filter_str,
        '-c:v', 'libx264', '-crf', '23',
        '-c:a', 'aac',
        '-y', str(output_path)
    ]

    click.echo("  Resizing...")
    subprocess.run(cmd, capture_output=True)

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Resized to {width}x{height_val}")
    click.echo(f"  Output: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--start', '-s', required=True, help='Start time (HH:MM:SS or seconds)')
@click.option('--end', '-e', help='End time (HH:MM:SS or seconds)')
@click.option('--duration', '-d', type=float, help='Duration in seconds')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def clip(file: str, start: str, end: Optional[str], duration: Optional[float],
         output: Optional[str]):
    """Extract a segment from video."""
    input_path = Path(file)

    start_sec = parse_time(start)

    if end:
        end_sec = parse_time(end)
        duration = end_sec - start_sec
    elif not duration:
        click.echo("Error: Specify --end or --duration")
        raise SystemExit(1)

    # Create output filename with timestamp
    start_clean = re.sub(r'[:]', '-', start)
    output_path = Path(output) if output else input_path.with_stem(f"{input_path.stem}_clip_{start_clean}")

    click.echo("\n  Video Clip")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Start: {format_time(start_sec)}")
    click.echo(f"  Duration: {duration:.1f}s")

    cmd = [
        'ffmpeg', '-i', str(input_path),
        '-ss', str(start_sec),
        '-t', str(duration),
        '-c:v', 'libx264', '-crf', '23',
        '-c:a', 'aac',
        '-y', str(output_path)
    ]

    click.echo("  Clipping...")
    subprocess.run(cmd, capture_output=True)

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Extracted {duration:.1f}s clip")
    click.echo(f"  Output: {output_path}")


@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--output', '-o', required=True, type=click.Path(), help='Output file path')
def concat(files: tuple, output: str):
    """Concatenate multiple videos."""
    if len(files) < 2:
        click.echo("Error: Need at least 2 videos to concatenate")
        raise SystemExit(1)

    output_path = Path(output)

    click.echo("\n  Video Concatenation")
    click.echo("  " + "=" * 40)
    click.echo(f"  Files: {len(files)}")
    for f in files:
        click.echo(f"    - {Path(f).name}")

    # Create concat file
    concat_file = Path('/tmp/concat_list.txt')
    with open(concat_file, 'w') as f:
        for video in files:
            f.write(f"file '{Path(video).absolute()}'\n")

    cmd = [
        'ffmpeg', '-f', 'concat', '-safe', '0',
        '-i', str(concat_file),
        '-c', 'copy',
        '-y', str(output_path)
    ]

    click.echo("  Concatenating...")
    subprocess.run(cmd, capture_output=True)

    concat_file.unlink()  # Clean up

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Merged {len(files)} videos")
    click.echo(f"  Output: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--time', '-t', 'timestamp', default='00:00:01', help='Timestamp to capture')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def thumbnail(file: str, timestamp: str, output: Optional[str]):
    """Generate thumbnail from video frame."""
    input_path = Path(file)
    output_path = Path(output) if output else input_path.with_suffix('.jpg')

    click.echo("\n  Thumbnail Generation")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Time: {timestamp}")

    time_sec = parse_time(timestamp)

    cmd = [
        'ffmpeg', '-i', str(input_path),
        '-ss', str(time_sec),
        '-vframes', '1',
        '-q:v', '2',
        '-y', str(output_path)
    ]

    click.echo("  Capturing frame...")
    subprocess.run(cmd, capture_output=True)

    click.echo("\n  " + "-" * 40)
    click.echo("  [Done] Generated thumbnail")
    click.echo(f"  Output: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
def info(file: str):
    """Display video information."""
    input_path = Path(file)

    click.echo("\n  Video Information")
    click.echo("  " + "=" * 40)

    info = get_video_info(str(input_path))

    # Format info
    fmt = info.get('format', {})
    click.echo(f"  File: {input_path.name}")
    click.echo(f"  Duration: {format_time(float(fmt.get('duration', 0)))}")
    click.echo(f"  Size: {int(fmt.get('size', 0)) / (1024*1024):.1f} MB")
    click.echo(f"  Bitrate: {int(fmt.get('bit_rate', 0)) / 1000:.0f} kbps")

    # Stream info
    for stream in info.get('streams', []):
        if stream['codec_type'] == 'video':
            click.echo("\n  Video Stream:")
            click.echo(f"    Codec: {stream.get('codec_name')}")
            click.echo(f"    Resolution: {stream.get('width')}x{stream.get('height')}")
            click.echo(f"    FPS: {eval(stream.get('r_frame_rate', '0/1')):.2f}")
        elif stream['codec_type'] == 'audio':
            click.echo("\n  Audio Stream:")
            click.echo(f"    Codec: {stream.get('codec_name')}")
            click.echo(f"    Sample rate: {stream.get('sample_rate')} Hz")
            click.echo(f"    Channels: {stream.get('channels')}")


if __name__ == "__main__":
    cli()
