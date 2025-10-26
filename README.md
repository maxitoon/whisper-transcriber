# Whisper Transcriber

A local-first transcription tool using OpenAI Whisper with YouTube download capabilities.

## Features

- 🎵 **YouTube Audio Download**: Extract audio from YouTube videos
- 🎙️ **High-Quality Transcription**: Powered by OpenAI Whisper
- 📁 **Local Processing**: Everything runs on your machine
- 🔧 **Multiple Scripts**: Various configurations for different use cases

## Quick Start

### Prerequisites

- **whisper-cli** (command-line Whisper tool)
- **yt-dlp** (YouTube downloader)
- **ffmpeg** (audio processing)
- **sox** (for live recording)

### Installation

**1. Install whisper-cli:**
```bash
# Download from: https://github.com/ggerganov/whisper.cpp
# Follow installation instructions for your platform
```

**2. Install system dependencies:**

**macOS:**
```bash
brew install ffmpeg sox yt-dlp
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg sox yt-dlp
```

**Windows:**
```bash
# Install via Chocolatey or download manually:
choco install ffmpeg sox yt-dlp
```

**3. Download Whisper models:**
```bash
# The script will prompt you to download models to ~/whisper-models/
# Download: ggml-base.en.bin, ggml-small.bin, ggml-medium.bin, ggml-large.bin
```

**4. Run transcription:**
```bash
# From the whisper-transcriber directory
../whisper-transcribe-with-download.sh

# Or create a convenient symlink:
ln -s ../whisper-transcribe-with-download.sh transcribe.sh
./transcribe.sh
```

## Usage Examples

### Interactive Mode
```bash
# Run the main script (interactive menu)
../whisper-transcribe-with-download.sh

# Choose from options:
# 1) 🔴 ORIGINAL Live Recording + Live Transcript
# 2) 🎥 YouTube Video + Transcript
# 3) 📥 YouTube Video Download Only
# 4) 💼 Zoom Recording + Transcript
# 5) 💬 WhatsApp Audio + Transcript
# 6) 📁 Other Audio/Video File + Transcript
```

### YouTube Transcription
```bash
# The script will prompt for URL and handle download + transcription
# Choose option 2 for "YouTube Video + Transcript"
```

### Live Transcription
```bash
# Records from microphone and shows real-time transcription
# Choose option 1 for "ORIGINAL Live Recording + Live Transcript"
```

## Main Script

This project uses the comprehensive `whisper-transcribe-with-download.sh` script which provides:

- 🎙️ **Live transcription** with real-time text display
- 🎥 **YouTube download + transcription** in one command
- 📁 **Local file transcription** (Zoom, WhatsApp, audio/video files)
- 🧹 **Automatic cleanup** of old files (7-day retention)

See the [scripts documentation](docs/scripts.md) for detailed usage.

## Development

The project is currently focused on the main `whisper-transcribe-with-download.sh` script. The Python modules in `src/` provide a foundation for future development.

```bash
# Install Python dependencies (for future development)
make dev

# Run tests
make test

# Format code
make format

# Run linting
make lint
```

## Architecture

- **Main Script**: `../whisper-transcribe-with-download.sh` - Complete transcription solution
- **Python Modules**: `src/transcriber/` - Future development framework
- **Documentation**: Complete guides and examples

See [architecture.md](docs/architecture.md) for detailed design.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Configuration

The application uses environment variables and configuration files:

- **Environment variables**: Model selection, device settings
- **Config files**: Copy `env.example` to `.env` and customize
- **CLI arguments**: Runtime options

```bash
cp env.example .env
# Edit .env with your preferred settings
```

## License

MIT - see [LICENSE](LICENSE) file.

## Troubleshooting

### Common Issues

**whisper-cli not found:**
- Download and install whisper-cli from: https://github.com/ggerganov/whisper.cpp
- Ensure it's in your PATH or provide full path to executable

**FFmpeg/Sox not found:**
- Ensure FFmpeg and Sox are installed and in your PATH
- On macOS: `brew install ffmpeg sox`
- On Ubuntu: `sudo apt install ffmpeg sox`

**yt-dlp not found:**
- Install yt-dlp: `pip install yt-dlp` or `brew install yt-dlp`
- Update regularly: `yt-dlp -U`

**Whisper models missing:**
- Download models to `~/whisper-models/` directory
- Available models: `ggml-base.en.bin`, `ggml-small.bin`, `ggml-medium.bin`, `ggml-large.bin`
- The script will guide you through model selection

**Memory issues:**
- Use smaller models (base, small) for limited RAM
- Close other applications during transcription
- Ensure adequate disk space for downloads

**YouTube download fails:**
- Check internet connection stability
- Some videos may be region-restricted or private
- Try different video quality settings
