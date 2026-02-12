# Whisper Transcriber

Local-first audio/video transcription tool powered by [whisper-cli](https://github.com/ggerganov/whisper.cpp) (whisper.cpp). Features an interactive shell script for live microphone transcription, YouTube downloads, and file-based transcription, plus a Python CLI for programmatic use.

## Features

- **Live microphone transcription** with incremental chunk-based output (text appears every ~5 seconds while you speak)
- **YouTube download + transcribe** — paste a URL, get a transcript
- **YouTube fallback download strategies** — retries multiple YouTube client profiles to reduce 403 failures
- **File transcription** — supports Zoom recordings, WhatsApp audio, and any audio/video file
- **Multiple output formats** — txt, srt, vtt, json
- **Multi-language support** — English, French, auto-detect
- **Multiple Whisper models** — base, small, medium, large

## Prerequisites

Install the following system dependencies:

```bash
# macOS (Homebrew)
brew install whisper-cpp ffmpeg sox yt-dlp

# The whisper-cli binary must be available in PATH
```

Download at least one Whisper model to `~/whisper-models/`:

```bash
# Example: download the base English model
curl -L -o ~/whisper-models/ggml-base.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin

# For multi-language support, also grab small or medium:
curl -L -o ~/whisper-models/ggml-small.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
```

## Quick Start

```bash
# Interactive transcription menu
make transcribe

# Or run directly
./whisper-transcribe-with-download.sh
```

This launches an interactive menu with these options:

1. **Live Recording** — Record from microphone with real-time transcription
2. **YouTube Video** — Download and transcribe a YouTube video
3. **YouTube Download Only** — Download video without transcription
4. **Zoom Recording** — Transcribe a Zoom recording file
5. **WhatsApp Audio** — Transcribe a WhatsApp voice message
6. **Other File** — Transcribe any audio/video file

Transcripts are saved to `~/Documents/Transcripts/`. Audio downloads are saved to `~/whisper-downloads/` and auto-cleaned after 7 days.

## YouTube Download Reliability

When YouTube changes delivery behavior (for example SABR-related client restrictions), a single `yt-dlp` strategy can fail with `HTTP Error 403: Forbidden`.

This project now retries YouTube downloads using multiple fallback profiles:

- Alternative audio/video format selectors
- Multiple YouTube player clients (`android`, `ios`, `web`)
- Conservative transfer settings (`--retries`, `--fragment-retries`, `--force-ipv4`)

If you still hit 403 errors, run:

```bash
yt-dlp -U
```

## How Live Transcription Works

The live recording mode (option 1) uses incremental chunk-based transcription:

1. `rec` (from sox) records audio from your microphone in the background
2. Every 2 seconds, the script checks if at least 5 seconds of new audio is available
3. New audio is extracted with `sox trim` and transcribed with `whisper-cli`
4. Only the new text is displayed — no re-processing of already-transcribed audio
5. On Ctrl+C, a final full-file transcription is performed for maximum accuracy and saved to disk

## Python CLI

A Python CLI is also available for programmatic use:

```bash
# Install
pip install -e .

# Transcribe a local file
whisper-transcriber transcribe <file> --model base --format txt

# Download and transcribe a YouTube video
whisper-transcriber youtube <url> --model base --format srt

# List available models
whisper-transcriber models
```

> **Note:** The Python CLI requires `openai-whisper` and `torch` as optional dependencies. The shell script (recommended) uses `whisper-cli` instead and has no Python dependencies.

## Development

```bash
make dev       # Install dev dependencies + editable install
make test      # Run pytest with coverage
make lint      # ruff check + mypy
make format    # black + isort
```

## Project Structure

```
whisper-transcriber/
  whisper-transcribe-with-download.sh  # Main interactive script (shell)
  src/transcriber/
    cli.py          # Python CLI (click-based)
    engine.py       # Whisper engine wrapper
    downloader.py   # YouTube downloader (yt-dlp wrapper)
  tests/
  Makefile
```

## License

MIT
