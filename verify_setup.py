#!/usr/bin/env python3
"""Verification script for Whisper Transcriber setup."""

import sys
from pathlib import Path


def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists and report the result."""
    path = Path(filepath)
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists


def check_directory_structure() -> bool:
    """Check if the directory structure is correct."""
    print("📁 Checking directory structure...")

    checks = [
        ("src/transcriber/__init__.py", "Main package init"),
        ("src/transcriber/cli.py", "CLI module"),
        ("src/transcriber/engine.py", "Transcription engine"),
        ("src/transcriber/downloader.py", "YouTube downloader"),
        ("src/transcriber/formatters/__init__.py", "Formatters package"),
        ("tests/__init__.py", "Tests package"),
        ("tests/test_cli.py", "CLI tests"),
        ("tests/test_engine.py", "Engine tests"),
        ("docs/architecture.md", "Architecture docs"),
        ("docs/roadmap.md", "Roadmap docs"),
        ("docs/scripts.md", "Scripts docs"),
        (".gitignore", "Git ignore file"),
        (".editorconfig", "Editor config"),
        ("pyproject.toml", "Project configuration"),
        ("setup.py", "Setup script"),
        ("requirements.txt", "Requirements"),
        ("requirements-dev.txt", "Dev requirements"),
        ("Makefile", "Build automation"),
        ("env.example", "Environment template"),
        ("README.md", "Main README"),
        ("CONTRIBUTING.md", "Contributing guide"),
        ("CODE_OF_CONDUCT.md", "Code of conduct"),
        ("SECURITY.md", "Security policy"),
        ("LICENSE", "License file"),
        (".pre-commit-config.yaml", "Pre-commit config"),
    ]

    all_passed = True
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_passed = False

    return all_passed


def check_github_structure() -> bool:
    """Check GitHub-specific files."""
    print("\n🔗 Checking GitHub configuration...")

    checks = [
        (".github/workflows/ci.yml", "CI workflow"),
        (".github/ISSUE_TEMPLATE/bug_report.md", "Bug report template"),
        (".github/ISSUE_TEMPLATE/feature_request.md", "Feature request template"),
        (".github/PULL_REQUEST_TEMPLATE.md", "PR template"),
    ]

    all_passed = True
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_passed = False

    return all_passed


def check_python_version() -> bool:
    """Check Python version compatibility."""
    print("\n🐍 Checking Python version...")

    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False


def main():
    """Run all verification checks."""
    print("🔍 Whisper Transcriber Setup Verification")
    print("=" * 50)

    all_checks_passed = True

    # Check directory structure
    if not check_directory_structure():
        all_checks_passed = False

    # Check GitHub structure
    if not check_github_structure():
        all_checks_passed = False

    # Check Python version
    if not check_python_version():
        all_checks_passed = False

    print("\n" + "=" * 50)

    if all_checks_passed:
        print("🎉 All checks passed! The project is ready for development.")
        print("\nNext steps:")
        print("1. Run 'make dev' to install development dependencies")
        print("2. Run 'make test' to verify tests work")
        print("3. Run 'python src/transcriber/cli.py --help' to test CLI")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
