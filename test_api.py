#!/usr/bin/env python3
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("_ANTHROPIC_API_KEY"),
    base_url=os.environ.get("_ANTHROPIC_BASE_URL")
)
model = os.environ.get("_MODEL_NAME", "claude-3-sonnet-20240229")

print("Testing API response structure...")
response = client.messages.create(
    model=model,
    max_tokens=100,
    messages=[{"role": "user", "content": "Say hello"}]
)

print(f"\nResponse type: {type(response)}")
print(f"Response content: {response.content}")
print(f"Content type: {type(response.content)}")

if response.content:
    print(f"\nFirst item type: {type(response.content[0])}")
    print(f"First item: {response.content[0]}")
    print(f"Dir: {dir(response.content[0])}")
