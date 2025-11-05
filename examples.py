#!/usr/bin/env python3

from multi_agent_system import MultiAgentSystem
from rich.console import Console
from rich.panel import Panel

console = Console()

EXAMPLES = {
    "1": {
        "name": "Technical Analysis: Quantum Computing",
        "task": """
Analyze the current state and future potential of quantum computing:
1. What are the main technical approaches (superconducting, ion trap, topological)?
2. What are the current limitations and error correction challenges?
3. What applications will benefit first from quantum advantage?
4. What timeline should we expect for practical quantum computing?
5. How will quantum computing impact cryptography and security?
"""
    },
    "2": {
        "name": "Business Strategy: AI Integration",
        "task": """
Develop a comprehensive strategy for a mid-size company to integrate AI:
1. What are the highest-ROI AI applications for different industries?
2. What infrastructure and talent requirements are needed?
3. What risks and challenges should be anticipated?
4. What is a realistic 3-year roadmap for AI adoption?
5. How can companies balance innovation with responsible AI practices?
"""
    },
    "3": {
        "name": "Scientific Research: Climate Solutions",
        "task": """
Analyze emerging technologies for climate change mitigation:
1. What are the most promising carbon capture and storage technologies?
2. How can renewable energy be scaled globally?
3. What role can AI and advanced materials play?
4. What are the economic and political barriers?
5. Propose a multi-faceted action plan with prioritized interventions.
"""
    },
    "4": {
        "name": "Creative Analysis: Future of Entertainment",
        "task": """
Explore how AI will transform entertainment and media:
1. How will AI-generated content coexist with human creativity?
2. What new forms of interactive and immersive entertainment will emerge?
3. How will content creation and distribution change?
4. What are the implications for artists, creators, and audiences?
5. How can we ensure diverse, quality content in an AI-assisted future?
"""
    },
    "5": {
        "name": "Custom Task",
        "task": None
    }
}

def display_menu():
    console.print(Panel.fit(
        "[bold magenta]Multi-Agent System - Example Tasks[/bold magenta]\n"
        "[cyan]Choose a complex task for the multi-agent system to analyze[/cyan]",
        border_style="magenta"
    ))
    
    console.print("\n[bold]Available Examples:[/bold]\n")
    for key, example in EXAMPLES.items():
        if example["name"] == "Custom Task":
            console.print(f"  [yellow]{key}.[/yellow] {example['name']}")
        else:
            console.print(f"  [cyan]{key}.[/cyan] {example['name']}")
    
    console.print("\n  [red]Q.[/red] Quit\n")

def run_example(example_key: str):
    if example_key not in EXAMPLES:
        console.print("[red]Invalid selection![/red]")
        return
    
    example = EXAMPLES[example_key]
    
    if example["task"] is None:
        console.print("\n[yellow]Enter your custom task (press Enter twice when done):[/yellow]")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        task = "\n".join(lines[:-1])
    else:
        task = example["task"]
    
    console.print(f"\n[bold green]Running: {example['name']}[/bold green]\n")
    
    try:
        system = MultiAgentSystem()
        result = system.run_complex_task(task)
        
        console.print("\n" + "="*80 + "\n")
        console.print(Panel(
            "[bold green]✓ Analysis Complete[/bold green]",
            style="bold green"
        ))
        
        console.print(f"\n[cyan]Final output length: {len(result)} characters[/cyan]")
        console.print(f"[cyan]Check logs/ directory for detailed request/response logs[/cyan]\n")
        
        return result
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        import traceback
        traceback.print_exc()
        return None

def main():
    while True:
        display_menu()
        
        choice = input("Select an example (1-5, Q to quit): ").strip().upper()
        
        if choice == "Q":
            console.print("\n[yellow]Goodbye![/yellow]\n")
            break
        
        if choice in EXAMPLES:
            run_example(choice)
            
            console.print("\n[yellow]Press Enter to continue...[/yellow]")
            input()
        else:
            console.print("[red]Invalid selection! Please try again.[/red]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user. Goodbye![/yellow]\n")
