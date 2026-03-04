# Example: Python Project with venv-proxy

This is a minimal example showing how venv-proxy works with a standard Python project.

## Project Structure

```
examples/claude-code/
├── CLAUDE.md          # Instructions for AI agents
├── README.md          # This file
├── .venv/             # Virtual environment (created by you)
│   └── bin/
│       ├── python
│       └── pip
├── src/
│   └── main.py        # Your code
└── requirements.txt   # Dependencies
```

## Setup

```bash
# Create the virtual environment
python -m venv .venv

# Install dependencies (automatically goes into .venv)
pip install -r requirements.txt

# Run your code (automatically uses .venv)
python src/main.py
```

## Sample Code

```python
# src/main.py
import sys

def main():
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version}")
    
    # Try importing a dependency
    try:
        import requests
        print(f"requests version: {requests.__version__}")
    except ImportError:
        print("requests not installed - run: pip install requests")

if __name__ == "__main__":
    main()
```

## Test It

```bash
# From this directory, run:
python src/main.py

# Or from a subdirectory (venv-proxy still finds .venv):
cd src && python main.py
```
