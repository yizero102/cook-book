#!/usr/bin/env python3
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def verify_environment():
    console.print("\n[bold cyan]1. Environment Variables Check[/bold cyan]")
    
    checks = [
        ("_ANTHROPIC_API_KEY", os.getenv("_ANTHROPIC_API_KEY") is not None),
        ("_ANTHROPIC_BASE_URL", os.getenv("_ANTHROPIC_BASE_URL") is not None),
        ("_MODEL_NAME", os.getenv("_MODEL_NAME") is not None),
    ]
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Variable", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Value", style="yellow")
    
    all_set = True
    for var_name, is_set in checks:
        status = "✓ SET" if is_set else "✗ NOT SET"
        value = os.getenv(var_name, "N/A")
        if var_name == "_ANTHROPIC_API_KEY":
            value = "***HIDDEN***" if is_set else "N/A"
        table.add_row(var_name, status, value)
        if not is_set:
            all_set = False
    
    console.print(table)
    return all_set


def verify_imports():
    console.print("\n[bold cyan]2. Package Imports Check[/bold cyan]")
    
    imports = [
        ("anthropic", "Anthropic SDK"),
        ("rich", "Rich Terminal Library"),
        ("ai_assistant", "Custom AI Assistant Module"),
    ]
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Package", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Status", style="white")
    
    all_imported = True
    for module_name, description in imports:
        try:
            __import__(module_name)
            table.add_row(module_name, description, "✓ OK")
        except ImportError as e:
            table.add_row(module_name, description, f"✗ FAILED: {str(e)}")
            all_imported = False
    
    console.print(table)
    return all_imported


def verify_initialization():
    console.print("\n[bold cyan]3. AI Assistant Initialization Check[/bold cyan]")
    
    try:
        from ai_assistant import AICodeAssistant
        assistant = AICodeAssistant()
        console.print("[green]✓ AI Assistant initialized successfully![/green]")
        return True
    except Exception as e:
        console.print(f"[red]✗ Failed to initialize: {str(e)}[/red]")
        return False


def verify_functionality():
    console.print("\n[bold cyan]4. Basic Functionality Check[/bold cyan]")
    
    try:
        from ai_assistant import AICodeAssistant
        assistant = AICodeAssistant()
        
        test_code = "def hello(): return 'world'"
        
        console.print("[yellow]Testing creative_challenge...[/yellow]")
        result = assistant.creative_challenge("Say hello in 3 words.")
        
        if result and len(result) > 0:
            console.print(f"[green]✓ API call successful! Response: {result[:50]}...[/green]")
            return True
        else:
            console.print("[red]✗ API call returned empty response[/red]")
            return False
    except Exception as e:
        console.print(f"[red]✗ Functionality test failed: {str(e)}[/red]")
        return False


def main():
    console.print(Panel.fit(
        "[bold magenta]Final Verification Suite[/bold magenta]\n"
        "Comprehensive system check",
        border_style="magenta"
    ))
    
    results = []
    
    results.append(("Environment Variables", verify_environment()))
    results.append(("Package Imports", verify_imports()))
    results.append(("AI Initialization", verify_initialization()))
    results.append(("Basic Functionality", verify_functionality()))
    
    console.print("\n" + "=" * 60)
    console.print("\n[bold cyan]Final Results Summary[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Check", style="cyan")
    table.add_column("Result", style="white")
    
    all_passed = True
    for check_name, passed in results:
        status = "[green]✓ PASSED[/green]" if passed else "[red]✗ FAILED[/red]"
        table.add_row(check_name, status)
        if not passed:
            all_passed = False
    
    console.print(table)
    
    if all_passed:
        console.print("\n" + "=" * 60)
        console.print(Panel.fit(
            "[bold green]🎉 ALL CHECKS PASSED! 🎉[/bold green]\n"
            "System is fully operational and ready to use!",
            border_style="green"
        ))
        return 0
    else:
        console.print("\n" + "=" * 60)
        console.print(Panel.fit(
            "[bold red]⚠️  SOME CHECKS FAILED ⚠️[/bold red]\n"
            "Please review the errors above.",
            border_style="red"
        ))
        return 1


if __name__ == "__main__":
    sys.exit(main())
