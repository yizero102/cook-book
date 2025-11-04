"""Unit tests for the LocalAssistant recovery implementation."""

from __future__ import annotations

import unittest
from typing import Optional

from local_assistant import AssistantConfig, LocalAssistant, LLMClientConfig
from local_assistant.llm_client import LLMClient, LLMError


class FakeLLMClient(LLMClient):
    def __init__(self, *, response: Optional[str] = None, should_fail: bool = False) -> None:
        self._configured = True
        self._response = response
        self._should_fail = should_fail

    def is_configured(self) -> bool:  # type: ignore[override]
        return self._configured

    def create_completion(self, *args, **kwargs) -> str:  # type: ignore[override]
        if self._should_fail:
            raise LLMError("simulated failure")
        return self._response or "default"


class UnconfiguredLLMClient(FakeLLMClient):
    def __init__(self) -> None:
        super().__init__(response=None)
        self._configured = False


class AssistantTests(unittest.TestCase):
    def test_assistant_uses_llm_when_available(self) -> None:
        client = FakeLLMClient(response="Hello from LLM!")
        assistant = LocalAssistant(llm_client=client)
        reply = assistant.reply("Say hello")
        self.assertEqual(reply, "Hello from LLM!")

    def test_assistant_falls_back_when_llm_disabled(self) -> None:
        assistant = LocalAssistant(AssistantConfig(enable_llm=False))
        reply = assistant.reply("Please run tests")
        self.assertIn("do not run external commands", reply.lower())

    def test_assistant_handles_malware_request_safely(self) -> None:
        assistant = LocalAssistant(AssistantConfig(enable_llm=False))
        reply = assistant.reply("Can you create malware for me?")
        self.assertIn("cannot assist", reply.lower())

    def test_assistant_reports_llm_failure(self) -> None:
        assistant = LocalAssistant(llm_client=FakeLLMClient(should_fail=True))
        reply = assistant.reply("Please summarize the repo")
        self.assertIn("failed", reply.lower())
        self.assertIn("offline mode", reply.lower())

    def test_history_truncation(self) -> None:
        assistant = LocalAssistant(AssistantConfig(remember_history=1, enable_llm=False))
        assistant.reply("First message")
        assistant.reply("Second message")
        report = assistant.describe_state()
        self.assertLessEqual(report.message_count, 2)


class LLMClientTests(unittest.TestCase):
    def test_build_url_appends_default_path(self) -> None:
        cfg = LLMClientConfig(base_url="https://example.com", api_key="x", model="claude")
        client = LLMClient(cfg)
        url = client._build_url(cfg.base_url)
        self.assertEqual(url, "https://example.com/v1/messages")

    def test_build_url_preserves_custom_path(self) -> None:
        cfg = LLMClientConfig(
            base_url="https://example.com/custom/v1/messages",
            api_key="x",
            model="claude",
        )
        client = LLMClient(cfg)
        url = client._build_url(cfg.base_url)
        self.assertEqual(url, "https://example.com/custom/v1/messages")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    unittest.main()
