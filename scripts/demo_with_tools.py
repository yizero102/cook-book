#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.settings import Settings
from src.ai_mirror import AIMirrorClient
from src.ai_mirror.tools import create_example_tools


def main():
    print("=" * 60)
    print("AI Mirror - Tools Demo")
    print("=" * 60)
    
    settings = Settings()
    tool_registry = create_example_tools()
    client = AIMirrorClient(settings, tool_registry)
    
    print(f"\nRegistered tools: {[tool.name for tool in tool_registry.get_all_tools()]}")
    
    test_messages = [
        "What tools do you have available?",
        "Can you calculate 15 multiplied by 7?",
        "What is 100 divided by 4?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[Message {i}] User: {message}")
        response = client.chat(message)
        print(f"[Message {i}] Assistant: {response}")
        print("-" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
