from __future__ import annotations

import unittest

from assistant_clone.config import LLMSettings
from assistant_clone.llm_client import AnthropicClient, AnthropicError


class AnthropicClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = LLMSettings(
            base_url="https://example.com",
            api_key="secret",
            model="test-model",
        )

    def test_create_message_uses_transport(self) -> None:
        observed: dict[str, object] = {}

        def transport(payload, headers):
            observed["payload"] = payload
            observed["headers"] = headers
            return {"content": [{"type": "text", "text": "ok"}]}

        client = AnthropicClient(self.settings, transport=transport)
        response = client.create_message(
            [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "hello",
                        }
                    ],
                }
            ],
            max_output_tokens=64,
        )
        self.assertIn("content", response)
        payload = observed["payload"]
        self.assertEqual(payload["model"], "test-model")
        self.assertEqual(payload["max_output_tokens"], 64)
        self.assertEqual(observed["headers"]["x-api-key"], "secret")

    def test_respond_to_prompt_extracts_text(self) -> None:
        client = AnthropicClient(
            self.settings,
            transport=lambda payload, headers: {"content": [{"type": "text", "text": "pong"}]},
        )
        text = client.respond_to_prompt("ping")
        self.assertEqual(text, "pong")

    def test_verify_reports_failure_without_text(self) -> None:
        client = AnthropicClient(
            self.settings,
            transport=lambda payload, headers: {"content": []},
        )
        result = client.verify()
        self.assertFalse(result.success)
        self.assertIn("textual content", result.detail.lower())

    def test_invalid_message_structure(self) -> None:
        client = AnthropicClient(self.settings, transport=lambda payload, headers: {})
        with self.assertRaises(ValueError):
            client.create_message([])
        with self.assertRaises(ValueError):
            client.create_message([{"role": "unknown", "content": []}])

    def test_extract_text_errors(self) -> None:
        client = AnthropicClient(self.settings, transport=lambda payload, headers: {})
        with self.assertRaises(AnthropicError):
            client.extract_text({"content": [{"type": "text"}]})


if __name__ == "__main__":
    unittest.main()
