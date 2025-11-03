"""Minimal HTTP client for interacting with the Anthropic Messages API.

The implementation intentionally focuses on the subset of behaviour required for
health checks and unit tests. All network access is isolated to allow mocking
in environments without outbound connectivity.
"""

from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from .config import LLMSettings


class AnthropicError(RuntimeError):
    """Raised for any issue encountered while talking to the Anthropic API."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


@dataclass(frozen=True)
class VerificationResult:
    """Structured outcome for LLM connectivity checks."""

    success: bool
    detail: str
    response: Mapping[str, Any] | None = None


Transport = Callable[[dict[str, Any], Mapping[str, str]], Mapping[str, Any]]


class AnthropicClient:
    """Small HTTP client tailored for message-style requests."""

    def __init__(
        self,
        settings: LLMSettings,
        *,
        request_timeout: float = 30.0,
        transport: Transport | None = None,
    ) -> None:
        self.settings = settings
        self.request_timeout = request_timeout
        self._transport = transport or self._default_transport

    def create_message(
        self,
        messages: Iterable[Mapping[str, Any]],
        *,
        max_output_tokens: int = 256,
        temperature: float | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> Mapping[str, Any]:
        message_list = self._normalise_messages(messages)
        payload = self.settings.to_payload(
            message_list,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            tools=tools,
        )
        headers = self.settings.to_headers()
        response = self._transport(payload, headers)
        if not isinstance(response, Mapping):
            raise AnthropicError("Provider returned a non-mapping response payload.")
        return response

    def respond_to_prompt(
        self,
        prompt: str,
        *,
        max_output_tokens: int = 256,
        temperature: float | None = None,
    ) -> str:
        response = self.create_message(
            [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                }
            ],
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )
        return self._extract_text(response)

    def verify(self) -> VerificationResult:
        """Attempt to reach the Anthropic API and return a structured verdict."""
        try:
            response = self.create_message(
                [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "ping",
                            }
                        ],
                    }
                ],
                max_output_tokens=32,
            )
        except AnthropicError as exc:
            return VerificationResult(False, str(exc))

        try:
            text = self._extract_text(response)
        except AnthropicError as exc:
            return VerificationResult(False, str(exc), response=response)
        detail = "Received response from Anthropic." if text else "Empty response body from Anthropic."
        return VerificationResult(bool(text), detail, response=response)

    def _default_transport(self, payload: dict[str, Any], headers: Mapping[str, str]) -> Mapping[str, Any]:
        url = f"{self.settings.base_url}/v1/messages"
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url=url, data=body, headers=dict(headers), method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.request_timeout) as response:  # type: ignore[arg-type]
                raw = response.read()
                text = raw.decode("utf-8")
        except urllib.error.HTTPError as exc:  # pragma: no cover - network behaviour
            status = getattr(exc, "code", None)
            try:
                detail_bytes = exc.read()
            except Exception:  # pragma: no cover - defensive
                detail_bytes = b""
            detail = detail_bytes.decode("utf-8", errors="ignore") or str(exc)
            raise AnthropicError(f"HTTP error {status}: {detail}", status_code=status) from exc
        except urllib.error.URLError as exc:  # pragma: no cover - network behaviour
            raise AnthropicError(f"Network error when contacting Anthropic: {exc.reason}") from exc
        except socket.timeout as exc:  # pragma: no cover - network behaviour
            raise AnthropicError("Request to Anthropic timed out.") from exc
        except Exception as exc:  # pragma: no cover - defensive
            raise AnthropicError(f"Unexpected transport failure: {exc!r}") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise AnthropicError("Anthropic returned non-JSON response.") from exc

    @staticmethod
    def _normalise_messages(messages: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
        message_list: list[dict[str, Any]] = []
        for message in messages:
            if not isinstance(message, Mapping):
                raise ValueError("Each message must be a mapping with role/content keys.")
            role = message.get("role")
            content = message.get("content")
            if role not in {"user", "assistant", "system"}:
                raise ValueError(f"Unsupported message role: {role!r}")
            if not isinstance(content, Iterable):
                raise ValueError("Message content must be an iterable of blocks.")
            blocks: list[dict[str, Any]] = []
            for block in content:
                if not isinstance(block, Mapping):
                    raise ValueError("Each content block must be a mapping.")
                block_type = block.get("type")
                if block_type != "text":
                    raise ValueError(f"Unsupported block type: {block_type!r}")
                text = block.get("text")
                if not isinstance(text, str):
                    raise ValueError("Text blocks must include a string 'text' field.")
                blocks.append({"type": "text", "text": text})
            message_list.append({"role": role, "content": blocks})
        if not message_list:
            raise ValueError("At least one message is required.")
        return message_list

    def extract_text(self, response: Mapping[str, Any]) -> str:
        """Public wrapper for extracting text content from a response."""
        return self._extract_text(response)

    @staticmethod
    def _extract_text(response: Mapping[str, Any]) -> str:
        content = response.get("content")
        if not isinstance(content, Iterable):
            raise AnthropicError("Response payload is missing a 'content' list.")
        texts: list[str] = []
        for block in content:
            if isinstance(block, Mapping) and block.get("type") == "text":
                text = block.get("text")
                if isinstance(text, str):
                    texts.append(text)
        if not texts:
            raise AnthropicError("Response payload did not include textual content.")
        return "".join(texts)
