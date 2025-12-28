# PyomoDebugger

A debugging tool and utility suite for [Pyomo](http://www.pyomo.org/), an open-source optimization modeling language in Python.

## Features

- Debugging utilities for Pyomo models
- Model inspection tools
- Performance analysis
- Error diagnosis and reporting

## Quick Start

### Prerequisites

- Python 3.8 or higher
- [uv](https://astral.sh/blog/uv/) package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PyomoDebugger
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

## Development

For detailed development setup instructions, see [DEVELOPMENT.md](DEVELOPMENT.md).

## Project Structure

```
PyomoDebugger/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .pre-commit-config.yaml
├── DEVELOPMENT.md
└── src/
    └── pyomo_debugger/
        └── __init__.py
```

## Contributing

Contributions are welcome! Please make sure to:
1. Run pre-commit checks before committing
2. Follow the code style guidelines (enforced by ruff and mypy)
3. Write clear commit messages

## License

[Add your license here]

## Support

For issues and questions, please open an issue on GitHub.
