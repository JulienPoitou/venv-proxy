# venv-proxy

[![Tests](https://github.com/yourusername/venv-proxy/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/venv-proxy/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/venv-proxy.svg)](https://pypi.org/project/venv-proxy/)
[![Python](https://img.shields.io/pypi/pyversions/venv-proxy.svg)](https://pypi.org/project/venv-proxy/)
[![License](https://img.shields.io/pypi/l/venv-proxy.svg)](https://github.com/yourusername/venv-proxy/blob/main/LICENSE)

**Never type `source .venv/bin/activate` again.**

Not you. Not your AI agent.

```bash
pip install venv-proxy
venv-proxy install
```

That's it. From now on, `python` and `pip` automatically use the right `.venv` — in any directory, in any shell, for any process.

---

## The problem

Every Python project has a `.venv`. Activating it is a manual step that breaks constantly:

```bash
# You forget it. Your agent ignores it. CI doesn't have it.
source .venv/bin/activate  # ← this shouldn't exist
```

When skipped, `pip install` pollutes your global Python. Dependencies conflict. Projects break silently.

**AI coding agents (Claude Code, Cursor, Copilot) make this worse.** They execute shell commands without TTY activation. They ignore your `CLAUDE.md` instructions. They install packages wherever they want.

[Real issue: anthropics/claude-code #9368](https://github.com/anthropics/claude-code/issues/9368) — duplicated 4 times, still open.

---

## How it works

venv-proxy installs lightweight shims for `python`, `python3`, `pip`, and `pip3` at the front of your PATH.

When invoked from any directory, each shim:

1. Walks up the filesystem from your current directory
2. Finds the nearest `.venv/bin/` folder
3. Replaces itself with the correct binary via `execv()` — **zero overhead, fully transparent**
4. Falls back to system Python if no `.venv` is found

```
my-project/
├── .venv/          ← found automatically
│   └── bin/
│       ├── python  ← used by shim
│       └── pip     ← used by shim
├── src/
│   └── main.py
└── tests/
    └── test_main.py  ← python here uses .venv too
```

---

## Install

```bash
pip install venv-proxy
venv-proxy install

# Add to your shell profile if not already there:
export PATH="$HOME/.local/bin:$PATH"
```

---

## Usage

```bash
# Before venv-proxy:
cd my-project
source .venv/bin/activate   # don't forget!
pip install requests         # now in .venv
python main.py

# After venv-proxy:
cd my-project
pip install requests         # automatically in .venv ✓
python main.py               # automatically uses .venv ✓
```

Works the same for AI agents — no config, no CLAUDE.md instructions needed.

---

## Commands

```bash
venv-proxy install     # install shims into ~/.local/bin
venv-proxy uninstall   # remove shims
venv-proxy status      # show which venv would be used from CWD
venv-proxy doctor      # diagnose PATH and shim issues
```

---

## Debug mode

```bash
VENV_PROXY_DEBUG=1 python script.py
# venv-proxy: using /home/user/my-project/.venv/bin/python
```

---

## FAQ

**Does it work with `uv`?**  
Yes. venv-proxy resolves `.venv/bin/python` regardless of how the venv was created (venv, virtualenv, uv, poetry).

**What if there's no `.venv`?**  
Falls back to system Python transparently.

**Does it slow things down?**  
No. It uses `os.execv()` which replaces the current process — there's no subprocess or wrapper overhead.

**Does it work in CI?**  
Yes. Any process that calls `python` or `pip` gets the right venv automatically.

**Windows?**  
Not yet. Linux and macOS only for now.

---

## Requirements

- Python 3.9+
- Linux or macOS

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions.

---

## License

MIT

---

*Built because [this GitHub issue](https://github.com/anthropics/claude-code/issues/9368) has been open too long.*
