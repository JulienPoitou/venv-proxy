"""
Example main.py - demonstrates venv-proxy in action.
"""
import sys


def main():
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"venv-proxy is working if this uses .venv/bin/python!")

    # Try importing a dependency
    try:
        import requests
        print(f"requests version: {requests.__version__}")
    except ImportError:
        print("requests not installed - run: pip install requests")


if __name__ == "__main__":
    main()
