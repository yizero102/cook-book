# Awesome Things with Anthropic

This project provides a lightweight wrapper around the Anthropic Messages API that reads its configuration
from environment variables. Use it to build awesome generative AI experiences from the command line.

## Requirements

Make sure the following environment variables are available before running the tool:

- `_ANTHROPIC_BASE_URL`
- `_ANTHROPIC_API_KEY`
- `_MODEL_NAME`

## Usage

Run the helper script with your prompt:

```bash
python scripts/run_awesome.py "Tell me an awesome fact"
```

Override the maximum number of response tokens with `--max-tokens` if needed:

```bash
python scripts/run_awesome.py "Write a short poem" --max-tokens 128
```

## Development

Run the unit tests to verify the code:

```bash
python -m unittest discover -s tests
```
