"""Transcription engine using OpenAI Whisper."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import torch
import whisper
from tqdm import tqdm


class TranscriptionEngine:
    """Handles audio transcription using OpenAI Whisper."""

    def __init__(
        self,
        model: str = "base",
        device: str = "cpu",
        verbose: bool = False,
    ):
        """Initialize the transcription engine.

        Args:
            model: Whisper model size (tiny, base, small, medium, large, large-v2, large-v3)
            device: Device to run on (cpu, cuda)
            verbose: Enable verbose output
        """
        self.model_name = model
        self.device = device
        self.verbose = verbose
        self.model = None

        # Auto-detect device if not specified
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self._load_model()

    def _load_model(self) -> None:
        """Load the Whisper model."""
        if self.verbose:
            print(f"Loading Whisper model: {self.model_name}")

        self.model = whisper.load_model(
            self.model_name,
            device=self.device,
        )

        if self.verbose:
            print(f"Model loaded on device: {self.device}")

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        chunk_length: int = 30,
    ) -> Dict[str, Any]:
        """Transcribe audio file.

        Args:
            audio_path: Path to audio file
            language: Language code (optional, auto-detected if None)
            chunk_length: Length of audio chunks in seconds

        Returns:
            Transcription result dictionary
        """
        if not self.model:
            raise RuntimeError("Model not loaded")

        if self.verbose:
            print(f"Transcribing: {audio_path}")

        # Transcribe with options
        result = self.model.transcribe(
            audio_path,
            verbose=self.verbose,
            language=language,
            task="transcribe",
        )

        return result

    def save_txt(self, result: Dict[str, Any], output_path: Path) -> None:
        """Save transcription as plain text."""
        text = result["text"].strip()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        if self.verbose:
            print(f"Saved text to: {output_path}")

    def save_srt(self, result: Dict[str, Any], output_path: Path) -> None:
        """Save transcription as SRT subtitle file."""
        segments = result.get("segments", [])

        with open(output_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments, 1):
                start = self._format_timestamp(segment["start"])
                end = self._format_timestamp(segment["end"])
                text = segment["text"].strip()

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        if self.verbose:
            print(f"Saved SRT to: {output_path}")

    def save_vtt(self, result: Dict[str, Any], output_path: Path) -> None:
        """Save transcription as VTT subtitle file."""
        segments = result.get("segments", [])

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")

            for segment in segments:
                start = self._format_timestamp(segment["start"], vtt=True)
                end = self._format_timestamp(segment["end"], vtt=True)
                text = segment["text"].strip()

                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        if self.verbose:
            print(f"Saved VTT to: {output_path}")

    def save_json(self, result: Dict[str, Any], output_path: Path) -> None:
        """Save transcription as JSON."""
        # Remove binary data if present
        clean_result = self._clean_result_for_json(result)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(clean_result, f, indent=2, ensure_ascii=False)

        if self.verbose:
            print(f"Saved JSON to: {output_path}")

    def _format_timestamp(self, seconds: float, vtt: bool = False) -> str:
        """Format timestamp for subtitle files."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60

        if vtt:
            return f"{hours"02d"}:{minutes"02d"}:{seconds"06.3f"}".replace(".", ",")
        else:
            return f"{hours"02d"}:{minutes"02d"}:{seconds"06.3f"}"

    def _clean_result_for_json(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Remove non-serializable data from result."""
        # Create a copy to avoid modifying original
        clean_result = {}

        for key, value in result.items():
            if isinstance(value, torch.Tensor):
                # Convert tensors to lists
                clean_result[key] = value.tolist()
            elif isinstance(value, dict):
                clean_result[key] = self._clean_result_for_json(value)
            elif isinstance(value, list):
                clean_result[key] = [
                    self._clean_result_for_json(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                clean_result[key] = value

        return clean_result
