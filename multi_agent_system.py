from typing import Dict, List, Any
from agents import (
    ResearchCoordinator, DataAnalystAgent, WriterAgent,
    CriticAgent, SynthesizerAgent, ResearcherAgent, BaseAgent
)
from llm_client import LLMClient
from llm_logger import LLMLogger
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
import time

console = Console()

class MultiAgentSystem:
    def __init__(self):
        self.logger = LLMLogger()
        self.llm_client = LLMClient(self.logger)
        
        self.agents: Dict[str, BaseAgent] = {
            "coordinator": ResearchCoordinator(self.llm_client),
            "researcher": ResearcherAgent(self.llm_client),
            "analyst": DataAnalystAgent(self.llm_client),
            "writer": WriterAgent(self.llm_client),
            "critic": CriticAgent(self.llm_client),
            "synthesizer": SynthesizerAgent(self.llm_client)
        }
        
        self.workspace: Dict[str, Any] = {}
        
    def run_complex_task(self, task_description: str) -> str:
        console.print(Panel(
            f"[bold magenta]Starting Multi-Agent System[/bold magenta]\n\n[yellow]Task:[/yellow] {task_description}",
            title="🤖 Multi-Agent Research System",
            border_style="magenta"
        ))
        
        console.print("\n[bold]Phase 1: Task Planning and Coordination[/bold]\n")
        coordination_prompt = f"""
Task: {task_description}

As the Research Coordinator, please:
1. Break down this task into specific research questions or subtasks
2. Identify what kind of analysis is needed
3. Outline the key areas that need to be explored
4. Create a structured plan for how different agents should contribute

Provide a clear, numbered list of subtasks and assignments.
"""
        
        coordination_plan = self.agents["coordinator"].process(coordination_prompt)
        self.workspace["coordination_plan"] = coordination_plan
        
        console.print("\n[bold]Phase 2: Deep Research[/bold]\n")
        research_prompt = f"""
Based on this coordination plan:
{coordination_plan}

Conduct comprehensive research on the main topic: {task_description}

Explore:
- Key concepts and definitions
- Historical context and evolution
- Current state and trends
- Different perspectives and approaches
- Important examples and case studies

Provide detailed, well-structured research findings.
"""
        
        research_findings = self.agents["researcher"].process(research_prompt)
        self.workspace["research_findings"] = research_findings
        
        console.print("\n[bold]Phase 3: Data Analysis[/bold]\n")
        analysis_prompt = f"""
Based on these research findings:
{research_findings}

Analyze the information to:
1. Extract key insights and patterns
2. Identify the most important points
3. Draw logical conclusions
4. Highlight interesting correlations or relationships
5. Provide data-driven recommendations

Present your analysis in a structured format with clear insights.
"""
        
        analysis_results = self.agents["analyst"].process(analysis_prompt)
        self.workspace["analysis_results"] = analysis_results
        
        console.print("\n[bold]Phase 4: Content Creation[/bold]\n")
        writing_prompt = f"""
Create a comprehensive, well-written report based on:

Research Findings:
{research_findings}

Analysis Results:
{analysis_results}

Write a clear, engaging, and informative piece that:
1. Has a strong introduction
2. Presents information logically
3. Incorporates key insights from the analysis
4. Is accessible to a general audience
5. Has a compelling conclusion

Make it professional and polished.
"""
        
        initial_draft = self.agents["writer"].process(writing_prompt)
        self.workspace["initial_draft"] = initial_draft
        
        console.print("\n[bold]Phase 5: Critical Review[/bold]\n")
        critique_prompt = f"""
Review this draft:
{initial_draft}

Provide a critical assessment:
1. What are the strengths?
2. What are the weaknesses or gaps?
3. Are there any logical flaws or unsupported claims?
4. What specific improvements should be made?
5. Rate the overall quality and suggest enhancements

Be thorough and constructive in your criticism.
"""
        
        critique = self.agents["critic"].process(critique_prompt)
        self.workspace["critique"] = critique
        
        console.print("\n[bold]Phase 6: Final Synthesis[/bold]\n")
        synthesis_prompt = f"""
Create the final comprehensive output by synthesizing:

Original Task: {task_description}

Research Findings:
{research_findings}

Analysis:
{analysis_results}

Initial Draft:
{initial_draft}

Critical Feedback:
{critique}

Produce a polished, complete final version that:
1. Incorporates all the best insights from research and analysis
2. Addresses the critique's suggestions
3. Is well-structured and flows naturally
4. Fully answers the original task
5. Is the highest quality possible

This is the final deliverable.
"""
        
        final_output = self.agents["synthesizer"].process(synthesis_prompt)
        self.workspace["final_output"] = final_output
        
        self._display_summary()
        
        return final_output
    
    def _display_summary(self):
        console.print("\n" + "="*80 + "\n")
        
        table = Table(title="Multi-Agent System Summary", show_header=True, header_style="bold magenta")
        table.add_column("Phase", style="cyan", width=20)
        table.add_column("Agent", style="yellow", width=20)
        table.add_column("Output Length", style="green", width=15)
        
        phases = [
            ("Planning", "coordinator", "coordination_plan"),
            ("Research", "researcher", "research_findings"),
            ("Analysis", "analyst", "analysis_results"),
            ("Writing", "writer", "initial_draft"),
            ("Critique", "critic", "critique"),
            ("Synthesis", "synthesizer", "final_output")
        ]
        
        for phase_name, agent_key, workspace_key in phases:
            output = self.workspace.get(workspace_key, "")
            length = f"{len(output)} chars"
            table.add_row(phase_name, self.agents[agent_key].name, length)
        
        console.print(table)
        console.print("\n")
    
    def get_final_output(self) -> str:
        return self.workspace.get("final_output", "No output generated")
