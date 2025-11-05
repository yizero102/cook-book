#!/usr/bin/env python3
"""
Interactive AI Assistant - A production-ready CLI assistant
Demonstrates real-world AI application capabilities.
"""

import os
import sys
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table

console = Console()


class InteractiveAssistant:
    """An interactive AI assistant with multiple capabilities."""
    
    def __init__(self):
        self.client = Anthropic(
            api_key=os.environ.get("_ANTHROPIC_API_KEY"),
            base_url=os.environ.get("_ANTHROPIC_BASE_URL")
        )
        self.model = os.environ.get("_MODEL_NAME")
        self.conversation_history = []
    
    def query(self, prompt: str, system: str = None, max_tokens: int = 2000) -> str:
        """Query the AI assistant."""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system:
            kwargs["system"] = system
        
        response = self.client.messages.create(**kwargs)
        text_parts = [block.text for block in response.content if block.type == 'text']
        return '\n'.join(text_parts)
    
    def show_menu(self):
        """Display the main menu."""
        console.clear()
        console.print(Panel(
            "[bold cyan]🤖 Interactive AI Assistant 🤖[/bold cyan]\n\n"
            "[yellow]Your intelligent companion for code, creativity, and problem-solving[/yellow]",
            border_style="blue"
        ))
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Option", style="bold cyan")
        table.add_column("Description", style="white")
        
        table.add_row("1", "💻 Generate Code")
        table.add_row("2", "🔍 Analyze Code")
        table.add_row("3", "✍️  Creative Writing")
        table.add_row("4", "🧮 Solve Math Problem")
        table.add_row("5", "💡 Ask Anything")
        table.add_row("6", "🏗️  Design System Architecture")
        table.add_row("7", "⚡ Optimize Code")
        table.add_row("8", "🔧 Debug Code")
        table.add_row("0", "👋 Exit")
        
        console.print(table)
        console.print()
    
    def generate_code(self):
        """Code generation mode."""
        console.print(Panel("[bold yellow]Code Generation Mode[/bold yellow]", border_style="yellow"))
        description = Prompt.ask("[cyan]Describe what you want to build[/cyan]")
        language = Prompt.ask("[cyan]Programming language[/cyan]", default="Python")
        
        console.print("\n[dim]Generating code...[/dim]\n")
        
        prompt = f"""Generate complete, production-ready {language} code for:

{description}

Requirements:
- Working, executable code
- Proper error handling
- Clear comments
- Best practices
- Ready to use immediately"""
        
        result = self.query(prompt, max_tokens=3000)
        console.print(Panel(result, title=f"Generated {language} Code", border_style="green"))
        
        if Confirm.ask("\n[yellow]Save to file?[/yellow]"):
            ext = {"Python": "py", "JavaScript": "js", "Java": "java", "C++": "cpp"}.get(language, "txt")
            filename = Prompt.ask("[cyan]Filename[/cyan]", default=f"generated_code.{ext}")
            
            # Extract code from markdown if present
            if "```" in result:
                start = result.find("```")
                end = result.rfind("```")
                if start < end:
                    code = result[start:end+3]
                    # Remove language markers
                    lines = code.split('\n')[1:-1]  # Skip first and last ``` lines
                    code = '\n'.join(lines)
                    result = code
            
            with open(filename, 'w') as f:
                f.write(result)
            console.print(f"[green]✓ Saved to {filename}[/green]")
    
    def analyze_code(self):
        """Code analysis mode."""
        console.print(Panel("[bold yellow]Code Analysis Mode[/bold yellow]", border_style="yellow"))
        console.print("[dim]Enter your code (type 'END' on a new line when done):[/dim]")
        
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        
        code = '\n'.join(lines)
        console.print("\n[dim]Analyzing code...[/dim]\n")
        
        prompt = f"""Analyze this code and provide:
1. Quality score (1-10)
2. Issues and bugs
3. Performance concerns
4. Security vulnerabilities
5. Recommended improvements
6. Refactored version

Code:
```
{code}
```"""
        
        result = self.query(prompt, system="You are an expert code reviewer.", max_tokens=3000)
        console.print(Panel(result, title="Code Analysis Results", border_style="blue"))
    
    def creative_writing(self):
        """Creative writing mode."""
        console.print(Panel("[bold yellow]Creative Writing Mode[/bold yellow]", border_style="yellow"))
        
        options = {
            "1": "Short Story",
            "2": "Poem",
            "3": "Essay",
            "4": "Technical Blog Post",
            "5": "Custom"
        }
        
        for key, value in options.items():
            console.print(f"  {key}. {value}")
        
        choice = Prompt.ask("\n[cyan]Choose type[/cyan]", choices=list(options.keys()))
        content_type = options[choice]
        
        if choice == "5":
            content_type = Prompt.ask("[cyan]Specify type[/cyan]")
        
        topic = Prompt.ask(f"[cyan]{content_type} about[/cyan]")
        
        console.print(f"\n[dim]Writing {content_type.lower()}...[/dim]\n")
        
        prompt = f"Write a compelling {content_type} about: {topic}"
        result = self.query(prompt, system="You are a master creative writer.", max_tokens=2500)
        
        console.print(Panel(result, title=f"{content_type}: {topic}", border_style="magenta"))
    
    def solve_math(self):
        """Math problem solving mode."""
        console.print(Panel("[bold yellow]Math Problem Solver[/bold yellow]", border_style="yellow"))
        problem = Prompt.ask("[cyan]Enter your math problem[/cyan]")
        
        console.print("\n[dim]Solving...[/dim]\n")
        
        prompt = f"""Solve this mathematical problem with detailed steps:

{problem}

Provide:
1. Problem understanding
2. Solution strategy
3. Step-by-step solution
4. Final answer
5. Verification"""
        
        result = self.query(prompt, system="You are a mathematics expert.", max_tokens=2500)
        console.print(Panel(result, title="Solution", border_style="cyan"))
    
    def ask_anything(self):
        """General Q&A mode."""
        console.print(Panel("[bold yellow]Ask Me Anything[/bold yellow]", border_style="yellow"))
        question = Prompt.ask("[cyan]Your question[/cyan]")
        
        console.print("\n[dim]Thinking...[/dim]\n")
        
        result = self.query(question, max_tokens=2500)
        console.print(Panel(result, title="Answer", border_style="green"))
    
    def design_system(self):
        """System architecture design mode."""
        console.print(Panel("[bold yellow]System Architecture Designer[/bold yellow]", border_style="yellow"))
        requirements = Prompt.ask("[cyan]Describe your system requirements[/cyan]")
        
        console.print("\n[dim]Designing architecture...[/dim]\n")
        
        prompt = f"""Design a system architecture for:

{requirements}

Provide:
1. High-level architecture diagram (ASCII art)
2. Component descriptions
3. Technology stack recommendations
4. Data flow
5. Scalability considerations
6. Security measures"""
        
        result = self.query(prompt, system="You are a senior system architect.", max_tokens=3000)
        console.print(Panel(result, title="System Architecture", border_style="red"))
    
    def optimize_code(self):
        """Code optimization mode."""
        console.print(Panel("[bold yellow]Code Optimizer[/bold yellow]", border_style="yellow"))
        console.print("[dim]Enter your code (type 'END' on a new line when done):[/dim]")
        
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        
        code = '\n'.join(lines)
        console.print("\n[dim]Optimizing code...[/dim]\n")
        
        prompt = f"""Optimize this code for maximum performance:

{code}

Provide:
1. Current performance analysis
2. Optimization opportunities
3. Optimized version
4. Performance improvement estimate
5. Trade-offs"""
        
        result = self.query(prompt, system="You are a performance optimization expert.", max_tokens=3000)
        console.print(Panel(result, title="Optimization Results", border_style="yellow"))
    
    def debug_code(self):
        """Code debugging mode."""
        console.print(Panel("[bold yellow]Code Debugger[/bold yellow]", border_style="yellow"))
        console.print("[dim]Enter your code (type 'END' on a new line when done):[/dim]")
        
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        
        code = '\n'.join(lines)
        error = Prompt.ask("[cyan]Describe the error/issue (or press Enter to skip)[/cyan]", default="")
        
        console.print("\n[dim]Debugging...[/dim]\n")
        
        prompt = f"""Debug this code:

Code:
```
{code}
```

{"Error: " + error if error else "Find and explain any issues."}

Provide:
1. Issues found
2. Root cause analysis
3. Fixed version
4. Explanation of fixes
5. Prevention tips"""
        
        result = self.query(prompt, system="You are an expert debugger.", max_tokens=3000)
        console.print(Panel(result, title="Debug Results", border_style="red"))
    
    def run(self):
        """Main application loop."""
        try:
            while True:
                self.show_menu()
                choice = Prompt.ask("[bold cyan]Choose an option[/bold cyan]", default="5")
                
                console.print()
                
                if choice == "0":
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                elif choice == "1":
                    self.generate_code()
                elif choice == "2":
                    self.analyze_code()
                elif choice == "3":
                    self.creative_writing()
                elif choice == "4":
                    self.solve_math()
                elif choice == "5":
                    self.ask_anything()
                elif choice == "6":
                    self.design_system()
                elif choice == "7":
                    self.optimize_code()
                elif choice == "8":
                    self.debug_code()
                else:
                    console.print("[red]Invalid choice. Please try again.[/red]")
                
                if choice != "0":
                    console.print()
                    Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Interrupted by user. Goodbye! 👋[/yellow]")
        except Exception as e:
            console.print(f"\n[bold red]Error: {e}[/bold red]")


def main():
    """Entry point."""
    assistant = InteractiveAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
