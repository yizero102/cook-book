# API Reference

Complete API documentation for the AI Assistant Replica.

## Table of Contents

1. [Assistant Class](#assistant-class)
2. [Tools](#tools)
3. [Data Types](#data-types)
4. [Error Handling](#error-handling)

## Assistant Class

### `Assistant(api_key=None, base_url=None, model_name=None, project_path="/home/engine/project", memory_file="assistant_memory.json")`

Main class for interacting with the AI Assistant.

**Parameters:**
- `api_key` (str, optional): Anthropic API key. Defaults to `_ANTHROPIC_API_KEY` environment variable.
- `base_url` (str, optional): API base URL. Defaults to `_ANTHROPIC_BASE_URL` environment variable.
- `model_name` (str, optional): Model name. Defaults to `_MODEL_NAME` environment variable.
- `project_path` (str): Path to project directory. Default: "/home/engine/project"
- `memory_file` (str): Filename for memory storage. Default: "assistant_memory.json"

**Raises:**
- `ValueError`: If API key is not provided and not found in environment

**Example:**
```python
from assistant_replica import Assistant

assistant = Assistant()
# or with explicit parameters
assistant = Assistant(
    api_key="your-key",
    base_url="https://api.example.com",
    model_name="model-name"
)
```

### Methods

#### `use_tool(tool_name: str, **kwargs) -> Dict[str, Any]`

Execute a tool with given parameters.

**Parameters:**
- `tool_name` (str): Name of the tool to execute
- `**kwargs`: Tool-specific parameters

**Returns:**
- `Dict[str, Any]`: Result dictionary with `success`, and tool-specific data

**Example:**
```python
result = assistant.use_tool(
    "ReadFile",
    filePath="/path/to/file.txt"
)
if result["success"]:
    print(result["content"])
```

#### `execute_simple_task(task: str) -> str`

Execute a simple task using the LLM.

**Parameters:**
- `task` (str): Task description or question

**Returns:**
- `str`: Assistant's response

**Example:**
```python
response = assistant.execute_simple_task(
    "Explain what this function does"
)
print(response)
```

#### `process_task(task_description: str, max_iterations: int = 10) -> Dict[str, Any]`

Process a complex multi-step task.

**Parameters:**
- `task_description` (str): Detailed task description
- `max_iterations` (int): Maximum number of LLM calls. Default: 10

**Returns:**
- `Dict[str, Any]`: Dictionary with:
  - `success` (bool): Whether task completed successfully
  - `message` (str): Status message
  - `iterations` (int): Number of iterations used
  - `tool_results` (list): Results from tool executions

**Example:**
```python
result = assistant.process_task(
    "Create a Python file with a hello world function",
    max_iterations=5
)
```

#### `update_memory(key: str, value: Any)`

Update persistent memory.

**Parameters:**
- `key` (str): Memory key
- `value` (Any): Value to store (must be JSON-serializable)

**Example:**
```python
assistant.update_memory("project_type", "web_app")
assistant.update_memory("test_command", "pytest")
```

#### `get_memory(key: str = None) -> Any`

Retrieve memory value.

**Parameters:**
- `key` (str, optional): Memory key. If None, returns entire memory dict.

**Returns:**
- `Any`: Stored value or None if key doesn't exist

**Example:**
```python
project_type = assistant.get_memory("project_type")
all_memory = assistant.get_memory()
```

## Tools

### ReadFileTool

Read file contents.

**Tool Name:** `ReadFile`

**Parameters:**
- `filePath` (str, required): Absolute path to file
- `offset` (int, optional): Line number to start reading. Default: 0
- `limit` (int, optional): Number of lines to read. Default: None (all lines)

**Returns:**
```python
{
    "success": True,
    "content": "file contents...",
    "path": "/path/to/file"
}
```

**Example:**
```python
# Read entire file
result = assistant.use_tool("ReadFile", filePath="/path/to/file.txt")

# Read lines 10-20
result = assistant.use_tool(
    "ReadFile",
    filePath="/path/to/file.txt",
    offset=10,
    limit=10
)
```

### WriteFileTool

Create or overwrite a file.

**Tool Name:** `WriteFile`

**Parameters:**
- `filePath` (str, required): Absolute path to file
- `content` (str, required): Content to write
- `addNewline` (bool, optional): Add newline at end. Default: True

**Returns:**
```python
{
    "success": True,
    "path": "/path/to/file"
}
```

**Example:**
```python
result = assistant.use_tool(
    "WriteFile",
    filePath="/path/to/file.py",
    content="#!/usr/bin/env python3\nprint('Hello')\n"
)
```

### EditFileTool

Edit file by replacing text.

**Tool Name:** `EditFile`

**Parameters:**
- `filePath` (str, required): Absolute path to file
- `oldString` (str, required): Text to replace (must be unique)
- `newString` (str, required): Replacement text

**Returns:**
```python
{
    "success": True,
    "path": "/path/to/file"
}
```

**Error Cases:**
- `oldString` not found: `success: False, error: "oldString not found"`
- Multiple matches: `success: False, error: "oldString appears N times"`

**Example:**
```python
result = assistant.use_tool(
    "EditFile",
    filePath="/path/to/file.py",
    oldString="def hello():\n    pass",
    newString="def hello():\n    print('Hello, World!')"
)
```

### TerminalTool

Execute shell commands.

**Tool Name:** `TerminalTool`

**Parameters:**
- `input` (str, required): Command to execute
- `resetTerminal` (bool, optional): Reset terminal state. Default: False

**Returns:**
```python
{
    "success": True,
    "stdout": "command output",
    "stderr": "error output",
    "returncode": 0,
    "command": "executed command"
}
```

**Example:**
```python
result = assistant.use_tool(
    "TerminalTool",
    input="ls -la"
)
print(result["stdout"])
```

### LsToolTool

List directory contents.

**Tool Name:** `LsTool`

**Parameters:**
- `path` (str, required): Absolute path to directory
- `limit` (int, optional): Maximum entries to return. Default: 50
- `offset` (int, optional): Number of entries to skip. Default: 0

**Returns:**
```python
{
    "success": True,
    "path": "/path/to/dir",
    "entries": ["file1", "file2", ...],
    "total": 10,
    "showing": 10
}
```

**Example:**
```python
result = assistant.use_tool("LsTool", path="/home/engine/project")
for entry in result["entries"]:
    print(entry)
```

### GlobToolTool

Find files by glob pattern.

**Tool Name:** `GlobTool`

**Parameters:**
- `pattern` (str, required): Glob pattern (e.g., "*.py", "**/*.txt")
- `path` (str, optional): Base path to search. Default: "/home/engine/project"

**Returns:**
```python
{
    "success": True,
    "pattern": "*.py",
    "matches": ["/path/to/file1.py", "/path/to/file2.py"],
    "count": 2
}
```

**Example:**
```python
# Find all Python files
result = assistant.use_tool("GlobTool", pattern="**/*.py")

# Find files in specific directory
result = assistant.use_tool(
    "GlobTool",
    pattern="*.json",
    path="/home/engine/project/config"
)
```

### GrepToolTool

Search file contents using regex.

**Tool Name:** `GrepTool`

**Parameters:**
- `pattern` (str, required): Regex pattern to search
- `path` (str, optional): Base path to search. Default: "/home/engine/project"
- `include` (str, optional): File pattern to include (e.g., "*.py")

**Returns:**
```python
{
    "success": True,
    "pattern": "def ",
    "matches": ["file.py:10:def hello():", ...],
    "count": 5
}
```

**Example:**
```python
# Find all function definitions
result = assistant.use_tool(
    "GrepTool",
    pattern="def ",
    include="*.py"
)

# Search for specific text
result = assistant.use_tool(
    "GrepTool",
    pattern="TODO",
    path="/home/engine/project/src"
)
```

## Data Types

### Tool Result

Standard structure for tool results:

```python
{
    "success": bool,      # Whether operation succeeded
    "error": str,         # Error message (if success=False)
    # Tool-specific fields...
}
```

### Memory Structure

```python
{
    "codebase_info": {
        "language": str,
        "framework": str,
        # ...
    },
    "preferences": {
        "indent_style": str,
        "indent_size": int,
        # ...
    },
    "important_commands": [str, ...]
}
```

## Error Handling

All tools follow a consistent error handling pattern:

### Success Response
```python
{
    "success": True,
    # ... tool-specific data
}
```

### Error Response
```python
{
    "success": False,
    "error": "Error description",
    # ... optional context
}
```

### Common Errors

**FileNotFoundError:**
```python
{
    "success": False,
    "error": "[Errno 2] No such file or directory: '/path/to/file'"
}
```

**PermissionError:**
```python
{
    "success": False,
    "error": "[Errno 13] Permission denied: '/path/to/file'"
}
```

**Timeout:**
```python
{
    "success": False,
    "error": "Command timeout (30s)"
}
```

## Best Practices

### 1. Always Check Success

```python
result = assistant.use_tool("ReadFile", filePath=path)
if result["success"]:
    process(result["content"])
else:
    handle_error(result["error"])
```

### 2. Use Absolute Paths

```python
# Good
assistant.use_tool("ReadFile", filePath="/home/engine/project/file.txt")

# Bad
assistant.use_tool("ReadFile", filePath="./file.txt")
```

### 3. Include Context for Edits

```python
# Good - unique context
assistant.use_tool(
    "EditFile",
    filePath=path,
    oldString="def hello():\n    print('old')\n    return True",
    newString="def hello():\n    print('new')\n    return True"
)

# Bad - might match multiple times
assistant.use_tool(
    "EditFile",
    filePath=path,
    oldString="print('old')",
    newString="print('new')"
)
```

### 4. Handle Timeouts

```python
result = assistant.use_tool("TerminalTool", input="long_running_command")
if not result["success"] and "timeout" in result.get("error", "").lower():
    # Handle timeout
    pass
```

### 5. Use Memory for Consistency

```python
# Store project conventions
assistant.update_memory("indent_size", 4)
assistant.update_memory("quote_style", "double")

# Retrieve when needed
indent_size = assistant.get_memory("indent_size")
```

## Thread Safety

**Warning:** The current implementation is not thread-safe. Do not share an `Assistant` instance across threads.

For concurrent operations, create separate instances:

```python
# Thread 1
assistant1 = Assistant()
assistant1.use_tool(...)

# Thread 2
assistant2 = Assistant()
assistant2.use_tool(...)
```

## Rate Limiting

LLM API calls may be rate-limited. The assistant does not currently implement automatic retry logic. Handle rate limit errors manually:

```python
import time

def call_with_retry(assistant, task, max_retries=3):
    for i in range(max_retries):
        try:
            return assistant.execute_simple_task(task)
        except Exception as e:
            if "rate limit" in str(e).lower() and i < max_retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
            else:
                raise
```

---

For more information, see:
- [Architecture Documentation](ARCHITECTURE.md)
- [Usage Guide](USAGE_GUIDE.md)
- [System Messages](SYSTEM_MESSAGES.md)
