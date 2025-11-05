#!/usr/bin/env python3
"""Quick demonstration of all capabilities."""
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

console.print(Panel("[bold cyan]🚀 Quick AI System Demo 🚀[/bold cyan]", style="bold blue"))

demos = [
    ("Code", "Write a one-line Python function to reverse a string"),
    ("Math", "What is 7 factorial? Just give me the number."),
    ("Creative", "Write a 3-line haiku about AI")
]

for i, (category, prompt) in enumerate(demos, 1):
    console.print(f"\n[yellow]Demo {i}: {category}[/yellow]")
    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    text_parts = [b.text for b in response.content if b.type == 'text']
    if text_parts:
        text = text_parts[0]
        console.print(f"[green]✓[/green] {text[:200]}...")
    else:
        console.print("[yellow]⚠ Response truncated[/yellow]")

console.print("\n[bold green]✅ All demos successful![/bold green]\n")
