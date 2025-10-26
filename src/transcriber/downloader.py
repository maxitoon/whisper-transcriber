"""YouTube audio downloader using yt-dlp."""

import tempfile
from pathlib import Path
from typing import Optional

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
        # Configure yt-dlp options
        ydl_opts = {
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

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Convert to audio format if needed
            if info.get("ext") != format:
                audio_filename = filename.rsplit(".", 1)[0] + f".{format}"
            else:
                audio_filename = filename

        audio_path = Path(audio_filename)
        if not audio_path.exists():
            # Fallback: look for the file with the expected extension
            expected_path = Path(filename.rsplit(".", 1)[0] + f".{format}")
            if expected_path.exists():
                audio_path = expected_path

        if not audio_path.exists():
            raise FileNotFoundError(f"Downloaded audio file not found: {audio_path}")

        return audio_path

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
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
