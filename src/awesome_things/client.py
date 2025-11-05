"""Client utilities for interacting with the Anthropic Messages API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional


class MissingEnvironmentVariableError(EnvironmentError):
    """Raised when a required Anthropics environment variable is missing."""


@dataclass
class AnthropicSettings:
    """Configuration settings for accessing the Anthropic API."""

    base_url: str
    api_key: str
    model_name: str
    max_tokens: int = 256

    @classmethod
    def from_environment(
        cls,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> "AnthropicSettings":
        """Create settings pulled from the current environment."""

        resolved_base_url = base_url or os.getenv("_ANTHROPIC_BASE_URL")
        resolved_api_key = api_key or os.getenv("_ANTHROPIC_API_KEY")
        resolved_model = model_name or os.getenv("_MODEL_NAME")

        missing = [
            name
            for name, value in (
                ("_ANTHROPIC_BASE_URL", resolved_base_url),
                ("_ANTHROPIC_API_KEY", resolved_api_key),
                ("_MODEL_NAME", resolved_model),
            )
            if not value
        ]

        if missing:
            raise MissingEnvironmentVariableError(
                "Required environment variables are missing: " + ", ".join(missing)
            )

        return cls(
            base_url=resolved_base_url.rstrip("/"),
            api_key=resolved_api_key,
            model_name=resolved_model,
            max_tokens=max_tokens or 256,
        )


class AnthropicClient:
    """A lightweight client for the Anthropic Messages API."""

    def __init__(
        self,
        settings: Optional[AnthropicSettings] = None,
        *,
        timeout: float = 30.0,
    ) -> None:
        self.settings = settings or AnthropicSettings.from_environment()
        self.timeout = timeout

    def _build_payload(self, prompt: str, *, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        return {
            "model": self.settings.model_name,
            "max_tokens": max_tokens or self.settings.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

    def _build_request(self, payload: Dict[str, Any]) -> urllib.request.Request:
        url = f"{self.settings.base_url}/v1/messages"
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.settings.api_key,
            "anthropic-version": "2023-06-01",
        }
        return urllib.request.Request(url, data=body, headers=headers, method="POST")

    def _extract_text(self, response_body: Dict[str, Any]) -> str:
        """Extract the textual content from a response."""

        content = response_body.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text")
                    if isinstance(text, str):
                        return text
        if isinstance(response_body.get("output_text"), str):
            return str(response_body["output_text"])
        raise ValueError("Unable to find textual content in Anthropic response")

    def send_prompt(self, prompt: str, *, max_tokens: Optional[int] = None) -> str:
        """Send a prompt to the Anthropic API and return the resulting text."""

        payload = self._build_payload(prompt, max_tokens=max_tokens)
        request = self._build_request(payload)

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(
                f"Anthropic API request failed with status {exc.code}: {error_body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Failed to reach Anthropic API: {exc}") from exc

        try:
            decoded = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Anthropic API returned invalid JSON") from exc

        return self._extract_text(decoded)


def generate_awesome_response(prompt: str, *, max_tokens: Optional[int] = None) -> str:
    """Convenience helper to generate a response using environment-backed settings."""

    client = AnthropicClient()
    return client.send_prompt(prompt, max_tokens=max_tokens)
