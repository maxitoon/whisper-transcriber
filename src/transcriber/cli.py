"""Command-line interface for Whisper Transcriber."""

import os
import sys
from pathlib import Path
from typing import Optional

import click

from .engine import TranscriptionEngine
from .downloader import YouTubeDownloader


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """Whisper Transcriber - Local-first transcription tool using OpenAI Whisper."""
    pass


@main.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (default: auto-generated)",
)
@click.option(
    "--model",
    default="base",
    type=click.Choice(["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]),
    help="Whisper model size (default: base)",
)
@click.option(
    "--format",
    type=click.Choice(["txt", "srt", "vtt", "json"]),
    default="txt",
    help="Output format (default: txt)",
)
@click.option(
    "--device",
    default="cpu",
    type=click.Choice(["cpu", "cuda"]),
    help="Device to run transcription on (default: cpu)",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def transcribe(
    input_path: str,
    output: Optional[str],
    model: str,
    format: str,
    device: str,
    verbose: bool,
) -> None:
    """Transcribe audio/video file."""
    try:
        engine = TranscriptionEngine(model=model, device=device, verbose=verbose)

        if output:
            output_path = Path(output)
        else:
            input_stem = Path(input_path).stem
            output_path = Path(f"{input_stem}_transcript.{format}")

        click.echo(f"Transcribing {input_path}...")
        result = engine.transcribe(input_path)

        if format == "json":
            engine.save_json(result, output_path)
        elif format == "srt":
            engine.save_srt(result, output_path)
        elif format == "vtt":
            engine.save_vtt(result, output_path)
        else:
            engine.save_txt(result, output_path)

        click.echo(f"Transcription saved to {output_path}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


@main.command()
@click.argument("url")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output transcript path",
)
@click.option(
    "--model",
    default="base",
    type=click.Choice(["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]),
    help="Whisper model size",
)
@click.option(
    "--format",
    type=click.Choice(["txt", "srt", "vtt", "json"]),
    default="txt",
    help="Output format",
)
@click.option(
    "--quality",
    default="best[height<=480]",
    help="Video quality to download (yt-dlp format)",
)
def youtube(
    url: str,
    output: Optional[str],
    model: str,
    format: str,
    quality: str,
) -> None:
    """Download and transcribe YouTube video."""
    try:
        # Download audio
        downloader = YouTubeDownloader()
        click.echo(f"Downloading audio from {url}...")
        audio_path = downloader.download_audio(url, quality=quality)

        # Transcribe
        transcribe.callback(
            input_path=str(audio_path),
            output=output,
            model=model,
            format=format,
            device="cpu",
            verbose=False,
        )

        # Clean up downloaded file
        os.unlink(audio_path)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def models() -> None:
    """List available Whisper models."""
    models_info = {
        "tiny": "39 MB - Fastest, least accurate",
        "base": "74 MB - Good balance of speed/accuracy",
        "small": "244 MB - Better accuracy",
        "medium": "769 MB - High accuracy",
        "large": "1550 MB - Highest accuracy",
        "large-v2": "1550 MB - Improved large model",
        "large-v3": "1550 MB - Latest large model",
    }

    click.echo("Available Whisper models:")
    for model, description in models_info.items():
        click.echo(f"  {model:10} - {description}")


if __name__ == "__main__":
    main()
