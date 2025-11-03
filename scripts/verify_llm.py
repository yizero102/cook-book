#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.settings import Settings
from src.ai_mirror import AIMirrorClient


def main():
    print("=" * 60)
    print("LLM Connection Verification")
    print("=" * 60)
    
    settings = Settings()
    
    print("\n1. Checking environment variables...")
    is_valid, error_msg = settings.validate()
    
    if not is_valid:
        print(f"   ❌ FAILED: {error_msg}")
        print("\nPlease ensure the following environment variables are set:")
        print("   - _ANTHROPIC_API_KEY")
        print("   - _ANTHROPIC_BASE_URL")
        print("   - _MODEL_NAME")
        return 1
    
    print("   ✓ All environment variables are set")
    print(f"   - Base URL: {settings.anthropic_base_url}")
    print(f"   - Model: {settings.model_name}")
    print(f"   - API Key: {settings.anthropic_api_key[:20]}...")
    
    print("\n2. Testing API connection...")
    try:
        client = AIMirrorClient(settings)
        success, message = client.verify_connection()
        
        if success:
            print(f"   ✓ {message}")
        else:
            print(f"   ❌ FAILED: {message}")
            return 1
            
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return 1
    
    print("\n3. Testing basic chat functionality...")
    try:
        response = client.chat("What is 2+2? Please answer briefly.")
        print(f"   ✓ Chat successful")
        print(f"   Response preview: {response[:100]}...")
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return 1
    
    print("\n" + "=" * 60)
    print("✓ All verification tests passed!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
