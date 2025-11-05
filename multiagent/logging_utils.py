from __future__ import annotations

import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from .config import LOG_DIR


_LOGGERS: dict[str, Logger] = {}


def get_logger(name: str, log_file: Optional[Path] = None) -> Logger:
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_path = log_file or LOG_DIR / "llm.log"
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    _LOGGERS[name] = logger
    return logger
