# Architecture

## Overview

Whisper Transcriber is built around the comprehensive `whisper-transcribe-with-download.sh` script, with Python modules providing a foundation for future development and modular features.

## Core Components

### Main Script (`../whisper-transcribe-with-download.sh`)
- Interactive menu-driven interface
- Live transcription with real-time text display
- YouTube download and transcription in one workflow
- Multi-format support (Zoom, WhatsApp, audio/video files)
- Automatic cleanup and file management

### Python Framework (`src/transcriber/`)
- **CLI Interface** (`cli.py`) - Command-line interface foundation
- **Transcription Engine** (`engine.py`) - Whisper integration framework
- **YouTube Downloader** (`downloader.py`) - Download functionality
- **Output Formatters** (`formatters/`) - Multiple format support

### Supporting Infrastructure
- **Documentation** - Complete guides and examples
- **Development Tools** - Testing, linting, and CI/CD
- **GitHub Integration** - Issue templates, PR templates, workflows

## Current Implementation

The main script handles the complete transcription workflow:

```
User Input → whisper-transcribe-with-download.sh → Output
     ↓                    ↓                           ↓
YouTube URL            Interactive Menu           Transcript
Local File             Download/Process           Audio File
Live Recording         Whisper Transcription      Cleanup
```

## Data Flow

1. **User Selection**: Choose from interactive menu options
2. **Input Handling**: YouTube URL, file path, or live recording
3. **Download/Record**: Extract audio or record from microphone
4. **Model Selection**: Choose appropriate Whisper model
5. **Transcription**: Process through whisper-cli
6. **Output**: Save transcript with timestamps
7. **Cleanup**: Remove old files (7-day retention)

## Dependencies

### Core Dependencies
- **whisper-cli**: Command-line Whisper transcription tool
- **yt-dlp**: YouTube video/audio downloading
- **ffmpeg**: Audio/video format conversion
- **sox**: Audio recording and processing

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking

## Configuration

The script uses simple directory-based configuration:

- **Models**: `~/whisper-models/` (ggml-*.bin files)
- **Downloads**: `~/whisper-downloads/` (temporary files)
- **Transcripts**: `~/Desktop/Transcripts/` (output files)
- **Cleanup**: Automatic removal of files older than 7 days

## Future Development

The Python framework in `src/transcriber/` provides:

- **Modular Components**: Separate CLI, engine, and downloader
- **Multiple Formats**: Support for TXT, SRT, VTT, JSON outputs
- **API Integration**: REST API for web applications
- **Plugin System**: Extensible architecture for new features
- **Testing**: Comprehensive test coverage
