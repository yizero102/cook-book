"""Anthropic-compatible HTTP client used by :class:`LocalAssistant`.

The implementation uses only the Python standard library so that it works in
restricted environments.  The client focuses on the minimum surface needed to
perform a text generation request and provides structured error reporting so the
assistant can fall back gracefully when the remote model is unavailable.
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Iterable, List, Mapping, MutableMapping, Optional


class LLMError(RuntimeError):
    """Raised when the language model request cannot be completed successfully."""


@dataclass
class LLMClientConfig:
    """Configuration container for :class:`LLMClient`."""

    base_url: str
    api_key: str
    model: str
    timeout: float = 30.0
    api_version: str = "2023-06-01"


class LLMClient:
    """Thin anthropic-compatible HTTP client with basic error handling."""

    _DEFAULT_PATH = "/v1/messages"

    def __init__(self, config: Optional[LLMClientConfig] = None) -> None:
        if config is None:
            env_config = self._config_from_env()
            self._config = env_config
        else:
            self._config = config

    @staticmethod
    def _config_from_env() -> Optional[LLMClientConfig]:
        base_url = os.getenv("_ANTHROPIC_BASE_URL")
        api_key = os.getenv("_ANTHROPIC_API_KEY")
        model = os.getenv("_MODEL_NAME")
        if not base_url or not api_key or not model:
            return None
        return LLMClientConfig(base_url=base_url, api_key=api_key, model=model)

    @property
    def config(self) -> Optional[LLMClientConfig]:
        return self._config

    def is_configured(self) -> bool:
        """Return ``True`` when the client has enough information to operate."""

        return self._config is not None

    # Anthropics expects the `messages` field to be a list of role/content
    # dictionaries.  We accept a more generic "Mapping" so that unit tests can
    # inject light-weight message containers.
    def create_completion(
        self,
        system_prompt: str,
        messages: Iterable[Mapping[str, str]],
        *,
        max_tokens: int = 512,
        temperature: float = 0.2,
    ) -> str:
        """Send a text-generation request and return the assistant text.

        Raises:
            LLMError: if configuration is missing, the request fails, or the
                response is not in the expected format.
        """

        if not self.is_configured():
            raise LLMError(
                "LLM client is not configured. Set _ANTHROPIC_BASE_URL, "
                "_ANTHROPIC_API_KEY, and _MODEL_NAME environment variables."
            )

        assert self._config is not None  # for type checkers
        payload: MutableMapping[str, object] = {
            "model": self._config.model,
            "system": system_prompt,
            "messages": list(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        request_body = json.dumps(payload).encode("utf-8")

        url = self._build_url(self._config.base_url)
        headers = {
            "content-type": "application/json",
            "x-api-key": self._config.api_key,
            "anthropic-version": self._config.api_version,
        }

        req = urllib.request.Request(url, data=request_body, headers=headers, method="POST")

        try:
            context = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=self._config.timeout, context=context) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:  # pragma: no cover - network dependent
            raise LLMError(f"LLM HTTP error {exc.code}: {exc.reason}") from exc
        except urllib.error.URLError as exc:  # pragma: no cover - network dependent
            raise LLMError(f"LLM network error: {exc.reason}") from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMError("LLM returned invalid JSON body") from exc

        text_chunks = []
        thinking_only = False

        content = data.get("content")
        if isinstance(content, list):
            for entry in content:
                if not isinstance(entry, Mapping):
                    continue
                text_value = entry.get("text")
                entry_type = entry.get("type")
                if isinstance(text_value, str) and text_value.strip():
                    # Skip explicit chain-of-thought disclosure by ignoring
                    # entries labelled as "thinking".
                    if entry_type != "thinking":
                        text_chunks.append(text_value.strip())
                elif entry_type == "thinking" and isinstance(entry.get("thinking"), str):
                    thinking_only = True
            if text_chunks:
                return "\n".join(text_chunks)

        output_text = data.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            first_choice = choices[0]
            if isinstance(first_choice, Mapping):
                message = first_choice.get("message")
                if isinstance(message, Mapping):
                    content_value = message.get("content")
                    if isinstance(content_value, str) and content_value.strip():
                        return content_value.strip()
                    if isinstance(content_value, list) and content_value:
                        joined = "\n".join(
                            segment
                            for segment in content_value
                            if isinstance(segment, str) and segment.strip()
                        )
                        if joined.strip():
                            return joined.strip()

        if thinking_only:
            return (
                "The LLM completed the request but only returned internal "
                "reasoning. Try increasing max_tokens or adjusting the "
                "prompt to elicit a visible response."
            )

        raise LLMError("Unexpected LLM response schema")

    @classmethod
    def _build_url(cls, base_url: str) -> str:
        base = base_url.rstrip("/")
        if base.endswith(cls._DEFAULT_PATH):
            return base
        return f"{base}{cls._DEFAULT_PATH}"


__all__ = ["LLMClient", "LLMClientConfig", "LLMError"]
