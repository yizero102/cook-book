# Usage Guide

A comprehensive guide to using the AI Assistant Replica effectively.

## Getting Started

### Installation

1. **Clone or download the project**
2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   export _ANTHROPIC_API_KEY="your-api-key"
   export _ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic"
   export _MODEL_NAME="MiniMax-M2"
   ```

5. **Verify installation:**
   ```bash
   python3 test_llm_connection.py
   python3 test_assistant.py
   ```

### Quick Start

```python
from assistant_replica import Assistant

# Initialize
assistant = Assistant()

# Simple question
response = assistant.execute_simple_task("What is Python?")
print(response)

# Create a file
assistant.use_tool(
    "WriteFile",
    filePath="/home/engine/project/hello.py",
    content="print('Hello, World!')"
)
```

## Common Use Cases

### 1. File Management

#### Creating Files

```python
# Python script
assistant.use_tool(
    "WriteFile",
    filePath="/home/engine/project/script.py",
    content='''#!/usr/bin/env python3
"""My script."""

def main():
    print("Hello!")

if __name__ == "__main__":
    main()
'''
)

# Configuration file
assistant.use_tool(
    "WriteFile",
    filePath="/home/engine/project/config.json",
    content='{\n    "setting": "value"\n}'
)
```

#### Reading Files

```python
# Read entire file
result = assistant.use_tool(
    "ReadFile",
    filePath="/home/engine/project/script.py"
)
print(result["content"])

# Read specific lines (100-200)
result = assistant.use_tool(
    "ReadFile",
    filePath="/home/engine/project/large_file.py",
    offset=100,
    limit=100
)
```

#### Editing Files

```python
# Make precise edits
result = assistant.use_tool(
    "EditFile",
    filePath="/home/engine/project/script.py",
    oldString='print("Hello!")',
    newString='print("Hello, World!")'
)

# Edit with context for uniqueness
assistant.use_tool(
    "EditFile",
    filePath="/home/engine/project/script.py",
    oldString='''def main():
    print("Hello!")''',
    newString='''def main():
    """Main entry point."""
    print("Hello, World!")'''
)
```

### 2. Code Analysis

#### Finding Files

```python
# Find all Python files
result = assistant.use_tool(
    "GlobTool",
    pattern="**/*.py"
)
print(f"Found {result['count']} Python files")

# Find test files
result = assistant.use_tool(
    "GlobTool",
    pattern="**/test_*.py"
)
```

#### Searching Code

```python
# Find function definitions
result = assistant.use_tool(
    "GrepTool",
    pattern="^def ",
    include="*.py"
)

# Find TODO comments
result = assistant.use_tool(
    "GrepTool",
    pattern="TODO",
    path="/home/engine/project"
)

# Find imports
result = assistant.use_tool(
    "GrepTool",
    pattern="^import |^from .* import",
    include="*.py"
)
```

#### Exploring Project Structure

```python
# List directory
result = assistant.use_tool(
    "LsTool",
    path="/home/engine/project"
)
for entry in result["entries"]:
    print(entry)

# List with pagination
result = assistant.use_tool(
    "LsTool",
    path="/home/engine/project",
    limit=10,
    offset=0
)
```

### 3. Running Commands

```python
# Run tests
result = assistant.use_tool(
    "TerminalTool",
    input="python3 -m pytest tests/"
)
print(result["stdout"])

# Check Python version
result = assistant.use_tool(
    "TerminalTool",
    input="python3 --version"
)

# Run linter
result = assistant.use_tool(
    "TerminalTool",
    input="flake8 ."
)

# Git operations
result = assistant.use_tool(
    "TerminalTool",
    input="git status"
)
```

### 4. Using LLM Intelligence

#### Code Review

```python
# Read file
result = assistant.use_tool(
    "ReadFile",
    filePath="/home/engine/project/mycode.py"
)

# Ask for review
if result["success"]:
    review = assistant.execute_simple_task(f"""
Review this Python code and suggest improvements:

{result['content']}

Provide specific, actionable feedback.
""")
    print(review)
```

#### Generating Code

```python
# Generate a function
code = assistant.execute_simple_task("""
Write a Python function that reads a JSON file and returns its contents
as a dictionary. Include error handling and type hints.
""")
print(code)
```

#### Documentation

```python
# Read code
result = assistant.use_tool("ReadFile", filePath="mymodule.py")

# Generate documentation
docs = assistant.execute_simple_task(f"""
Generate documentation for this Python module in markdown format:

{result['content']}
""")

# Save documentation
assistant.use_tool(
    "WriteFile",
    filePath="docs/mymodule.md",
    content=docs
)
```

### 5. Memory Management

```python
# Store project information
assistant.update_memory("project_type", "web_application")
assistant.update_memory("framework", "flask")
assistant.update_memory("test_command", "pytest")
assistant.update_memory("lint_command", "flake8")

# Retrieve information
framework = assistant.get_memory("framework")
test_cmd = assistant.get_memory("test_command")

# View all memory
all_memory = assistant.get_memory()
print(all_memory)
```

## Advanced Patterns

### Pattern 1: Safe File Editing

Always read before editing to ensure you understand the context:

```python
def safe_edit(assistant, filepath, old, new):
    """Safely edit a file with validation."""
    # 1. Read file
    result = assistant.use_tool("ReadFile", filePath=filepath)
    if not result["success"]:
        print(f"Error reading: {result['error']}")
        return False
    
    # 2. Verify old string exists
    if old not in result["content"]:
        print(f"String not found in file")
        return False
    
    # 3. Check uniqueness
    count = result["content"].count(old)
    if count > 1:
        print(f"String appears {count} times. Need more context.")
        return False
    
    # 4. Make edit
    result = assistant.use_tool(
        "EditFile",
        filePath=filepath,
        oldString=old,
        newString=new
    )
    
    return result["success"]
```

### Pattern 2: Backup Before Modify

```python
def edit_with_backup(assistant, filepath, old, new):
    """Edit file with automatic backup."""
    # Create backup
    result = assistant.use_tool("ReadFile", filePath=filepath)
    if not result["success"]:
        return False
    
    backup_path = f"{filepath}.backup"
    assistant.use_tool(
        "WriteFile",
        filePath=backup_path,
        content=result["content"]
    )
    
    # Make edit
    result = assistant.use_tool(
        "EditFile",
        filePath=filepath,
        oldString=old,
        newString=new
    )
    
    if not result["success"]:
        # Restore from backup
        backup = assistant.use_tool("ReadFile", filePath=backup_path)
        assistant.use_tool(
            "WriteFile",
            filePath=filepath,
            content=backup["content"]
        )
        return False
    
    return True
```

### Pattern 3: Multi-File Refactoring

```python
def rename_function(assistant, old_name, new_name):
    """Rename a function across all Python files."""
    # Find all Python files
    result = assistant.use_tool("GlobTool", pattern="**/*.py")
    if not result["success"]:
        return
    
    # Search for function usage
    grep_result = assistant.use_tool(
        "GrepTool",
        pattern=old_name,
        include="*.py"
    )
    
    # Process each file
    files_to_edit = set()
    for match in grep_result["matches"]:
        filepath = match.split(":")[0]
        files_to_edit.add(filepath)
    
    # Edit each file
    for filepath in files_to_edit:
        result = assistant.use_tool("ReadFile", filePath=filepath)
        if result["success"]:
            new_content = result["content"].replace(old_name, new_name)
            assistant.use_tool(
                "WriteFile",
                filePath=filepath,
                content=new_content
            )
```

### Pattern 4: Intelligent Code Generation

```python
def generate_test_file(assistant, source_file):
    """Generate test file for a source file."""
    # Read source
    result = assistant.use_tool("ReadFile", filePath=source_file)
    if not result["success"]:
        return
    
    # Ask LLM to generate tests
    tests = assistant.execute_simple_task(f"""
Generate comprehensive unit tests for this Python code:

{result['content']}

Use pytest and include:
- Test class with descriptive name
- Tests for normal cases
- Tests for edge cases
- Tests for error conditions
""")
    
    # Save test file
    test_file = source_file.replace(".py", "_test.py")
    assistant.use_tool(
        "WriteFile",
        filePath=test_file,
        content=tests
    )
    
    return test_file
```

### Pattern 5: Project Analysis

```python
def analyze_project(assistant, project_path):
    """Analyze project structure and statistics."""
    stats = {
        "total_files": 0,
        "python_files": 0,
        "test_files": 0,
        "functions": 0,
        "classes": 0,
    }
    
    # Count Python files
    result = assistant.use_tool("GlobTool", pattern="**/*.py", path=project_path)
    stats["python_files"] = result["count"]
    
    # Count test files
    result = assistant.use_tool("GlobTool", pattern="**/test_*.py", path=project_path)
    stats["test_files"] = result["count"]
    
    # Count functions
    result = assistant.use_tool("GrepTool", pattern="^def ", path=project_path)
    stats["functions"] = result["count"]
    
    # Count classes
    result = assistant.use_tool("GrepTool", pattern="^class ", path=project_path)
    stats["classes"] = result["count"]
    
    return stats
```

## Best Practices

### 1. Error Handling

Always check for success:

```python
result = assistant.use_tool("ReadFile", filePath=path)
if not result["success"]:
    print(f"Error: {result['error']}")
    # Handle error appropriately
else:
    # Process result
    process(result["content"])
```

### 2. Path Management

Always use absolute paths:

```python
import os

# Good
base_path = "/home/engine/project"
file_path = os.path.join(base_path, "myfile.py")
assistant.use_tool("ReadFile", filePath=file_path)

# Bad
assistant.use_tool("ReadFile", filePath="./myfile.py")
```

### 3. Context in Edits

Include sufficient context to ensure uniqueness:

```python
# Good - includes surrounding context
assistant.use_tool(
    "EditFile",
    filePath=path,
    oldString="""def calculate(a, b):
    return a + b

def main():""",
    newString="""def calculate(a, b):
    return a * b

def main():"""
)

# Bad - might match elsewhere
assistant.use_tool(
    "EditFile",
    filePath=path,
    oldString="return a + b",
    newString="return a * b"
)
```

### 4. Memory Usage

Use memory for persistent information:

```python
# Store once
assistant.update_memory("code_style", {
    "indent": 4,
    "quotes": "double",
    "line_length": 88
})

# Retrieve as needed
style = assistant.get_memory("code_style")
```

### 5. LLM Task Design

Write clear, specific prompts:

```python
# Good - specific and clear
response = assistant.execute_simple_task("""
Refactor this function to use list comprehension:

def square_evens(numbers):
    result = []
    for n in numbers:
        if n % 2 == 0:
            result.append(n ** 2)
    return result

Provide only the refactored function.
""")

# Bad - vague
response = assistant.execute_simple_task("Fix this code")
```

## Troubleshooting

### Issue: File Not Found

```python
# Check if file exists first
result = assistant.use_tool("LsTool", path=directory)
if filepath in result["entries"]:
    # File exists
    assistant.use_tool("ReadFile", filePath=filepath)
```

### Issue: Edit String Not Unique

```python
# Solution: Add more context
# Instead of:
old = "print(x)"

# Use:
old = """def my_function():
    print(x)
    return x"""
```

### Issue: Command Timeout

```python
# Run long commands in background
result = assistant.use_tool(
    "TerminalTool",
    input="long_command > output.log 2>&1 &"
)

# Check output later
result = assistant.use_tool("ReadFile", filePath="output.log")
```

### Issue: Rate Limiting

```python
import time

def with_retry(func, *args, max_retries=3, **kwargs):
    for i in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(2 ** i)
            else:
                raise
```

## Integration Examples

### With Version Control

```python
def commit_changes(assistant, message):
    """Commit changes with git."""
    # Check status
    status = assistant.use_tool("TerminalTool", input="git status")
    
    # Add files
    assistant.use_tool("TerminalTool", input="git add .")
    
    # Commit
    result = assistant.use_tool(
        "TerminalTool",
        input=f'git commit -m "{message}"'
    )
    
    return result["success"]
```

### With Testing

```python
def test_and_fix(assistant, test_file):
    """Run tests and attempt to fix failures."""
    # Run tests
    result = assistant.use_tool(
        "TerminalTool",
        input=f"python3 -m pytest {test_file} -v"
    )
    
    if result["returncode"] == 0:
        return True
    
    # Analyze failure
    failure_analysis = assistant.execute_simple_task(f"""
Analyze these test failures and suggest fixes:

{result['stdout']}
{result['stderr']}
""")
    
    print(failure_analysis)
    return False
```

### With CI/CD

```python
def pre_commit_check(assistant):
    """Run pre-commit checks."""
    checks = []
    
    # Lint
    result = assistant.use_tool("TerminalTool", input="flake8 .")
    checks.append(("Linting", result["returncode"] == 0))
    
    # Type check
    result = assistant.use_tool("TerminalTool", input="mypy .")
    checks.append(("Type checking", result["returncode"] == 0))
    
    # Tests
    result = assistant.use_tool("TerminalTool", input="pytest")
    checks.append(("Tests", result["returncode"] == 0))
    
    return all(passed for _, passed in checks)
```

## Performance Tips

1. **Batch file operations** when possible
2. **Use pagination** for large directories
3. **Cache LLM responses** for repeated queries
4. **Use specific patterns** in glob/grep to reduce search space
5. **Limit LLM context** to relevant information only

## Security Considerations

1. **Validate file paths** before operations
2. **Sanitize command inputs** to prevent injection
3. **Use timeouts** for all command executions
4. **Restrict to project directory** for file operations
5. **Never store sensitive data** in memory

---

For more information:
- [API Reference](API_REFERENCE.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [System Messages](SYSTEM_MESSAGES.md)
