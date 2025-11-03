# Quick Start Guide

## 5-Minute Setup

### 1. Verify Environment (30 seconds)

```bash
# Check that environment variables are set
env | grep -E "(_ANTHROPIC_|_MODEL_NAME)"
```

You should see:
- `_ANTHROPIC_API_KEY`
- `_ANTHROPIC_BASE_URL`
- `_MODEL_NAME`

### 2. Install Dependencies (2 minutes)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Connection (30 seconds)

```bash
python scripts/verify_llm.py
```

Expected output: ✅ All verification tests passed!

### 4. Try It Out (2 minutes)

```bash
# Basic chat demo
python scripts/demo_basic_chat.py

# Or interactive mode
python main.py
```

## Common Commands

### Using Makefile (Recommended)

```bash
make verify       # Verify LLM connection
make validate     # Validate Python scripts
make test         # Run all tests
make demo         # Run basic demo
make interactive  # Start interactive chat
make clean        # Clean cache files
```

### Manual Commands

```bash
# Activate venv first
source venv/bin/activate

# Verify LLM
python scripts/verify_llm.py

# Validate scripts
python scripts/validate_python.py

# Run tests
pytest tests/ -v

# Run demo
python scripts/demo_basic_chat.py

# Interactive chat
python main.py
```

## Basic Usage

### Simple Chat

```python
from config.settings import Settings
from src.ai_mirror import AIMirrorClient

# Create client
client = AIMirrorClient(Settings())

# Chat
response = client.chat("Hello!")
print(response)
```

### With System Prompt

```python
client.set_system_prompt("You are a helpful coding assistant.")
response = client.chat("How do I reverse a list in Python?")
```

### Conversation

```python
# Context is maintained automatically
client.chat("My name is Alice")
client.chat("What's my name?")  # Will remember "Alice"
```

### Using Tools

```python
from src.ai_mirror.tools import create_example_tools

# Create client with tools
registry = create_example_tools()
client = AIMirrorClient(Settings(), registry)

# AI can use calculator
response = client.chat("What is 25 * 4?")
```

## Testing Your Changes

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_client.py -v

# Run with coverage
pytest tests/ --cov=src --cov=config
```

## Troubleshooting

### Issue: Connection Failed

**Solution**:
```bash
# Check environment variables
env | grep _ANTHROPIC

# Verify they're set correctly
python scripts/verify_llm.py
```

### Issue: Import Errors

**Solution**:
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Tests Failing

**Solution**:
```bash
# Validate Python scripts
python scripts/validate_python.py

# Run tests with verbose output
pytest tests/ -v -s
```

## Interactive Mode Commands

When running `python main.py`:

- Type your message and press Enter to chat
- `quit` or `exit` - Exit the program
- `clear` - Clear conversation history
- `history` - Show message count
- `Ctrl+C` - Exit gracefully

## What to Try

### 1. Basic Conversation

```python
client.chat("What is Python?")
client.chat("What are its main features?")
client.chat("Give me a code example")
```

### 2. Multi-turn Context

```python
client.chat("I'm working on a web app")
client.chat("What framework should I use?")
client.chat("How do I get started with it?")
```

### 3. Different System Prompts

```python
# Technical expert
client.set_system_prompt("You are a senior software engineer.")
client.chat("How should I structure my code?")

# Creative writer
client.set_system_prompt("You are a creative writer.")
client.chat("Write a short story about AI")
```

## Project Structure Overview

```
├── config/          → Settings and configuration
├── src/ai_mirror/   → Core AI system
├── scripts/         → Utility scripts
├── tests/           → Test suite
├── main.py          → Interactive entry point
└── requirements.txt → Dependencies
```

## Next Steps

1. ✅ Read the full README.md for detailed documentation
2. ✅ Check ARCHITECTURE.md to understand the design
3. ✅ Look at test files for more usage examples
4. ✅ Try creating your own tools
5. ✅ Extend the system with custom features

## Quick Reference Card

| Task | Command |
|------|---------|
| Setup | `make install` |
| Verify | `make verify` |
| Test | `make test` |
| Demo | `make demo` |
| Interactive | `make interactive` |
| Clean | `make clean` |

## Get Help

- **README.md**: Complete documentation
- **ARCHITECTURE.md**: Design and architecture
- **tests/**: Usage examples
- **scripts/**: Demo implementations

---

**You're all set! Start with `python main.py` for interactive chat.**
