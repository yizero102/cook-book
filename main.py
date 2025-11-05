#!/usr/bin/env python3

import sys
from multi_agent_system import MultiAgentSystem
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def main():
    console.print(Panel.fit(
        "[bold magenta]Multi-Agent AI Research System[/bold magenta]\n"
        "[cyan]A sophisticated system with 6 specialized AI agents[/cyan]\n"
        "[yellow]Working collaboratively on complex tasks[/yellow]",
        border_style="magenta"
    ))
    
    complex_task = """
Analyze the concept of 'Artificial General Intelligence (AGI)' from multiple dimensions:

1. Technical Perspective: What are the key technical challenges and approaches to achieving AGI? 
   What are the current limitations of narrow AI that prevent it from becoming AGI?

2. Philosophical Perspective: What does it mean for a machine to have 'general' intelligence? 
   How do we define and measure intelligence in a way that applies to both humans and machines?

3. Societal Impact: What are the potential benefits and risks of AGI for humanity? 
   How might AGI transform work, economy, and social structures?

4. Timeline and Feasibility: Based on current progress, what are expert opinions on when AGI 
   might be achieved? What are the key milestones we should watch for?

5. Ethical Considerations: What ethical frameworks should guide AGI development? 
   How do we ensure AGI aligns with human values?

Provide a comprehensive analysis that synthesizes these perspectives into actionable insights.
"""
    
    try:
        system = MultiAgentSystem()
        
        console.print("\n[bold green]Initializing multi-agent system...[/bold green]\n")
        
        final_result = system.run_complex_task(complex_task)
        
        console.print("\n" + "="*80 + "\n")
        console.print(Panel(
            "[bold green]FINAL OUTPUT FROM MULTI-AGENT SYSTEM[/bold green]",
            style="bold green"
        ))
        console.print("\n")
        
        md = Markdown(final_result)
        console.print(Panel(md, border_style="green", padding=(1, 2)))
        
        console.print("\n" + "="*80 + "\n")
        console.print("[bold green]✅ Multi-Agent System completed successfully![/bold green]")
        console.print(f"[cyan]Check the logs directory for detailed interaction logs[/cyan]")
        
        return 0
        
    except Exception as e:
        error_msg = str(e).replace('[', '\\[').replace(']', '\\]')
        console.print(f"[bold red]Error: {error_msg}[/bold red]")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
