from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class LLMConfig:
    base_url: str | None
    api_key: str
    model: str
    reasoning_split: bool = True


def _get_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def load_llm_config() -> LLMConfig:
    base_url = _get_env("_OPENAI_BASE_URL", "OPENAI_BASE_URL")
    api_key = _get_env("_OPENAI_API_KEY", "OPENAI_API_KEY")
    model = _get_env("_MODEL_NAME", "OPENAI_MODEL", "OPENAI_DEFAULT_MODEL")

    if not api_key:
        raise RuntimeError("OpenAI API key must be provided via _OPENAI_API_KEY or OPENAI_API_KEY.")

    if not model:
        raise RuntimeError("Model name must be provided via _MODEL_NAME or OPENAI_MODEL.")

    return LLMConfig(base_url=base_url, api_key=api_key, model=model)
