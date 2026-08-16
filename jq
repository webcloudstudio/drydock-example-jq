#!/usr/bin/env python3
"""Executable entry point for the self-contained jq interpreter."""

from jq_cli import main

if __name__ == "__main__":
    import sys

    raise SystemExit(main(sys.argv[1:]))
