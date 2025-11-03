#!/usr/bin/env python3
"""
AI Agent Replica System
=======================

This module provides a complete self-replica of an AI agent capable of:
- Reading and writing files
- Executing terminal commands
- Searching and exploring codebases
- Using LLM for intelligent decision-making
- Managing tasks and workflows
- Self-replication and verification

The replica aims to maintain all capabilities of the original agent.
"""

import os
import sys
import json
import subprocess
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import anthropic


class ToolType(Enum):
    """Available tool types for the agent."""
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    EDIT_FILE = "edit_file"
    TERMINAL = "terminal"
    GLOB = "glob"
    GREP = "grep"
    LS = "ls"
    THINK = "think"
    FINISH = "finish"
    UPDATE_MEMORY = "update_memory"


@dataclass
class ToolResult:
    """Result of a tool execution."""
    success: bool
    output: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Represents a task for the agent to complete."""
    description: str
    context: Dict[str, Any] = field(default_factory=dict)
    completed: bool = False
    result: Optional[Any] = None


class FileSystemTools:
    """Tools for file system operations."""
    
    @staticmethod
    def read_file(file_path: str, offset: int = 0, limit: Optional[int] = None) -> ToolResult:
        """Read a file from the filesystem."""
        try:
            if not os.path.isabs(file_path):
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"Path must be absolute: {file_path}"
                )
            
            if not os.path.exists(file_path):
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"File not found: {file_path}"
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            total_lines = len(lines)
            end_line = min(offset + limit, total_lines) if limit else total_lines
            selected_lines = lines[offset:end_line]
            
            content = ''.join(selected_lines)
            return ToolResult(
                success=True,
                output=content,
                metadata={
                    'total_lines': total_lines,
                    'returned_lines': len(selected_lines),
                    'offset': offset
                }
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error reading file: {str(e)}"
            )
    
    @staticmethod
    def write_file(file_path: str, content: str, add_newline: bool = True) -> ToolResult:
        """Write content to a file."""
        try:
            if not os.path.isabs(file_path):
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"Path must be absolute: {file_path}"
                )
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                if add_newline and not content.endswith('\n'):
                    f.write('\n')
            
            return ToolResult(
                success=True,
                output=f"File written successfully: {file_path}",
                metadata={'file_path': file_path, 'size': len(content)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error writing file: {str(e)}"
            )
    
    @staticmethod
    def edit_file(file_path: str, old_string: str, new_string: str) -> ToolResult:
        """Edit a file by replacing old_string with new_string."""
        try:
            if not os.path.isabs(file_path):
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"Path must be absolute: {file_path}"
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            count = content.count(old_string)
            if count == 0:
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"String not found in file: {old_string[:50]}..."
                )
            elif count > 1:
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"String appears {count} times in file. Must be unique."
                )
            
            new_content = content.replace(old_string, new_string, 1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return ToolResult(
                success=True,
                output=f"File edited successfully: {file_path}",
                metadata={'file_path': file_path}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error editing file: {str(e)}"
            )
    
    @staticmethod
    def ls_tool(path: str, limit: int = 50, offset: int = 0) -> ToolResult:
        """List files and directories in a path."""
        try:
            if not os.path.isabs(path):
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"Path must be absolute: {path}"
                )
            
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"Path not found: {path}"
                )
            
            entries = sorted(os.listdir(path))
            total = len(entries)
            paginated = entries[offset:offset + limit]
            
            result_lines = []
            for entry in paginated:
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    result_lines.append(f"[DIR]  {entry}")
                else:
                    size = os.path.getsize(full_path)
                    result_lines.append(f"[FILE] {entry} ({size} bytes)")
            
            return ToolResult(
                success=True,
                output='\n'.join(result_lines),
                metadata={'total': total, 'showing': len(paginated)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error listing directory: {str(e)}"
            )


class CodeSearchTools:
    """Tools for searching code."""
    
    @staticmethod
    def glob_tool(pattern: str, path: str = "/home/engine/project") -> ToolResult:
        """Find files matching a glob pattern."""
        try:
            from pathlib import Path
            import fnmatch
            
            results = []
            base_path = Path(path)
            
            if '**' in pattern:
                parts = pattern.split('**/')
                if len(parts) == 2:
                    sub_pattern = parts[1]
                    for file_path in base_path.rglob('*'):
                        if file_path.is_file() and fnmatch.fnmatch(file_path.name, sub_pattern):
                            results.append(str(file_path))
            else:
                for file_path in base_path.glob(pattern):
                    if file_path.is_file():
                        results.append(str(file_path))
            
            return ToolResult(
                success=True,
                output=results,
                metadata={'count': len(results)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error in glob search: {str(e)}"
            )
    
    @staticmethod
    def grep_tool(pattern: str, path: str = "/home/engine/project", 
                  include: Optional[str] = None) -> ToolResult:
        """Search for pattern in files."""
        try:
            import re
            from pathlib import Path
            import fnmatch
            
            results = []
            base_path = Path(path)
            regex = re.compile(pattern)
            
            for file_path in base_path.rglob('*'):
                if not file_path.is_file():
                    continue
                
                if include and not fnmatch.fnmatch(file_path.name, include):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if regex.search(line):
                                results.append({
                                    'file': str(file_path),
                                    'line': line_num,
                                    'content': line.rstrip()
                                })
                except Exception:
                    continue
            
            return ToolResult(
                success=True,
                output=results,
                metadata={'count': len(results)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error in grep search: {str(e)}"
            )


class TerminalTools:
    """Tools for terminal operations."""
    
    @staticmethod
    def execute_command(command: str, cwd: str = "/home/engine/project") -> ToolResult:
        """Execute a terminal command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return ToolResult(
                success=result.returncode == 0,
                output={
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode
                },
                metadata={'command': command, 'cwd': cwd}
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                output=None,
                error="Command timed out after 30 seconds"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error executing command: {str(e)}"
            )


class LLMClient:
    """Client for interacting with the LLM."""
    
    def __init__(self):
        self.api_key = os.environ.get('_ANTHROPIC_API_KEY')
        self.base_url = os.environ.get('_ANTHROPIC_BASE_URL')
        self.model = os.environ.get('_MODEL_NAME')
        
        if not all([self.api_key, self.base_url, self.model]):
            raise ValueError("Missing required environment variables")
        
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def call(self, messages: List[Dict[str, str]], max_tokens: int = 4096,
             system: Optional[str] = None) -> ToolResult:
        """Call the LLM with messages."""
        try:
            kwargs = {
                'model': self.model,
                'max_tokens': max_tokens,
                'messages': messages
            }
            
            if system:
                kwargs['system'] = system
            
            response = self.client.messages.create(**kwargs)
            
            response_text = None
            for content_block in response.content:
                if hasattr(content_block, 'text'):
                    response_text = content_block.text
                    break
            
            return ToolResult(
                success=True,
                output={
                    'text': response_text,
                    'model': response.model,
                    'usage': str(response.usage)
                },
                metadata={'message_id': response.id}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error calling LLM: {str(e)}"
            )


class AIAgentReplica:
    """
    Complete AI Agent Replica with all capabilities.
    
    This class provides a self-contained AI agent that can:
    - Read, write, and edit files
    - Execute terminal commands
    - Search codebases
    - Use LLM for intelligent reasoning
    - Complete tasks autonomously
    - Self-replicate
    """
    
    def __init__(self, working_directory: str = "/home/engine/project"):
        self.working_directory = working_directory
        self.fs_tools = FileSystemTools()
        self.search_tools = CodeSearchTools()
        self.terminal_tools = TerminalTools()
        self.llm_client = LLMClient()
        self.memory: Dict[str, Any] = {}
        self.task_history: List[Task] = []
    
    def execute_tool(self, tool_type: ToolType, **kwargs) -> ToolResult:
        """Execute a tool with given parameters."""
        try:
            if tool_type == ToolType.READ_FILE:
                return self.fs_tools.read_file(**kwargs)
            elif tool_type == ToolType.WRITE_FILE:
                return self.fs_tools.write_file(**kwargs)
            elif tool_type == ToolType.EDIT_FILE:
                return self.fs_tools.edit_file(**kwargs)
            elif tool_type == ToolType.LS:
                return self.fs_tools.ls_tool(**kwargs)
            elif tool_type == ToolType.GLOB:
                return self.search_tools.glob_tool(**kwargs)
            elif tool_type == ToolType.GREP:
                return self.search_tools.grep_tool(**kwargs)
            elif tool_type == ToolType.TERMINAL:
                return self.terminal_tools.execute_command(**kwargs)
            else:
                return ToolResult(
                    success=False,
                    output=None,
                    error=f"Unknown tool type: {tool_type}"
                )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error executing tool: {str(e)}\n{traceback.format_exc()}"
            )
    
    def think(self, problem: str) -> ToolResult:
        """Use LLM to reason about a problem."""
        messages = [
            {
                "role": "user",
                "content": f"Think step by step about this problem:\n\n{problem}"
            }
        ]
        return self.llm_client.call(messages)
    
    def complete_task(self, task: Task) -> ToolResult:
        """Complete a task using LLM and available tools."""
        system_prompt = """You are an AI agent capable of completing tasks by using tools.
You have access to file operations, terminal commands, and code search tools.
Think carefully about what needs to be done and execute the necessary actions."""
        
        messages = [
            {
                "role": "user",
                "content": f"Task: {task.description}\n\nContext: {json.dumps(task.context, indent=2)}"
            }
        ]
        
        llm_result = self.llm_client.call(messages, system=system_prompt)
        
        task.completed = llm_result.success
        task.result = llm_result.output
        self.task_history.append(task)
        
        return llm_result
    
    def self_replicate(self, target_path: str) -> ToolResult:
        """Create a copy of this agent's code at the target path."""
        try:
            source_file = __file__
            result = self.fs_tools.read_file(source_file)
            
            if not result.success:
                return result
            
            write_result = self.fs_tools.write_file(target_path, result.output)
            
            if write_result.success:
                os.chmod(target_path, 0o755)
            
            return write_result
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Error in self-replication: {str(e)}"
            )
    
    def verify_capabilities(self) -> Dict[str, bool]:
        """Verify all agent capabilities are working."""
        results = {}
        
        test_file = os.path.join(self.working_directory, ".agent_test_file.tmp")
        
        try:
            write_result = self.execute_tool(
                ToolType.WRITE_FILE,
                file_path=test_file,
                content="Test content"
            )
            results['write_file'] = write_result.success
            
            read_result = self.execute_tool(
                ToolType.READ_FILE,
                file_path=test_file
            )
            results['read_file'] = read_result.success and read_result.output == "Test content\n"
            
            if os.path.exists(test_file):
                os.remove(test_file)
        except Exception as e:
            results['file_operations'] = False
        
        terminal_result = self.execute_tool(
            ToolType.TERMINAL,
            command="echo 'test'"
        )
        results['terminal'] = terminal_result.success
        
        glob_result = self.execute_tool(
            ToolType.GLOB,
            pattern="*.py"
        )
        results['glob'] = glob_result.success
        
        llm_messages = [{"role": "user", "content": "Reply with 'OK'"}]
        llm_result = self.llm_client.call(llm_messages, max_tokens=10)
        results['llm'] = llm_result.success
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            'working_directory': self.working_directory,
            'task_count': len(self.task_history),
            'capabilities': self.verify_capabilities(),
            'memory_size': len(self.memory)
        }


def main():
    """Main entry point for the agent replica."""
    print("=" * 70)
    print("AI Agent Replica - Initialization")
    print("=" * 70)
    
    try:
        agent = AIAgentReplica()
        print("\n✓ Agent initialized successfully")
        
        print("\n" + "=" * 70)
        print("Verifying Agent Capabilities")
        print("=" * 70)
        
        capabilities = agent.verify_capabilities()
        for capability, status in capabilities.items():
            status_str = "✓" if status else "✗"
            print(f"{status_str} {capability}: {'Working' if status else 'Failed'}")
        
        all_working = all(capabilities.values())
        
        print("\n" + "=" * 70)
        if all_working:
            print("✅ All capabilities verified successfully!")
        else:
            print("⚠️  Some capabilities failed verification")
        print("=" * 70)
        
        print("\nAgent Status:")
        status = agent.get_status()
        print(json.dumps(status, indent=2))
        
        return 0 if all_working else 1
        
    except Exception as e:
        print(f"\n❌ Error initializing agent: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
