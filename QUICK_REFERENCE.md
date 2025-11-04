# Quick Reference Guide

## 🚀 Getting Started (30 seconds)

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run assistant
python3 assistant_replica.py

# 3. Run tests (optional)
python3 run_all_verifications.py
```

## 📝 Basic Usage

### Initialize Assistant
```python
from assistant_replica import Assistant
assistant = Assistant()
```

### Create a File
```python
assistant.use_tool(
    "WriteFile",
    filePath="/home/engine/project/file.py",
    content="print('Hello!')"
)
```

### Read a File
```python
result = assistant.use_tool(
    "ReadFile",
    filePath="/home/engine/project/file.py"
)
print(result["content"])
```

### Edit a File
```python
assistant.use_tool(
    "EditFile",
    filePath="/home/engine/project/file.py",
    oldString="print('Hello!')",
    newString="print('Hello, World!')"
)
```

### Run a Command
```python
result = assistant.use_tool(
    "TerminalTool",
    input="python3 file.py"
)
print(result["stdout"])
```

### Find Files
```python
result = assistant.use_tool(
    "GlobTool",
    pattern="*.py"
)
print(f"Found {result['count']} files")
```

### Search Content
```python
result = assistant.use_tool(
    "GrepTool",
    pattern="def ",
    include="*.py"
)
print(f"Found {result['count']} matches")
```

### Ask a Question
```python
response = assistant.execute_simple_task(
    "What does this code do?"
)
print(response)
```

### Use Memory
```python
# Store
assistant.update_memory("key", "value")

# Retrieve
value = assistant.get_memory("key")
```

## 🔧 Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `ReadFile` | Read file contents | `ReadFile(filePath="/path/to/file")` |
| `WriteFile` | Create/overwrite file | `WriteFile(filePath="/path", content="...")` |
| `EditFile` | Replace text in file | `EditFile(filePath="/path", oldString="...", newString="...")` |
| `TerminalTool` | Run shell command | `TerminalTool(input="ls -la")` |
| `LsTool` | List directory | `LsTool(path="/path/to/dir")` |
| `GlobTool` | Find files by pattern | `GlobTool(pattern="*.py")` |
| `GrepTool` | Search file contents | `GrepTool(pattern="search term")` |

## ✅ Verification Commands

```bash
# Test LLM connection
python3 test_llm_connection.py

# Run unit tests
python3 test_assistant.py

# Run behavior tests
python3 test_behavior_comparison.py

# Run all verifications
python3 run_all_verifications.py

# Try examples
python3 examples/basic_usage.py
python3 examples/file_operations.py
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Main documentation |
| `PROJECT_SUMMARY.md` | Complete project summary |
| `docs/SYSTEM_MESSAGES.md` | System behavior definition |
| `docs/ARCHITECTURE.md` | Technical architecture |
| `docs/API_REFERENCE.md` | Complete API docs |
| `docs/USAGE_GUIDE.md` | Detailed usage guide |

## 🐛 Troubleshooting

### LLM Not Working
```bash
# Check environment variables
env | grep -E "(ANTHROPIC|MODEL)"

# Test connection
python3 test_llm_connection.py
```

### Import Errors
```bash
# Activate venv
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### Tests Failing
```bash
# Check you're in project directory
pwd  # Should be /home/engine/project

# Check Python version
python3 --version  # Should be 3.8+
```

## 💡 Common Patterns

### Safe File Edit
```python
# 1. Read first
result = assistant.use_tool("ReadFile", filePath=path)

# 2. Verify content
if old_text in result["content"]:
    # 3. Edit
    assistant.use_tool("EditFile", filePath=path, 
                      oldString=old_text, newString=new_text)
```

### Find and Replace
```python
# 1. Find files
files = assistant.use_tool("GlobTool", pattern="*.py")

# 2. Search content
matches = assistant.use_tool("GrepTool", pattern="old_name")

# 3. Edit each file
for match in matches["matches"]:
    filepath = match.split(":")[0]
    # Edit file...
```

### Run and Verify
```python
# 1. Make changes
assistant.use_tool("WriteFile", ...)

# 2. Run tests
result = assistant.use_tool("TerminalTool", input="pytest")

# 3. Check result
if result["returncode"] == 0:
    print("Tests passed!")
```

## 🎯 Environment Variables

Required environment variables:

```bash
export _ANTHROPIC_API_KEY="your-api-key"
export _ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic"
export _MODEL_NAME="MiniMax-M2"
```

## 📞 Getting Help

1. Check `README.md` for overview
2. See `docs/USAGE_GUIDE.md` for examples
3. Review `docs/API_REFERENCE.md` for details
4. Look at `examples/` for working code
5. Check `PROJECT_SUMMARY.md` for status

## 🎉 Quick Test

```bash
# One-line test
python3 -c "from assistant_replica import Assistant; a = Assistant(); print(a.execute_simple_task('What is 2+2?'))"
```

## 📊 Status Check

```bash
# Quick status
python3 run_all_verifications.py | grep -E "(PASSED|FAILED|Success Rate)"
```

---

**For complete documentation, see README.md and docs/**
