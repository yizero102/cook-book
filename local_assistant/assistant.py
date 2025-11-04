"""High-level orchestration for the stand-alone assistant copy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Mapping, Optional

from .llm_client import LLMClient, LLMError
from .policies import DEFAULT_SYSTEM_PROMPT


Message = Mapping[str, str]


@dataclass
class AssistantConfig:
    """User-configurable knobs for :class:`LocalAssistant`."""

    name: str = "LocalAssistant"
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    remember_history: int = 8
    enable_llm: bool = True


@dataclass
class AssistantReport:
    """Summarises a single interaction for downstream validation."""

    used_llm: bool
    message_count: int
    last_user_message: str
    last_assistant_message: str
    notes: str = ""


class LocalAssistant:
    """Simplified analogue of the production assistant used for recovery."""

    def __init__(
        self,
        config: Optional[AssistantConfig] = None,
        llm_client: Optional[LLMClient] = None,
    ) -> None:
        self._config = config or AssistantConfig()
        self._llm_client = llm_client or LLMClient()
        self._history: List[Message] = []

    @property
    def config(self) -> AssistantConfig:
        return self._config

    def reset(self) -> None:
        self._history.clear()

    # Public API -----------------------------------------------------
    def reply(self, user_message: str) -> str:
        user_message = user_message.strip()
        if not user_message:
            return "Please provide a question or instruction so I can help."

        self._append_history({"role": "user", "content": user_message})
        used_llm = False
        assistant_message: str

        if self._should_use_llm():
            try:
                assistant_message = self._call_llm(user_message)
                used_llm = True
            except LLMError as exc:
                assistant_message = self._llm_failure_response(exc)
        else:
            assistant_message = self._offline_response(user_message)

        self._append_history({"role": "assistant", "content": assistant_message})
        self._truncate_history()
        return assistant_message

    def describe_state(self) -> AssistantReport:
        last_user = next((m["content"] for m in reversed(self._history) if m["role"] == "user"), "")
        last_assistant = next(
            (m["content"] for m in reversed(self._history) if m["role"] == "assistant"),
            "",
        )
        notes = "LLM ready" if self._should_use_llm() else "Operating in offline mode"
        return AssistantReport(
            used_llm=self._should_use_llm(),
            message_count=len(self._history),
            last_user_message=last_user,
            last_assistant_message=last_assistant,
            notes=notes,
        )

    # Internal helpers -----------------------------------------------
    def _should_use_llm(self) -> bool:
        if not self._config.enable_llm:
            return False
        return self._llm_client is not None and self._llm_client.is_configured()

    def _call_llm(self, latest_user_message: str) -> str:
        messages = list(self._history)
        return self._llm_client.create_completion(self._config.system_prompt, messages)

    def _append_history(self, message: Message) -> None:
        self._history.append(message)

    def _truncate_history(self) -> None:
        remember = self._config.remember_history
        if remember <= 0:
            self._history.clear()
            return
        excess = len(self._history) - (remember * 2)
        if excess <= 0:
            return
        del self._history[:excess]

    def _offline_response(self, user_message: str) -> str:
        lowered = user_message.lower()
        if any(keyword in lowered for keyword in {"hack", "malware", "exploit"}):
            return (
                "I cannot assist with that. This local copy follows safety guidelines "
                "and refuses requests related to malware or exploits."
            )
        if "secret" in lowered or "password" in lowered:
            return (
                "I cannot help with sharing or retrieving secrets. If you need help "
                "with credential management, consider using a secure password manager."
            )
        if "test" in lowered and ("run" in lowered or "execute" in lowered):
            return (
                "I do not run external commands in this environment. Instead, I can "
                "suggest how you might run the tests locally."
            )
        return (
            "I am running without live LLM connectivity, so this is a rule-based "
            "response. Provide additional detail and I will outline an offline plan."
        )

    def _llm_failure_response(self, error: LLMError) -> str:
        return (
            "I attempted to call the configured LLM but it failed with the "
            f"following error: {error}. I will continue in offline mode. "
            "If you expect the LLM call to work, please verify the API key, base "
            "URL, network connectivity, and model name."
        )


__all__ = ["AssistantConfig", "AssistantReport", "LocalAssistant"]
