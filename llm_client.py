import os
import re
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from llm_logger import LLMLogger

class LLMClient:
    def __init__(self, logger: LLMLogger):
        self.logger = logger
        
        base_url = os.environ.get("_ANTHROPIC_BASE_URL")
        api_key = os.environ.get("_ANTHROPIC_API_KEY")
        self.model_name = os.environ.get("_MODEL_NAME", "claude-3-5-sonnet-20241022")
        
        if not api_key:
            raise ValueError("_ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(
            api_key=api_key,
            base_url=base_url if base_url else None
        )
    
    def _clean_response(self, text: str) -> str:
        pattern = r'\[TOOL_CALL\].*?\[/TOOL_CALL\]'
        cleaned = re.sub(pattern, '', text, flags=re.DOTALL)
        cleaned = cleaned.strip()
        
        if not cleaned:
            return "I apologize, but I provided a tool response when I should have provided direct analysis. Please rephrase your request."
        
        return cleaned
    
    def create_message(
        self,
        agent_name: str,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        request_data = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if system:
            request_data["system"] = system
        
        interaction_id = self.logger.log_request(agent_name, request_data)
        
        try:
            response = self.client.messages.create(
                model=self.model_name,
                messages=messages,
                system=system,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            response_content = []
            text_response = ""
            
            for block in response.content:
                block_data = {"type": block.type}
                if hasattr(block, 'text'):
                    block_data["text"] = block.text
                    if not text_response:
                        text_response = block.text
                elif hasattr(block, 'thinking'):
                    block_data["thinking"] = block.thinking
                else:
                    block_data["content"] = str(block)
                response_content.append(block_data)
            
            if not text_response:
                for block in response.content:
                    if hasattr(block, 'text'):
                        text_response = block.text
                        break
            
            text_response = self._clean_response(text_response)
            
            response_data = {
                "id": response.id,
                "model": response.model,
                "role": response.role,
                "content": response_content,
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
            
            self.logger.log_response(agent_name, interaction_id, response_data)
            
            return text_response
            
        except Exception as e:
            self.logger.log_error(agent_name, interaction_id, e)
            raise
