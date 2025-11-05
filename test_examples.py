#!/usr/bin/env python3
import os
from ai_assistant import AICodeAssistant
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def test_code_review():
    console.print("\n[bold cyan]Testing Code Review Feature[/bold cyan]")
    
    assistant = AICodeAssistant()
    
    buggy_code = """
def divide_numbers(a, b):
    return a / b

def process_list(items):
    total = 0
    for i in range(len(items)):
        total += items[i]
    return total / len(items)
"""
    
    console.print("[yellow]Analyzing potentially buggy code...[/yellow]")
    analysis = assistant.analyze_code(buggy_code, "python")
    console.print(Panel(Markdown(analysis), title="Bug Analysis", border_style="red"))


def test_creative_writing():
    console.print("\n[bold cyan]Testing Creative Writing Feature[/bold cyan]")
    
    assistant = AICodeAssistant()
    
    prompts = [
        "Explain recursion using a real-world analogy that a 10-year-old could understand.",
        "Write a motivational message for developers facing debugging challenges.",
    ]
    
    for prompt in prompts:
        console.print(f"\n[yellow]Prompt: {prompt}[/yellow]")
        response = assistant.creative_challenge(prompt)
        console.print(Panel(Markdown(response), border_style="cyan"))


def test_javascript_code():
    console.print("\n[bold cyan]Testing JavaScript Code Analysis[/bold cyan]")
    
    assistant = AICodeAssistant()
    
    js_code = """
function fetchUserData(userId) {
    fetch(`https://api.example.com/users/${userId}`)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log("Error:", error));
}
"""
    
    console.print("[yellow]Analyzing JavaScript code...[/yellow]")
    improvements = assistant.suggest_improvements(js_code, "javascript")
    console.print(Panel(Markdown(improvements), title="JS Improvements", border_style="green"))


def main():
    console.print(Panel.fit(
        "[bold magenta]Additional AI Assistant Tests[/bold magenta]\n"
        "Demonstrating various capabilities",
        border_style="magenta"
    ))
    
    test_code_review()
    test_creative_writing()
    test_javascript_code()
    
    console.print("\n[bold green]✓ All additional tests completed![/bold green]")


if __name__ == "__main__":
    main()
