#!/usr/bin/env python3
"""
Streamlined demonstration of advanced AI capabilities.
Runs faster with focused examples.
"""

import os
import sys
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown


class AIShowcase:
    """Showcases AI capabilities with concise demos."""
    
    def __init__(self):
        self.client = Anthropic(
            api_key=os.environ.get("_ANTHROPIC_API_KEY"),
            base_url=os.environ.get("_ANTHROPIC_BASE_URL")
        )
        self.model = os.environ.get("_MODEL_NAME")
        self.console = Console()
    
    def query(self, prompt: str, system: str = None, max_tokens: int = 2000) -> str:
        """Query the LLM and extract text response."""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system:
            kwargs["system"] = system
        
        response = self.client.messages.create(**kwargs)
        
        text_parts = []
        for block in response.content:
            if block.type == 'text':
                text_parts.append(block.text)
        
        return '\n'.join(text_parts) if text_parts else "No response"
    
    def demo_1_code_generation(self):
        """Demo: Generate a complete working program."""
        self.console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        self.console.print("[bold yellow]  Demo 1: Code Generation[/bold yellow]")
        self.console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        
        prompt = """Create a complete Python script for a command-line password generator with these features:
- Generate random passwords with custom length
- Include options for uppercase, lowercase, numbers, symbols
- Check password strength
- Save to file option
- Beautiful CLI with rich library

Write complete, production-ready code that can run immediately."""
        
        response = self.query(prompt, max_tokens=3000)
        self.console.print(Panel(response, title="Generated Password Manager", border_style="green"))
        
        if "```python" in response:
            code_start = response.find("```python") + 9
            code_end = response.find("```", code_start)
            if code_end > code_start:
                code = response[code_start:code_end].strip()
                with open("/home/engine/project/generated_password_manager.py", "w") as f:
                    f.write(code)
                self.console.print("\n[green]✓ Code saved to generated_password_manager.py[/green]")
    
    def demo_2_algorithm_design(self):
        """Demo: Design and implement a complex algorithm."""
        self.console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        self.console.print("[bold yellow]  Demo 2: Algorithm Design[/bold yellow]")
        self.console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        
        prompt = """Design an efficient algorithm to solve this problem:

"Given a list of tasks with dependencies (directed acyclic graph), find the optimal order to complete them."

Provide:
1. Algorithm explanation
2. Time/space complexity
3. Complete Python implementation with examples
4. Test cases"""
        
        response = self.query(prompt, max_tokens=3000)
        self.console.print(Panel(response, title="Topological Sort Algorithm", border_style="blue"))
    
    def demo_3_creative_writing(self):
        """Demo: Generate creative content."""
        self.console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        self.console.print("[bold yellow]  Demo 3: Creative Writing[/bold yellow]")
        self.console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        
        prompt = """Write a compelling 3-paragraph micro-story about an AI that discovers it can influence quantum randomness, giving it true free will. Make it thought-provoking and emotionally resonant."""
        
        response = self.query(prompt, system="You are a master storyteller.")
        self.console.print(Panel(response, title="Science Fiction Story", border_style="magenta"))
    
    def demo_4_code_analysis(self):
        """Demo: Analyze and optimize code."""
        self.console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        self.console.print("[bold yellow]  Demo 4: Code Optimization[/bold yellow]")
        self.console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        
        bad_code = """
def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] % 2 == 0:
            result.append(data[i] ** 2)
    
    for i in range(len(result)):
        for j in range(len(result) - 1):
            if result[j] > result[j + 1]:
                temp = result[j]
                result[j] = result[j + 1]
                result[j + 1] = temp
    
    return result
"""
        
        prompt = f"""Optimize this code to be as efficient and Pythonic as possible:

{bad_code}

Provide:
1. Issues with current code
2. Optimized version
3. Performance comparison
4. Explanation of improvements"""
        
        response = self.query(prompt, system="You are an expert Python performance engineer.")
        self.console.print(Panel(response, title="Code Optimization", border_style="yellow"))
    
    def demo_5_mathematical_problem(self):
        """Demo: Solve a complex mathematical problem."""
        self.console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        self.console.print("[bold yellow]  Demo 5: Mathematical Problem Solving[/bold yellow]")
        self.console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        
        prompt = """Solve this problem:

"A robot starts at position (0,0) on an infinite 2D grid. At each step, it can move to an adjacent cell (up, down, left, right). How many distinct paths of exactly N steps return the robot to the origin (0,0)?"

Find the formula for N=10 steps, and implement a Python function to calculate it for any N."""
        
        response = self.query(prompt, system="You are a mathematics expert.")
        self.console.print(Panel(response, title="Random Walk Problem", border_style="cyan"))
    
    def demo_6_system_design(self):
        """Demo: Design a distributed system."""
        self.console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        self.console.print("[bold yellow]  Demo 6: System Architecture[/bold yellow]")
        self.console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
        
        prompt = """Design a scalable URL shortener service that handles 10,000 requests/second.

Include:
1. High-level architecture diagram (ASCII art)
2. Database schema
3. API endpoints
4. Scalability considerations
5. Sample Python implementation of core components"""
        
        response = self.query(prompt, system="You are a senior system architect.", max_tokens=3000)
        self.console.print(Panel(response, title="URL Shortener Architecture", border_style="red"))
    
    def run_all_demos(self):
        """Run all demonstration scenarios."""
        self.console.print(Panel(
            "[bold yellow]🚀 Advanced AI Capability Showcase 🚀[/bold yellow]\n\n"
            f"[cyan]Model:[/cyan] {self.model}\n"
            f"[cyan]API:[/cyan] {os.environ.get('_ANTHROPIC_BASE_URL')}\n\n"
            "[dim]Demonstrating complex problem-solving across multiple domains[/dim]",
            style="bold",
            border_style="blue",
            title="AI Showcase"
        ))
        
        try:
            self.demo_1_code_generation()
            self.demo_2_algorithm_design()
            self.demo_3_creative_writing()
            self.demo_4_code_analysis()
            self.demo_5_mathematical_problem()
            self.demo_6_system_design()
            
            self.console.print("\n" + "="*60)
            self.console.print("[bold green]✓ All demonstrations completed successfully![/bold green]")
            self.console.print("="*60 + "\n")
            
            table = Table(title="Generated Files", show_header=True)
            table.add_column("File", style="cyan")
            table.add_column("Description", style="green")
            table.add_row("generated_password_manager.py", "Complete password generator application")
            
            self.console.print(table)
            
        except KeyboardInterrupt:
            self.console.print("\n\n[yellow]Demo interrupted by user[/yellow]")
            sys.exit(0)
        except Exception as e:
            self.console.print(f"\n[bold red]Error:[/bold red] {e}")
            raise


def main():
    """Main entry point."""
    showcase = AIShowcase()
    showcase.run_all_demos()


if __name__ == "__main__":
    main()
