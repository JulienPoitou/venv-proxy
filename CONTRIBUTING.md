# Contributing to venv-proxy

Thank you for considering contributing to venv-proxy! This document provides guidelines and instructions for contributing.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/venv-proxy.git
cd venv-proxy

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with test dependencies
pip install -e .
pip install pytest
```

## Running Tests

```bash
# Run all tests
python -m pytest test_*.py -v

# Run specific test file
python -m pytest test_resolver.py -v

# Run with coverage
python -m pytest test_*.py --cov=venv_proxy --cov-report=term-missing
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where possible
- Write docstrings for public functions
- Keep functions small and focused

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation if needed
7. Commit with clear messages
8. Open a Pull Request

## Reporting Issues

When reporting a bug, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Any relevant error messages

## Feature Requests

Feature requests are welcome! Please include:
- What problem you're trying to solve
- How you envision the feature working
- Any alternative solutions you've considered

## License

By contributing to venv-proxy, you agree that your contributions will be licensed under the MIT License.
