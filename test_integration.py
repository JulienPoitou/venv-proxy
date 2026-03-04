"""
End-to-end integration tests for venv-proxy.
Tests the full workflow: install shims, create venv, run commands.
"""
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from venv_proxy.cli import install, uninstall, SHIM_DIR, SHIMS
from venv_proxy.resolver import resolve_venv


@pytest.fixture
def isolated_env(tmp_path, monkeypatch):
    """Create an isolated test environment."""
    # Create isolated directories
    test_shim_dir = tmp_path / ".local" / "bin"
    test_home = tmp_path / "home"
    test_home.mkdir()

    # Monkeypatch environment
    monkeypatch.setenv("HOME", str(test_home))
    monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)

    return {
        "tmp_path": tmp_path,
        "shim_dir": test_shim_dir,
        "home": test_home,
    }


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_install_creates_working_shims(self, isolated_env, monkeypatch):
        """Installer crée des shims qui fonctionnent."""
        # Install shims
        install()

        # Verify shims exist and are executable
        for binary in SHIMS:
            shim_path = isolated_env["shim_dir"] / binary
            assert shim_path.exists()
            assert shim_path.stat().st_mode & stat.S_IEXEC

            # Verify shim content
            content = shim_path.read_text()
            assert "venv-proxy shim" in content
            assert f'run_shim("{binary}")' in content

    def test_resolver_finds_venv_in_cwd(self, tmp_path):
        """Le resolver trouve le .venv dans le CWD."""
        venv_bin = tmp_path / ".venv" / "bin"
        venv_bin.mkdir(parents=True)
        python = venv_bin / "python"
        python.write_text("#!/usr/bin/env python3\n")
        python.chmod(python.stat().st_mode | 0o111)

        result = resolve_venv(tmp_path, "python")
        assert result == python

    def test_resolver_finds_venv_in_parent(self, tmp_path):
        """Le resolver trouve le .venv depuis un sous-dossier."""
        venv_bin = tmp_path / ".venv" / "bin"
        venv_bin.mkdir(parents=True)
        python = venv_bin / "python"
        python.write_text("#!/usr/bin/env python3\n")
        python.chmod(python.stat().st_mode | 0o111)

        # Create subdirectory
        subdir = tmp_path / "src" / "module"
        subdir.mkdir(parents=True)

        result = resolve_venv(subdir, "python")
        assert result == python

    def test_full_workflow(self, tmp_path, monkeypatch, capsys):
        """Test complet: install + create venv + verify resolution."""
        # Setup isolated environment
        test_shim_dir = tmp_path / ".local" / "bin"
        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)

        # Step 1: Install shims
        install()
        assert test_shim_dir.exists()

        # Step 2: Create a fake project with .venv
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        venv_bin = project_dir / ".venv" / "bin"
        venv_bin.mkdir(parents=True)

        # Create fake python in venv
        venv_python = venv_bin / "python"
        venv_python.write_text("#!/usr/bin/env python3\n")
        venv_python.chmod(venv_python.stat().st_mode | 0o111)

        # Step 3: Verify resolver finds it
        monkeypatch.chdir(project_dir)
        result = resolve_venv(project_dir, "python")
        assert result == venv_python

        # Step 4: Verify from subdirectory
        src_dir = project_dir / "src"
        src_dir.mkdir()
        monkeypatch.chdir(src_dir)
        result = resolve_venv(src_dir, "python")
        assert result == venv_python

    def test_uninstall_removes_shims(self, isolated_env, capsys):
        """Uninstall supprime les shims."""
        # Install first
        install()
        capsys.readouterr()  # Clear output

        # Verify shims exist
        for binary in SHIMS:
            assert (isolated_env["shim_dir"] / binary).exists()

        # Uninstall
        uninstall()

        # Verify shims are removed
        for binary in SHIMS:
            assert not (isolated_env["shim_dir"] / binary).exists()

        captured = capsys.readouterr()
        assert "removed shims" in captured.out

    def test_no_venv_falls_back_to_none(self, tmp_path):
        """Quand pas de .venv, resolve_venv retourne None."""
        result = resolve_venv(tmp_path, "python")
        assert result is None

    def test_multiple_venvs_prefers_nearest(self, tmp_path):
        """Quand plusieurs .venv existent, le plus proche est choisi."""
        # Outer venv
        outer_bin = tmp_path / ".venv" / "bin"
        outer_bin.mkdir(parents=True)
        outer_python = (outer_bin / "python")
        outer_python.write_text("#!/usr/bin/env python3\n")
        outer_python.chmod(outer_python.stat().st_mode | 0o111)

        # Inner project with its own venv
        inner = tmp_path / "subproject"
        inner_bin = inner / ".venv" / "bin"
        inner_bin.mkdir(parents=True)
        inner_python = (inner_bin / "python")
        inner_python.write_text("#!/usr/bin/env python3\n")
        inner_python.chmod(inner_python.stat().st_mode | 0o111)

        # Should find inner venv
        result = resolve_venv(inner, "python")
        assert result == inner_python

        # From outer level, should find outer venv
        result = resolve_venv(tmp_path, "python")
        assert result == outer_python
