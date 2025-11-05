#!/usr/bin/env python3
"""Run an awesome Anthropic prompt from the command line."""

import argparse
import sys

from awesome_things import generate_awesome_response


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create something awesome with Anthropic")
    parser.add_argument("prompt", help="The prompt to send to the Anthropic model")
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Override the default maximum number of tokens in the response",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        response = generate_awesome_response(args.prompt, max_tokens=args.max_tokens)
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to generate response: {exc}", file=sys.stderr)
        return 1

    print(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
