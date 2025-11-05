from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional

from openai import OpenAI

from .config import LLMConfig
from .logging_utils import get_logger


@dataclass(frozen=True)
class LLMResult:
    content: str
    reasoning: List[str]
    raw: Any


def _stringify_content(content: Any) -> str:
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, Iterable) and not isinstance(content, (bytes, bytearray, Mapping)):
        parts: List[str] = []
        for item in content:
            parts.append(_stringify_content(item))
        return "\n".join(filter(None, parts))

    return str(content)


def _sanitize_messages(messages: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for message in messages:
        content = message.get("content")
        sanitized.append({
            "role": message.get("role"),
            "content": _stringify_content(content),
            **({"name": message["name"]} if "name" in message else {}),
        })
    return sanitized


def _truncate(value: str, limit: int = 4000) -> str:
    if len(value) <= limit:
        return value
    truncated = value[:limit]
    omitted = len(value) - limit
    return f"{truncated}… (truncated {omitted} chars)"


class LLMClient:
    def __init__(self, config: LLMConfig) -> None:
        kwargs: dict[str, Any] = {"api_key": config.api_key}
        if config.base_url:
            kwargs["base_url"] = config.base_url

        self._client = OpenAI(**kwargs)
        self._model = config.model
        self._reasoning_split = config.reasoning_split
        self._logger = get_logger("multiagent.llm")

    def chat(self, messages: list[dict[str, Any]], **kwargs: Any) -> LLMResult:
        sanitized_messages = _sanitize_messages(messages)
        request_log = {
            "model": kwargs.get("model", self._model),
            "messages": sanitized_messages,
            "extra_body": kwargs.get("extra_body", {"reasoning_split": self._reasoning_split}),
        }
        self._logger.info("LLM request: %s", json.dumps(request_log, ensure_ascii=False))

        payload: MutableMapping[str, Any] = {
            "model": self._model,
            "messages": messages,
            "extra_body": {"reasoning_split": self._reasoning_split},
        }
        payload.update(kwargs)

        try:
            response = self._client.chat.completions.create(**payload)
        except Exception as exc:
            self._logger.exception("LLM request failed: %s", exc)
            raise

        choice = response.choices[0]
        message = choice.message
        content = _stringify_content(getattr(message, "content", None))

        reasoning_as_text: list[str] = []
        raw_reasoning = getattr(message, "reasoning_details", None) or []
        for item in raw_reasoning:
            if isinstance(item, Mapping):
                text = _stringify_content(item.get("text"))
                if text:
                    reasoning_as_text.append(text)

        usage = getattr(response, "usage", None)
        usage_log: Optional[dict[str, Any]] = None
        if usage is not None:
            usage_log = {
                "prompt_tokens": getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
            }

        response_log = {
            "id": getattr(response, "id", None),
            "created": getattr(response, "created", None),
            "model": getattr(response, "model", None),
            "finish_reason": choice.finish_reason,
            "content": _truncate(content, 8000),
            "reasoning": [_truncate(text, 4000) for text in reasoning_as_text],
            "usage": usage_log,
        }
        self._logger.info("LLM response: %s", json.dumps(response_log, ensure_ascii=False))

        return LLMResult(content=content, reasoning=reasoning_as_text, raw=response)
