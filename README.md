# cook-book

## Overview

This repository hosts a lightweight Python implementation that emulates a subset of the
behaviour provided by the AI assistant that powers this platform. The goal is to offer a
recoverable set of utilities that can:

- Validate connectivity to an Anthropic Messages API endpoint.
- Provide a constrained **Assistant Replica** capable of multi-turn conversations,
  basic tool execution, and self-diagnostics.
- Confirm that all Python sources in the project remain syntactically valid.

The solution intentionally documents any missing capabilities so that, during an outage,
you know which features would require manual intervention.

## Project layout

```
assistant_clone/
  __init__.py          Exposes public package interface.
  assistant.py         High-level assistant façade built on top of the LLM client.
  config.py            Environment variable parsing and validation helpers.
  llm_client.py        Minimal Anthropic Messages API HTTP client.
  validation.py        Functions for parsing Python files with `ast`.
scripts/
  verify_llm.py        Connectivity check that exercises the LLM client.
  validate_python.py   Wrapper script to confirm all Python files parse correctly.
tests/                 Unit tests covering the modules above.
```

## Environment variables

The LLM client expects the following variables to be set in the environment:

- `_ANTHROPIC_BASE_URL` – e.g. `https://api.anthropic.com`.
- `_ANTHROPIC_API_KEY` – the API token provisioned for your deployment.
- `_MODEL_NAME` – the Anthropic model identifier to target.

All configuration errors are surfaced with descriptive messages so you can fix them
before executing any other verification steps.

## Using the assistant replica

```bash
# Activate your virtual environment if required
export _ANTHROPIC_BASE_URL="https://api.anthropic.com"
export _ANTHROPIC_API_KEY="<redacted>"
export _MODEL_NAME="claude-3-opus-20240229"

python scripts/verify_llm.py
```

If the check succeeds, you can work with the replica programmatically:

```python
from assistant_clone import AssistantReplica, AnthropicClient, LLMSettings

settings = LLMSettings.from_env()
client = AnthropicClient(settings)
assistant = AssistantReplica(client)
assistant.register_tool(
    "add",
    lambda a, b: a + b,
    description="Adds two numbers together.",
)
print(assistant.ask("What is 2 + 2?"))
print(assistant.describe())
```

The replica maintains conversation history and reports any capabilities it cannot
fulfil (for example, if no tools are currently registered).

## Validating Python sources

Run the parsing guard to ensure the repository contains valid Python:

```bash
python scripts/validate_python.py
```

## Running the automated tests

The unit tests exercise configuration loading, the Anthropic client, the assistant
replica, and the parsing utilities:

```bash
python -m unittest discover -s tests
```

All tests avoid performing real network calls; instead, the Anthropic client is
isolated behind a transport layer so you can substitute a mock when executing tests.
