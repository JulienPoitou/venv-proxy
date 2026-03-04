"""
Shim logic — called by the python and pip shim scripts.
Resolves the correct venv binary and execv into it.
"""
import os
import sys
from pathlib import Path

from venv_proxy.resolver import resolve_venv


def run_shim(binary: str) -> None:
    """
    Resolve the correct binary for `binary` (e.g. 'python', 'pip')
    and replace the current process with it via execv.
    """
    # Guard against infinite recursion if shim calls itself
    if os.environ.get("VENV_PROXY_ACTIVE") == binary:
        # Already inside a shim — fall through to system binary
        _exec_system(binary)
        return

    os.environ["VENV_PROXY_ACTIVE"] = binary

    cwd = Path.cwd()
    target = resolve_venv(cwd, binary)

    if target:
        _debug(f"venv-proxy: using {target}")
        os.execv(str(target), [str(target)] + sys.argv[1:])
    else:
        _debug(f"venv-proxy: no .venv found, falling back to system {binary}")
        _exec_system(binary)


def _exec_system(binary: str) -> None:
    """Fall back to the system binary via PATH (excluding our shim dir)."""
    import shutil

    shim_dir = str(Path(__file__).parent.parent / "bin")
    clean_path = ":".join(
        p for p in os.environ.get("PATH", "").split(":")
        if p != shim_dir and "venv-proxy" not in p
    )

    system_bin = shutil.which(binary, path=clean_path)
    if not system_bin:
        print(f"venv-proxy: could not find system {binary}", file=sys.stderr)
        sys.exit(1)

    os.execv(system_bin, [system_bin] + sys.argv[1:])


def _debug(msg: str) -> None:
    if os.environ.get("VENV_PROXY_DEBUG"):
        print(msg, file=sys.stderr)
