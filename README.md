# awesome-foamlib  [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![All Contributors](https://img.shields.io/github/all-contributors/tkoyama010/awesome-foamlib?color=ee8449)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

<div align="center">
<a href="https://github.com/gerlero/foamlib"><img src="https://github.com/gerlero/foamlib/raw/main/logo.png" height="65"></a>
</div>

> **foamlib** is a modern Python package that provides an elegant, streamlined interface for interacting with OpenFOAM. It's designed to make OpenFOAM-based workflows more accessible, reproducible, and precise for researchers and engineers.

An awesome list for [foamlib](https://github.com/exasim-project/foamlib) with OpenFOAM tutorials using sphinx-gallery.

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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tkoyama010"><img src="https://avatars.githubusercontent.com/u/7513610?v=4?s=100" width="100px;" alt="Tetsuo Koyama"/><br /><sub><b>Tetsuo Koyama</b></sub></a><br /><a href="#ideas-tkoyama010" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
