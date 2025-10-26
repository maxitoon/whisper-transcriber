# Scripts Documentation

This project includes references to existing transcription scripts in the parent directory. These scripts provide various approaches to transcription and can serve as examples or be used directly.

## Available Scripts

The following scripts are available in the parent directory:

### Basic Transcription
- **`whisper-transcribe.sh`** - Basic transcription functionality
- **`whisper-transcribe-fixed.sh`** - Improved basic transcription
- **`whisper-transcribe-complete.sh`** - Complete transcription workflow

### Live Transcription
- **`whisper-transcribe-live.sh`** - Live audio transcription
- **`whisper-transcribe-realtime.sh`** - Real-time processing
- **`whisper-transcribe-streaming.sh`** - Streaming transcription

### Advanced Features
- **`whisper-transcribe-with-download.sh`** - YouTube download + transcription
- **`whisper-transcribe-with-progress.sh`** - Progress tracking
- **`whisper-transcribe-smart.sh`** - Smart transcription features

### Specialized Scripts
- **`whisper-transcribe-ultimate.sh`** - Advanced comprehensive script
- **`whisper-transcribe-true-live.sh`** - True live transcription
- **`whisper-transcribe-working-live.sh`** - Working live implementation

## Usage Examples

### Basic Usage
```bash
# Basic transcription
../whisper-transcribe.sh input.mp4

# With fixed improvements
../whisper-transcribe-fixed.sh input.mp4
```

### YouTube Integration
```bash
# Download and transcribe YouTube video
../whisper-transcribe-with-download.sh "https://youtube.com/watch?v=..."
```

### Live Transcription
```bash
# Live microphone transcription
../whisper-transcribe-live.sh

# Real-time processing
../whisper-transcribe-realtime.sh
```

## Script Features

### Common Features
- Audio format conversion
- Model selection options
- Output format selection
- Error handling
- Progress indicators

### Advanced Features
- Batch processing
- Language detection
- Speaker diarization
- Timestamp alignment
- Quality optimization

## Integration with New CLI

The new CLI tool (`src/transcriber/cli.py`) provides a more structured approach while maintaining compatibility with these existing scripts:

```bash
# New CLI approach
python src/transcriber/cli.py input.mp4

# Or use existing scripts
../whisper-transcribe.sh input.mp4
```

## Migration Guide

### From Scripts to CLI

**Basic transcription:**
```bash
# Old
../whisper-transcribe.sh input.mp4

# New
python src/transcriber/cli.py input.mp4
```

**YouTube transcription:**
```bash
# Old
../whisper-transcribe-with-download.sh "https://youtube.com/watch?v=..."

# New
python src/transcriber/cli.py --youtube "https://youtube.com/watch?v=..."
```

## Contributing to Scripts

When improving existing scripts:

1. Maintain backward compatibility
2. Add proper error handling
3. Include usage documentation
4. Test on multiple platforms
5. Consider adding to the new CLI system

## Best Practices

- Use absolute paths when possible
- Handle different audio formats gracefully
- Provide clear error messages
- Include progress indicators for long operations
- Test with various model sizes
- Consider memory usage for large files
