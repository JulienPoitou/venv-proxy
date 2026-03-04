"""
Core venv resolution logic.
Traverses the filesystem upward from CWD to find the nearest .venv.
"""
from pathlib import Path


def resolve_venv(cwd: Path, binary: str = "python", max_depth: int = 10) -> Path | None:
    """
    Walk up from `cwd` looking for a .venv/bin/<binary>.
    Returns the full path if found, None otherwise.
    
    Handles:
    - Symlinks (resolved automatically via exists())
    - Corrupted .venv (returns None if binary is not executable)
    - Max depth limit to avoid infinite loops
    """
    for i, parent in enumerate([cwd, *cwd.parents]):
        if i >= max_depth:
            break
        candidate = parent / ".venv" / "bin" / binary
        
        # Check if candidate exists (follows symlinks)
        if not candidate.exists():
            continue
            
        # Check if it's a file (or symlink to file)
        if not candidate.is_file():
            continue
        
        # Check if it's executable (handles corrupted venv)
        try:
            mode = candidate.stat().st_mode
            if not (mode & 0o111):  # Not executable by anyone
                continue
        except (OSError, PermissionError):
            continue
            
        return candidate
        
    return None
