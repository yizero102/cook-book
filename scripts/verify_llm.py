"""Utility script that verifies the remote LLM configuration."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from local_assistant import LLMClient, LLMError
from local_assistant.policies import DEFAULT_SYSTEM_PROMPT


PROMPT_EXAMPLE = "Reply with a short confirmation sentence so I can verify connectivity."


def main() -> int:
    client = LLMClient()

    if not client.is_configured():
        print(
            "LLM client is not configured. Set _ANTHROPIC_BASE_URL, "
            "_ANTHROPIC_API_KEY, and _MODEL_NAME environment variables before running this script.",
            file=sys.stderr,
        )
        return 2

    try:
        message = client.create_completion(
            DEFAULT_SYSTEM_PROMPT,
            [{"role": "user", "content": PROMPT_EXAMPLE}],
            max_tokens=512,
            temperature=0.0,
        )
    except LLMError as exc:
        print(f"LLM verification failed: {exc}", file=sys.stderr)
        return 3

    print("LLM verification succeeded. Model response:")
    print(message)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
