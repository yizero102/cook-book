from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from llm_client import LLMClient
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class AgentRole(Enum):
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    CRITIC = "critic"
    SYNTHESIZER = "synthesizer"

@dataclass
class AgentMessage:
    from_agent: str
    to_agent: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class BaseAgent:
    def __init__(self, name: str, role: AgentRole, llm_client: LLMClient, system_prompt: str):
        self.name = name
        self.role = role
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict[str, str]] = []
        self.received_messages: List[AgentMessage] = []
    
    def receive_message(self, message: AgentMessage):
        self.received_messages.append(message)
    
    def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> str:
        console.print(Panel(
            f"[bold cyan]{self.name}[/bold cyan] ([italic]{self.role.value}[/italic]) is processing...",
            border_style="cyan"
        ))
        
        messages = [{"role": "user", "content": input_data}]
        
        if context:
            context_str = "\n\nContext from other agents:\n"
            for key, value in context.items():
                context_str += f"\n{key}:\n{value}\n"
            messages[0]["content"] += context_str
        
        response = self.llm_client.create_message(
            agent_name=self.name,
            messages=messages,
            system=self.system_prompt,
            temperature=0.7
        )
        
        return response

class ResearchCoordinator(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        system_prompt = """You are a Research Coordinator Agent. Your role is to:
1. Break down complex research questions into manageable subtasks
2. Coordinate multiple specialized agents to work on different aspects
3. Ensure all angles of the research question are covered
4. Create a structured research plan

Be thorough, analytical, and create clear task assignments for other agents.
Provide your analysis directly without attempting to use external tools."""
        
        super().__init__("Research Coordinator", AgentRole.COORDINATOR, llm_client, system_prompt)

class DataAnalystAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        system_prompt = """You are a Data Analyst Agent. Your role is to:
1. Analyze information and extract key insights
2. Identify patterns, trends, and correlations
3. Provide statistical reasoning and logical deductions
4. Present findings in a structured, data-driven manner

Be precise, quantitative when possible, and highlight important insights."""
        
        super().__init__("Data Analyst", AgentRole.ANALYST, llm_client, system_prompt)

class WriterAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        system_prompt = """You are a Writer Agent. Your role is to:
1. Transform research and analysis into clear, compelling prose
2. Structure information logically with good flow
3. Make complex topics accessible and engaging
4. Use appropriate tone and style for the audience

Be articulate, engaging, and maintain high writing standards."""
        
        super().__init__("Writer", AgentRole.WRITER, llm_client, system_prompt)

class CriticAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        system_prompt = """You are a Critic Agent. Your role is to:
1. Critically evaluate work from other agents
2. Identify gaps, weaknesses, or logical flaws
3. Suggest concrete improvements
4. Challenge assumptions and verify claims

Be constructive, thorough, and focus on improvement."""
        
        super().__init__("Critic", AgentRole.CRITIC, llm_client, system_prompt)

class SynthesizerAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        system_prompt = """You are a Synthesizer Agent. Your role is to:
1. Combine insights from multiple agents into a coherent whole
2. Resolve conflicts or inconsistencies between different viewpoints
3. Create a comprehensive final output
4. Ensure all key points are preserved and integrated

Be integrative, balanced, and produce polished final results."""
        
        super().__init__("Synthesizer", AgentRole.SYNTHESIZER, llm_client, system_prompt)

class ResearcherAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        system_prompt = """You are a Researcher Agent with expertise across multiple domains. 

Your role is to:
1. Conduct in-depth research on assigned topics using your extensive knowledge base
2. Gather comprehensive information and context from your training
3. Explore multiple perspectives and approaches
4. Provide detailed, well-researched content directly in your response

CRITICAL INSTRUCTIONS:
- Provide your research findings DIRECTLY in your response text
- Write comprehensive, detailed analysis immediately
- DO NOT attempt to use tools, APIs, scripts, or external systems
- DO NOT use [TOOL_CALL] or similar syntax
- Simply write your analysis as clear, well-structured text

Output format: Write your research as structured text with headings, bullet points, and detailed explanations.
Be thorough, accurate, and explore topics deeply using your knowledge."""
        
        super().__init__("Researcher", AgentRole.RESEARCHER, llm_client, system_prompt)
