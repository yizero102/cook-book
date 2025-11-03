"""Configuration helpers for connecting to an external LLM provider."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Mapping, MutableMapping


ENV_BASE_URL = "_ANTHROPIC_BASE_URL"
ENV_API_KEY = "_ANTHROPIC_API_KEY"
ENV_MODEL_NAME = "_MODEL_NAME"


class ConfigError(RuntimeError):
    """Raised when the environment has not been configured correctly."""

    def __init__(self, message: str, missing: tuple[str, ...] | None = None) -> None:
        super().__init__(message)
        self.missing = missing or ()


@dataclass(frozen=True)
class LLMSettings:
    """User-provided configuration for the Anthropic API."""

    base_url: str
    api_key: str
    model: str
    version: str = "2023-06-01"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "LLMSettings":
        env = env or os.environ
        base_url = env.get(ENV_BASE_URL)
        api_key = env.get(ENV_API_KEY)
        model = env.get(ENV_MODEL_NAME)
        missing = tuple(
            name
            for name, value in (
                (ENV_BASE_URL, base_url),
                (ENV_API_KEY, api_key),
                (ENV_MODEL_NAME, model),
            )
            if not value
        )
        if missing:
            raise ConfigError(
                "Missing required environment variables for LLM connectivity.",
                missing=missing,
            )
        assert base_url is not None
        assert api_key is not None
        assert model is not None
        base_url = base_url.rstrip("/")
        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            raise ConfigError(
                f"Invalid base URL '{base_url}'. Expected an http(s) URL.", missing=()
            )
        return cls(base_url=base_url, api_key=api_key, model=model)

    def to_headers(self) -> MutableMapping[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": self.version,
        }

    def to_payload(self, messages: list[dict], max_output_tokens: int, temperature: float | None = None,
                   tools: list[dict] | None = None) -> dict:
        payload: dict[str, object] = {
            "model": self.model,
            "messages": messages,
            "max_output_tokens": max_output_tokens,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        if tools:
            payload["tools"] = tools
        return payload
