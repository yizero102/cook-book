"""Tests for the Anthropic client utilities."""

from __future__ import annotations

import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import urllib.error

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from awesome_things.client import (  # noqa: E402
    AnthropicClient,
    AnthropicSettings,
    MissingEnvironmentVariableError,
    generate_awesome_response,
)


class AnthropicSettingsTests(unittest.TestCase):
    def test_missing_env_variables_raise_error(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(MissingEnvironmentVariableError):
                AnthropicSettings.from_environment()

    def test_settings_are_read_from_environment(self) -> None:
        env = {
            "_ANTHROPIC_BASE_URL": "https://example.com",
            "_ANTHROPIC_API_KEY": "secret",
            "_MODEL_NAME": "awesome-model",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = AnthropicSettings.from_environment(max_tokens=99)

        self.assertEqual(settings.base_url, "https://example.com")
        self.assertEqual(settings.api_key, "secret")
        self.assertEqual(settings.model_name, "awesome-model")
        self.assertEqual(settings.max_tokens, 99)


class AnthropicClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = AnthropicSettings(
            base_url="https://example.com",
            api_key="secret",
            model_name="awesome-model",
        )

    @patch("urllib.request.urlopen")
    def test_send_prompt_success(self, mock_urlopen: MagicMock) -> None:
        response_payload = {
            "content": [
                {
                    "type": "text",
                    "text": "Here is something awesome!",
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(response_payload).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        client = AnthropicClient(self.settings)
        prompt = "Tell me something awesome."
        result = client.send_prompt(prompt, max_tokens=123)

        self.assertEqual(result, "Here is something awesome!")
        request = mock_urlopen.call_args[0][0]
        self.assertIn("/v1/messages", request.full_url)
        headers = {key.lower(): value for key, value in request.header_items()}
        self.assertEqual(headers["x-api-key"], "secret")
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "awesome-model")
        self.assertEqual(payload["max_tokens"], 123)

    @patch("urllib.request.urlopen")
    def test_send_prompt_http_error(self, mock_urlopen: MagicMock) -> None:
        error = urllib.error.HTTPError(
            url="https://example.com/v1/messages",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=io.BytesIO(b"Not allowed"),
        )
        mock_urlopen.side_effect = error

        client = AnthropicClient(self.settings)

        with self.assertRaises(RuntimeError) as ctx:
            client.send_prompt("Hello")

        self.assertIn("401", str(ctx.exception))
        self.assertIn("Not allowed", str(ctx.exception))


class GenerateAwesomeResponseTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "_ANTHROPIC_BASE_URL": "https://example.com",
            "_ANTHROPIC_API_KEY": "secret",
            "_MODEL_NAME": "awesome-model",
        },
        clear=True,
    )
    @patch("awesome_things.client.AnthropicClient.send_prompt", return_value="Great success!")
    def test_generate_awesome_response_uses_client(self, mock_send_prompt: MagicMock) -> None:
        result = generate_awesome_response("Make it awesome")

        self.assertEqual(result, "Great success!")
        mock_send_prompt.assert_called_once_with("Make it awesome", max_tokens=None)


if __name__ == "__main__":
    unittest.main()
