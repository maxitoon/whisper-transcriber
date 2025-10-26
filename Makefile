.PHONY: help dev test format lint clean transcribe install

PYTHON := python3
PIP := pip3

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Main Commands:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ''
	@echo 'Quick Start:'
	@echo '  make quick-setup    # Show setup instructions'
	@echo '  make transcribe     # Run main transcription script'

dev: ## Install development dependencies
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

install: ## Install production dependencies
	$(PIP) install -r requirements.txt

test: ## Run tests
	pytest tests/ -v --cov=src/transcriber

format: ## Format code with black and isort
	black src/ tests/
	isort src/ tests/

lint: ## Run linting with ruff and mypy
	ruff check src/ tests/
	mypy src/ tests/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

transcribe: ## Run the main transcription script
	@echo "🎙️  Starting Whisper Transcription..."
	@echo "Make sure whisper-cli and dependencies are installed!"
	@echo ""
	../whisper-transcribe-with-download.sh

quick-setup: ## Quick setup and run
	@echo "🔧 Quick Setup Guide:"
	@echo "1. Install whisper-cli from: https://github.com/ggerganov/whisper.cpp"
	@echo "2. Install dependencies: brew install ffmpeg sox yt-dlp"
	@echo "3. Download Whisper models to ~/whisper-models/"
	@echo "4. Run: make transcribe"

build: ## Build package
	$(PYTHON) -m build

publish: ## Publish to PyPI (requires credentials)
	$(PYTHON) -m twine upload dist/*

# Default target
.DEFAULT_GOAL := help
