#!/usr/bin/env python3
import os
import anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class AICodeAssistant:
    def __init__(self):
        api_key = os.getenv('_ANTHROPIC_API_KEY')
        base_url = os.getenv('_ANTHROPIC_BASE_URL')
        self.model_name = os.getenv('_MODEL_NAME', 'claude-3-5-sonnet-20241022')
        
        if not api_key:
            raise ValueError("_ANTHROPIC_API_KEY environment variable is not set")
        
        self.client = anthropic.Anthropic(
            api_key=api_key,
            base_url=base_url if base_url else None
        )
        
        console.print(f"[green]✓ AI Assistant initialized with model: {self.model_name}[/green]")
        if base_url:
            console.print(f"[blue]Using custom base URL: {base_url}[/blue]")
    
    def _extract_text_from_message(self, message) -> str:
        for block in message.content:
            if hasattr(block, 'text'):
                return block.text
        return str(message.content)
    
    def analyze_code(self, code: str, language: str = "python") -> str:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task(description="Analyzing code...", total=None)
            
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze this {language} code and provide:
1. A brief overview of what the code does
2. Code quality assessment (1-10)
3. Potential bugs or issues
4. Performance improvements
5. Best practice recommendations

Code:
```{language}
{code}
```"""
                    }
                ]
            )
        
        return self._extract_text_from_message(message)
    
    def generate_documentation(self, code: str, language: str = "python") -> str:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task(description="Generating documentation...", total=None)
            
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Generate comprehensive documentation for this {language} code including:
1. Function/class descriptions
2. Parameter explanations
3. Return value descriptions
4. Usage examples

Code:
```{language}
{code}
```"""
                    }
                ]
            )
        
        return self._extract_text_from_message(message)
    
    def suggest_improvements(self, code: str, language: str = "python") -> str:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task(description="Suggesting improvements...", total=None)
            
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Suggest improvements for this {language} code and provide:
1. Refactored version of the code
2. Explanation of changes made
3. Benefits of the improvements

Code:
```{language}
{code}
```"""
                    }
                ]
            )
        
        return self._extract_text_from_message(message)
    
    def creative_challenge(self, prompt: str) -> str:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task(description="Thinking creatively...", total=None)
            
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        
        return self._extract_text_from_message(message)


def main():
    console.print(Panel.fit(
        "[bold cyan]AI-Powered Code Assistant[/bold cyan]\n"
        "Using Anthropic's LLM for code analysis and improvements",
        border_style="cyan"
    ))
    
    try:
        assistant = AICodeAssistant()
        
        sample_code = """
def calculate_fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

result = calculate_fibonacci(10)
print(result)
"""
        
        console.print("\n[bold yellow]Sample Code to Analyze:[/bold yellow]")
        console.print(Panel(sample_code, title="fibonacci.py", border_style="yellow"))
        
        console.print("\n[bold magenta]1. Code Analysis[/bold magenta]")
        analysis = assistant.analyze_code(sample_code, "python")
        console.print(Panel(Markdown(analysis), title="Analysis", border_style="magenta"))
        
        console.print("\n[bold green]2. Documentation Generation[/bold green]")
        docs = assistant.generate_documentation(sample_code, "python")
        console.print(Panel(Markdown(docs), title="Documentation", border_style="green"))
        
        console.print("\n[bold blue]3. Code Improvements[/bold blue]")
        improvements = assistant.suggest_improvements(sample_code, "python")
        console.print(Panel(Markdown(improvements), title="Suggested Improvements", border_style="blue"))
        
        console.print("\n[bold cyan]4. Creative Challenge: Write a Haiku about Programming[/bold cyan]")
        haiku = assistant.creative_challenge(
            "Write a beautiful haiku about the joy of programming and creating software. "
            "Make it inspiring and poetic."
        )
        console.print(Panel(Markdown(haiku), title="AI Poetry", border_style="cyan"))
        
        console.print("\n[bold green]✓ All tests completed successfully![/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        raise


if __name__ == "__main__":
    main()
