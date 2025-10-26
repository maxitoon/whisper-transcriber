.PHONY: help dev test format lint clean transcribe install

PYTHON := python3
PIP := pip3

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

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

transcribe: ## Run basic transcription (example usage)
	@echo "Usage: python src/transcriber/cli.py <audio_file>"
	@echo "Or use existing scripts from parent directory"

build: ## Build package
	$(PYTHON) -m build

publish: ## Publish to PyPI (requires credentials)
	$(PYTHON) -m twine upload dist/*

# Default target
.DEFAULT_GOAL := help
