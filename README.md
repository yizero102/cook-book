# AI Mirror System

A Python-based AI system that mirrors conversational AI capabilities using the Anthropic API (compatible with MiniMax and other Anthropic-compatible services).

## Features

- 🤖 **Full AI Chat Capabilities**: Engage in natural conversations with context retention
- 🔧 **Tool/Function Calling**: Extensible tool system for custom functions
- 💬 **Conversation Management**: Track and manage multi-turn conversations
- ⚙️ **Flexible Configuration**: Environment-based settings with validation
- 🧪 **Comprehensive Testing**: 46+ test cases covering all scenarios
- 📝 **Well-Structured**: Clean, modular architecture following best practices

## Project Structure

```
.
├── config/                  # Configuration management
│   ├── __init__.py
│   └── settings.py         # Settings with environment variable support
├── src/
│   └── ai_mirror/          # Core AI mirror system
│       ├── __init__.py
│       ├── client.py       # Main AI client
│       ├── conversation.py # Conversation & message models
│       └── tools.py        # Tool/function calling system
├── scripts/                # Utility scripts
│   ├── verify_llm.py      # LLM connection verification
│   ├── validate_python.py # Python script validator
│   ├── demo_basic_chat.py # Basic chat demonstration
│   └── demo_with_tools.py # Tool usage demonstration
├── tests/                  # Comprehensive test suite
│   ├── conftest.py        # Pytest configuration & fixtures
│   ├── test_client.py     # Client tests
│   ├── test_conversation.py # Conversation tests
│   ├── test_settings.py   # Settings tests
│   └── test_tools.py      # Tool system tests
├── requirements.txt        # Python dependencies
├── pytest.ini             # Pytest configuration
└── README.md              # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   cd /path/to/project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The system requires the following environment variables:

- `_ANTHROPIC_API_KEY`: Your API key (e.g., from MiniMax or Anthropic)
- `_ANTHROPIC_BASE_URL`: The base URL for the API (e.g., `https://api.minimax.io/anthropic`)
- `_MODEL_NAME`: The model name to use (e.g., `MiniMax-M2`)

These should already be set in your environment. To verify:

```bash
env | grep -E "(_ANTHROPIC_|_MODEL_NAME)"
```

## Quick Start

### 1. Verify LLM Connection

```bash
source venv/bin/activate
python scripts/verify_llm.py
```

### 2. Basic Chat Example

```python
from config.settings import Settings
from src.ai_mirror import AIMirrorClient

# Initialize client
settings = Settings()
client = AIMirrorClient(settings)

# Set system prompt
client.set_system_prompt("You are a helpful assistant.")

# Chat
response = client.chat("What is Python?")
print(response)
```

### 3. Run Demo Scripts

**Basic Chat Demo**:
```bash
python scripts/demo_basic_chat.py
```

**Tools Demo**:
```bash
python scripts/demo_with_tools.py
```

## Usage Guide

### Basic Chat

```python
from src.ai_mirror import AIMirrorClient
from config.settings import Settings

client = AIMirrorClient(Settings())

# Simple chat
response = client.chat("Hello!")
print(response)

# Chat with system prompt
response = client.chat(
    "Explain quantum computing",
    system_prompt="You are a physics professor."
)
```

### Conversation Management

```python
# Add system prompt
client.set_system_prompt("You are a friendly AI assistant.")

# Multi-turn conversation
client.chat("My name is Alice")
client.chat("What's my name?")  # Context maintained

# Get conversation history
history = client.get_conversation_history()
print(f"Total messages: {len(history['messages'])}")

# Clear conversation
client.clear_conversation()
```

### Using Tools

```python
from src.ai_mirror.tools import create_example_tools

# Create client with tools
tool_registry = create_example_tools()
client = AIMirrorClient(Settings(), tool_registry)

# AI can now use tools
response = client.chat("Calculate 15 multiplied by 7")
```

### Creating Custom Tools

```python
from src.ai_mirror.tools import Tool, ToolRegistry

# Define a custom tool
weather_tool = Tool(
    name="get_weather",
    description="Get weather information for a city",
    input_schema={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name"
            }
        },
        "required": ["city"]
    }
)

# Add handler
async def weather_handler(city: str) -> str:
    # Your weather API logic here
    return f"Weather in {city}: Sunny, 25°C"

weather_tool.handler = weather_handler

# Register tool
registry = ToolRegistry()
registry.register(weather_tool)

# Use with client
client = AIMirrorClient(Settings(), registry)
```

## Testing

### Run All Tests

```bash
source venv/bin/activate
pytest tests/ -v
```

### Run Specific Test Categories

```bash
# Test client functionality
pytest tests/test_client.py -v

# Test conversation management
pytest tests/test_conversation.py -v

# Test tool system
pytest tests/test_tools.py -v

# Test settings
pytest tests/test_settings.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov=config --cov-report=html
```

## Validation

### Validate All Python Scripts

```bash
python scripts/validate_python.py
```

This will check all Python files in the project for syntax errors and compilation issues.

## API Reference

### AIMirrorClient

Main client for interacting with the AI system.

**Methods**:
- `verify_connection() -> tuple[bool, Optional[str]]`: Verify API connection
- `chat(user_message: str, system_prompt: Optional[str] = None) -> str`: Send a message and get response
- `chat_async(user_message: str, system_prompt: Optional[str] = None) -> str`: Async version of chat
- `chat_stream(user_message: str, system_prompt: Optional[str] = None) -> AsyncIterator[str]`: Stream response
- `set_system_prompt(prompt: str) -> None`: Set system prompt
- `clear_conversation() -> None`: Clear conversation history
- `get_conversation_history() -> Dict[str, Any]`: Get conversation history
- `get_settings() -> Settings`: Get current settings

### Settings

Configuration management with environment variable support.

**Fields**:
- `anthropic_api_key: str`: API key
- `anthropic_base_url: str`: Base URL for API
- `model_name: str`: Model name
- `max_tokens: int`: Maximum tokens (default: 4096)
- `temperature: float`: Temperature (default: 0.7)

**Methods**:
- `validate() -> tuple[bool, Optional[str]]`: Validate settings

### Conversation

Manages conversation state and message history.

**Methods**:
- `add_message(role, content, metadata=None)`: Add a message
- `get_messages_for_api() -> List[Dict]`: Get messages formatted for API
- `get_system_message() -> Optional[str]`: Get system message
- `clear()`: Clear all messages
- `get_last_message() -> Optional[Message]`: Get last message
- `to_dict() -> Dict`: Export conversation to dictionary

### Tool & ToolRegistry

Tool/function calling system.

**Tool Methods**:
- `to_anthropic_format() -> Dict`: Convert to Anthropic format
- `execute(**kwargs) -> Any`: Execute tool handler

**ToolRegistry Methods**:
- `register(tool: Tool)`: Register a tool
- `get(name: str) -> Optional[Tool]`: Get tool by name
- `get_all_tools() -> List[Tool]`: Get all registered tools
- `to_anthropic_format() -> List[Dict]`: Convert all tools to Anthropic format
- `has_tools() -> bool`: Check if any tools are registered

## Test Coverage

The project includes 46+ comprehensive test cases covering:

✅ **Settings & Configuration**
- Environment variable loading
- Validation logic
- Default and custom values

✅ **Conversation Management**
- Message creation and storage
- Context retention
- History management
- Conversation clearing

✅ **Client Functionality**
- Connection verification
- Basic chat
- System prompts
- Multi-turn conversations
- Error handling

✅ **Tool System**
- Tool registration
- Tool execution
- Calculator example
- Error handling

✅ **Integration Tests**
- Full conversation flows
- Context maintenance
- Tool integration

## Troubleshooting

### Connection Issues

If you encounter connection errors:

1. Verify environment variables are set:
   ```bash
   env | grep -E "(_ANTHROPIC_|_MODEL_NAME)"
   ```

2. Run verification script:
   ```bash
   python scripts/verify_llm.py
   ```

3. Check API key validity and base URL

### Import Errors

If you get import errors:

1. Ensure virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Test Failures

If tests fail:

1. Run validation:
   ```bash
   python scripts/validate_python.py
   ```

2. Check specific test output:
   ```bash
   pytest tests/test_client.py -v -s
   ```

## Development

### Adding New Features

1. Create module in `src/ai_mirror/`
2. Add tests in `tests/test_<module>.py`
3. Update `__init__.py` exports
4. Run validation and tests
5. Update documentation

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for public APIs
- Keep functions focused and small
- Test all new functionality

## License

This project is provided as-is for educational and development purposes.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues or questions:

1. Check this README
2. Review test cases for usage examples
3. Run verification scripts
4. Check API documentation

---

**Built with ❤️ using Python and Anthropic API**
