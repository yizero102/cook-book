"""
LLM Request/Response Logger
Logs all LLM interactions with timestamps and reasoning details.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class LLMLogger:
    """Handles logging of LLM requests and responses."""
    
    def __init__(self, log_dir: str = "llm_logs"):
        """Initialize the logger with a directory for logs."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.request_count = 0
        
    def _get_log_filename(self, request_id: int) -> Path:
        """Generate a unique filename for each log entry."""
        return self.log_dir / f"{self.session_id}_request_{request_id:04d}.json"
    
    def log_request_response(
        self,
        agent_name: str,
        messages: List[Dict[str, str]],
        response: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Log a complete LLM request/response cycle.
        
        Args:
            agent_name: Name of the agent making the request
            messages: The messages sent to the LLM
            response: The response object from the LLM
            metadata: Additional metadata to log
            
        Returns:
            The request ID
        """
        self.request_count += 1
        request_id = self.request_count
        
        # Extract response details
        try:
            choice = response.choices[0]
            message = choice.message
            
            # Extract reasoning if available
            reasoning = None
            if hasattr(message, 'reasoning_details') and message.reasoning_details:
                reasoning = message.reasoning_details[0].get('text', '')
            
            response_content = message.content
            
            log_entry = {
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "agent_name": agent_name,
                "request": {
                    "messages": messages,
                    "model": getattr(response, 'model', 'unknown'),
                },
                "response": {
                    "content": response_content,
                    "reasoning": reasoning,
                    "finish_reason": choice.finish_reason,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens if hasattr(response, 'usage') else None,
                        "completion_tokens": response.usage.completion_tokens if hasattr(response, 'usage') else None,
                        "total_tokens": response.usage.total_tokens if hasattr(response, 'usage') else None,
                    }
                },
                "metadata": metadata or {}
            }
            
            # Write to file
            log_file = self._get_log_filename(request_id)
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_entry, f, indent=2, ensure_ascii=False)
            
            # Also append to summary log
            self._append_to_summary(log_entry)
            
            return request_id
            
        except Exception as e:
            # Log the error
            error_log = {
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "agent_name": agent_name,
                "error": str(e),
                "messages": messages
            }
            
            error_file = self.log_dir / f"{self.session_id}_error_{request_id:04d}.json"
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(error_log, f, indent=2, ensure_ascii=False)
            
            raise
    
    def _append_to_summary(self, log_entry: Dict[str, Any]):
        """Append a summary to the session summary file."""
        summary_file = self.log_dir / f"{self.session_id}_summary.jsonl"
        
        summary = {
            "request_id": log_entry["request_id"],
            "timestamp": log_entry["timestamp"],
            "agent_name": log_entry["agent_name"],
            "user_message": log_entry["request"]["messages"][-1]["content"] if log_entry["request"]["messages"] else "",
            "response_preview": log_entry["response"]["content"][:200] if log_entry["response"]["content"] else "",
            "has_reasoning": bool(log_entry["response"]["reasoning"]),
            "tokens": log_entry["response"]["usage"]["total_tokens"]
        }
        
        with open(summary_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(summary, ensure_ascii=False) + '\n')
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        return {
            "session_id": self.session_id,
            "total_requests": self.request_count,
            "log_directory": str(self.log_dir)
        }
