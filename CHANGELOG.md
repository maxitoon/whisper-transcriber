# Changelog

All notable changes to Whisper Transcriber will be documented in this file.

The format follows practical, human-readable release notes. Add new entries above the initial baseline section.

## Unreleased

- Improved README SEO and LLM discoverability with clearer positioning, use cases, examples, FAQ, alternatives, and roadmap sections.
- Added `.seo/project-profile.md` as the canonical SEO/LLM context file for the project.
- Added `llms.txt` for LLM crawler and assistant discoverability.

## Initial baseline

- Local-first interactive transcription workflow using `whisper-cli` from whisper.cpp.
- Live microphone transcription with incremental chunk-based output.
- YouTube download and transcription via `yt-dlp` with fallback strategies.
- Local file transcription for Zoom recordings, WhatsApp audio, and arbitrary audio/video files.
- Optional Python CLI for programmatic transcription workflows.
