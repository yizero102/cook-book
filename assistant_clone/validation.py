"""Helpers for ensuring local Python sources remain valid."""

from __future__ import annotations

import ast
import pathlib
from typing import Iterable

EXCLUDE_DIRS = {".git", "__pycache__"}


def iter_python_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def validate_files(paths: Iterable[pathlib.Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path}: unable to read file: {exc}")
            continue
        try:
            ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path}:{exc.lineno}:{exc.offset}: {exc.msg}")
    return errors
