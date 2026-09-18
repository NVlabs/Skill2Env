#!/usr/bin/env python3
"""
Whisper Transcription - Audio/Video to Text using OpenAI Whisper.

Usage:
    python main.py transcribe audio.mp3 --model medium
    python main.py batch ./recordings/ --format srt
    python main.py translate foreign.mp3 --to en
"""

import click
from pathlib import Path
from typing import Optional
import json


def check_whisper():
    """Check if whisper is installed."""
    try:
        import whisper  # noqa: F401
        return True
    except ImportError:
        return False


def get_model(model_name: str):
    """Load whisper model."""
    import whisper
    click.echo(f"  Loading model '{model_name}'...")
    return whisper.load_model(model_name)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_vtt_timestamp(seconds: float) -> str:
    """Convert seconds to VTT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def write_srt(segments: list, output_path: Path):
    """Write segments to SRT format."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg['start'])
            end = format_timestamp(seg['end'])
            text = seg['text'].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def write_vtt(segments: list, output_path: Path):
    """Write segments to VTT format."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, 1):
            start = format_vtt_timestamp(seg['start'])
            end = format_vtt_timestamp(seg['end'])
            text = seg['text'].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def write_txt(result: dict, output_path: Path, include_timestamps: bool = False):
    """Write transcription to text file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        if include_timestamps:
            for seg in result['segments']:
                start = format_timestamp(seg['start']).split(',')[0]
                f.write(f"[{start}] {seg['text'].strip()}\n")
        else:
            f.write(result['text'])


@click.group()
def cli():
    """Whisper Transcription - Audio/Video to Text."""
    if not check_whisper():
        click.echo("Error: openai-whisper not installed")
        click.echo("Run: pip install openai-whisper torch")
        raise SystemExit(1)


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--model', '-m', default='small',
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']),
              help='Whisper model size')
@click.option('--format', '-f', 'output_format', default='txt',
              type=click.Choice(['txt', 'srt', 'vtt', 'json', 'tsv']),
              help='Output format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--language', '-l', help='Source language (auto-detected if not specified)')
@click.option('--timestamps', is_flag=True, help='Include timestamps in txt output')
def transcribe(file: str, model: str, output_format: str, output: Optional[str],
               language: Optional[str], timestamps: bool):
    """Transcribe audio or video file to text."""

    input_path = Path(file)

    click.echo("\n  Whisper Transcription")
    click.echo("  " + "=" * 40)
    click.echo(f"  Input: {input_path.name}")
    click.echo(f"  Model: {model}")
    click.echo(f"  Format: {output_format}")

    # Load model
    whisper_model = get_model(model)

    # Transcribe
    click.echo("  Transcribing...")
    options = {}
    if language:
        options['language'] = language

    result = whisper_model.transcribe(str(input_path), **options)

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.with_suffix(f'.{output_format}')

    # Write output
    click.echo(f"  Writing: {output_path.name}")

    if output_format == 'txt':
        write_txt(result, output_path, timestamps)
    elif output_format == 'srt':
        write_srt(result['segments'], output_path)
    elif output_format == 'vtt':
        write_vtt(result['segments'], output_path)
    elif output_format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    elif output_format == 'tsv':
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("start\tend\ttext\n")
            for seg in result['segments']:
                f.write(f"{seg['start']:.2f}\t{seg['end']:.2f}\t{seg['text'].strip()}\n")

    click.echo("\n  " + "-" * 40)
    click.echo(f"  [Done] Transcribed {input_path.name}")
    click.echo(f"  Output: {output_path}")
    click.echo(f"  Language detected: {result.get('language', 'unknown')}")

    # Show preview
    preview = result['text'][:200].strip()
    click.echo(f"\n  Preview:\n  {preview}...")


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('--model', '-m', default='small',
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']))
@click.option('--format', '-f', 'output_format', default='txt',
              type=click.Choice(['txt', 'srt', 'vtt', 'json']))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def batch(folder: str, model: str, output_format: str, output: Optional[str]):
    """Batch transcribe all audio/video files in folder."""

    input_dir = Path(folder)
    output_dir = Path(output) if output else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find audio/video files
    extensions = {'.mp3', '.wav', '.m4a', '.mp4', '.mkv', '.webm', '.ogg', '.flac'}
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in extensions]

    if not files:
        click.echo(f"No audio/video files found in {folder}")
        return

    click.echo("\n  Batch Transcription")
    click.echo("  " + "=" * 40)
    click.echo(f"  Found {len(files)} files")
    click.echo(f"  Model: {model}")

    whisper_model = get_model(model)

    for i, file_path in enumerate(files, 1):
        click.echo(f"\n  [{i}/{len(files)}] {file_path.name}")

        result = whisper_model.transcribe(str(file_path))

        output_path = output_dir / file_path.with_suffix(f'.{output_format}').name

        if output_format == 'txt':
            write_txt(result, output_path)
        elif output_format == 'srt':
            write_srt(result['segments'], output_path)
        elif output_format == 'vtt':
            write_vtt(result['segments'], output_path)
        elif output_format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        click.echo(f"  -> {output_path.name}")

    click.echo(f"\n  [Done] Transcribed {len(files)} files")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--to', '-t', 'target_lang', default='en', help='Target language')
@click.option('--model', '-m', default='small',
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def translate(file: str, target_lang: str, model: str, output: Optional[str]):
    """Transcribe and translate audio to target language."""

    input_path = Path(file)

    click.echo(f"\n  Translate to {target_lang}")
    click.echo("  " + "=" * 40)

    whisper_model = get_model(model)

    click.echo("  Transcribing and translating...")
    result = whisper_model.transcribe(str(input_path), task='translate')

    output_path = Path(output) if output else input_path.with_suffix(f'.{target_lang}.txt')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])

    click.echo(f"\n  [Done] Translated to {target_lang}")
    click.echo(f"  Output: {output_path}")


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--model', '-m', default='small',
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']))
@click.option('--format', '-f', 'output_format', default='json',
              type=click.Choice(['json', 'txt']))
def timestamps(file: str, model: str, output_format: str):
    """Extract timestamps with text segments."""

    input_path = Path(file)

    click.echo("\n  Extract Timestamps")
    click.echo("  " + "=" * 40)

    whisper_model = get_model(model)
    result = whisper_model.transcribe(str(input_path))

    segments = []
    for seg in result['segments']:
        segments.append({
            'start': seg['start'],
            'end': seg['end'],
            'start_formatted': format_timestamp(seg['start']).split(',')[0],
            'end_formatted': format_timestamp(seg['end']).split(',')[0],
            'text': seg['text'].strip()
        })

    output_path = input_path.with_suffix('.timestamps.' + output_format)

    if output_format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(segments, f, indent=2, ensure_ascii=False)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            for seg in segments:
                f.write(f"[{seg['start_formatted']} - {seg['end_formatted']}]\n")
                f.write(f"{seg['text']}\n\n")

    click.echo(f"\n  [Done] Extracted {len(segments)} segments")
    click.echo(f"  Output: {output_path}")


if __name__ == "__main__":
    cli()
