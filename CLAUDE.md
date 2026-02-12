# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Local-first audio/video transcription tool using whisper-cli (whisper.cpp). Provides a Python CLI that wraps OpenAI Whisper for transcription and yt-dlp for YouTube audio downloading. Outputs in txt, srt, vtt, or json formats.

## Commands

```bash
make dev          # Install dev deps + editable install
make test         # Run pytest with coverage
make lint         # ruff check + mypy
make format       # black + isort
make transcribe   # Run shell-based transcription (interactive)

# Run a single test
pytest tests/test_engine.py -v
pytest tests/test_cli.py::test_transcribe_command -v

# CLI usage (after `pip install -e .`)
whisper-transcriber transcribe <file> --model base --format txt
whisper-transcriber youtube <url> --model base --format srt
whisper-transcriber models
```

## Architecture

### Shell script (primary workflow)
- **`whisper-transcribe-with-download.sh`** — Interactive menu-driven script. Handles live mic recording, YouTube downloads, and file transcription using `whisper-cli`, `sox`, `yt-dlp`, and `ffmpeg`.
  - `original_live_transcription()` — Incremental chunk-based live transcription. Records via `rec` (sox), polls every 2s, extracts new audio chunks with `sox trim` when 5+ seconds of new audio is available, transcribes each chunk independently with `whisper-cli`, and displays text incrementally. On Ctrl+C, performs a final full-file transcription for accuracy.

### Python CLI
The CLI (`click`-based) has three commands: `transcribe` (local file), `youtube` (download + transcribe), and `models` (list available models).

- **`src/transcriber/cli.py`** - Click CLI with commands. The `youtube` command delegates to `downloader` then calls `transcribe` internally.
- **`src/transcriber/engine.py`** - `TranscriptionEngine` wraps the Python `whisper` library. Handles model loading, transcription, and saving results in multiple formats (txt/srt/vtt/json). Python Whisper (`openai-whisper`, `torch`) is an optional dependency; the primary workflow uses `whisper-cli` via the shell script.
- **`src/transcriber/downloader.py`** - `YouTubeDownloader` wraps `yt-dlp` for audio extraction. Also optional import guarded.

Both `engine.py` and `downloader.py` use try/except imports with `*_AVAILABLE` flags so the package can be installed without `torch` or `yt-dlp`.

## Key Details

- Python >=3.8, line length 88 (black), isort profile "black"
- mypy strict mode enabled (`disallow_untyped_defs`, etc.)
- Package installed from `src/` layout via setuptools
- Entry point: `whisper-transcriber` CLI → `transcriber.cli:main`
- External tool dependencies: `whisper-cli`, `ffmpeg`, `sox`, `yt-dlp`
- Whisper model files (ggml-*.bin) expected in `~/whisper-models/`
