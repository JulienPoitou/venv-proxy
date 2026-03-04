# Changelog

All notable changes to venv-proxy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Full test suite (43 tests) covering resolver, shim, CLI, and integration
- GitHub Actions workflows for CI/CD (test on Ubuntu/macOS × Python 3.9/3.11/3.13)
- GitHub Actions workflow for PyPI publishing on release
- `doctor` command enhancements: detect conflicting shims, pyenv, and conda
- Support for symlinks in `.venv/bin/`
- Handling of corrupted `.venv` directories (non-executable binaries)
- Example project with CLAUDE.md for AI coding agents

### Changed
- Improved resolver to check executable permissions
- Better error handling in shim fallback

### Fixed
- Resolver now properly follows symlinks
- Resolver ignores non-executable files in `.venv/bin/`

## [0.1.0] - 2026-03-04

### Added
- Initial release
- `venv-proxy install` command
- `venv-proxy uninstall` command
- `venv-proxy status` command
- `venv-proxy doctor` command
- Automatic `.venv` resolution by walking up filesystem
- Transparent `execv()` shim for zero overhead
- Fallback to system Python when no `.venv` found
- Debug mode via `VENV_PROXY_DEBUG=1`

[Unreleased]: https://github.com/yourusername/venv-proxy/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/venv-proxy/releases/tag/v0.1.0
