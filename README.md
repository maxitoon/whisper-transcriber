# Whisper Transcriber — Local Audio and Video Transcription with Whisper

Whisper Transcriber is a local-first speech-to-text tool for converting audio, video, YouTube videos, Zoom recordings, and voice notes into private transcripts using `whisper-cli` from whisper.cpp. It is designed for creators, researchers, journalists, developers, and anyone who wants local audio transcription without uploading sensitive files to a cloud service.

## Features

- **Live microphone transcription** with incremental chunk-based output (text appears every ~5 seconds while you speak)
- **YouTube download + transcribe** — paste a URL, get a transcript
- **YouTube fallback download strategies** — retries multiple YouTube client profiles to reduce 403 failures
- **File transcription** — supports Zoom recordings, WhatsApp audio, and any audio/video file
- **Multiple output formats** — txt, srt, vtt, json
- **Multi-language support** — English, French, auto-detect
- **Multiple Whisper models** — base, small, medium, large
- **Local-first workflow** — the recommended shell workflow uses local `whisper-cli` instead of cloud transcription APIs

## Use Cases

- Transcribe meeting recordings, interviews, podcasts, lectures, and research calls
- Turn YouTube videos into searchable text notes or subtitles
- Generate `.srt` and `.vtt` subtitle files from local audio/video files
- Record live microphone audio and see incremental transcription while speaking
- Keep sensitive voice notes, client recordings, and research audio on your own machine

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
mkdir -p ~/whisper-models
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

## Examples

### Transcribe a local audio or video file

```bash
./whisper-transcribe-with-download.sh
# Choose option 6: Other File
# Enter the file path when prompted
```

### Transcribe a YouTube video

```bash
./whisper-transcribe-with-download.sh
# Choose option 2: YouTube Video
# Paste the YouTube URL when prompted
```

### Use the Python CLI

```bash
pip install -e .
whisper-transcriber transcribe meeting.mp3 --model base --format txt
whisper-transcriber transcribe interview.mp4 --model small --format srt
whisper-transcriber youtube "https://www.youtube.com/watch?v=VIDEO_ID" --model base --format vtt
whisper-transcriber models
```

## YouTube Download Reliability

When YouTube changes delivery behavior (for example SABR-related client restrictions), a single `yt-dlp` strategy can fail with `HTTP Error 403: Forbidden`.

This project retries YouTube downloads using multiple fallback profiles:

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

## FAQ

### What is Whisper Transcriber used for?

Whisper Transcriber is used to convert local audio files, video files, YouTube videos, Zoom recordings, WhatsApp voice notes, and microphone recordings into text transcripts or subtitle files.

### Is Whisper Transcriber private?

Yes, the recommended shell workflow runs transcription locally through `whisper-cli` and keeps your files on your machine. YouTube mode downloads audio locally before transcription.

### Does Whisper Transcriber require a GPU?

No. `whisper.cpp` can run on CPU, though larger models and long recordings will be faster with stronger hardware.

### Which output formats are supported?

The Python CLI supports `txt`, `srt`, `vtt`, and `json`. The shell workflow focuses on practical local transcript files saved under `~/Documents/Transcripts/`.

### Can it transcribe YouTube videos?

Yes. It uses `yt-dlp` to download YouTube audio, then transcribes the downloaded file locally. The script includes fallback strategies for common YouTube download failures.

### What is the difference between `whisper-cli` and the Python CLI?

The interactive shell script is the primary local-first workflow and uses `whisper-cli` from whisper.cpp. The Python CLI wraps Python Whisper and `yt-dlp` for programmatic use.

## Alternatives and Comparisons

- **Whisper Transcriber vs OpenAI API transcription:** Whisper Transcriber is local-first and avoids uploading audio to a remote API; the OpenAI API is easier to scale but cloud-based.
- **Whisper Transcriber vs MacWhisper:** MacWhisper is a polished desktop app; Whisper Transcriber is scriptable, CLI-friendly, and easier to customize.
- **Whisper Transcriber vs Otter.ai:** Otter is a hosted meeting assistant; Whisper Transcriber is better when privacy, local files, and automation matter more than collaboration features.
- **Whisper Transcriber vs raw whisper.cpp:** This repo adds practical workflows for live recording, YouTube downloads, file routing, and transcript organization.

## Development

```bash
make dev       # Install dev dependencies + editable install
make test      # Run pytest with coverage
make lint      # ruff check + mypy
make format    # black + isort
```

## Project Structure

```text
whisper-transcriber/
  whisper-transcribe-with-download.sh  # Main interactive script (shell)
  src/transcriber/
    cli.py          # Python CLI (click-based)
    engine.py       # Whisper engine wrapper
    downloader.py   # YouTube downloader (yt-dlp wrapper)
  tests/
  Makefile
```

## Roadmap

- Add screenshots or a terminal demo GIF
- Publish a short examples page for common transcription workflows
- Add packaged release artifacts for easier installation
- Document Linux-specific setup steps for `whisper-cli`, `ffmpeg`, `sox`, and microphone access

## License

MIT
