"""
Tests for venv-proxy shim logic.
"""
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from venv_proxy.shim import run_shim, _exec_system, _debug


class TestRunShim:
    """Tests for the main shim entry point."""

    def test_cas_nominal_python(self, tmp_path, monkeypatch):
        """Quand un .venv est trouvé, execv est appelé avec le bon binaire."""
        venv_bin = tmp_path / ".venv" / "bin"
        venv_bin.mkdir(parents=True)
        python = venv_bin / "python"
        python.write_text("#!/usr/bin/env python3\n")
        python.chmod(python.stat().st_mode | 0o111)

        mock_execv = MagicMock()
        mock_argv = ["python", "script.py"]

        with patch("venv_proxy.shim.resolve_venv", return_value=python):
            with patch("venv_proxy.shim.os.execv", mock_execv):
                with patch.object(sys, "argv", mock_argv):
                    monkeypatch.setenv("VENV_PROXY_ACTIVE", "", prepend=":" if os.environ.get("VENV_PROXY_ACTIVE") else "")
                    if "VENV_PROXY_ACTIVE" in os.environ:
                        del os.environ["VENV_PROXY_ACTIVE"]

                    try:
                        run_shim("python")
                    except SystemExit:
                        pass

                    mock_execv.assert_called_once_with(
                        str(python),
                        [str(python), "script.py"]
                    )

    def test_cas_nominal_pip(self, tmp_path, monkeypatch):
        """Quand un .venv est trouvé, execv est appelé avec le bon binaire pip."""
        venv_bin = tmp_path / ".venv" / "bin"
        venv_bin.mkdir(parents=True)
        pip = venv_bin / "pip"
        pip.write_text("#!/usr/bin/env python3\n")
        pip.chmod(pip.stat().st_mode | 0o111)

        mock_execv = MagicMock()
        mock_argv = ["pip", "install", "requests"]

        with patch("venv_proxy.shim.resolve_venv", return_value=pip):
            with patch("venv_proxy.shim.os.execv", mock_execv):
                with patch.object(sys, "argv", mock_argv):
                    if "VENV_PROXY_ACTIVE" in os.environ:
                        del os.environ["VENV_PROXY_ACTIVE"]

                    try:
                        run_shim("pip")
                    except SystemExit:
                        pass

                    mock_execv.assert_called_once_with(
                        str(pip),
                        [str(pip), "install", "requests"]
                    )

    def test_fallback_systeme_quand_pas_de_venv(self, monkeypatch):
        """Quand aucun .venv n'est trouvé, tombe sur le binaire système."""
        mock_exec_system = MagicMock()

        with patch("venv_proxy.shim.resolve_venv", return_value=None):
            with patch("venv_proxy.shim._exec_system", mock_exec_system):
                if "VENV_PROXY_ACTIVE" in os.environ:
                    del os.environ["VENV_PROXY_ACTIVE"]

                run_shim("python")

                mock_exec_system.assert_called_once_with("python")

    def test_guard_anti_recursion(self, monkeypatch):
        """Le guard VENV_PROXY_ACTIVE empêche la récursion infinie."""
        mock_exec_system = MagicMock()

        with patch("venv_proxy.shim._exec_system", mock_exec_system):
            monkeypatch.setenv("VENV_PROXY_ACTIVE", "python")

            run_shim("python")

            mock_exec_system.assert_called_once_with("python")

    def test_debug_mode(self, tmp_path, monkeypatch, capsys):
        """Le mode debug affiche des messages sur stderr."""
        venv_bin = tmp_path / ".venv" / "bin"
        venv_bin.mkdir(parents=True)
        python = venv_bin / "python"
        python.write_text("#!/usr/bin/env python3\n")
        python.chmod(python.stat().st_mode | 0o111)

        mock_execv = MagicMock(side_effect=SystemExit(0))

        with patch("venv_proxy.shim.resolve_venv", return_value=python):
            with patch("venv_proxy.shim.os.execv", mock_execv):
                with patch.object(sys, "argv", ["python"]):
                    monkeypatch.setenv("VENV_PROXY_DEBUG", "1")
                    if "VENV_PROXY_ACTIVE" in os.environ:
                        del os.environ["VENV_PROXY_ACTIVE"]

                    try:
                        run_shim("python")
                    except SystemExit:
                        pass

                    captured = capsys.readouterr()
                    assert "venv-proxy: using" in captured.err


class TestExecSystem:
    """Tests pour le fallback système."""

    def test_exec_system_trouve_binaire(self, monkeypatch):
        """_exec_system trouve et exécute le binaire système via PATH."""
        mock_execv = MagicMock()
        import shutil

        def mock_which(binary, path=None):
            return "/usr/bin/python3"

        monkeypatch.setattr(shutil, "which", mock_which)

        with patch("os.execv", mock_execv):
            with patch.object(sys, "argv", ["python", "test.py"]):
                try:
                    _exec_system("python")
                except SystemExit:
                    pass

                mock_execv.assert_called_once_with(
                    "/usr/bin/python3",
                    ["/usr/bin/python3", "test.py"]
                )

    def test_exec_system_sans_binaire(self, capsys, monkeypatch):
        """_exec_system échoue proprement si aucun binaire système trouvé."""
        mock_exit = MagicMock(side_effect=SystemExit(1))
        import shutil

        def mock_which(binary, path=None):
            return None

        monkeypatch.setattr(shutil, "which", mock_which)

        with patch.object(sys, "exit", mock_exit):
            with patch.object(sys, "argv", ["python"]):
                with pytest.raises(SystemExit):
                    _exec_system("python")

                mock_exit.assert_called_once_with(1)
                captured = capsys.readouterr()
                assert "could not find system python" in captured.err


class TestDebug:
    """Tests pour la fonction de debug."""

    def test_debug_quand_active(self, monkeypatch, capsys):
        """_debug affiche quand VENV_PROXY_DEBUG est set."""
        monkeypatch.setenv("VENV_PROXY_DEBUG", "1")

        _debug("test message")

        captured = capsys.readouterr()
        assert "test message" in captured.err

    def test_debug_silent_quand_inactive(self, monkeypatch, capsys):
        """_debug n'affiche rien quand VENV_PROXY_DEBUG n'est pas set."""
        if "VENV_PROXY_DEBUG" in os.environ:
            del os.environ["VENV_PROXY_DEBUG"]

        _debug("test message")

        captured = capsys.readouterr()
        assert captured.err == ""
