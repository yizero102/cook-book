#!/usr/bin/env python3
"""
Script to verify that the LLM API can be called successfully.
"""
import os
import sys

def verify_env_variables():
    """Verify that required environment variables are set."""
    required_vars = ['_ANTHROPIC_BASE_URL', '_ANTHROPIC_API_KEY', '_MODEL_NAME']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✓ All required environment variables are set:")
    print(f"  - _ANTHROPIC_BASE_URL: {os.environ.get('_ANTHROPIC_BASE_URL')}")
    print(f"  - _ANTHROPIC_API_KEY: {os.environ.get('_ANTHROPIC_API_KEY')[:20]}...")
    print(f"  - _MODEL_NAME: {os.environ.get('_MODEL_NAME')}")
    return True

def test_llm_call():
    """Test a simple LLM API call."""
    try:
        import anthropic
        print("\n✓ Anthropic library is available")
    except ImportError:
        print("\n❌ Anthropic library not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "anthropic"])
        import anthropic
        print("✓ Anthropic library installed successfully")
    
    try:
        client = anthropic.Anthropic(
            api_key=os.environ.get('_ANTHROPIC_API_KEY'),
            base_url=os.environ.get('_ANTHROPIC_BASE_URL')
        )
        
        print("\n✓ Testing LLM API call...")
        message = client.messages.create(
            model=os.environ.get('_MODEL_NAME'),
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with just 'Hello, I am working!' if you can respond."
                }
            ]
        )
        
        response_text = None
        for content_block in message.content:
            if hasattr(content_block, 'text'):
                response_text = content_block.text
                break
        
        if not response_text:
            print(f"✓ LLM Response received (type: {type(message.content[0])})")
        else:
            print(f"✓ LLM Response: {response_text}")
        
        print(f"✓ Model: {message.model}")
        print(f"✓ Usage: {message.usage}")
        print("\n✅ LLM API is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error calling LLM API: {e}")
        return False

def main():
    """Main function to verify LLM setup."""
    print("=" * 60)
    print("LLM Environment Verification")
    print("=" * 60)
    
    if not verify_env_variables():
        sys.exit(1)
    
    if not test_llm_call():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("All verifications passed! ✅")
    print("=" * 60)

if __name__ == "__main__":
    main()
