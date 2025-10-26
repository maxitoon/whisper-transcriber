# Scripts Documentation

This project includes references to existing transcription scripts in the parent directory. These scripts provide various approaches to transcription and can serve as examples or be used directly.

## Main Script

The project uses the single comprehensive `whisper-transcribe-with-download.sh` script which provides all transcription functionality in one tool.

## Usage Examples

### Quick Start
```bash
# Run the main transcription script
../whisper-transcribe-with-download.sh
```

### YouTube Transcription
```bash
# The script will prompt for YouTube URL and options
# Choose option 2 for "YouTube Video + Transcript"
# Choose option 3 for "YouTube Video Download Only"
```

### Live Transcription
```bash
# Choose option 1 for "ORIGINAL Live Recording + Live Transcript"
# Records from microphone and shows real-time transcription
```

### Local Files
```bash
# Choose options 4-6 for Zoom, WhatsApp, or other audio/video files
# The script will prompt for file paths
```

## Script Features

### Core Features
- 🎙️ **Live transcription** with real-time text display
- 🎥 **YouTube download** and transcription in one workflow
- 📁 **Multi-format support** (Zoom, WhatsApp, audio/video files)
- 🧹 **Automatic cleanup** (removes files older than 7 days)
- 🌍 **Multi-language support** with model selection
- 📱 **Interactive interface** with color-coded output

### Advanced Features
- Real-time audio processing during recording
- Multiple Whisper model support (base, small, medium, large)
- Automatic audio format detection and conversion
- Progress tracking and status updates
- Error handling and recovery
- Timestamped output files

## Requirements

The script requires:
- **whisper-cli** (Whisper command-line tool)
- **yt-dlp** (YouTube downloader)
- **ffmpeg** (audio processing)
- **sox** (for live recording)

## Setup

1. **Install whisper-cli:**
   ```bash
   # Download and install whisper-cli from the official repository
   ```

2. **Download Whisper models:**
   ```bash
   # The script will guide you to download models to ~/whisper-models/
   # Available: ggml-base.en.bin, ggml-small.bin, ggml-medium.bin, ggml-large.bin
   ```

3. **Install dependencies:**
   ```bash
   # Ubuntu/Debian:
   sudo apt install ffmpeg sox yt-dlp

   # macOS:
   brew install ffmpeg sox yt-dlp
   ```

## Best Practices

- Run from the directory containing the script
- Ensure whisper-cli and models are properly installed
- Check available disk space for downloads
- Use stable internet connection for YouTube downloads
- Test with short clips before processing long videos
