"""Tests for transcription engine."""

import pytest
from unittest.mock import Mock, patch

from transcriber.engine import TranscriptionEngine, WHISPER_AVAILABLE


class TestTranscriptionEngine:
    """Test cases for transcription engine."""

    @pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Python Whisper not installed")
    def test_init_default(self):
        """Test engine initialization with default parameters."""
        engine = TranscriptionEngine()
        assert engine.model_name == "base"
        assert engine.device == "cpu"
        assert engine.verbose is False
        assert engine.model is not None

    @pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Python Whisper not installed")
    def test_init_custom_params(self):
        """Test engine initialization with custom parameters."""
        engine = TranscriptionEngine(model="tiny", device="cpu", verbose=True)
        assert engine.model_name == "tiny"
        assert engine.device == "cpu"
        assert engine.verbose is True

    def test_whisper_not_available(self):
        """Test behavior when Python Whisper is not available."""
        if not WHISPER_AVAILABLE:
            with pytest.raises(ImportError, match="Python Whisper is not installed"):
                TranscriptionEngine()

    @pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Python Whisper not installed")
    def test_format_timestamp_srt(self):
        """Test SRT timestamp formatting."""
        engine = TranscriptionEngine()

        # Test basic formatting
        assert engine._format_timestamp(0) == "00:00:00.000"
        assert engine._format_timestamp(3661.5) == "01:01:01.500"

    @pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Python Whisper not installed")
    def test_format_timestamp_vtt(self):
        """Test VTT timestamp formatting."""
        engine = TranscriptionEngine()

        # Test VTT formatting (uses commas instead of periods)
        assert engine._format_timestamp(0, vtt=True) == "00:00:00,000"
        assert engine._format_timestamp(3661.5, vtt=True) == "01:01:01,500"

    @pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Python Whisper not installed")
    def test_clean_result_for_json(self):
        """Test cleaning result for JSON serialization."""
        engine = TranscriptionEngine()

        # Mock result with various data types
        mock_result = {
            "text": "Hello world",
            "segments": [
                {
                    "start": 0.0,
                    "end": 1.0,
                    "text": "Hello",
                }
            ],
            "language": "en",
        }

        clean_result = engine._clean_result_for_json(mock_result)

        # Should be identical since no tensors or complex objects
        assert clean_result == mock_result

    @pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Python Whisper not installed")
    @patch('whisper.load_model')
    def test_load_model_called(self, mock_load_model):
        """Test that whisper.load_model is called during initialization."""
        mock_model = Mock()
        mock_load_model.return_value = mock_model

        engine = TranscriptionEngine(model="tiny")

        mock_load_model.assert_called_once_with("tiny", device="cpu")
        assert engine.model == mock_model
