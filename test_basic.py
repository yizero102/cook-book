"""
Basic test to verify the system setup.
"""

import os
from llm_client import LLMClient
from llm_logger import LLMLogger

def main():
    print("Testing basic LLM client setup...")
    
    # Check environment variables
    print(f"Base URL: {os.environ.get('_OPENAI_BASE_URL', 'NOT SET')}")
    print(f"Model: {os.environ.get('_MODEL_NAME', 'NOT SET')}")
    print(f"API Key: {'SET' if os.environ.get('_OPENAI_API_KEY') else 'NOT SET'}")
    
    # Initialize client
    logger = LLMLogger(log_dir="llm_logs")
    client = LLMClient(logger=logger)
    print("\n✓ Client initialized successfully")
    
    # Test a simple request
    print("\nTesting LLM request...")
    response = client.chat(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, Multi-Agent System!' and explain what you are in one sentence."}
        ],
        agent_name="TestAgent"
    )
    
    print("\n=== Response ===")
    print(f"Content: {response['content']}")
    if response['reasoning']:
        print(f"\nReasoning: {response['reasoning'][:200]}...")
    print(f"\nRequest ID: {response['request_id']}")
    
    print("\n✓ Test completed successfully!")
    print(f"✓ Check the '{logger.log_dir}' directory for logs")
    
    return 0

if __name__ == "__main__":
    main()
