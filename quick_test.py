#!/usr/bin/env python3
"""Quick test of a single agent."""

import os
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel

console = Console()

client = Anthropic(
    api_key=os.environ.get("_ANTHROPIC_API_KEY"),
    base_url=os.environ.get("_ANTHROPIC_BASE_URL")
)
model = os.environ.get("_MODEL_NAME")

console.print(Panel(
    f"[cyan]Testing Anthropic API[/cyan]\n"
    f"Model: {model}\n"
    f"Base URL: {os.environ.get('_ANTHROPIC_BASE_URL')}",
    title="Configuration"
))

console.print("\n[yellow]Test 1: Simple Query[/yellow]")
response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Write a haiku about programming"}
    ]
)

text_parts = []
for block in response.content:
    if block.type == 'text':
        text_parts.append(block.text)

result = '\n'.join(text_parts)
console.print(Panel(result, title="Haiku Result", border_style="green"))

console.print("\n[yellow]Test 2: Code Analysis[/yellow]")
code_sample = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

response = client.messages.create(
    model=model,
    max_tokens=2000,
    system="You are a code expert. Analyze code and provide suggestions.",
    messages=[
        {"role": "user", "content": f"Analyze this Python code and suggest improvements:\n\n{code_sample}"}
    ]
)

text_parts = []
for block in response.content:
    if block.type == 'text':
        text_parts.append(block.text)

result = '\n'.join(text_parts)
console.print(Panel(result, title="Code Analysis", border_style="blue"))

console.print("\n[green]✓ All tests passed![/green]")
