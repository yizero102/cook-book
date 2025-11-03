#!/usr/bin/env python3
"""Check that all Python sources in the repository can be parsed."""

from __future__ import annotations

import pathlib
import sys

from assistant_clone.validation import iter_python_files, validate_files


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    errors = validate_files(iter_python_files(repo_root))
    if errors:
        print("Found issues while parsing Python files:")
        for error in errors:
            print(f" - {error}")
        return 1
    print("All Python files parse successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
