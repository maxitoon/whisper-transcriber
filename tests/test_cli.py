"""Tests for CLI functionality."""

import pytest
from click.testing import CliRunner

from transcriber.cli import main
from transcriber.downloader import YT_DLP_AVAILABLE
from transcriber.engine import WHISPER_AVAILABLE


class TestCLI:
    """Test cases for command-line interface."""

    def test_main_help(self):
        """Test main help command."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Whisper Transcriber" in result.output
        assert "transcribe" in result.output
        assert "youtube" in result.output

    def test_models_command(self):
        """Test models listing command."""
        runner = CliRunner()
        result = runner.invoke(main, ["models"])

        assert result.exit_code == 0
        assert "Available Whisper models:" in result.output
        assert "base" in result.output
        assert "tiny" in result.output
        assert "large" in result.output

    @pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Python Whisper not installed")
    def test_transcribe_missing_file(self):
        """Test transcribe command with missing file."""
        runner = CliRunner()
        result = runner.invoke(main, ["transcribe", "nonexistent.mp3"])

        # Should fail gracefully
        assert result.exit_code != 0

    def test_transcribe_without_whisper(self):
        """Test transcribe command when Whisper is not available."""
        if not WHISPER_AVAILABLE:
            # Create a dummy file so we can test the whisper availability check
            import tempfile
            import os

            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tmp_path = tmp.name

            try:
                runner = CliRunner()
                result = runner.invoke(main, ["transcribe", tmp_path])

                assert result.exit_code != 0
                assert "Python Whisper is not installed" in result.output
            finally:
                os.unlink(tmp_path)

    @pytest.mark.skipif(not YT_DLP_AVAILABLE, reason="yt-dlp not installed")
    def test_youtube_missing_url(self):
        """Test youtube command with missing URL."""
        runner = CliRunner()
        result = runner.invoke(main, ["youtube"])

        assert result.exit_code != 0

    def test_youtube_without_ytdlp(self):
        """Test youtube command when yt-dlp is not available."""
        if not YT_DLP_AVAILABLE:
            runner = CliRunner()
            result = runner.invoke(main, ["youtube", "https://youtube.com/watch?v=test"])

            assert result.exit_code != 0
            assert "yt-dlp is not installed" in result.output
