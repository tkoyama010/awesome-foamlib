# awesome-foamlib  [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

<div align="center">
<a href="https://github.com/gerlero/foamlib"><img src="https://github.com/gerlero/foamlib/raw/main/logo.png" height="65"></a>
</div>

> **foamlib** is a modern Python package that provides an elegant, streamlined interface for interacting with OpenFOAM. It's designed to make OpenFOAM-based workflows more accessible, reproducible, and precise for researchers and engineers.

An awesome list for [foamlib](https://github.com/exasim-project/foamlib) with OpenFOAM tutorials using sphinx-gallery.

## Features

- Curated list of foamlib resources
- Interactive tutorials using sphinx-gallery
- Docker SDK-based OpenFOAM runner for robust container management
- Modern Python packaging with uv
- Comprehensive documentation

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

## Quick Start

### Docker SDK Runner

Run OpenFOAM commands in Docker containers with a robust Python API:

```python
from pathlib import Path
from awesome_foamlib import DockerFoamRunner

# Initialize runner
runner = DockerFoamRunner()

# Run OpenFOAM commands
runner.run(Path("./cavity"), "blockMesh")
runner.run(Path("./cavity"), "icoFoam")
```

## Development

This project uses [uv](https://github.com/astral-sh/uv) for fast, modern Python package management.

### Setup development environment

```bash
# Sync all dependencies including dev dependencies
uv sync

# Run tests (after test files are created)
uv run pytest

# Run type checking
uv run mypy src/

# Run linting
uv run ruff check src/

# Build documentation (after setting up docs/ directory with Sphinx configuration)
# cd docs
# uv run make html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3 - see the [LICENSE](LICENSE) file for details.

Copyright (C) 2025 Tetsuo Koyama

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

## Related Projects

- [foamlib](https://github.com/exasim-project/foamlib) - Python library for OpenFOAM
- [OpenFOAM](https://www.openfoam.com/) - Open source CFD software
