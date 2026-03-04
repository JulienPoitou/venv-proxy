"""
Tests for venv-proxy CLI.
"""
import os
import stat
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import pytest

from venv_proxy.cli import install, uninstall, status, doctor, _check_path_warning, SHIM_DIR, SHIMS


class TestInstall:
    """Tests pour la commande install."""

    def test_install_creée_shims(self, tmp_path, monkeypatch, capsys):
        """venv-proxy install crée les shims dans ~/.local/bin."""
        test_shim_dir = tmp_path / ".local" / "bin"
        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)

        with patch("venv_proxy.cli._check_path_warning"):
            install()

        for binary in SHIMS:
            shim_path = test_shim_dir / binary
            assert shim_path.exists()
            assert shim_path.stat().st_mode & stat.S_IEXEC
            content = shim_path.read_text()
            assert "venv-proxy shim" in content
            assert binary in content

        captured = capsys.readouterr()
        assert "venv-proxy installed shims" in captured.out

    def test_install_crée_dossier_si_nexiste_pas(self, tmp_path, monkeypatch):
        """install crée le dossier ~/.local/bin s'il n'existe pas."""
        test_shim_dir = tmp_path / ".local" / "bin"

        with patch("venv_proxy.cli._check_path_warning"):
            monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)
            install()

        assert test_shim_dir.exists()


class TestUninstall:
    """Tests pour la commande uninstall."""

    def test_uninstall_supprime_shims(self, tmp_path, monkeypatch, capsys):
        """venv-proxy uninstall supprime les shims."""
        test_shim_dir = tmp_path / ".local" / "bin"
        test_shim_dir.mkdir(parents=True)

        for binary in SHIMS:
            shim_path = test_shim_dir / binary
            shim_path.write_text("#!/usr/bin/env python3\n# venv-proxy shim — test\n")
            shim_path.chmod(shim_path.stat().st_mode | stat.S_IEXEC)

        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)

        uninstall()

        for binary in SHIMS:
            shim_path = test_shim_dir / binary
            assert not shim_path.exists()

        captured = capsys.readouterr()
        assert "venv-proxy removed shims" in captured.out

    def test_uninstall_ignore_autres_shims(self, tmp_path, monkeypatch, capsys):
        """uninstall ne supprime pas les shims qui ne sont pas de venv-proxy."""
        test_shim_dir = tmp_path / ".local" / "bin"
        test_shim_dir.mkdir(parents=True)

        shim_path = test_shim_dir / "python"
        shim_path.write_text("#!/usr/bin/env python3\n# autre shim\n")

        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)

        uninstall()

        assert shim_path.exists()


class TestStatus:
    """Tests pour la commande status."""

    def test_status_affiche_chemin_venv(self, tmp_path, monkeypatch, capsys):
        """status affiche le bon chemin vers le .venv."""
        venv_bin = tmp_path / ".venv" / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "python").write_text("#!/usr/bin/env python3\n")
        (venv_bin / "python").chmod(0o755)
        (venv_bin / "pip").write_text("#!/usr/bin/env python3\n")
        (venv_bin / "pip").chmod(0o755)

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("venv_proxy.cli._check_path_warning", lambda: None)

        status()

        captured = capsys.readouterr()
        assert "python" in captured.out
        assert ".venv" in captured.out
        assert "pip" in captured.out

    def test_status_sans_venv(self, tmp_path, monkeypatch, capsys):
        """status indique quand aucun .venv n'est trouvé."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("venv_proxy.cli._check_path_warning", lambda: None)

        status()

        captured = capsys.readouterr()
        assert "no .venv found" in captured.out or "system" in captured.out


class TestDoctor:
    """Tests pour la commande doctor."""

    def test_doctor_vérifie_shims(self, tmp_path, monkeypatch, capsys):
        """doctor vérifie la présence des shims."""
        test_shim_dir = tmp_path / ".local" / "bin"
        test_shim_dir.mkdir(parents=True)

        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)

        doctor()

        captured = capsys.readouterr()
        assert "shim for python" in captured.out
        assert "shim for pip" in captured.out

    def test_doctor_detecte_PATH_mal_configure(self, tmp_path, monkeypatch, capsys):
        """doctor détecte quand ~/.local/bin n'est pas dans PATH."""
        test_shim_dir = tmp_path / ".local" / "bin"
        test_shim_dir.mkdir(parents=True)

        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)
        monkeypatch.setenv("PATH", "/usr/bin:/bin")

        doctor()

        captured = capsys.readouterr()
        assert "NOT in PATH" in captured.out or "position" in captured.out

    def test_doctor_PATH_correct(self, tmp_path, monkeypatch, capsys):
        """doctor confirme quand ~/.local/bin est en première position."""
        test_shim_dir = tmp_path / ".local" / "bin"
        test_shim_dir.mkdir(parents=True)

        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", test_shim_dir)
        monkeypatch.setenv("PATH", f"{test_shim_dir}:/usr/bin:/bin")

        doctor()

        captured = capsys.readouterr()
        assert "first in PATH" in captured.out


class TestCheckPathWarning:
    """Tests pour la fonction de vérification du PATH."""

    def test_check_path_warning_quand_ok(self, capsys, monkeypatch):
        """_check_path_warning n'affiche rien quand PATH est correct."""
        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", Path("/test/path"))
        monkeypatch.setenv("PATH", "/test/path:/usr/bin")

        _check_path_warning()

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_check_path_warning_quand_manque(self, capsys, monkeypatch):
        """_check_path_warning affiche un warning quand PATH est incorrect."""
        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", Path("/test/path"))
        monkeypatch.setenv("PATH", "/usr/bin:/bin")

        _check_path_warning()

        captured = capsys.readouterr()
        assert "Add" in captured.out or "PATH" in captured.out


class TestCheckConflictingShims:
    """Tests pour la détection de shims conflictuels."""

    def test_no_conflicts(self, capsys, monkeypatch, tmp_path):
        """Aucun conflit quand seul venv-proxy est présent."""
        venv_proxy_dir = tmp_path / "venv_proxy"
        venv_proxy_dir.mkdir()
        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", venv_proxy_dir)

        # Créer un dossier vide pour simuler un PATH sans autres shims
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        path_dirs = [str(venv_proxy_dir), str(empty_dir)]

        from venv_proxy.cli import _check_conflicting_shims
        _check_conflicting_shims(path_dirs)

        captured = capsys.readouterr()
        assert "No conflicting shims" in captured.out

    def test_detects_pyenv_conflict(self, capsys, monkeypatch, tmp_path):
        """Détecte un shim pyenv comme conflit."""
        pyenv_dir = tmp_path / "pyenv" / "shims"
        pyenv_dir.mkdir(parents=True)
        (pyenv_dir / "python").write_text("#!/bin/bash\n")

        venv_proxy_dir = tmp_path / "venv_proxy"
        venv_proxy_dir.mkdir()
        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", venv_proxy_dir)

        path_dirs = [str(pyenv_dir), str(venv_proxy_dir)]

        from venv_proxy.cli import _check_conflicting_shims
        _check_conflicting_shims(path_dirs)

        captured = capsys.readouterr()
        assert "pyenv" in captured.out


class TestCheckPyenvConda:
    """Tests pour la détection de pyenv/conda."""

    def test_no_pyenv_conda(self, capsys):
        """Aucun message quand pyenv/conda absent."""
        path_dirs = ["/usr/bin", "/usr/local/bin"]

        from venv_proxy.cli import _check_pyenv_conda
        _check_pyenv_conda(path_dirs)

        captured = capsys.readouterr()
        assert "No pyenv or conda" in captured.out

    def test_detects_pyenv_before(self, capsys, monkeypatch, tmp_path):
        """Détecte pyenv avant venv-proxy dans PATH."""
        pyenv_dir = tmp_path / ".pyenv" / "bin"
        pyenv_dir.mkdir(parents=True)
        shim_dir = tmp_path / ".local" / "bin"
        shim_dir.mkdir(parents=True)

        monkeypatch.setattr("venv_proxy.cli.SHIM_DIR", shim_dir)
        path_dirs = [str(pyenv_dir), str(shim_dir), "/usr/bin"]

        from venv_proxy.cli import _check_pyenv_conda
        _check_pyenv_conda(path_dirs)

        captured = capsys.readouterr()
        assert "pyenv is before" in captured.out
