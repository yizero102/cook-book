#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from config.settings import Settings
from src.ai_mirror import AIMirrorClient


def main():
    print("=" * 60)
    print("AI Mirror System - Interactive Demo")
    print("=" * 60)
    
    settings = Settings()
    is_valid, error_msg = settings.validate()
    
    if not is_valid:
        print(f"\n❌ Configuration Error: {error_msg}")
        print("\nPlease ensure the following environment variables are set:")
        print("  - _ANTHROPIC_API_KEY")
        print("  - _ANTHROPIC_BASE_URL")
        print("  - _MODEL_NAME")
        return 1
    
    print(f"\n✓ Configuration loaded:")
    print(f"  Model: {settings.model_name}")
    print(f"  Base URL: {settings.anthropic_base_url}")
    
    client = AIMirrorClient(settings)
    
    print("\n✓ Verifying connection...")
    success, message = client.verify_connection()
    
    if not success:
        print(f"❌ {message}")
        return 1
    
    print(f"✓ {message}")
    
    client.set_system_prompt(
        "You are a helpful AI assistant. Provide clear, concise, and friendly responses."
    )
    
    print("\n" + "=" * 60)
    print("Interactive Chat (type 'quit' to exit, 'clear' to reset)")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                client.clear_conversation()
                print("🔄 Conversation cleared!")
                continue
            
            if user_input.lower() == 'history':
                history = client.get_conversation_history()
                print(f"\n📜 Conversation has {len(history['messages'])} messages")
                continue
            
            response = client.chat(user_input)
            print(f"\nAI: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
