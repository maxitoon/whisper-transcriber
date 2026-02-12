"""YouTube audio downloader using yt-dlp."""

import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


class YouTubeDownloader:
    """Handles downloading audio from YouTube videos."""

    def __init__(self, output_dir: Optional[str] = None):
        """Initialize the downloader.

        Args:
            output_dir: Directory to save downloads (default: system temp)
        """
        if not YT_DLP_AVAILABLE:
            raise ImportError(
                "yt-dlp is not installed. "
                "Install it with: pip install yt-dlp"
            )

        self.output_dir = Path(output_dir) if output_dir else Path(tempfile.gettempdir())
        self.output_dir.mkdir(exist_ok=True)

    def download_audio(
        self,
        url: str,
        quality: str = "best[height<=480]",
        format: str = "m4a",
    ) -> Path:
        """Download audio from YouTube video.

        Args:
            url: YouTube URL
            quality: Video quality filter for yt-dlp
            format: Audio format (m4a, mp3, wav, etc.)

        Returns:
            Path to downloaded audio file
        """
        # Common yt-dlp options shared across retry strategies.
        base_opts = {
            "format": f"{quality}/best[height<=480]/best",
            "extract_audio": True,
            "audio_format": format,
            "audio_quality": "192K",
            "outtmpl": str(self.output_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format,
                    "preferredquality": "192",
                }
            ],
        }
        errors: List[str] = []
        for strategy in self._download_strategies(quality):
            ydl_opts = dict(base_opts)
            ydl_opts.update(strategy)

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                return self._resolve_audio_path(
                    filename=filename,
                    input_ext=info.get("ext", ""),
                    output_format=format,
                )
            except Exception as exc:  # pragma: no cover - passthrough from yt-dlp
                errors.append(str(exc))

        last_error = errors[-1] if errors else "unknown yt-dlp failure"
        raise RuntimeError(
            "Failed to download YouTube audio after multiple strategies. "
            "Update yt-dlp (`yt-dlp -U`) and retry. "
            f"Last error: {last_error}"
        )

    def get_video_info(self, url: str) -> dict:
        """Get video information without downloading.

        Args:
            url: YouTube URL

        Returns:
            Video information dictionary
        """
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "ios", "web"],
                }
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info

    def list_formats(self, url: str) -> None:
        """List available formats for a video.

        Args:
            url: YouTube URL
        """
        ydl_opts = {
            "listformats": True,
            "quiet": True,
            "no_warnings": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "ios", "web"],
                }
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)

    def _download_strategies(self, quality: str) -> List[Dict[str, Any]]:
        """Return prioritized yt-dlp download strategies for flaky YouTube clients."""
        return [
            {
                "format": f"{quality}/bestaudio[ext=m4a]/bestaudio/best",
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "ios", "web"],
                    }
                },
            },
            {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "ios", "web"],
                    }
                },
            },
            {
                "format": "140/bestaudio[ext=m4a]/bestaudio/best",
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "web"],
                    }
                },
            },
            {
                "format": "bestaudio/best",
            },
        ]

    def _resolve_audio_path(
        self,
        filename: str,
        input_ext: str,
        output_format: str,
    ) -> Path:
        """Resolve audio output path after post-processing."""
        if input_ext != output_format:
            audio_filename = filename.rsplit(".", 1)[0] + f".{output_format}"
        else:
            audio_filename = filename

        audio_path = Path(audio_filename)
        if not audio_path.exists():
            expected_path = Path(filename.rsplit(".", 1)[0] + f".{output_format}")
            if expected_path.exists():
                audio_path = expected_path

        if not audio_path.exists():
            raise FileNotFoundError(f"Downloaded audio file not found: {audio_path}")

        return audio_path
