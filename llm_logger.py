import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

console = Console()

class LLMLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"llm_interactions_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("LLMLogger")
        self.interaction_count = 0
        
    def log_request(self, agent_name: str, request_data: Dict[str, Any]) -> int:
        self.interaction_count += 1
        interaction_id = self.interaction_count
        
        timestamp = datetime.now().isoformat()
        log_entry = {
            "interaction_id": interaction_id,
            "timestamp": timestamp,
            "type": "request",
            "agent": agent_name,
            "data": request_data
        }
        
        self.logger.info(f"REQUEST #{interaction_id} from {agent_name}")
        self.logger.info(json.dumps(log_entry, indent=2))
        
        console.print(Panel(
            Text.from_markup(f"[bold cyan]REQUEST #{interaction_id}[/bold cyan]\n[yellow]Agent:[/yellow] {agent_name}\n[yellow]Timestamp:[/yellow] {timestamp}"),
            title="🚀 LLM Request",
            border_style="cyan"
        ))
        
        if "messages" in request_data:
            for msg in request_data["messages"]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                if isinstance(content, list):
                    content = json.dumps(content, indent=2)
                
                console.print(f"[bold]{role.upper()}:[/bold]")
                console.print(Panel(content, border_style="dim"))
        
        return interaction_id
    
    def log_response(self, agent_name: str, interaction_id: int, response_data: Dict[str, Any]):
        timestamp = datetime.now().isoformat()
        log_entry = {
            "interaction_id": interaction_id,
            "timestamp": timestamp,
            "type": "response",
            "agent": agent_name,
            "data": response_data
        }
        
        self.logger.info(f"RESPONSE #{interaction_id} to {agent_name}")
        self.logger.info(json.dumps(log_entry, indent=2))
        
        console.print(Panel(
            Text.from_markup(f"[bold green]RESPONSE #{interaction_id}[/bold green]\n[yellow]Agent:[/yellow] {agent_name}\n[yellow]Timestamp:[/yellow] {timestamp}"),
            title="✅ LLM Response",
            border_style="green"
        ))
        
        if "content" in response_data:
            content = response_data["content"]
            if isinstance(content, list):
                for block in content:
                    if block.get("type") == "text":
                        console.print(Panel(block.get("text", ""), border_style="green"))
            else:
                console.print(Panel(str(content), border_style="green"))
        
        console.print("\n" + "="*80 + "\n")
    
    def log_error(self, agent_name: str, interaction_id: Optional[int], error: Exception):
        timestamp = datetime.now().isoformat()
        log_entry = {
            "interaction_id": interaction_id,
            "timestamp": timestamp,
            "type": "error",
            "agent": agent_name,
            "error": str(error),
            "error_type": type(error).__name__
        }
        
        self.logger.error(f"ERROR #{interaction_id} in {agent_name}")
        self.logger.error(json.dumps(log_entry, indent=2))
        
        console.print(Panel(
            Text.from_markup(f"[bold red]ERROR #{interaction_id}[/bold red]\n[yellow]Agent:[/yellow] {agent_name}\n[yellow]Error:[/yellow] {str(error)}"),
            title="❌ LLM Error",
            border_style="red"
        ))
