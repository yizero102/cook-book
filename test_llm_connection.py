#!/usr/bin/env python3
"""
Test script to verify LLM connection using environment variables.
"""
import os
import sys
import anthropic

def test_llm_connection():
    """Test the LLM connection with environment variables."""
    print("=" * 60)
    print("Testing LLM Connection")
    print("=" * 60)
    
    # Get environment variables
    api_key = os.getenv("_ANTHROPIC_API_KEY")
    base_url = os.getenv("_ANTHROPIC_BASE_URL")
    model_name = os.getenv("_MODEL_NAME")
    
    print(f"\nEnvironment Variables:")
    print(f"  Base URL: {base_url}")
    print(f"  Model: {model_name}")
    print(f"  API Key: {'*' * 20}{api_key[-10:] if api_key else 'NOT SET'}")
    
    if not api_key or not base_url or not model_name:
        print("\n❌ ERROR: Missing required environment variables!")
        print("Required: _ANTHROPIC_API_KEY, _ANTHROPIC_BASE_URL, _MODEL_NAME")
        return False
    
    try:
        # Initialize client
        print("\n📡 Initializing Anthropic client...")
        client = anthropic.Anthropic(
            api_key=api_key,
            base_url=base_url
        )
        
        # Make a test call
        print("📤 Sending test message to LLM...")
        message = client.messages.create(
            model=model_name,
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with 'OK' if you can read this message."
                }
            ]
        )
        
        # Extract text from response (handling thinking blocks)
        response_text = ""
        for block in message.content:
            if hasattr(block, 'text'):
                response_text += block.text
        print(f"📥 Response received: {response_text}")
        
        print("\n✅ SUCCESS: LLM connection is working!")
        print(f"   Model: {message.model}")
        print(f"   Usage: {message.usage}")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to connect to LLM!")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_llm_connection()
    sys.exit(0 if success else 1)
