#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from multiagent.orchestrator import run_default_workflow
from multiagent.logging_utils import get_logger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the multi-agent orchestration workflow for an ambitious mission.",
    )
    parser.add_argument(
        "--mission",
        required=True,
        help="High-level mission the agents must accomplish.",
    )
    parser.add_argument(
        "--context",
        help="Optional context that will be shared with every agent.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the combined Markdown report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = get_logger("multiagent.runner")
    logger.info("Starting multi-agent workflow for mission: %s", args.mission)

    result = run_default_workflow(mission=args.mission, context=args.context)

    print("\n===== STRATEGIC PLAN =====\n")
    print(result.plan.content)

    print("\n===== INSIGHT SYNTHESIS =====\n")
    print(result.insights.content)

    print("\n===== EXECUTION BLUEPRINT =====\n")
    print(result.blueprint.content)

    print("\n===== EXECUTIVE ASSESSMENT =====\n")
    print(result.assessment.content)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result.to_markdown(), encoding="utf-8")
        logger.info("Wrote Markdown report to %s", args.output)

    logger.info("Workflow finished successfully")


if __name__ == "__main__":
    main()
