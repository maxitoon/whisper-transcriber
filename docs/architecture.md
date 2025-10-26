# Architecture

## Overview

Whisper Transcriber is designed as a modular system that can work with existing transcription scripts while providing a clean, extensible architecture for new development.

## Core Components

### CLI Interface (`src/transcriber/cli.py`)
- Main entry point for the application
- Handles command-line arguments and options
- Orchestrates transcription workflow

### Transcription Engine (`src/transcriber/engine.py`)
- Core transcription functionality using OpenAI Whisper
- Model loading and management
- Audio processing and chunking

### YouTube Downloader (`src/transcriber/downloader.py`)
- YouTube audio extraction using yt-dlp
- Format selection and optimization
- Download progress tracking

### Output Formatters (`src/transcriber/formatters/`)
- Multiple output format support (TXT, SRT, VTT, JSON)
- Timestamp formatting
- File output management

## Integration with Existing Scripts

The project is designed to coexist with existing transcription scripts:

```
whisper-transcriber/
├── src/transcriber/        # New modular code
└── ../                    # Existing scripts (referenced in docs)
    ├── whisper-transcribe.sh
    ├── whisper-transcribe-live.sh
    └── ...
```

## Data Flow

1. **Input**: Audio/video file or YouTube URL
2. **Download** (if URL): Extract audio using yt-dlp
3. **Preprocessing**: Convert to optimal format for Whisper
4. **Transcription**: Process through Whisper model
5. **Formatting**: Convert to desired output format
6. **Output**: Save transcription to file

## Dependencies

### Core Dependencies
- **openai-whisper**: Transcription engine
- **torch/torchaudio**: ML framework and audio processing
- **yt-dlp**: YouTube downloading
- **click**: CLI framework

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking

## Configuration

The application uses environment variables and configuration files:

- **Environment variables**: Model selection, device settings
- **Config files**: Output formats, quality settings
- **CLI arguments**: Runtime options

## Extensibility

The architecture supports easy extension through:

- **Plugin system**: Additional output formats
- **Model support**: Multiple Whisper model sizes
- **Source support**: Beyond YouTube (local files, other platforms)
- **Processing options**: Custom preprocessing, chunking strategies
