# Contributing to Whisper Transcriber

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Pull Request Process

1. Update the README.md with details of changes to the interface, if applicable
2. Update the version numbers in any examples files and the README.md to the new version that this Pull Request would represent
3. Follow the PR template when creating your pull request

## Testing

- All new features should include tests
- Run the test suite with `make test`
- Ensure code coverage doesn't decrease significantly

## Code Style

- Follow PEP 8 style guidelines
- Use `make format` to format your code
- Use `make lint` to check for issues

## Commit Messages

We follow the [Conventional Commits](https://conventionalcommits.org/) specification:

```
feat: add new transcription model support
fix: resolve memory leak in audio processing
docs: update README with new examples
test: add unit tests for YouTube downloader
```

## License

By contributing, you agree that your contributions will be licensed under the same license as the original project.

## References

This document is adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/master/CONTRIBUTING.md).
