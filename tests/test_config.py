from __future__ import annotations

import unittest

from assistant_clone.config import (
    ENV_API_KEY,
    ENV_BASE_URL,
    ENV_MODEL_NAME,
    ConfigError,
    LLMSettings,
)


class LLMSettingsTests(unittest.TestCase):
    def test_from_env_success(self) -> None:
        env = {
            ENV_BASE_URL: "https://example.com",
            ENV_API_KEY: "key",
            ENV_MODEL_NAME: "model",
        }
        settings = LLMSettings.from_env(env)
        self.assertEqual(settings.base_url, "https://example.com")
        self.assertEqual(settings.api_key, "key")
        self.assertEqual(settings.model, "model")

    def test_missing_variables_raise_error(self) -> None:
        env = {ENV_BASE_URL: "https://example.com"}
        with self.assertRaises(ConfigError) as cm:
            LLMSettings.from_env(env)
        self.assertIn(ENV_API_KEY, cm.exception.missing)
        self.assertIn(ENV_MODEL_NAME, cm.exception.missing)

    def test_invalid_base_url(self) -> None:
        env = {
            ENV_BASE_URL: "example.com",
            ENV_API_KEY: "key",
            ENV_MODEL_NAME: "model",
        }
        with self.assertRaises(ConfigError):
            LLMSettings.from_env(env)


if __name__ == "__main__":
    unittest.main()
