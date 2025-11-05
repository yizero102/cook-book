"""
Base Agent Class
Provides the foundation for all specialized agents.
"""

from typing import Any, Dict, List, Optional

from llm_client import LLMClient


class BaseAgent:
    """Base class for all agents in the multi-agent system."""
    
    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        llm_client: LLMClient,
        temperature: float = 0.7
    ):
        """
        Initialize a base agent.
        
        Args:
            name: Unique name for the agent
            role: Role description
            system_prompt: System prompt defining the agent's behavior
            llm_client: LLM client for making API calls
            temperature: Temperature for LLM sampling
        """
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.llm_client = llm_client
        self.temperature = temperature
        self.memory: List[Dict[str, str]] = []
    
    def think(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a prompt and return a response.
        
        Args:
            prompt: The user prompt
            context: Optional conversation context
            metadata: Additional metadata for logging
            
        Returns:
            Dictionary with response content and reasoning
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if context:
            messages.extend(context)
        
        messages.append({"role": "user", "content": prompt})
        
        # Add metadata about the agent
        full_metadata = {
            "agent_name": self.name,
            "agent_role": self.role,
            **(metadata or {})
        }
        
        response = self.llm_client.chat(
            messages=messages,
            agent_name=self.name,
            metadata=full_metadata,
            temperature=self.temperature
        )
        
        # Store in memory
        self.memory.append({"role": "user", "content": prompt})
        self.memory.append({"role": "assistant", "content": response["content"]})
        
        return response
    
    def get_memory(self) -> List[Dict[str, str]]:
        """Get the agent's conversation memory."""
        return self.memory.copy()
    
    def clear_memory(self):
        """Clear the agent's conversation memory."""
        self.memory.clear()
    
    def __str__(self) -> str:
        return f"{self.name} ({self.role})"
