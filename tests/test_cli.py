"""Tests for CLI functionality."""

import pytest
from click.testing import CliRunner

from transcriber.cli import main


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

    def test_transcribe_missing_file(self):
        """Test transcribe command with missing file."""
        runner = CliRunner()
        result = runner.invoke(main, ["transcribe", "nonexistent.mp3"])

        # Should fail gracefully
        assert result.exit_code != 0

    def test_youtube_missing_url(self):
        """Test youtube command with missing URL."""
        runner = CliRunner()
        result = runner.invoke(main, ["youtube"])

        assert result.exit_code != 0
