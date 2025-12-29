# awesome-foamlib

An awesome list for [foamlib](https://github.com/exasim-project/foamlib) with OpenFOAM tutorials using sphinx-gallery.

## Overview

This repository serves as a curated collection of resources, tools, and tutorials for working with foamlib - a Python library for interacting with OpenFOAM.

## Features

- 📚 Curated list of foamlib resources
- 🎓 Interactive tutorials using sphinx-gallery
- 🚀 Modern Python packaging with uv
- 📖 Comprehensive documentation

## Installation

### Using uv (recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/tkoyama010/awesome-foamlib.git
cd awesome-foamlib

# Sync dependencies
uv sync
```

### Using pip

```bash
pip install -e .
```

## Development

This project uses [uv](https://github.com/astral-sh/uv) for fast, modern Python package management.

### Setup development environment

```bash
# Sync all dependencies including dev dependencies
uv sync

# Run tests (after test files are created)
uv run pytest

# Build documentation (after setting up docs/ directory with Sphinx configuration)
# cd docs
# uv run make html
```

## Project Structure

```
awesome-foamlib/
├── src/
│   └── awesome_foamlib/    # Main package
├── docs/                    # Documentation (future)
├── examples/                # Tutorial examples (future)
├── pyproject.toml          # Project configuration
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Related Projects

- [foamlib](https://github.com/exasim-project/foamlib) - Python library for OpenFOAM
- [OpenFOAM](https://www.openfoam.com/) - Open source CFD software