#!/usr/bin/env python3
import sys
from ai_assistant import AICodeAssistant
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


def display_menu():
    table = Table(title="AI Code Assistant Menu", show_header=True, header_style="bold cyan")
    table.add_column("Option", style="cyan", width=10)
    table.add_column("Description", style="white")
    
    table.add_row("1", "Analyze Code")
    table.add_row("2", "Generate Documentation")
    table.add_row("3", "Suggest Improvements")
    table.add_row("4", "Creative AI Challenge")
    table.add_row("5", "Quick Code Review")
    table.add_row("q", "Quit")
    
    console.print(table)


def get_code_input():
    console.print("\n[yellow]Enter your code (type 'END' on a new line to finish):[/yellow]")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)


def analyze_code_interactive(assistant):
    code = get_code_input()
    if not code.strip():
        console.print("[red]No code provided![/red]")
        return
    
    language = Prompt.ask("\n[cyan]Programming language[/cyan]", default="python")
    
    console.print("\n[yellow]Analyzing code...[/yellow]")
    result = assistant.analyze_code(code, language)
    console.print(Panel(Markdown(result), title="Code Analysis", border_style="magenta"))


def generate_docs_interactive(assistant):
    code = get_code_input()
    if not code.strip():
        console.print("[red]No code provided![/red]")
        return
    
    language = Prompt.ask("\n[cyan]Programming language[/cyan]", default="python")
    
    console.print("\n[yellow]Generating documentation...[/yellow]")
    result = assistant.generate_documentation(code, language)
    console.print(Panel(Markdown(result), title="Documentation", border_style="green"))


def suggest_improvements_interactive(assistant):
    code = get_code_input()
    if not code.strip():
        console.print("[red]No code provided![/red]")
        return
    
    language = Prompt.ask("\n[cyan]Programming language[/cyan]", default="python")
    
    console.print("\n[yellow]Suggesting improvements...[/yellow]")
    result = assistant.suggest_improvements(code, language)
    console.print(Panel(Markdown(result), title="Suggested Improvements", border_style="blue"))


def creative_challenge_interactive(assistant):
    console.print("\n[yellow]Enter your creative prompt:[/yellow]")
    prompt = input()
    
    if not prompt.strip():
        console.print("[red]No prompt provided![/red]")
        return
    
    console.print("\n[yellow]Thinking creatively...[/yellow]")
    result = assistant.creative_challenge(prompt)
    console.print(Panel(Markdown(result), title="AI Response", border_style="cyan"))


def quick_code_review(assistant):
    examples = {
        "1": ("Python: Potential Division by Zero", """
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""),
        "2": ("JavaScript: Missing Error Handling", """
async function getData() {
    const response = await fetch('https://api.example.com/data');
    return response.json();
}
"""),
        "3": ("Python: Performance Issue", """
def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates
"""),
    }
    
    console.print("\n[bold cyan]Quick Code Review - Select an example:[/bold cyan]")
    for key, (title, _) in examples.items():
        console.print(f"  {key}. {title}")
    
    choice = Prompt.ask("Choose an example", choices=["1", "2", "3"], default="1")
    
    title, code = examples[choice]
    language = "python" if "Python" in title else "javascript"
    
    console.print(f"\n[bold yellow]Reviewing: {title}[/bold yellow]")
    console.print(Panel(code, border_style="yellow"))
    
    result = assistant.analyze_code(code, language)
    console.print(Panel(Markdown(result), title="Code Review", border_style="red"))


def main():
    console.print(Panel.fit(
        "[bold green]AI-Powered Code Assistant - Interactive Mode[/bold green]\n"
        "Powered by Anthropic's LLM",
        border_style="green"
    ))
    
    try:
        assistant = AICodeAssistant()
        
        while True:
            console.print("\n")
            display_menu()
            
            choice = Prompt.ask("\n[bold cyan]Select an option[/bold cyan]", default="q")
            
            if choice.lower() == "q":
                console.print("\n[green]Thanks for using AI Code Assistant! Goodbye![/green]")
                break
            elif choice == "1":
                analyze_code_interactive(assistant)
            elif choice == "2":
                generate_docs_interactive(assistant)
            elif choice == "3":
                suggest_improvements_interactive(assistant)
            elif choice == "4":
                creative_challenge_interactive(assistant)
            elif choice == "5":
                quick_code_review(assistant)
            else:
                console.print("[red]Invalid option! Please try again.[/red]")
            
            if not Confirm.ask("\n[cyan]Continue?[/cyan]", default=True):
                console.print("\n[green]Thanks for using AI Code Assistant! Goodbye![/green]")
                break
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user. Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
