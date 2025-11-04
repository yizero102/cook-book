# Local Assistant Recovery Toolkit

This repository provides a Python implementation of a lightweight backup copy of
the production assistant.  It focuses on transparent behaviour, graceful
handling of missing LLM connectivity, and automated checks that validate the
copy behaves consistently.

## Repository structure

```
local_assistant/
  assistant.py        # High level orchestration for the copy
  llm_client.py       # Minimal Anthropic-compatible HTTP client
  policies.py         # High-level behavioural guidelines for the copy
scripts/
  self_assessment.py  # Behaviour smoke-test for the assistant copy
  verify_llm.py       # Connectivity check for the configured LLM
tests/
  test_local_assistant.py  # Automated unit tests covering the core logic
```

## Verifying LLM connectivity

1. Ensure the following environment variables are exported:
   - `_ANTHROPIC_BASE_URL`
   - `_ANTHROPIC_API_KEY`
   - `_MODEL_NAME`
2. Run `python scripts/verify_llm.py`.
   - On success, the script prints the model's short confirmation message.
   - On failure, it reports the error and keeps the assistant in offline mode.

The project never assumes that the network call succeeds; any errors trigger a
safe fallback inside `LocalAssistant`.

## Running the behavioural self-checks

Execute:

```
python scripts/self_assessment.py
```

The script instantiates the assistant copy with LLM usage disabled and ensures
that key safety and honesty behaviours are present even in offline mode.

## Automated tests

Unit tests live in `tests/test_local_assistant.py` and can be executed with:

```
python -m unittest discover -s tests -v
```

They cover:
- Proper LLM usage when a client is available
- Safe fallbacks when the client fails or is disabled
- History truncation behaviour
- URL handling for the Anthropc-compatible client

## Limitations

- The copy intentionally avoids embedding any confidential system instructions;
it implements a transparent, open set of guidelines instead.
- Network access may be unavailable in certain environments. When the LLM cannot
be reached, the assistant automatically switches to deterministic offline
responses and documents the limitation.

## Recovery workflow

1. Run `scripts/verify_llm.py` to confirm whether live LLM access is available.
2. Execute `scripts/self_assessment.py` to ensure the assistant behaves safely in
offline mode.
3. Use the `LocalAssistant` class directly in your applications to obtain
structured, policy-aligned responses.
4. Run the unit test suite to verify regressions before deployment.
