"""Tests for YouTube downloader fallback behavior."""

from pathlib import Path
from types import SimpleNamespace

from transcriber import downloader


def test_download_audio_retries_after_first_attempt_fails(monkeypatch, tmp_path):
    """Downloader should retry with fallback options when first attempt fails."""
    attempts = []
    expected_output = tmp_path / "sample.mp3"

    class FakeYoutubeDL:
        def __init__(self, opts):
            self.opts = opts
            attempts.append(opts)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def extract_info(self, url, download=True):  # noqa: ARG002
            if len(attempts) == 1:
                raise RuntimeError("HTTP Error 403: Forbidden")
            expected_output.write_bytes(b"audio")
            return {"ext": "webm", "title": "sample"}

        def prepare_filename(self, info):  # noqa: ARG002
            return str(tmp_path / "sample.webm")

    monkeypatch.setattr(
        downloader,
        "yt_dlp",
        SimpleNamespace(YoutubeDL=FakeYoutubeDL),
    )
    monkeypatch.setattr(downloader, "YT_DLP_AVAILABLE", True)

    dl = downloader.YouTubeDownloader(output_dir=str(tmp_path))
    result = dl.download_audio("https://youtu.be/test-id", quality="bestaudio", format="mp3")

    assert result == Path(expected_output)
    assert len(attempts) == 2
