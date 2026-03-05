# 📢 venv-proxy — Plan de Promotion

**Package publié :** https://pypi.org/project/venv-proxy/  
**Repo GitHub :** https://github.com/JulienPoitou/venv-proxy

---

## 🎯 1. GitHub Issues à commenter (PRIORITÉ HAUTE)

### Issue #1 : microsoft/vscode-python-environments #298927
**URL :** https://github.com/microsoft/vscode/issues/298927  
**Pourquoi :** Problème d'environnement Python dans VS Code

```
I built an external tool that solves this right now without waiting for a native fix:

**venv-proxy** automatically resolves the nearest .venv and uses it transparently — 
no activation needed, works for AI agents too (Claude Code, Cursor, etc.).

pip install venv-proxy && venv-proxy install

https://github.com/JulienPoitou/venv-proxy
```

---

### Issue #2 : anthropics/claude-code #21728
**URL :** https://github.com/anthropics/claude-code/issues/21728  
**Pourquoi :** VS Code extension ne charge pas $PATH — ton outil résout ça

```
This is exactly the problem that led me to build venv-proxy.

Instead of waiting for the extension to fix $PATH, venv-proxy makes python/pip 
automatically resolve the correct .venv from any directory. No activation needed, 
works for AI agents out of the box.

pip install venv-proxy

https://github.com/JulienPoitou/venv-proxy
```

---

### Issue #3 : anthropics/claude-code #28228
**URL :** https://github.com/anthropics/claude-code/issues/28228  
**Pourquoi :** Persistent shell context — ton outil rend ça inutile

```
I faced the same frustration with having to re-activate venv on every bash call.

I built venv-proxy as a different approach: instead of persisting shell state, 
it makes python/pip automatically find and use the nearest .venv from any directory. 
Zero config, works for AI agents (Claude Code, Cursor) without any CLAUDE.md instructions.

pip install venv-proxy && venv-proxy install

https://github.com/JulienPoitou/venv-proxy
```

---

### Issue #4 : zed-industries/zed #47345
**URL :** https://github.com/zed-industries/zed/issues/47345  
**Pourquoi :** Zed ajoute des commandes venv automatiquement — ton outil simplifie

```
I built a tool that makes this unnecessary:

**venv-proxy** installs shims that automatically resolve the nearest .venv/bin/python 
— no activation scripts, no terminal commands needed. Works transparently in any 
editor (Zed, VS Code, Cursor, etc.).

https://github.com/JulienPoitou/venv-proxy
```

---

### Issue #5 : comfy-org/desktop #1574
**URL :** https://github.com/comfy-org/desktop/issues/1574  
**Pourquoi :** .venv existe mais n'est pas trouvé

```
This is the exact problem venv-proxy solves:

It automatically finds and uses .venv from any directory, regardless of how it was 
created (venv, virtualenv, uv, poetry). No manual activation needed.

pip install venv-proxy

https://github.com/JulienPoitou/venv-proxy
```

---

## 📱 2. Posts Reddit (PRIORITÉ MOYENNE)

### r/Python — Daily Thread ou post dédié

**Titre :**
```
Never type `source .venv/bin/activate` again — venv-proxy
```

**Contenu :**
```
I got tired of:
- Forgetting to activate my virtualenv
- My AI agent (Claude Code) ignoring my CLAUDE.md instructions about venv
- pip installing packages in the wrong place
- Breaking CI because the venv wasn't activated

So I built **venv-proxy**.

It installs lightweight shims for python/pip that automatically find and use the 
nearest .venv — zero config, works in any shell, for any process (including AI agents).

Installation:
  pip install venv-proxy
  venv-proxy install

That's it. From now on, `python` and `pip` automatically use the right .venv in 
any directory, any shell.

GitHub: https://github.com/JulienPoitou/venv-proxy
PyPI: https://pypi.org/project/venv-proxy/

Built in a weekend with GitHub Actions CI/CD. Would love feedback from the community!
```

---

### r/learnpython — Post éducatif

**Titre :**
```
PSA: Stop activating virtualenv manually — here's a better way
```

**Contenu :**
```
I see a lot of beginners (and experienced devs!) struggling with virtualenv activation:

  source .venv/bin/activate  # ← you forget this
  pip install something      # ← installs globally oops

Or worse, your AI coding agent ignores it completely.

**The real problem:** Activation is a manual step that breaks constantly.

**A better approach:** Make python/pip automatically find the right .venv.

I built a tool called venv-proxy that does exactly this. It installs shims that 
transparently resolve the nearest .venv from any directory.

No activation needed. No CLAUDE.md instructions for your AI agent. Just works.

  pip install venv-proxy
  venv-proxy install

https://github.com/JulienPoitou/venv-proxy

This is how Python development should be in 2026.
```

---

### r/ChatGPTCoding — Self Promotion Thread

**Contenu :**
```
🚀 **venv-proxy — Automatic virtualenv resolution for AI coding agents**

Problem: AI agents (Claude Code, Cursor, Copilot) constantly forget to activate 
virtualenvs. They ignore CLAUDE.md instructions. They pip install in the wrong place.

Solution: venv-proxy makes python/pip automatically find and use the nearest .venv 
— no activation needed, works for any AI agent out of the box.

pip install venv-proxy && venv-proxy install

GitHub: https://github.com/JulienPoitou/venv-proxy
PyPI: https://pypi.org/project/venv-proxy/

Built because this GitHub issue has been open too long: 
https://github.com/anthropics/claude-code/issues/9368
```

---

### r/PythonDevTools — Post dédié

**Titre :**
```
venv-proxy — Automatic virtualenv resolution (never activate again)
```

**Contenu :**
```
After years of forgetting `source .venv/bin/activate` and watching my AI agent 
do the same, I finally built a solution.

**venv-proxy** installs shims for python/pip that:
1. Walk up from CWD to find the nearest .venv/bin/
2. execv() into the correct binary — zero overhead
3. Fall back to system Python if no .venv found

Features:
✅ Works in any directory, any shell
✅ Works for AI agents (Claude Code, Cursor, etc.)
✅ Works with uv, poetry, virtualenv, standard venv
✅ Debug mode: VENV_PROXY_DEBUG=1
✅ Doctor command: venv-proxy doctor

pip install venv-proxy
venv-proxy install

https://github.com/JulienPoitou/venv-proxy

Feedback welcome! What other devtools pain points should I tackle next?
```

---

## 🐦 3. Posts Twitter / X

### Tweet 1 — Announcement

```
🐍 Tired of `source .venv/bin/activate`?

I built venv-proxy — automatic virtualenv resolution for Python.

✅ Works in any directory
✅ Works for AI agents (Claude Code, Cursor)
✅ Zero config
✅ 100% transparent

pip install venv-proxy

https://github.com/JulienPoitou/venv-proxy

#Python #devtools #AI #opensource
```

---

### Tweet 2 — Problem/Solution

```
Your AI coding agent:
❌ Forgets to activate .venv
❌ Ignores your CLAUDE.md
❌ pip installs globally
❌ Breaks your environment

venv-proxy:
✅ Auto-finds .venv from any directory
✅ No config needed
✅ Works for any process

https://github.com/JulienPoitou/venv-proxy

#Python #AI #coding
```

---

### Tweet 3 — Technical

```
How venv-proxy works:

1. Installs shims at ~/.local/bin/{python,pip}
2. Shim walks up from CWD looking for .venv/bin/
3. os.execv() into the correct binary
4. Zero overhead (process replacement)

No subprocess. No wrapper. Just works.

https://github.com/JulienPoitou/venv-proxy

#Python #engineering
```

---

### Tweet 4 — Social Proof

```
venv-proxy is now on PyPI! 🎉

Never type `source .venv/bin/activate` again.

pip install venv-proxy
venv-proxy install

https://pypi.org/project/venv-proxy/
https://github.com/JulienPoitou/venv-proxy

#Python #PyPI #devtools
```

---

## 📧 4. Newsletters à contacter

### Python Weekly
**URL :** https://www.pythonweekly.com/  
**Email :** pythonweekly@gmail.com  
**Template :**
```
Subject: New Tool: venv-proxy — Automatic virtualenv resolution

Hi Python Weekly team,

I just published venv-proxy, a tool that automatically resolves the nearest .venv 
for python/pip commands — no activation needed.

Key features:
- Works in any directory, any shell
- Compatible with AI coding agents (Claude Code, Cursor)
- Zero overhead (uses os.execv())
- Works with venv, virtualenv, uv, poetry

PyPI: https://pypi.org/project/venv-proxy/
GitHub: https://github.com/JulienPoitou/venv-proxy

Would love to be featured in the next issue if you think it's useful for your readers!

Best,
Julien
```

---

### Import Python
**URL :** https://importpython.com/  
**Email :** newsletter@importpython.com  
**Template :** (même que ci-dessus, adapter le sujet)

---

### Real Python
**URL :** https://realpython.com/python-newsletter/  
**Submit :** Via leur formulaire de contact

---

## 📝 5. Articles de Blog à écrire

### Dev.to — "How I built venv-proxy in a weekend"

**Outline :**
1. The problem (forgetting activation, AI agents ignoring config)
2. The solution (shim approach)
3. Technical deep-dive (os.execv, PATH resolution)
4. GitHub Actions CI/CD setup
5. Publishing to PyPI
6. Lessons learned

**Titre :** "How I Built a Python Devtool in a Weekend — venv-proxy Story"

---

### Medium — "Why virtualenv activation is broken in 2026"

**Outline :**
1. History of virtualenv activation
2. Why it's a problem (AI agents, CI/CD, muscle memory)
3. Alternative approaches (shims, wrappers)
4. Introducing venv-proxy
5. Call to action

---

## 🎤 6. Communautés à partager

| Communauté | Type | Lien |
|------------|------|------|
| Python Discord | Discord | https://discord.gg/python |
| Real Python Discord | Discord | https://realpython.com/discord |
| PySlackers | Slack | https://pyslackers.com/ |
| Dev.to | Blog/Community | https://dev.to |
| Hashnode | Blog | https://hashnode.com |
| Lobsters | News | https://lobste.rs |

---

## 📊 7. Checklist de Publication

- [ ] ✅ Package sur PyPI
- [ ] ✅ README avec badges
- [ ] ⬜ Commenter 5 issues GitHub
- [ ] ⬜ Poster sur r/Python
- [ ] ⬜ Poster sur r/learnpython
- [ ] ⬜ Poster sur r/ChatGPTCoding
- [ ] ⬜ 4 tweets sur X
- [ ] ⬜ Contacter Python Weekly
- [ ] ⬜ Écrire article Dev.to
- [ ] ⬜ Partager sur Discord Python
- [ ] ⬜ Submit sur Hacker News ("Show HN")
- [ ] ⬜ Submit sur Product Hunt

---

## 🚀 8. Actions Immédiates (30 min)

```
1. Copier-coller les commentaires GitHub (10 min)
2. Poster sur r/Python daily thread (5 min)
3. Poster 4 tweets (5 min)
4. Partager sur Python Discord (5 min)
5. Envoyer email à Python Weekly (5 min)
```

---

**Généré automatiquement pour venv-proxy v0.1.0**  
**Date :** 5 mars 2026
