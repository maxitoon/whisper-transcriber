# Whisper Transcriber

A local-first transcription tool using OpenAI Whisper with YouTube download capabilities.

## Features

- 🎵 **YouTube Audio Download**: Extract audio from YouTube videos
- 🎙️ **High-Quality Transcription**: Powered by OpenAI Whisper
- 📁 **Local Processing**: Everything runs on your machine
- 🔧 **Multiple Scripts**: Various configurations for different use cases

## Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg (for audio processing)
- PyTorch (will be installed automatically)

### One-Command Setup

```bash
# 1. Clone and setup
git clone <repository-url>
cd whisper-transcriber

# 2. Install dependencies
make dev

# 3. Run transcription
make transcribe
```

### FFmpeg Installation

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Download from [FFmpeg website](https://ffmpeg.org/download.html) or use Chocolatey:
```bash
choco install ffmpeg
```

## Usage Examples

### Basic Transcription
```bash
# Transcribe audio/video file
python src/transcriber/cli.py input.mp4
```

### YouTube Transcription
```bash
# Download and transcribe YouTube video
python src/transcriber/cli.py --youtube "https://youtube.com/watch?v=..."
```

## Available Scripts

This project includes multiple specialized transcription scripts:

- **Basic transcription**: `whisper-transcribe.sh`
- **Live transcription**: `whisper-transcribe-live.sh`
- **YouTube integration**: `whisper-transcribe-with-download.sh`
- **Real-time processing**: `whisper-transcribe-realtime.sh`

See the [scripts documentation](docs/scripts.md) for detailed usage.

## Development

```bash
# Install development dependencies
make dev

# Run tests
make test

# Format code
make format

# Run linting
make lint
```

## Architecture

- **Core Library**: `src/transcriber/` - Main transcription functionality
- **CLI Interface**: `src/transcriber/cli.py` - Command-line interface
- **External Scripts**: Reference existing whisper scripts in parent directory

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

**FFmpeg not found:**
- Ensure FFmpeg is installed and in your PATH
- On macOS: `brew install ffmpeg`

**PyTorch/CUDA issues:**
- The project uses CPU-only PyTorch by default
- For GPU support, install CUDA-enabled PyTorch manually:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  ```

**Memory issues:**
- Use smaller models (tiny, base) for limited RAM
- Process files in chunks for very large files
