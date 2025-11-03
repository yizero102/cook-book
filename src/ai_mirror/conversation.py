from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content
        }


class Conversation(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def add_message(self, role: Literal["user", "assistant", "system"], content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        message = Message(role=role, content=content, metadata=metadata)
        self.messages.append(message)
    
    def get_messages_for_api(self) -> List[Dict[str, Any]]:
        return [msg.to_dict() for msg in self.messages if msg.role != "system"]
    
    def get_system_message(self) -> Optional[str]:
        system_messages = [msg.content for msg in self.messages if msg.role == "system"]
        return "\n".join(system_messages) if system_messages else None
    
    def clear(self) -> None:
        self.messages.clear()
    
    def get_last_message(self) -> Optional[Message]:
        return self.messages[-1] if self.messages else None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "metadata": msg.metadata
                }
                for msg in self.messages
            ],
            "metadata": self.metadata
        }
