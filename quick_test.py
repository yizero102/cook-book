#!/usr/bin/env python3

import sys
from multi_agent_system import MultiAgentSystem
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.print(Panel.fit(
        "[bold cyan]Quick Multi-Agent Test[/bold cyan]\n"
        "[yellow]Running a simplified task to verify the system[/yellow]",
        border_style="cyan"
    ))
    
    simple_task = """
Analyze the concept of 'Multi-Agent AI Systems' briefly:

1. What are multi-agent systems and how do they differ from single-agent systems?
2. What are the key benefits of using multiple specialized agents?
3. What are the main challenges in coordinating multiple agents?
4. Provide one real-world application example.

Keep your response concise and focused (500-1000 words total across all phases).
"""
    
    try:
        system = MultiAgentSystem()
        
        console.print("\n[bold green]Starting quick test...[/bold green]\n")
        
        result = system.run_complex_task(simple_task)
        
        console.print("\n" + "="*80 + "\n")
        console.print(Panel(
            "[bold green]QUICK TEST COMPLETED SUCCESSFULLY ✓[/bold green]",
            style="bold green"
        ))
        
        console.print(f"\n[cyan]Final output length: {len(result)} characters[/cyan]")
        console.print(f"[cyan]Output preview (first 500 chars):[/cyan]\n")
        console.print(Panel(result[:500] + "...", border_style="dim"))
        
        console.print("\n[yellow]Full logs available in logs/ directory[/yellow]\n")
        
        return 0
        
    except Exception as e:
        console.print(f"\n[bold red]Test failed: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
