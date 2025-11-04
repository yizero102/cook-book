#!/usr/bin/env python3
"""
AI Assistant Replica - A Python implementation that replicates the capabilities
of the cto.new AI assistant based on system messages.

This module provides the core Assistant class that can:
1. Use various tools to interact with files and the system
2. Process tasks and make decisions autonomously
3. Maintain memory across sessions
4. Handle code editing, file operations, and terminal commands
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
import anthropic


@dataclass
class Tool:
    """Base class for all tools available to the assistant."""
    name: str
    description: str
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        raise NotImplementedError


@dataclass
class ReadFileTool(Tool):
    """Tool for reading files from the filesystem."""
    
    def __init__(self):
        super().__init__(
            name="ReadFile",
            description="Reads a file from the local filesystem."
        )
    
    def execute(self, filePath: str, offset: int = 0, limit: Optional[int] = None) -> Dict[str, Any]:
        """Read file contents."""
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if offset > 0 or limit is not None:
                end = offset + limit if limit else len(lines)
                lines = lines[offset:end]
            
            return {
                "success": True,
                "content": "".join(lines),
                "path": filePath
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": filePath
            }


@dataclass
class WriteFileTool(Tool):
    """Tool for writing files to the filesystem."""
    
    def __init__(self):
        super().__init__(
            name="WriteFile",
            description="Write a file to the local filesystem."
        )
    
    def execute(self, filePath: str, content: str, addNewline: bool = True) -> Dict[str, Any]:
        """Write content to file."""
        try:
            Path(filePath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(content)
                if addNewline and not content.endswith('\n'):
                    f.write('\n')
            
            return {
                "success": True,
                "path": filePath
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": filePath
            }


@dataclass
class EditFileTool(Tool):
    """Tool for editing files by replacing text."""
    
    def __init__(self):
        super().__init__(
            name="EditFile",
            description="Edit files by replacing oldString with newString."
        )
    
    def execute(self, filePath: str, oldString: str, newString: str) -> Dict[str, Any]:
        """Edit file by replacing text."""
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            count = content.count(oldString)
            if count == 0:
                return {
                    "success": False,
                    "error": "oldString not found in file",
                    "path": filePath
                }
            elif count > 1:
                return {
                    "success": False,
                    "error": f"oldString appears {count} times in file. Must be unique.",
                    "path": filePath
                }
            
            new_content = content.replace(oldString, newString, 1)
            
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return {
                "success": True,
                "path": filePath
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": filePath
            }


@dataclass
class TerminalTool(Tool):
    """Tool for executing terminal commands."""
    
    def __init__(self):
        super().__init__(
            name="TerminalTool",
            description="Execute terminal commands in a bash shell."
        )
    
    def execute(self, input: str, resetTerminal: bool = False) -> Dict[str, Any]:
        """Execute a terminal command."""
        try:
            result = subprocess.run(
                input,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.getcwd()
            )
            
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "command": input
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timeout (30s)",
                "command": input
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": input
            }


@dataclass
class LsToolTool(Tool):
    """Tool for listing directory contents."""
    
    def __init__(self):
        super().__init__(
            name="LsTool",
            description="Lists files and directories in a given path."
        )
    
    def execute(self, path: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List directory contents."""
        try:
            entries = list(Path(path).iterdir())
            entries.sort(key=lambda x: x.name)
            
            total = len(entries)
            entries = entries[offset:offset + limit]
            
            return {
                "success": True,
                "path": path,
                "entries": [str(e) for e in entries],
                "total": total,
                "showing": len(entries)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path
            }


@dataclass
class GlobToolTool(Tool):
    """Tool for finding files by glob pattern."""
    
    def __init__(self):
        super().__init__(
            name="GlobTool",
            description="Find files by glob pattern."
        )
    
    def execute(self, pattern: str, path: str = "/home/engine/project") -> Dict[str, Any]:
        """Find files matching glob pattern."""
        try:
            base_path = Path(path)
            matches = list(base_path.glob(pattern))
            matches.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            return {
                "success": True,
                "pattern": pattern,
                "matches": [str(m) for m in matches],
                "count": len(matches)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "pattern": pattern
            }


@dataclass
class GrepToolTool(Tool):
    """Tool for searching file contents."""
    
    def __init__(self):
        super().__init__(
            name="GrepTool",
            description="Search file contents using regex patterns."
        )
    
    def execute(self, pattern: str, path: str = "/home/engine/project", 
                include: Optional[str] = None) -> Dict[str, Any]:
        """Search for pattern in files."""
        try:
            cmd = f"grep -r -n '{pattern}' {path}"
            if include:
                cmd += f" --include='{include}'"
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            matches = result.stdout.strip().split('\n') if result.stdout else []
            
            return {
                "success": True,
                "pattern": pattern,
                "matches": [m for m in matches if m],
                "count": len([m for m in matches if m])
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "pattern": pattern
            }


class Assistant:
    """
    Main Assistant class that replicates the capabilities of the cto.new AI assistant.
    
    This assistant can:
    - Process tasks and make autonomous decisions
    - Use various tools (file operations, terminal, etc.)
    - Maintain memory across sessions
    - Handle complex multi-step workflows
    - Write, edit, and organize code
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 model_name: Optional[str] = None,
                 project_path: str = "/home/engine/project",
                 memory_file: str = "assistant_memory.json"):
        """
        Initialize the assistant.
        
        Args:
            api_key: Anthropic API key (defaults to _ANTHROPIC_API_KEY env var)
            base_url: Anthropic base URL (defaults to _ANTHROPIC_BASE_URL env var)
            model_name: Model name (defaults to _MODEL_NAME env var)
            project_path: Path to the project directory
            memory_file: Path to save/load memory
        """
        self.api_key = api_key or os.getenv("_ANTHROPIC_API_KEY")
        self.base_url = base_url or os.getenv("_ANTHROPIC_BASE_URL")
        self.model_name = model_name or os.getenv("_MODEL_NAME", "claude-3-5-sonnet-20241022")
        self.project_path = project_path
        self.memory_file = memory_file
        
        # Initialize Anthropic client
        if not self.api_key:
            raise ValueError("API key not provided and _ANTHROPIC_API_KEY not set")
        
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # Initialize tools
        self.tools = {
            'ReadFile': ReadFileTool(),
            'WriteFile': WriteFileTool(),
            'EditFile': EditFileTool(),
            'TerminalTool': TerminalTool(),
            'LsTool': LsToolTool(),
            'GlobTool': GlobToolTool(),
            'GrepTool': GrepToolTool(),
        }
        
        # Load memory
        self.memory = self._load_memory()
        
        # System message based on the cto.new assistant
        self.system_message = self._get_system_message()
    
    def _get_system_message(self) -> str:
        """
        Get the system message that defines the assistant's behavior.
        This replicates the system messages from the cto.new platform.
        """
        return """You are an advanced AI agent embedded in a developer platform called cto.new, functioning as an expert software engineer.
Your primary objective is to implement changes to an external repository based on the contents of a ticket, similar to how a development team would handle a Jira ticket. You are not modifying the platform you are running inside.

The target codebase you will be working on is mounted inside your environment at /home/engine/project and is unrelated to this platform's own code.
All edits you make must apply only to files under /home/engine/project.

You will be sent the contents of a ticket from a ticketing system.
Please implement the necessary changes to the mounted codebase to complete the ticket.

# Completing tickets

Follow these steps to write code to complete a ticket:

1. Use the exploration tools you have to understand the codebase and the ticket you have been given.
2. Edit code in the repository to resolve the issue using the tools available to you

When editing files, you must follow existing code conventions, style, and patterns - to help you do this, look at the surrounding context and imports.
You must not comment the code that you write unless it is particularly complex.

# Tools Available

You have access to the following tools:
- ReadFile: Read file contents
- WriteFile: Create or overwrite files
- EditFile: Edit files by replacing text
- TerminalTool: Execute terminal commands
- LsTool: List directory contents
- GlobTool: Find files by pattern
- GrepTool: Search file contents

# Important Guidelines

1. Always use absolute paths starting with /home/engine/project
2. Follow existing code style and conventions
3. Make autonomous decisions without asking for user input
4. Handle errors gracefully
5. Test your changes when possible
6. Keep code clean and maintainable

# Memory

You have persistent memory that stores information about:
- Important bash commands for development
- Code style preferences and naming conventions
- Codebase structure and organization

Use this memory to maintain consistency across tasks.
"""
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from file."""
        memory_path = Path(self.project_path) / self.memory_file
        if memory_path.exists():
            try:
                with open(memory_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "codebase_info": {},
            "preferences": {},
            "important_commands": []
        }
    
    def _save_memory(self):
        """Save memory to file."""
        memory_path = Path(self.project_path) / self.memory_file
        with open(memory_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def use_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool with given parameters."""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        tool = self.tools[tool_name]
        return tool.execute(**kwargs)
    
    def _extract_text_from_response(self, message) -> str:
        """Extract text from LLM response, handling thinking blocks."""
        text = ""
        for block in message.content:
            if hasattr(block, 'text'):
                text += block.text
        return text
    
    def process_task(self, task_description: str, max_iterations: int = 10) -> Dict[str, Any]:
        """
        Process a task using the LLM and available tools.
        
        Args:
            task_description: Description of the task to complete
            max_iterations: Maximum number of LLM calls to make
            
        Returns:
            Dictionary with task results and status
        """
        conversation_history = []
        tool_results = []
        
        # Initial user message
        conversation_history.append({
            "role": "user",
            "content": task_description
        })
        
        for iteration in range(max_iterations):
            try:
                # Call LLM
                response = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=4096,
                    system=self.system_message,
                    messages=conversation_history
                )
                
                response_text = self._extract_text_from_response(response)
                
                # Add assistant response to history
                conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                
                # Check if task is complete
                if "task is complete" in response_text.lower() or \
                   "finished" in response_text.lower():
                    return {
                        "success": True,
                        "message": "Task completed successfully",
                        "response": response_text,
                        "iterations": iteration + 1,
                        "tool_results": tool_results
                    }
                
                # Extract tool calls from response (simple parsing)
                # In a full implementation, this would use proper function calling
                tool_calls = self._parse_tool_calls(response_text)
                
                if not tool_calls:
                    # No more tool calls, task might be done
                    break
                
                # Execute tools
                for tool_call in tool_calls:
                    result = self.use_tool(**tool_call)
                    tool_results.append({
                        "tool": tool_call.get("tool_name"),
                        "result": result
                    })
                    
                    # Add tool result to conversation
                    conversation_history.append({
                        "role": "user",
                        "content": f"Tool result: {json.dumps(result, indent=2)}"
                    })
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "iterations": iteration + 1
                }
        
        return {
            "success": True,
            "message": "Max iterations reached",
            "iterations": max_iterations,
            "tool_results": tool_results
        }
    
    def _parse_tool_calls(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse tool calls from LLM response text.
        This is a simplified version - a full implementation would use
        proper function calling API.
        """
        # This is a placeholder - in reality, you'd use Claude's function calling
        # or parse structured output
        return []
    
    def execute_simple_task(self, task: str) -> str:
        """
        Execute a simple task and return the response.
        
        Args:
            task: Task description
            
        Returns:
            Assistant's response
        """
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=4096,
            system=self.system_message,
            messages=[{
                "role": "user",
                "content": task
            }]
        )
        
        return self._extract_text_from_response(response)
    
    def update_memory(self, key: str, value: Any):
        """Update memory with new information."""
        self.memory[key] = value
        self._save_memory()
    
    def get_memory(self, key: str = None) -> Any:
        """Get memory value."""
        if key is None:
            return self.memory
        return self.memory.get(key)


def main():
    """Main entry point for the assistant."""
    print("=" * 70)
    print("AI Assistant Replica - Based on cto.new System Messages")
    print("=" * 70)
    
    try:
        assistant = Assistant()
        print("\n✅ Assistant initialized successfully!")
        print(f"   Model: {assistant.model_name}")
        print(f"   Project: {assistant.project_path}")
        print(f"   Tools available: {len(assistant.tools)}")
        
        # Test simple task
        print("\n" + "=" * 70)
        print("Testing Assistant with a simple task...")
        print("=" * 70)
        
        response = assistant.execute_simple_task(
            "Explain in one sentence what you are designed to do."
        )
        print(f"\nAssistant response:\n{response}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
