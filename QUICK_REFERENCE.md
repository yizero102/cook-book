# Quick Reference Guide

## 🚀 Quick Start (30 seconds)

```bash
# Activate environment
source venv/bin/activate

# Run master validation (verifies everything)
python run_all_validations.py
```

**Expected**: `🎉 ALL VALIDATIONS PASSED! 🎉`

---

## 📋 Common Commands

### Verification Commands

```bash
# Verify LLM connectivity (5 seconds)
python verify_llm.py

# Test agent capabilities (2 seconds)  
python ai_agent_replica.py

# Run all tests (20 seconds)
python test_agent_replica.py

# Verify identity (5 seconds)
python verify_replica_identity.py

# Complete validation (40 seconds)
python run_all_validations.py
```

### Interactive Demo

```bash
# Run interactive demonstration
python demo.py
# Press Enter to proceed through 8 demos
```

---

## 💻 Python API Quick Reference

### Initialize Agent

```python
from ai_agent_replica import AIAgentReplica, ToolType

agent = AIAgentReplica()
```

### File Operations

```python
# Write file
agent.execute_tool(
    ToolType.WRITE_FILE,
    file_path="/path/to/file.txt",
    content="Content here"
)

# Read file
result = agent.execute_tool(
    ToolType.READ_FILE,
    file_path="/path/to/file.txt"
)

# Edit file
agent.execute_tool(
    ToolType.EDIT_FILE,
    file_path="/path/to/file.txt",
    old_string="old text",
    new_string="new text"
)
```

### Search Operations

```python
# Find files by pattern
result = agent.execute_tool(
    ToolType.GLOB,
    pattern="**/*.py",
    path="/path/to/search"
)

# Search file contents
result = agent.execute_tool(
    ToolType.GREP,
    pattern="def.*function",
    path="/path/to/search",
    include="*.py"
)
```

### Terminal Operations

```python
# Execute command
result = agent.execute_tool(
    ToolType.TERMINAL,
    command="ls -la"
)
print(result.output['stdout'])
```

### LLM Operations

```python
# Use LLM for reasoning
result = agent.think("What is the best approach to solve X?")
print(result.output['text'])
```

### Self-Replication

```python
# Create backup
agent.self_replicate("/backup/agent.py")
```

### Verification

```python
# Check capabilities
capabilities = agent.verify_capabilities()
all_working = all(capabilities.values())

# Get status
status = agent.get_status()
```

---

## 📊 Project Files Overview

| File | Purpose | Size |
|------|---------|------|
| `ai_agent_replica.py` | Main agent | 20KB |
| `test_agent_replica.py` | Test suite | 20KB |
| `verify_llm.py` | LLM check | 3KB |
| `verify_replica_identity.py` | Identity check | 10KB |
| `run_all_validations.py` | Master validator | 10KB |
| `demo.py` | Interactive demo | 9KB |
| `requirements.txt` | Dependencies | 35B |
| `README.md` | Full guide | 10KB |
| `DEPLOYMENT_GUIDE.md` | Deploy guide | 11KB |
| `PROJECT_SUMMARY.md` | Summary | 13KB |

---

## ✅ Validation Checklist

Quick health check:

```bash
□ Environment variables set (verify_llm.py)
□ Agent initializes (ai_agent_replica.py)
□ All tests pass (test_agent_replica.py)
□ Identity verified (verify_replica_identity.py)
```

If all ✅, system is operational!

---

## 🔧 Troubleshooting

### Problem: LLM not connecting
**Solution**: 
```bash
# Check environment variables
echo $_ANTHROPIC_API_KEY
echo $_ANTHROPIC_BASE_URL
echo $_MODEL_NAME

# Run verification
python verify_llm.py
```

### Problem: Import errors
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: Tests failing
**Solution**:
```bash
# Run with verbose output
python test_agent_replica.py -v

# Check specific test
python -m unittest test_agent_replica.TestFileSystemTools
```

---

## 🎯 Success Indicators

System is healthy when:
- ✅ `verify_llm.py` outputs: "All verifications passed!"
- ✅ `ai_agent_replica.py` shows: "All capabilities verified successfully!"
- ✅ `test_agent_replica.py` shows: "OK (32 tests passed)"
- ✅ `verify_replica_identity.py` shows: "7/7 tests passed"
- ✅ `run_all_validations.py` shows: "ALL VALIDATIONS PASSED!"

---

## 📚 Documentation Map

- **Quick Start**: This file
- **Complete Guide**: README.md
- **Deployment**: DEPLOYMENT_GUIDE.md
- **Project Overview**: PROJECT_SUMMARY.md

---

## 🔄 Disaster Recovery (1 minute)

```bash
# 1. Find replica
find / -name "ai_agent_replica.py" 2>/dev/null

# 2. Verify environment  
python verify_llm.py

# 3. Test agent
python ai_agent_replica.py

# 4. Start using
python
>>> from ai_agent_replica import AIAgentReplica
>>> agent = AIAgentReplica()
>>> # Ready to use!
```

---

## 🚦 System Status Reference

All systems operational when:

```
LLM:        ✅ Connected
File Ops:   ✅ Working
Search:     ✅ Working
Terminal:   ✅ Working
Replication:✅ Working
Tests:      ✅ 32/32
Identity:   ✅ 7/7
```

---

**Last Updated**: System fully operational and validated ✅
