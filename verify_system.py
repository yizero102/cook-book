#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from multi_agent_system import MultiAgentSystem
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def verify_environment():
    console.print(Panel.fit("[bold cyan]Step 1: Verifying Environment Variables[/bold cyan]", border_style="cyan"))
    
    required_vars = {
        "_ANTHROPIC_API_KEY": os.environ.get("_ANTHROPIC_API_KEY"),
        "_ANTHROPIC_BASE_URL": os.environ.get("_ANTHROPIC_BASE_URL"),
        "_MODEL_NAME": os.environ.get("_MODEL_NAME")
    }
    
    table = Table(title="Environment Variables")
    table.add_column("Variable", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Value", style="yellow")
    
    all_set = True
    for var_name, var_value in required_vars.items():
        if var_value:
            display_value = var_value if var_name != "_ANTHROPIC_API_KEY" else f"{var_value[:10]}...{var_value[-10:]}"
            table.add_row(var_name, "✓ Set", display_value)
        else:
            table.add_row(var_name, "✗ Not Set", "N/A")
            all_set = False
    
    console.print(table)
    return all_set

def verify_logging():
    console.print("\n")
    console.print(Panel.fit("[bold cyan]Step 2: Verifying Logging Setup[/bold cyan]", border_style="cyan"))
    
    logs_dir = Path("logs")
    if logs_dir.exists():
        log_files = list(logs_dir.glob("*.log"))
        console.print(f"[green]✓ Logs directory exists with {len(log_files)} log file(s)[/green]")
        
        if log_files:
            latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
            size = latest_log.stat().st_size
            console.print(f"[green]  Latest log: {latest_log.name} ({size:,} bytes)[/green]")
        
        return True
    else:
        console.print("[yellow]⚠ Logs directory doesn't exist yet (will be created on first run)[/yellow]")
        return True

def verify_agents():
    console.print("\n")
    console.print(Panel.fit("[bold cyan]Step 3: Verifying Agent Initialization[/bold cyan]", border_style="cyan"))
    
    try:
        from llm_logger import LLMLogger
        from llm_client import LLMClient
        from agents import (ResearchCoordinator, DataAnalystAgent, WriterAgent,
                          CriticAgent, SynthesizerAgent, ResearcherAgent)
        
        logger = LLMLogger()
        llm_client = LLMClient(logger)
        
        agents = [
            ("Research Coordinator", ResearchCoordinator(llm_client)),
            ("Researcher", ResearcherAgent(llm_client)),
            ("Data Analyst", DataAnalystAgent(llm_client)),
            ("Writer", WriterAgent(llm_client)),
            ("Critic", CriticAgent(llm_client)),
            ("Synthesizer", SynthesizerAgent(llm_client))
        ]
        
        table = Table(title="Agent Initialization")
        table.add_column("Agent Name", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Role", style="yellow")
        
        for name, agent in agents:
            table.add_row(name, "✓ Initialized", agent.role.value)
        
        console.print(table)
        console.print(f"[green]✓ All {len(agents)} agents initialized successfully[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Failed to initialize agents: {e}[/red]")
        return False

def run_quick_test():
    console.print("\n")
    console.print(Panel.fit("[bold cyan]Step 4: Running Quick Test[/bold cyan]", border_style="cyan"))
    
    try:
        system = MultiAgentSystem()
        
        test_task = """
Provide a brief analysis of the benefits and challenges of multi-agent AI systems.
Focus on: 1) Collaboration advantages, 2) Complexity challenges, 3) Practical applications.
Keep the response concise (3-4 paragraphs).
"""
        
        console.print("[yellow]Running simplified test task...[/yellow]\n")
        
        result = system.run_complex_task(test_task)
        
        console.print("\n[green]✓ Test completed successfully![/green]")
        console.print(f"[green]  Final output length: {len(result)} characters[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Test failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False

def main():
    console.print("\n")
    console.print(Panel.fit(
        "[bold magenta]Multi-Agent System Verification[/bold magenta]\n"
        "[cyan]Verifying all components are working correctly[/cyan]",
        border_style="magenta"
    ))
    console.print("\n")
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        task1 = progress.add_task("[cyan]Checking environment...", total=None)
        result1 = verify_environment()
        results.append(("Environment", result1))
        progress.update(task1, completed=True)
        
        task2 = progress.add_task("[cyan]Checking logging...", total=None)
        result2 = verify_logging()
        results.append(("Logging", result2))
        progress.update(task2, completed=True)
        
        task3 = progress.add_task("[cyan]Checking agents...", total=None)
        result3 = verify_agents()
        results.append(("Agents", result3))
        progress.update(task3, completed=True)
    
    console.print("\n")
    console.print(Panel.fit("[bold cyan]Step 5: Verification Summary[/bold cyan]", border_style="cyan"))
    
    summary_table = Table(title="Verification Results")
    summary_table.add_column("Component", style="cyan")
    summary_table.add_column("Status", style="bold")
    
    all_passed = True
    for component, passed in results:
        status = "[green]✓ PASS[/green]" if passed else "[red]✗ FAIL[/red]"
        summary_table.add_row(component, status)
        if not passed:
            all_passed = False
    
    console.print(summary_table)
    
    if all_passed:
        console.print("\n[bold green]═══════════════════════════════════════════[/bold green]")
        console.print("[bold green]✓ ALL VERIFICATIONS PASSED[/bold green]")
        console.print("[bold green]═══════════════════════════════════════════[/bold green]\n")
        
        console.print("[yellow]To run the full system with a complex task:[/yellow]")
        console.print("[cyan]  python main.py[/cyan]\n")
        
        console.print("[yellow]To run this quick verification test:[/yellow]")
        console.print("[cyan]  python verify_system.py --test[/cyan]\n")
        
        if "--test" in sys.argv:
            run_quick_test()
        
        return 0
    else:
        console.print("\n[bold red]✗ SOME VERIFICATIONS FAILED[/bold red]\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
