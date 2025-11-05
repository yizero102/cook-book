"""
LLM Client Wrapper
Provides a unified interface for LLM calls with automatic logging.
"""

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from llm_logger import LLMLogger


class LLMClient:
    """Wrapper around OpenAI client with automatic logging."""
    
    def __init__(self, logger: Optional[LLMLogger] = None):
        """Initialize the LLM client."""
        self.base_url = os.environ.get('_OPENAI_BASE_URL', '')
        self.api_key = os.environ.get('_OPENAI_API_KEY', '')
        self.model_name = os.environ.get('_MODEL_NAME', 'gpt-4')
        
        if not self.base_url or not self.api_key:
            raise ValueError("Environment variables _OPENAI_BASE_URL and _OPENAI_API_KEY must be set")
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        self.logger = logger or LLMLogger()
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        agent_name: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
        with_reasoning: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send a chat completion request with logging.
        
        Args:
            messages: List of message dictionaries
            agent_name: Name of the agent making the request
            metadata: Additional metadata to log
            with_reasoning: Whether to request reasoning details
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary with 'content', 'reasoning', and 'request_id'
        """
        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        
        if with_reasoning:
            kwargs["extra_body"] = {"reasoning_split": True}
        
        # Make the API call
        response = self.client.chat.completions.create(**kwargs)
        
        # Log the request and response
        request_id = self.logger.log_request_response(
            agent_name=agent_name,
            messages=messages,
            response=response,
            metadata=metadata
        )
        
        # Extract and return the result
        choice = response.choices[0]
        message = choice.message
        
        reasoning = None
        if hasattr(message, 'reasoning_details') and message.reasoning_details:
            reasoning = message.reasoning_details[0].get('text', '')
        
        return {
            "content": message.content,
            "reasoning": reasoning,
            "request_id": request_id,
            "finish_reason": choice.finish_reason
        }
    
    def get_logger(self) -> LLMLogger:
        """Get the logger instance."""
        return self.logger
