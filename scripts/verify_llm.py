#!/usr/bin/env python3
"""Utility script that checks whether the Anthropic API is reachable."""

from __future__ import annotations

import json
import sys

from assistant_clone.config import ConfigError, LLMSettings
from assistant_clone.llm_client import AnthropicClient


def main() -> int:
    try:
        settings = LLMSettings.from_env()
    except ConfigError as exc:
        payload = {
            "ok": False,
            "error": "configuration",
            "detail": str(exc),
            "missing": list(exc.missing),
        }
        print(json.dumps(payload, indent=2))
        return 2

    client = AnthropicClient(settings)
    result = client.verify()
    payload = {
        "ok": result.success,
        "detail": result.detail,
    }
    if result.response is not None:
        payload["response_keys"] = sorted(result.response.keys())
    print(json.dumps(payload, indent=2))
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
