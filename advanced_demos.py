#!/usr/bin/env python3
"""
Advanced demonstrations showcasing hard computational problems.
"""

import os
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown


class AdvancedAIChallenge:
    """Showcases AI solving genuinely difficult problems."""
    
    def __init__(self):
        self.client = Anthropic(
            api_key=os.environ.get("_ANTHROPIC_API_KEY"),
            base_url=os.environ.get("_ANTHROPIC_BASE_URL")
        )
        self.model = os.environ.get("_MODEL_NAME", "claude-3-sonnet-20240229")
        self.console = Console()
    
    def query_llm(self, prompt: str, system: str = None) -> str:
        """Query the LLM with a prompt."""
        messages = [{"role": "user", "content": prompt}]
        kwargs = {"model": self.model, "max_tokens": 8192, "messages": messages}
        if system:
            kwargs["system"] = system
        
        response = self.client.messages.create(**kwargs)
        
        text_parts = []
        for block in response.content:
            if block.type == 'text':
                text_parts.append(block.text)
            elif block.type == 'thinking':
                pass
        
        return '\n'.join(text_parts) if text_parts else "No response generated (increase max_tokens)"
    
    def challenge_1_algorithm_design(self):
        """Challenge: Design an optimal algorithm for a complex problem."""
        self.console.print("\n[bold cyan]═══ Challenge 1: Advanced Algorithm Design ═══[/bold cyan]\n")
        
        prompt = """Design an efficient algorithm for the following problem:

Problem: "Optimal Meeting Room Scheduler with Conflicts and Priorities"
Given:
- N meetings with start time, end time, priority (1-10), and required room capacity
- M meeting rooms with different capacities
- Some meetings have conflicts (cannot be in adjacent time slots)
- Goal: Maximize the weighted sum of scheduled meeting priorities

Provide:
1. Problem analysis and complexity considerations
2. Algorithm design (with pseudocode)
3. Time and space complexity analysis
4. Complete Python implementation with comments
5. Test cases demonstrating correctness

Make it production-ready and highly optimized."""
        
        response = self.query_llm(prompt)
        self.console.print(Panel(response, title="Algorithm Design Solution", border_style="green"))
        return response
    
    def challenge_2_code_optimization(self):
        """Challenge: Optimize poorly written code."""
        self.console.print("\n[bold cyan]═══ Challenge 2: Extreme Code Optimization ═══[/bold cyan]\n")
        
        bad_code = """
def process_data(data):
    result = []
    for i in range(len(data)):
        temp = []
        for j in range(len(data[i])):
            if data[i][j] > 0:
                temp.append(data[i][j] ** 2)
            else:
                temp.append(data[i][j])
        result.append(sum(temp) / len(temp) if len(temp) > 0 else 0)
    
    final = []
    for i in range(len(result)):
        if result[i] > 100:
            final.append(result[i])
    
    for i in range(len(final)):
        for j in range(len(final) - 1 - i):
            if final[j] > final[j + 1]:
                temp = final[j]
                final[j] = final[j + 1]
                final[j + 1] = temp
    
    return final
"""
        
        prompt = f"""Optimize this Python code to be as efficient as possible:

{bad_code}

Provide:
1. Analysis of current inefficiencies
2. Big-O complexity of original code
3. Optimized version using modern Python features (list comprehensions, numpy if beneficial, etc.)
4. Big-O complexity of optimized code
5. Performance comparison explanation
6. Multiple optimization strategies (readability vs. raw performance)"""
        
        response = self.query_llm(prompt)
        self.console.print(Panel(response, title="Code Optimization Solution", border_style="yellow"))
        return response
    
    def challenge_3_architectural_design(self):
        """Challenge: Design a complex distributed system."""
        self.console.print("\n[bold cyan]═══ Challenge 3: Distributed System Architecture ═══[/bold cyan]\n")
        
        prompt = """Design a highly scalable, fault-tolerant real-time analytics platform with:

Requirements:
- Process 1 million events per second
- Real-time aggregations and complex queries
- Exactly-once processing guarantees
- Support for late-arriving data
- Multi-tenant with isolation
- Global distribution across 5+ regions
- Sub-second query latency
- 99.99% availability

Provide:
1. Complete architecture diagram (in text/ASCII art)
2. Technology stack with justifications
3. Data flow and processing pipeline
4. Fault tolerance and disaster recovery strategies
5. Scaling strategy
6. Sample implementation of critical components in Python
7. Monitoring and observability approach

Be specific and production-ready."""
        
        response = self.query_llm(prompt)
        self.console.print(Panel(response, title="System Architecture Solution", border_style="magenta"))
        return response
    
    def challenge_4_creative_problem(self):
        """Challenge: Solve a genuinely hard creative problem."""
        self.console.print("\n[bold cyan]═══ Challenge 4: Creative Technical Challenge ═══[/bold cyan]\n")
        
        prompt = """Create a Python program that generates procedural music based on mathematical concepts:

Requirements:
1. Use fractals, cellular automata, or other mathematical structures
2. Generate actual audio (WAV format)
3. Allow parameters: mood, complexity, length
4. Create harmonious, pleasant-sounding music (not random noise)
5. Implement at least 3 different generation algorithms
6. Include visualization of the mathematical patterns
7. Full working implementation with no external music libraries (use numpy and wave module)

Provide complete, runnable code that actually works."""
        
        response = self.query_llm(prompt)
        self.console.print(Panel(response, title="Creative Technical Solution", border_style="cyan"))
        
        # Extract and save the code if present
        if "```python" in response:
            code_start = response.find("```python") + 9
            code_end = response.find("```", code_start)
            if code_end > code_start:
                code = response[code_start:code_end].strip()
                with open("/home/engine/project/generated_music_generator.py", "w") as f:
                    f.write(code)
                self.console.print("\n[green]✓ Music generator code saved to generated_music_generator.py[/green]")
        
        return response
    
    def challenge_5_mathematical_proof(self):
        """Challenge: Construct a mathematical proof."""
        self.console.print("\n[bold cyan]═══ Challenge 5: Mathematical Proof Construction ═══[/bold cyan]\n")
        
        prompt = """Construct a rigorous mathematical proof for the following:

Theorem: "For any graph G with n vertices, if every vertex has degree at least n/2, 
then the graph contains a Hamiltonian cycle."

Provide:
1. Formal statement of the theorem
2. Required lemmas and prerequisites
3. Complete rigorous proof
4. Visual explanations and examples
5. Discussion of why the degree condition is necessary
6. Python code to verify the theorem with random graph generation
7. Counter-examples when the condition is not met

Make it pedagogically excellent and mathematically rigorous."""
        
        response = self.query_llm(prompt)
        self.console.print(Panel(response, title="Mathematical Proof", border_style="blue"))
        return response
    
    def run_all_challenges(self):
        """Run all advanced challenges."""
        self.console.print(Panel(
            "[bold yellow]🔥 Advanced AI Challenge Suite 🔥[/bold yellow]\n\n"
            "[cyan]Testing AI on genuinely difficult computational problems[/cyan]",
            style="bold",
            border_style="red"
        ))
        
        results = []
        
        results.append(("Algorithm Design", self.challenge_1_algorithm_design()))
        results.append(("Code Optimization", self.challenge_2_code_optimization()))
        results.append(("System Architecture", self.challenge_3_architectural_design()))
        results.append(("Creative Technical", self.challenge_4_creative_problem()))
        results.append(("Mathematical Proof", self.challenge_5_mathematical_proof()))
        
        self.console.print("\n[bold green]✓ All advanced challenges completed![/bold green]\n")
        return results


def main():
    """Main entry point."""
    challenge = AdvancedAIChallenge()
    challenge.run_all_challenges()


if __name__ == "__main__":
    main()
