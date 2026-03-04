"""
venv-proxy CLI — install, uninstall, status, doctor
"""
import os
import shutil
import stat
import sys
from pathlib import Path

SHIM_DIR = Path.home() / ".local" / "bin"
SHIMS = ["python", "python3", "pip", "pip3"]

SHIM_TEMPLATE = """#!/usr/bin/env python3
# venv-proxy shim — {binary}
import sys
from venv_proxy.shim import run_shim
run_shim("{binary}")
"""


def install():
    SHIM_DIR.mkdir(parents=True, exist_ok=True)

    installed = []
    for binary in SHIMS:
        shim_path = SHIM_DIR / binary
        shim_path.write_text(SHIM_TEMPLATE.format(binary=binary))
        shim_path.chmod(shim_path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        installed.append(str(shim_path))

    print("✓ venv-proxy installed shims:")
    for p in installed:
        print(f"  {p}")

    _check_path_warning()


def uninstall():
    removed = []
    for binary in SHIMS:
        shim_path = SHIM_DIR / binary
        if shim_path.exists() and "venv-proxy shim" in shim_path.read_text():
            shim_path.unlink()
            removed.append(str(shim_path))

    if removed:
        print("✓ venv-proxy removed shims:")
        for p in removed:
            print(f"  {p}")
    else:
        print("Nothing to remove.")


def status():
    from venv_proxy.resolver import resolve_venv

    cwd = Path.cwd()
    print(f"CWD: {cwd}")

    for binary in ["python", "pip"]:
        target = resolve_venv(cwd, binary)
        if target:
            print(f"  {binary} → {target}")
        else:
            print(f"  {binary} → (no .venv found, would use system)")

    _check_path_warning()


def doctor():
    print("venv-proxy doctor\n")

    # Check shims exist
    for binary in SHIMS:
        shim_path = SHIM_DIR / binary
        ok = shim_path.exists() and "venv-proxy shim" in shim_path.read_text()
        icon = "✓" if ok else "✗"
        print(f"  {icon} shim for {binary}: {shim_path}")

    # Check PATH order
    path_dirs = os.environ.get("PATH", "").split(":")
    shim_index = next((i for i, p in enumerate(path_dirs) if str(SHIM_DIR) in p), None)

    print()
    if shim_index == 0:
        print("  ✓ ~/.local/bin is first in PATH")
    elif shim_index is not None:
        print(f"  ⚠ ~/.local/bin is in PATH but at position {shim_index + 1} (should be first)")
        print(f"    Add this to your shell profile:")
        print(f"    export PATH=\"{SHIM_DIR}:$PATH\"")
    else:
        print(f"  ✗ ~/.local/bin is NOT in PATH")
        print(f"    Add this to your ~/.bashrc or ~/.zshrc:")
        print(f"    export PATH=\"{SHIM_DIR}:$PATH\"")

    # Check for conflicting shims
    print()
    _check_conflicting_shims(path_dirs)

    # Check for pyenv/conda
    _check_pyenv_conda(path_dirs)


def _check_conflicting_shims(path_dirs: list) -> None:
    """Detect other python/pip shims that might conflict."""
    conflicts = []
    for path_dir in path_dirs:
        if not path_dir or path_dir == str(SHIM_DIR):
            continue
        path_obj = Path(path_dir)
        if not path_obj.exists():
            continue
        for binary in SHIMS:
            bin_path = path_obj / binary
            if bin_path.exists() and bin_path.is_file():
                try:
                    content = bin_path.read_text()
                    if "venv-proxy shim" not in content:
                        # Check if it's a known conflicting shim
                        if "pyenv" in path_dir.lower():
                            conflicts.append((binary, path_dir, "pyenv shim"))
                        elif "conda" in path_dir.lower() or "anaconda" in path_dir.lower():
                            conflicts.append((binary, path_dir, "conda shim"))
                        elif "uv" in path_dir.lower():
                            conflicts.append((binary, path_dir, "uv shim"))
                        else:
                            conflicts.append((binary, path_dir, "unknown shim"))
                except (UnicodeDecodeError, PermissionError):
                    # Binary file or no permission, skip
                    pass

    if conflicts:
        print("  ⚠ Conflicting shims found:")
        for binary, path_dir, shim_type in conflicts:
            print(f"    - {binary} at {path_dir} ({shim_type})")
            print(f"      This may intercept calls before venv-proxy shims.")
    else:
        print("  ✓ No conflicting shims detected")


def _check_pyenv_conda(path_dirs: list) -> None:
    """Detect if pyenv or conda might intercept before venv-proxy."""
    pyenv_found = False
    conda_found = False

    for i, path_dir in enumerate(path_dirs):
        if not path_dir:
            continue
        if "pyenv" in path_dir.lower():
            pyenv_found = True
            if shim_index := next((j for j, p in enumerate(path_dirs) if str(SHIM_DIR) in p), None):
                if i < shim_index:
                    print(f"\n  ⚠ pyenv is before venv-proxy in PATH (position {i + 1} vs {shim_index + 1})")
                    print(f"     pyenv may intercept python calls before venv-proxy.")
            break
        if "conda" in path_dir.lower() or "anaconda" in path_dir.lower():
            conda_found = True
            if shim_index := next((j for j, p in enumerate(path_dirs) if str(SHIM_DIR) in p), None):
                if i < shim_index:
                    print(f"\n  ⚠ conda is before venv-proxy in PATH (position {i + 1} vs {shim_index + 1})")
                    print(f"     conda may intercept python calls before venv-proxy.")
            break

    if not pyenv_found and not conda_found:
        print("  ✓ No pyenv or conda detected in PATH")


def _check_path_warning():
    path_dirs = os.environ.get("PATH", "").split(":")
    if str(SHIM_DIR) not in path_dirs:
        print(f"\n⚠  Add this to your shell profile to activate:")
        print(f'   export PATH="{SHIM_DIR}:$PATH"')
    elif path_dirs[0] != str(SHIM_DIR):
        print(f"\n⚠  Move {SHIM_DIR} to the front of PATH:")
        print(f'   export PATH="{SHIM_DIR}:$PATH"')


def main():
    args = sys.argv[1:]
    if not args or args[0] == "install":
        install()
    elif args[0] == "uninstall":
        uninstall()
    elif args[0] == "status":
        status()
    elif args[0] == "doctor":
        doctor()
    else:
        print("Usage: venv-proxy [install|uninstall|status|doctor]")
        sys.exit(1)


if __name__ == "__main__":
    main()
