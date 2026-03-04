"""
Tests for venv-proxy resolver.
"""
import stat
from pathlib import Path
import pytest
from venv_proxy.resolver import resolve_venv


@pytest.fixture
def tmp_project(tmp_path):
    """Create a fake project with a .venv."""
    venv_bin = tmp_path / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    python = venv_bin / "python"
    python.write_text("#!/usr/bin/env python3\n")
    python.chmod(python.stat().st_mode | stat.S_IEXEC)
    pip = venv_bin / "pip"
    pip.write_text("#!/usr/bin/env python3\n")
    pip.chmod(pip.stat().st_mode | stat.S_IEXEC)
    return tmp_path


def test_finds_venv_in_cwd(tmp_project):
    result = resolve_venv(tmp_project, "python")
    assert result == tmp_project / ".venv" / "bin" / "python"


def test_finds_venv_in_parent(tmp_project):
    subdir = tmp_project / "src" / "mymodule"
    subdir.mkdir(parents=True)
    result = resolve_venv(subdir, "python")
    assert result == tmp_project / ".venv" / "bin" / "python"


def test_finds_venv_deeply_nested(tmp_project):
    deep = tmp_project / "a" / "b" / "c" / "d"
    deep.mkdir(parents=True)
    result = resolve_venv(deep, "python")
    assert result == tmp_project / ".venv" / "bin" / "python"


def test_returns_none_when_no_venv(tmp_path):
    result = resolve_venv(tmp_path, "python")
    assert result is None


def test_finds_pip(tmp_project):
    result = resolve_venv(tmp_project, "pip")
    assert result == tmp_project / ".venv" / "bin" / "pip"


def test_returns_none_for_missing_binary(tmp_project):
    result = resolve_venv(tmp_project, "nonexistent-binary")
    assert result is None


def test_max_depth_respected(tmp_path):
    # Create venv at root but search from deep subdir with max_depth=2
    venv_bin = tmp_path / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    python = venv_bin / "python"
    python.write_text("#!/usr/bin/env python3\n")
    python.chmod(python.stat().st_mode | stat.S_IEXEC)

    deep = tmp_path / "a" / "b" / "c"
    deep.mkdir(parents=True)

    # max_depth=2 won't reach tmp_path from deep
    result = resolve_venv(deep, "python", max_depth=2)
    assert result is None


def test_finds_within_max_depth(tmp_project):
    subdir = tmp_project / "src"
    subdir.mkdir()
    result = resolve_venv(subdir, "python", max_depth=2)
    assert result == tmp_project / ".venv" / "bin" / "python"


def test_prefers_nearest_venv(tmp_path):
    # Outer venv
    outer_bin = tmp_path / ".venv" / "bin"
    outer_bin.mkdir(parents=True)
    outer_py = outer_bin / "python"
    outer_py.write_text("#!/usr/bin/env python3\n")
    outer_py.chmod(outer_py.stat().st_mode | stat.S_IEXEC)

    # Inner venv (closer)
    inner = tmp_path / "sub"
    inner_bin = inner / ".venv" / "bin"
    inner_bin.mkdir(parents=True)
    inner_py = inner_bin / "python"
    inner_py.write_text("#!/usr/bin/env python3\n")
    inner_py.chmod(inner_py.stat().st_mode | stat.S_IEXEC)

    result = resolve_venv(inner, "python")
    assert result == inner / ".venv" / "bin" / "python"


def test_handles_symlinks(tmp_path):
    """Le resolver suit les symlinks vers le binaire."""
    venv_bin = tmp_path / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    
    # Create real python
    real_python = venv_bin / "python3.11"
    real_python.write_text("#!/usr/bin/env python3\n")
    real_python.chmod(real_python.stat().st_mode | stat.S_IEXEC)
    
    # Create symlink python -> python3.11
    python_link = venv_bin / "python"
    python_link.symlink_to(real_python)
    
    result = resolve_venv(tmp_path, "python")
    assert result == python_link


def test_ignores_corrupted_venv(tmp_path):
    """Le resolver ignore les .venv avec binaire non exécutable."""
    venv_bin = tmp_path / ".venv" / "bin"
    venv_bin.mkdir(parents=True)
    
    # Create non-executable python
    python = venv_bin / "python"
    python.write_text("#!/usr/bin/env python3\n")
    # Don't make it executable
    
    result = resolve_venv(tmp_path, "python")
    assert result is None


def test_ignores_corrupted_venv_directory(tmp_path):
    """Le resolver ignore les .venv qui sont des fichiers, pas des dossiers."""
    # Create .venv as a file instead of directory
    venv_file = tmp_path / ".venv"
    venv_file.write_text("not a directory")
    
    result = resolve_venv(tmp_path, "python")
    assert result is None
