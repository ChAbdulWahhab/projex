# Installation

## Requirements

- **Python 3.8+** - Required
- **pip** - Package manager
- **Git** - For version control (optional)

## Quick Install

### From PyPI (Recommended)

```bash
pip install projex
```

### Verify Installation

```bash
projex --version
# Output: projex, version 4.0.0

projex --help
# Shows all available commands
```

## Install from Source

For development or latest features:

```bash
# Clone repository
git clone https://github.com/ChAbdulWahhab/projex.git
cd projex

# Install in editable mode
pip install -e .
```

## Upgrade Projex

```bash
pip install --upgrade projex
```

## Uninstall

```bash
pip uninstall projex
```

## Platform-Specific Notes

### Windows

```powershell
# Install
pip install projex

# Add to PATH if needed
# Python Scripts folder should be in PATH
```

### Linux/Mac

```bash
# Install
pip3 install projex

# If permission error
pip3 install --user projex
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install
pip install projex
```

## Dependencies

Projex automatically installs:

- `click` - CLI framework
- `rich` - Beautiful terminal output
- `jinja2` - Template engine
- `requests` - HTTP library

## Troubleshooting

### Command not found

```bash
# Add Python Scripts to PATH
# Windows: Add C:\Python3X\Scripts to PATH
# Linux/Mac: Add ~/.local/bin to PATH
```

### Permission Denied

```bash
# Use --user flag
pip install --user projex
```

### SSL Certificate Error

```bash
# Use trusted host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org projex
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Create Your First Project](first-project.md)