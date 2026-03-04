# venv-proxy Setup for this Project

This project uses [venv-proxy](https://github.com/yourusername/venv-proxy) to automatically manage the Python virtual environment.

## Quick Setup

```bash
# Install venv-proxy (one-time system-wide setup)
pip install venv-proxy
venv-proxy install

# Make sure ~/.local/bin is in your PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

**No manual activation needed!** Just run commands normally:

```bash
# These automatically use the .venv in this project
python -m pytest
pip install requests
python src/main.py
```

## For AI Agents

If you're an AI coding assistant (Claude Code, Cursor, Copilot), **do not** try to activate the virtual environment manually. The venv-proxy shims handle it automatically.

❌ **Don't do this:**
```bash
source .venv/bin/activate  # NOT NEEDED!
```

✅ **Just run commands directly:**
```bash
pip install package-name
python script.py
```

## How It Works

venv-proxy installs lightweight shims for `python`, `python3`, `pip`, and `pip3` that:
1. Find the nearest `.venv/` folder by walking up from the current directory
2. Automatically execute commands using that virtual environment
3. Fall back to system Python if no `.venv` is found

## Troubleshooting

```bash
# Check which venv would be used from current directory
venv-proxy status

# Diagnose PATH and shim issues
venv-proxy doctor
```

## Verify Installation

```bash
# Should show venv-proxy shims
which python
# Output: /home/user/.local/bin/python

# Should show the .venv path
venv-proxy status
```
