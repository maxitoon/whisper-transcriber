# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of our project seriously. If you discover a security vulnerability, please follow these steps:

1. **Do NOT** open a public issue
2. **Do NOT** disclose the vulnerability publicly until it has been addressed
3. Email the security team at security@example.com
4. Provide a detailed description of the vulnerability
5. Include steps to reproduce the issue
6. If possible, provide a proof of concept

## Response Time

We will acknowledge receipt of your vulnerability report within 48 hours and provide a more detailed response within 7 days indicating the next steps in handling your report.

## Security Considerations

This project processes audio files and downloads content from external sources. Please be aware of the following:

### Audio File Processing
- Audio files are processed locally and not uploaded to external services by default
- Be cautious when processing audio files from untrusted sources
- Large files may consume significant system resources

### YouTube Downloads
- The project uses yt-dlp to download content from YouTube
- Downloaded content is stored locally in the `downloads/` directory
- Be mindful of copyright when downloading content

### Dependencies
- This project relies on several third-party libraries (PyTorch, Whisper, yt-dlp)
- Keep dependencies updated to receive security patches
- Use `pip install --upgrade` to update packages regularly

## Best Practices

1. **Environment Variables**: Use the provided `.env.example` file to configure sensitive settings
2. **File Permissions**: Ensure appropriate permissions on downloaded and generated files
3. **Regular Updates**: Keep the project and its dependencies updated
4. **Input Validation**: The project includes basic input validation, but users should still be cautious

## Disclosure Policy

When a security vulnerability is fixed:
- A security advisory will be published
- The fix will be included in the next release
- Users will be notified through GitHub releases and security advisories

## Contact

For security-related questions or reports, please contact security@example.com.
