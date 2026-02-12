#!/bin/bash

# Enhanced Whisper Transcription Script with YouTube Download Option
# Shows live transcription text appearing in real-time as you speak

MODELS_DIR="$HOME/whisper-models"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
TRANSCRIPT_DIR="$HOME/Documents/Transcripts"
AUDIO_DOWNLOAD_DIR="$HOME/whisper-downloads"

# Create necessary directories
mkdir -p "$MODELS_DIR"
mkdir -p "$TRANSCRIPT_DIR"
mkdir -p "$AUDIO_DOWNLOAD_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_color() {
    color=$1
    shift
    echo -e "${color}$@${NC}" >&2
}

print_header() {
    echo "" >&2
    echo "" >&2
    print_color "$CYAN" "╔════════════════════════════════════════════════════╗"
    print_color "$CYAN" "║   🎙️  Live Whisper Transcription Tool 🎙️   ║"
    print_color "$CYAN" "╚════════════════════════════════════════════════════╝"
    echo "" >&2
}

# Function to detect available models
detect_available_models() {
    local available_models=()
    
    if [ -f "$MODELS_DIR/ggml-base.en.bin" ]; then
        available_models+=("$MODELS_DIR/ggml-base.en.bin")
    fi
    
    if [ -f "$MODELS_DIR/ggml-small.bin" ]; then
        available_models+=("$MODELS_DIR/ggml-small.bin")
    fi
    
    if [ -f "$MODELS_DIR/ggml-medium.bin" ]; then
        available_models+=("$MODELS_DIR/ggml-medium.bin")
    fi
    
    if [ -f "$MODELS_DIR/ggml-large.bin" ]; then
        available_models+=("$MODELS_DIR/ggml-large.bin")
    fi
    
    echo "${available_models[@]}"
}

# Function to select model from available ones
select_available_model() {
    local available_models=($(detect_available_models))
    local model_names=()
    
    if [ -f "$MODELS_DIR/ggml-base.en.bin" ]; then
        model_names+=("Base (English, faster)")
    fi
    
    if [ -f "$MODELS_DIR/ggml-small.bin" ]; then
        model_names+=("Small (Multi-language, balanced)")
    fi
    
    if [ -f "$MODELS_DIR/ggml-medium.bin" ]; then
        model_names+=("Medium (Multi-language, more accurate)")
    fi
    
    if [ -f "$MODELS_DIR/ggml-large.bin" ]; then
        model_names+=("Large (Multi-language, most accurate)")
    fi
    
    if [ ${#available_models[@]} -eq 0 ]; then
        print_color "$RED" "❌ No whisper models found in $MODELS_DIR"
        print_color "$YELLOW" "Please download models first:"
        print_color "$YELLOW" "  - ggml-base.en.bin (English only)"
        print_color "$YELLOW" "  - ggml-small.bin (Multi-language)"
        exit 1
    fi
    
    print_color "$YELLOW" "\nSelect Whisper Model:"
    for i in "${!available_models[@]}"; do
        echo "$((i+1))) ${model_names[$i]}" >&2
    done
    
    read -p "Enter your choice (1-${#available_models[@]}) [default: 1]: " model_choice
    model_choice=${model_choice:-1}
    
    if [ "$model_choice" -ge 1 ] && [ "$model_choice" -le "${#available_models[@]}" ]; then
        echo "${available_models[$((model_choice-1))]}"
    else
        print_color "$RED" "Invalid choice. Using first available model."
        echo "${available_models[0]}"
    fi
}

# Function to select language
select_language() {
    print_color "$YELLOW" "\nSelect Language:"
    echo "1) English (en)" >&2
    echo "2) French (fr)" >&2
    echo "3) Auto-detect" >&2
    read -p "Enter choice (1-3) [default: 3]: " lang_choice
    case $lang_choice in
        1) echo "en" ;;
        2) echo "fr" ;;
        *) echo "auto" ;;
    esac
}

# Function to clean up old audio files (older than 7 days)
cleanup_old_audio() {
    print_color "$BLUE" "🧹 Cleaning up audio files older than 7 days..." >&2
    find "$AUDIO_DOWNLOAD_DIR" -name "*_live_recording.wav" -type f -mtime +7 -delete 2>/dev/null
    find "$AUDIO_DOWNLOAD_DIR" -name "*_audio.mp3" -type f -mtime +7 -delete 2>/dev/null
    find "$AUDIO_DOWNLOAD_DIR" -name "*_video.*" -type f -mtime +7 -delete 2>/dev/null
    print_color "$GREEN" "✅ Cleanup completed" >&2
}

download_youtube_audio_with_fallback() {
    local youtube_url=$1
    local output_template=$2

    local -a formats=(
        "bestaudio[ext=m4a]/bestaudio/best"
        "140/bestaudio[ext=m4a]/bestaudio/best"
        "bestaudio/best"
    )
    local -a clients=(
        "youtube:player_client=android,ios,web"
        "youtube:player_client=android,web"
        ""
    )

    for i in "${!formats[@]}"; do
        local format_selector="${formats[$i]}"
        local extractor_args="${clients[$i]}"

        print_color "$YELLOW" "Trying download profile $((i+1))/${#formats[@]}..." >&2
        local -a cmd=(
            yt-dlp
            --no-playlist
            --retries 10
            --fragment-retries 10
            --force-ipv4
            --concurrent-fragments 1
            -f "$format_selector"
            --extract-audio
            --audio-format mp3
            --audio-quality 0
            -o "$output_template"
        )

        if [ -n "$extractor_args" ]; then
            cmd+=(--extractor-args "$extractor_args")
        fi
        cmd+=("$youtube_url")

        "${cmd[@]}" >&2
        if [ $? -eq 0 ]; then
            return 0
        fi
    done

    return 1
}

download_youtube_video_with_fallback() {
    local youtube_url=$1
    local output_template=$2

    local -a formats=(
        "bv*[height<=720]+ba[ext=m4a]/b[height<=720]/best[height<=720]"
        "best[height<=720]/best"
    )
    local -a clients=(
        "youtube:player_client=android,ios,web"
        ""
    )

    for i in "${!formats[@]}"; do
        local format_selector="${formats[$i]}"
        local extractor_args="${clients[$i]}"

        print_color "$YELLOW" "Trying video profile $((i+1))/${#formats[@]}..." >&2
        local -a cmd=(
            yt-dlp
            --no-playlist
            --retries 10
            --fragment-retries 10
            --force-ipv4
            --concurrent-fragments 1
            --merge-output-format mp4
            -f "$format_selector"
            -o "$output_template"
        )

        if [ -n "$extractor_args" ]; then
            cmd+=(--extractor-args "$extractor_args")
        fi
        cmd+=("$youtube_url")

        "${cmd[@]}" >&2
        if [ $? -eq 0 ]; then
            return 0
        fi
    done

    return 1
}

# Function for ORIGINAL live transcription
original_live_transcription() {
    local model_file=$1
    local language=$2
    local recording_wav="$AUDIO_DOWNLOAD_DIR/${TIMESTAMP}_live_recording.wav"
    local recording_raw="/tmp/live_recording_${TIMESTAMP}.raw"
    local transcript_file="$TRANSCRIPT_DIR/${TIMESTAMP}_live_transcript"

    print_color "$CYAN" "🎙️  ORIGINAL Live Transcription Setup"
    echo "" >&2
    print_color "$YELLOW" "Recording will be saved to: $recording_wav" >&2
    print_color "$YELLOW" "Audio file will be kept for 7 days" >&2
    print_color "$YELLOW" "Live transcript will appear below every ~10 seconds:" >&2
    print_color "$YELLOW" "Final transcript will be saved to: ${transcript_file}.txt" >&2
    echo "" >&2
    print_color "$BLUE" "Press Ctrl+C to stop recording and save transcript" >&2
    echo "" >&2

    # Record as raw PCM (no WAV header) so we can reliably read during recording.
    # Format: 16kHz, mono, 16-bit signed integer, little-endian = 32000 bytes/sec
    print_color "$GREEN" "🔴 Recording started... (Press Ctrl+C to stop)" >&2
    rec -t raw -r 16000 -c 1 -b 16 -e signed-integer "$recording_raw" >/dev/null 2>&1 &
    local rec_pid=$!

    # Show live transcription area
    print_color "$CYAN" "📝 LIVE TRANSCRIPTION:" >&2
    print_color "$CYAN" "════════════════════════════════════════════════════" >&2

    # Function to handle cleanup on exit
    cleanup() {
        print_color "$YELLOW" "\n🛑 Stopping recording..." >&2
        kill $rec_pid 2>/dev/null
        wait $rec_pid 2>/dev/null

        if [ -f "$recording_raw" ] && [ -s "$recording_raw" ]; then
            # Convert raw PCM to WAV for permanent storage and final transcription
            sox -t raw -r 16000 -c 1 -b 16 -e signed-integer -L \
                "$recording_raw" "$recording_wav" 2>/dev/null
            rm -f "$recording_raw"

            print_color "$GREEN" "✅ Recording saved: $recording_wav" >&2
            print_color "$YELLOW" "📁 Audio file will be kept for 7 days" >&2

            # Final transcription of the complete recording
            print_color "$BLUE" "🎯 Performing final transcription..." >&2
            whisper-cli -m "$model_file" -f "$recording_wav" -l "$language" -otxt -of "$transcript_file" -pp -nt >&2

            if [ $? -eq 0 ] && [ -f "${transcript_file}.txt" ]; then
                print_color "$GREEN" "✅ Final transcript saved: ${transcript_file}.txt" >&2
                print_color "$YELLOW" "📝 Final transcript preview:" >&2
                print_color "$CYAN" "────────────────────────────────────────" >&2
                head -20 "${transcript_file}.txt" >&2
                print_color "$CYAN" "────────────────────────────────────────" >&2
            else
                print_color "$RED" "❌ Final transcription failed!" >&2
            fi
        else
            print_color "$RED" "❌ No recording was made!" >&2
        fi

        # Clean up
        rm -f "$recording_raw" 2>/dev/null
        cleanup_old_audio

        exit 0
    }

    # Set up signal handler for cleanup
    trap cleanup SIGINT SIGTERM

    # Incremental chunk-based live transcription
    # Recording is raw PCM: 16kHz, mono, 16-bit = 32000 bytes/sec, no header.
    # File size directly equals audio bytes, so duration = size / 32000.
    # sox reads the raw file and trims out time ranges into proper WAV chunks.
    local BYTES_PER_SEC=32000
    local MIN_CHUNK_SECS=10
    local OVERLAP_SECS=2
    local last_secs=0
    local chunk_count=0
    local running_transcript="/tmp/running_transcript_${TIMESTAMP}.txt"
    touch "$running_transcript"

    while kill -0 $rec_pid 2>/dev/null; do
        if [ -f "$recording_raw" ]; then
            local current_size
            current_size=$(stat -f%z "$recording_raw" 2>/dev/null || echo "0")
            local current_secs=$((current_size / BYTES_PER_SEC))
            local new_secs=$((current_secs - last_secs))

            if [ "$new_secs" -ge "$MIN_CHUNK_SECS" ]; then
                chunk_count=$((chunk_count + 1))

                local chunk_file="/tmp/chunk_${TIMESTAMP}_${chunk_count}.wav"

                # Include overlap from previous chunk for context (except first chunk)
                local trim_start=$last_secs
                if [ "$chunk_count" -gt 1 ] && [ "$trim_start" -ge "$OVERLAP_SECS" ]; then
                    trim_start=$((trim_start - OVERLAP_SECS))
                fi
                local trim_duration=$((current_secs - trim_start))

                # Extract time range from raw PCM → proper WAV for whisper-cli
                sox -t raw -r 16000 -c 1 -b 16 -e signed-integer -L \
                    "$recording_raw" "$chunk_file" \
                    trim "$trim_start" "$trim_duration" 2>/dev/null

                if [ -f "$chunk_file" ] && [ -s "$chunk_file" ]; then
                    local chunk_transcript="/tmp/chunk_transcript_${TIMESTAMP}_${chunk_count}"

                    whisper-cli -m "$model_file" -f "$chunk_file" -l "$language" -otxt -of "$chunk_transcript" -pp -nt >/dev/null 2>&1

                    if [ -f "${chunk_transcript}.txt" ] && [ -s "${chunk_transcript}.txt" ]; then
                        local new_text
                        new_text=$(cat "${chunk_transcript}.txt" | sed '/^$/d')
                        # Filter out Whisper hallucinations on silence/noise
                        local filtered_text
                        filtered_text=$(echo "$new_text" | grep -viE '^[[:space:]]*[][(*].*[])*][[:space:]]*$|^[[:space:]]*$' || true)
                        if [ -n "$filtered_text" ]; then
                            echo "$filtered_text" >> "$running_transcript"
                            print_color "$GREEN" "$filtered_text" >&2
                        fi
                    fi

                    rm -f "$chunk_file" "${chunk_transcript}.txt" 2>/dev/null
                fi

                last_secs=$current_secs
            fi
        fi
        sleep 2
    done

    # Clean up running transcript temp file
    rm -f "$running_transcript" 2>/dev/null

    # Wait for recording to complete
    wait $rec_pid
}

# Main program
print_header

# Clean up old audio files at start
cleanup_old_audio

print_color "$YELLOW" "Select Option:"
echo "" >&2
echo "  🎙️  LIVE TRANSCRIPTION OPTIONS:" >&2
echo "    1) 🔴 ORIGINAL Live Recording + Live Transcript" >&2
echo "    2) 🎥 YouTube Video + Transcript" >&2
echo "    3) 📥 YouTube Video Download Only" >&2
echo "    4) 💼 Zoom Recording + Transcript" >&2
echo "    5) 💬 WhatsApp Audio + Transcript" >&2
echo "    6) 📁 Other Audio/Video File + Transcript" >&2
echo "" >&2
echo "   7) ❌ Exit" >&2
echo "" >&2

read -p "Enter your choice (1-7): " choice

case $choice in
    1) # ORIGINAL Live Recording + Live Transcript
        MODEL_FILE=$(select_available_model)
        LANGUAGE=$(select_language)
        original_live_transcription "$MODEL_FILE" "$LANGUAGE"
        ;;
    2) # YouTube Video + Transcript
        read -p "Enter YouTube URL: " youtube_url
        print_color "$BLUE" "\n📥 Downloading YouTube audio..."
        download_youtube_audio_with_fallback "$youtube_url" "$AUDIO_DOWNLOAD_DIR/${TIMESTAMP}_audio.%(ext)s"
        if [ $? -eq 0 ]; then
            audio_file=$(find "$AUDIO_DOWNLOAD_DIR" -name "${TIMESTAMP}_audio.mp3" -type f -print -quit)
            if [ -n "$audio_file" ]; then
                print_color "$GREEN" "✅ Download complete!"
                print_color "$YELLOW" "📁 Audio file will be kept for 7 days" >&2
                MODEL_FILE=$(select_available_model)
                LANGUAGE=$(select_language)
                print_color "$BLUE" "\n🎯 Transcribing..."
                whisper-cli -m "$MODEL_FILE" -f "$audio_file" -l "$LANGUAGE" -otxt -of "$TRANSCRIPT_DIR/${TIMESTAMP}_youtube" -pp -nt >&2
                if [ $? -eq 0 ]; then
                    print_color "$GREEN" "✅ Transcript saved: $TRANSCRIPT_DIR/${TIMESTAMP}_youtube.txt"
                fi
            fi
        else
            print_color "$RED" "❌ YouTube audio download failed after all fallback attempts."
            print_color "$YELLOW" "Tip: update yt-dlp with: yt-dlp -U" >&2
        fi
        ;;
    3) # YouTube Video Download Only
        read -p "Enter YouTube URL: " youtube_url
        print_color "$BLUE" "\n📥 Downloading YouTube video..."
        download_youtube_video_with_fallback "$youtube_url" "$AUDIO_DOWNLOAD_DIR/${TIMESTAMP}_video.%(ext)s"
        if [ $? -eq 0 ]; then
            video_file=$(find "$AUDIO_DOWNLOAD_DIR" -name "${TIMESTAMP}_video.*" -type f -print -quit)
            if [ -n "$video_file" ]; then
                print_color "$GREEN" "✅ Video download complete!"
                print_color "$YELLOW" "📁 Video file will be kept for 7 days" >&2
                print_color "$BLUE" "📹 Video saved to: $video_file" >&2
            else
                print_color "$RED" "❌ Video download failed!"
            fi
        else
            print_color "$RED" "❌ Video download failed after all fallback attempts!"
            print_color "$YELLOW" "Tip: update yt-dlp with: yt-dlp -U" >&2
        fi
        ;;
    4) # Zoom Recording
        print_color "$YELLOW" "💼 Zoom Recording File:"
        echo "Tip: Drag and drop the file into this terminal" >&2
        read -e -p "Enter file path: " zoom_file
        zoom_file=$(echo "$zoom_file" | sed "s/^'//;s/'$//;s/^\"//;s/\"$//")
        if [ ! -f "$zoom_file" ]; then
            print_color "$RED" "❌ File not found: $zoom_file"
            exit 1
        fi
        MODEL_FILE=$(select_available_model)
        LANGUAGE=$(select_language)
        print_color "$BLUE" "\n🎯 Transcribing..."
        whisper-cli -m "$MODEL_FILE" -f "$zoom_file" -l "$LANGUAGE" -otxt -of "$TRANSCRIPT_DIR/${TIMESTAMP}_zoom" -pp -nt >&2
        if [ $? -eq 0 ]; then
            print_color "$GREEN" "✅ Transcript saved: $TRANSCRIPT_DIR/${TIMESTAMP}_zoom.txt"
        fi
        ;;
    5) # WhatsApp Audio
        print_color "$YELLOW" "💬 WhatsApp Audio File:"
        echo "Tip: Drag and drop the file into this terminal" >&2
        read -e -p "Enter file path: " whatsapp_file
        whatsapp_file=$(echo "$whatsapp_file" | sed "s/^'//;s/'$//;s/^\"//;s/\"$//")
        if [ ! -f "$whatsapp_file" ]; then
            print_color "$RED" "❌ File not found: $whatsapp_file"
            exit 1
        fi
        MODEL_FILE=$(select_available_model)
        LANGUAGE=$(select_language)
        print_color "$BLUE" "\n🎯 Transcribing..."
        whisper-cli -m "$MODEL_FILE" -f "$whatsapp_file" -l "$LANGUAGE" -otxt -of "$TRANSCRIPT_DIR/${TIMESTAMP}_whatsapp" -pp -nt >&2
        if [ $? -eq 0 ]; then
            print_color "$GREEN" "✅ Transcript saved: $TRANSCRIPT_DIR/${TIMESTAMP}_whatsapp.txt"
        fi
        ;;
    6) # Other Audio/Video File
        print_color "$YELLOW" "📁 Audio/Video File:"
        echo "Tip: Drag and drop the file into this terminal" >&2
        read -e -p "Enter file path: " local_file
        local_file=$(echo "$local_file" | sed "s/^'//;s/'$//;s/^\"//;s/\"$//")
        if [ ! -f "$local_file" ]; then
            print_color "$RED" "❌ File not found: $local_file"
            exit 1
        fi
        MODEL_FILE=$(select_available_model)
        LANGUAGE=$(select_language)
        print_color "$BLUE" "\n🎯 Transcribing..."
        whisper-cli -m "$MODEL_FILE" -f "$local_file" -l "$LANGUAGE" -otxt -of "$TRANSCRIPT_DIR/${TIMESTAMP}_local" -pp -nt >&2
        if [ $? -eq 0 ]; then
            print_color "$GREEN" "✅ Transcript saved: $TRANSCRIPT_DIR/${TIMESTAMP}_local.txt"
        fi
        ;;
    7) # Exit
        print_color "$GREEN" "👋 Goodbye!"
        exit 0
        ;;
    *)
        print_color "$RED" "❌ Invalid choice!"
        exit 1
        ;;
esac
