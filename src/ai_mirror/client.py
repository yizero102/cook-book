import anthropic
from typing import Optional, Dict, Any, List, AsyncIterator
from config.settings import Settings
from .conversation import Conversation, Message
from .tools import ToolRegistry
import json


class AIMirrorClient:
    def __init__(self, settings: Optional[Settings] = None, tool_registry: Optional[ToolRegistry] = None):
        self.settings = settings or Settings()
        self.tool_registry = tool_registry or ToolRegistry()
        
        is_valid, error_msg = self.settings.validate()
        if not is_valid:
            raise ValueError(f"Invalid settings: {error_msg}")
        
        self.client = anthropic.Anthropic(
            api_key=self.settings.anthropic_api_key,
            base_url=self.settings.anthropic_base_url
        )
        self.conversation = Conversation()
    
    def verify_connection(self) -> tuple[bool, Optional[str]]:
        try:
            response = self.client.messages.create(
                model=self.settings.model_name,
                max_tokens=100,
                messages=[{"role": "user", "content": "Hello, can you hear me?"}]
            )
            
            if response and response.content:
                return True, "Connection successful"
            return False, "No response from API"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        self.conversation.add_message("user", user_message)
        
        request_params = {
            "model": self.settings.model_name,
            "max_tokens": self.settings.max_tokens,
            "temperature": self.settings.temperature,
            "messages": self.conversation.get_messages_for_api()
        }
        
        if system_prompt:
            request_params["system"] = system_prompt
        elif self.conversation.get_system_message():
            request_params["system"] = self.conversation.get_system_message()
        
        if self.tool_registry.has_tools():
            request_params["tools"] = self.tool_registry.to_anthropic_format()
        
        try:
            response = self.client.messages.create(**request_params)
            
            if response.stop_reason == "tool_use":
                return self._handle_tool_use(response)
            
            assistant_message = self._extract_text_content(response)
            self.conversation.add_message("assistant", assistant_message)
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error during chat: {str(e)}"
            return error_msg
    
    async def chat_async(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        return self.chat(user_message, system_prompt)
    
    def chat_stream(self, user_message: str, system_prompt: Optional[str] = None) -> AsyncIterator[str]:
        self.conversation.add_message("user", user_message)
        
        request_params = {
            "model": self.settings.model_name,
            "max_tokens": self.settings.max_tokens,
            "temperature": self.settings.temperature,
            "messages": self.conversation.get_messages_for_api()
        }
        
        if system_prompt:
            request_params["system"] = system_prompt
        elif self.conversation.get_system_message():
            request_params["system"] = self.conversation.get_system_message()
        
        try:
            with self.client.messages.stream(**request_params) as stream:
                full_response = ""
                for text in stream.text_stream:
                    full_response += text
                    yield text
                
                self.conversation.add_message("assistant", full_response)
                
        except Exception as e:
            yield f"Error during streaming: {str(e)}"
    
    def _extract_text_content(self, response) -> str:
        if hasattr(response, 'content') and response.content:
            text_blocks = [block.text for block in response.content if hasattr(block, 'text')]
            return ''.join(text_blocks) if text_blocks else str(response.content)
        return ""
    
    def _handle_tool_use(self, response) -> str:
        tool_results = []
        
        for block in response.content:
            if hasattr(block, 'type') and block.type == 'tool_use':
                tool = self.tool_registry.get(block.name)
                if tool and tool.handler:
                    try:
                        result = tool.handler(**block.input)
                        tool_results.append(f"Tool '{block.name}' result: {result}")
                    except Exception as e:
                        tool_results.append(f"Tool '{block.name}' error: {str(e)}")
                else:
                    tool_results.append(f"Tool '{block.name}' not found or has no handler")
        
        return "\n".join(tool_results) if tool_results else "Tool execution completed"
    
    def set_system_prompt(self, prompt: str) -> None:
        self.conversation.add_message("system", prompt)
    
    def clear_conversation(self) -> None:
        self.conversation.clear()
    
    def get_conversation_history(self) -> Dict[str, Any]:
        return self.conversation.to_dict()
    
    def get_settings(self) -> Settings:
        return self.settings
