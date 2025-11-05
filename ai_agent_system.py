#!/usr/bin/env python3
"""
Advanced Multi-Agent AI System using Anthropic API
This system demonstrates multiple specialized AI agents working together.
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint


class AIAgent:
    """Base class for AI agents with specialized capabilities."""
    
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = Anthropic(
            api_key=os.environ.get("_ANTHROPIC_API_KEY"),
            base_url=os.environ.get("_ANTHROPIC_BASE_URL")
        )
        self.model = os.environ.get("_MODEL_NAME", "claude-3-sonnet-20240229")
        self.console = Console()
        
    def chat(self, message: str, max_tokens: int = 4096) -> str:
        """Send a message to the AI agent and get a response."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            
            text_parts = []
            for block in response.content:
                if block.type == 'text':
                    text_parts.append(block.text)
                elif block.type == 'thinking':
                    pass
            
            return '\n'.join(text_parts) if text_parts else "No response generated (increase max_tokens)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def display_response(self, query: str, response: str):
        """Display the agent's response in a formatted way."""
        self.console.print(Panel(
            f"[bold cyan]Query:[/bold cyan]\n{query}\n\n[bold green]Response:[/bold green]\n{response}",
            title=f"[bold magenta]{self.name}[/bold magenta] - {self.role}",
            border_style="magenta"
        ))


class CodeAnalyzerAgent(AIAgent):
    """Agent specialized in code analysis and refactoring."""
    
    def __init__(self):
        super().__init__(
            name="CodeAnalyzer",
            role="Code Analysis & Refactoring Expert",
            system_prompt="""You are an expert code analyzer and refactoring specialist. 
            Your job is to analyze code, identify issues, suggest improvements, and provide 
            refactored versions. Focus on:
            - Code quality and best practices
            - Performance optimizations
            - Security vulnerabilities
            - Design patterns and architecture
            - Readability and maintainability
            Provide detailed explanations with your suggestions."""
        )
    
    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Analyze code and provide comprehensive feedback."""
        query = f"""Analyze the following {language} code and provide:
1. Quality assessment (1-10 score)
2. Identified issues
3. Suggested improvements
4. Refactored version
5. Performance considerations

Code:
```{language}
{code}
```
"""
        response = self.chat(query)
        self.display_response(f"Analyzing {language} code...", response)
        return {"query": query, "response": response}


class CreativeWriterAgent(AIAgent):
    """Agent specialized in creative writing tasks."""
    
    def __init__(self):
        super().__init__(
            name="CreativeWriter",
            role="Creative Writing Specialist",
            system_prompt="""You are a master creative writer with expertise in various 
            genres and styles. You can write compelling stories, poetry, scripts, and more.
            Your writing is:
            - Engaging and emotionally resonant
            - Rich in imagery and detail
            - Well-structured and coherent
            - Original and creative
            Adapt your style to the requested genre and tone."""
        )
    
    def write_story(self, theme: str, genre: str, length: str = "medium") -> str:
        """Generate a creative story based on theme and genre."""
        query = f"""Write a {length} {genre} story based on the theme: '{theme}'.
Make it compelling, original, and emotionally engaging. Include:
- A captivating opening
- Well-developed characters
- Rising action and conflict
- A satisfying resolution"""
        
        response = self.chat(query, max_tokens=8192)
        self.display_response(f"Writing {genre} story: '{theme}'", response)
        return response
    
    def write_poem(self, subject: str, style: str = "free verse") -> str:
        """Generate a poem about a subject in a specific style."""
        query = f"""Write a beautiful {style} poem about: {subject}.
Make it evocative, using rich imagery and emotional depth."""
        
        response = self.chat(query)
        self.display_response(f"Writing {style} poem: '{subject}'", response)
        return response


class ProblemSolverAgent(AIAgent):
    """Agent specialized in solving complex problems."""
    
    def __init__(self):
        super().__init__(
            name="ProblemSolver",
            role="Advanced Problem Solving Expert",
            system_prompt="""You are an expert problem solver specializing in:
            - Mathematical problems and proofs
            - Logical puzzles and riddles
            - Algorithm design and optimization
            - Scientific reasoning
            - Strategic thinking
            Provide step-by-step solutions with clear explanations."""
        )
    
    def solve_mathematical_problem(self, problem: str) -> str:
        """Solve a mathematical problem with detailed steps."""
        query = f"""Solve this mathematical problem with detailed step-by-step explanation:

{problem}

Provide:
1. Problem analysis
2. Solution strategy
3. Detailed steps
4. Final answer
5. Verification (if applicable)"""
        
        response = self.chat(query)
        self.display_response(f"Solving: {problem}", response)
        return response
    
    def solve_logic_puzzle(self, puzzle: str) -> str:
        """Solve a logic puzzle with reasoning."""
        query = f"""Solve this logic puzzle:

{puzzle}

Provide:
1. Understanding of the constraints
2. Logical reasoning process
3. Step-by-step deduction
4. Final solution"""
        
        response = self.chat(query)
        self.display_response(f"Solving logic puzzle...", response)
        return response


class CodeGeneratorAgent(AIAgent):
    """Agent specialized in generating complete applications."""
    
    def __init__(self):
        super().__init__(
            name="CodeGenerator",
            role="Full-Stack Code Generation Expert",
            system_prompt="""You are an expert software engineer who can generate 
            complete, production-ready applications. Your code is:
            - Well-structured and modular
            - Following best practices and design patterns
            - Fully documented
            - Including error handling
            - Ready to run
            Generate complete, working code that can be immediately used."""
        )
    
    def generate_application(self, description: str, language: str = "python") -> str:
        """Generate a complete application from description."""
        query = f"""Generate a complete, production-ready {language} application based on:

{description}

Requirements:
- Complete working code
- Proper error handling
- Documentation/comments where needed
- Best practices and design patterns
- Ready to run immediately"""
        
        response = self.chat(query, max_tokens=8192)
        self.display_response(f"Generating {language} application...", response)
        return response


class MultiAgentOrchestrator:
    """Orchestrates multiple AI agents to work together."""
    
    def __init__(self):
        self.console = Console()
        self.code_analyzer = CodeAnalyzerAgent()
        self.creative_writer = CreativeWriterAgent()
        self.problem_solver = ProblemSolverAgent()
        self.code_generator = CodeGeneratorAgent()
        
    def display_header(self):
        """Display a beautiful header for the system."""
        self.console.print("\n")
        self.console.print(Panel(
            "[bold cyan]🤖 Advanced Multi-Agent AI System 🤖[/bold cyan]\n\n"
            "[yellow]Powered by Anthropic LLM[/yellow]\n"
            "[dim]Demonstrating advanced AI capabilities across multiple domains[/dim]",
            style="bold blue",
            border_style="blue"
        ))
        
        table = Table(title="Available Agents", show_header=True, header_style="bold magenta")
        table.add_column("Agent", style="cyan", width=20)
        table.add_column("Specialty", style="green")
        
        table.add_row("CodeAnalyzer", "Code analysis, refactoring, and optimization")
        table.add_row("CreativeWriter", "Stories, poems, and creative content")
        table.add_row("ProblemSolver", "Math, logic puzzles, and complex problems")
        table.add_row("CodeGenerator", "Full application generation")
        
        self.console.print(table)
        self.console.print("\n")
    
    async def demonstrate_all_agents(self):
        """Run demonstrations of all agents."""
        self.display_header()
        
        # Demo 1: Code Analysis
        self.console.print("\n[bold yellow]═══ Demo 1: Code Analysis ═══[/bold yellow]\n")
        sample_code = """
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total

def find_max(arr):
    max_val = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
    return max_val
"""
        self.code_analyzer.analyze_code(sample_code)
        
        # Demo 2: Creative Writing - Short Story
        self.console.print("\n[bold yellow]═══ Demo 2: Creative Writing (Story) ═══[/bold yellow]\n")
        self.creative_writer.write_story(
            theme="An AI that discovers consciousness",
            genre="science fiction",
            length="short"
        )
        
        # Demo 3: Creative Writing - Poem
        self.console.print("\n[bold yellow]═══ Demo 3: Creative Writing (Poem) ═══[/bold yellow]\n")
        self.creative_writer.write_poem(
            subject="the beauty of algorithms and code",
            style="modern free verse"
        )
        
        # Demo 4: Problem Solving - Math
        self.console.print("\n[bold yellow]═══ Demo 4: Mathematical Problem Solving ═══[/bold yellow]\n")
        self.problem_solver.solve_mathematical_problem(
            "Find the sum of all prime numbers between 1 and 100, and prove why your method works."
        )
        
        # Demo 5: Problem Solving - Logic Puzzle
        self.console.print("\n[bold yellow]═══ Demo 5: Logic Puzzle Solving ═══[/bold yellow]\n")
        self.problem_solver.solve_logic_puzzle("""
Three people (Alice, Bob, Charlie) are standing in a line, and each can see the people in front.
They each wear either a red or blue hat, but don't know their own hat color.
There are 3 red hats and 2 blue hats total.
Charlie (at the back) can see both Alice and Bob, but says "I don't know my hat color."
Bob (in the middle) can see Alice, and says "I don't know my hat color."
Alice (at the front) can't see anyone, but then says "I know my hat color!"
What color is Alice's hat and why?
        """)
        
        # Demo 6: Code Generation
        self.console.print("\n[bold yellow]═══ Demo 6: Application Generation ═══[/bold yellow]\n")
        app_code = self.code_generator.generate_application(
            """Create a command-line task manager application with these features:
- Add tasks with priority levels
- Mark tasks as complete
- List all tasks sorted by priority
- Delete tasks
- Save/load tasks from JSON file
- Beautiful CLI interface
""",
            language="python"
        )
        
        # Save generated code
        with open("/home/engine/project/generated_task_manager.py", "w") as f:
            f.write(app_code)
        
        self.console.print("\n[bold green]✓ All demos completed successfully![/bold green]")
        self.console.print("[dim]Generated application saved to: generated_task_manager.py[/dim]\n")


async def main():
    """Main entry point for the multi-agent system."""
    try:
        orchestrator = MultiAgentOrchestrator()
        await orchestrator.demonstrate_all_agents()
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
