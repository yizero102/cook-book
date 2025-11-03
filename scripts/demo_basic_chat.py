#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.settings import Settings
from src.ai_mirror import AIMirrorClient


def main():
    print("=" * 60)
    print("AI Mirror - Basic Chat Demo")
    print("=" * 60)
    
    settings = Settings()
    client = AIMirrorClient(settings)
    
    client.set_system_prompt(
        "You are a helpful AI assistant. You provide clear, concise answers."
    )
    
    test_messages = [
        "Hello! What is your purpose?",
        "Can you help me with Python programming?",
        "What are the key principles of good software design?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[Message {i}] User: {message}")
        response = client.chat(message)
        print(f"[Message {i}] Assistant: {response}")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("Conversation History:")
    print("=" * 60)
    history = client.get_conversation_history()
    print(f"Total messages: {len(history['messages'])}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
