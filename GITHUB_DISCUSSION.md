---
title: "🚀 venv-proxy is now on PyPI — Never activate a virtualenv again"
category: "Announcements"
labels: ["announcement"]
---

## venv-proxy v0.1.0 is now available on PyPI! 🎉

**Install:**
```bash
pip install venv-proxy
venv-proxy install
```

---

## What is venv-proxy?

venv-proxy automatically resolves the nearest `.venv` and uses it transparently — **no activation needed**.

### The Problem

```bash
# You forget it. Your AI agent ignores it. CI doesn't have it.
source .venv/bin/activate  # ← this shouldn't exist in 2026
```

### The Solution

venv-proxy installs lightweight shims for `python`, `python3`, `pip`, and `pip3` that:
1. Walk up from your CWD to find `.venv/bin/`
2. `execv()` into the correct binary — **zero overhead**
3. Fall back to system Python if no `.venv` found

---

## Who is this for?

- **Developers** tired of forgetting to activate their virtualenv
- **AI coding agent users** (Claude Code, Cursor, Copilot) whose agents ignore CLAUDE.md instructions
- **Teams** who want consistent Python environments across local dev and CI
- **CI/CD pipelines** that need reliable venv resolution

---

## Features

✅ Works in any directory, any shell  
✅ Works for AI agents without any config  
✅ Works with `venv`, `virtualenv`, `uv`, `poetry`  
✅ Debug mode: `VENV_PROXY_DEBUG=1`  
✅ Doctor command: `venv-proxy doctor`  
✅ Zero runtime overhead (uses `os.execv()`)  

---

## Quick Start

```bash
# Install
pip install venv-proxy

# Install shims
venv-proxy install

# Add to PATH if not already done
export PATH="$HOME/.local/bin:$PATH"

# That's it! python and pip now auto-resolve .venv
```

---

## Links

- **GitHub:** https://github.com/JulienPoitou/venv-proxy
- **PyPI:** https://pypi.org/project/venv-proxy/
- **Issues:** https://github.com/JulienPoitou/venv-proxy/issues

---

## Feedback Welcome!

venv-proxy was built in a weekend to solve a real pain point. I'd love to hear:

- Does it work for your setup?
- What features would you like to see?
- Any bugs or edge cases?

Drop a comment below! 👇

---

*Built because [this GitHub issue](https://github.com/anthropics/claude-code/issues/9368) has been open too long.*
