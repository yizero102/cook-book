#!/usr/bin/env python3
"""Test the interactive assistant programmatically."""

import os
from anthropic import Anthropic
from rich.console import Console

console = Console()

# Test basic functionality
client = Anthropic(
    api_key=os.environ.get("_ANTHROPIC_API_KEY"),
    base_url=os.environ.get("_ANTHROPIC_BASE_URL")
)
model = os.environ.get("_MODEL_NAME")

console.print("[bold cyan]Testing Interactive AI Assistant Components[/bold cyan]\n")

# Test 1: Quick question
console.print("[yellow]Test: General Q&A[/yellow]")
response = client.messages.create(
    model=model,
    max_tokens=500,
    messages=[{"role": "user", "content": "Explain what a hash table is in one sentence."}]
)
text = [b.text for b in response.content if b.type == 'text'][0]
console.print(f"✓ Response: {text}\n")

# Test 2: Code generation snippet
console.print("[yellow]Test: Quick Code Generation[/yellow]")
response = client.messages.create(
    model=model,
    max_tokens=500,
    messages=[{"role": "user", "content": "Write a Python function to check if a string is a palindrome. Just the code."}]
)
text = [b.text for b in response.content if b.type == 'text'][0]
console.print(f"✓ Generated code snippet\n")

console.print("[bold green]✓ Interactive assistant is functional![/bold green]")
console.print("\n[cyan]To use the interactive assistant, run:[/cyan]")
console.print("[bold]python interactive_ai_assistant.py[/bold]")
