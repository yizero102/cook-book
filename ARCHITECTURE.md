# AI Mirror System - Architecture Documentation

## Overview

The AI Mirror System is a well-structured Python application that provides a mirror implementation of conversational AI capabilities using the Anthropic API. The system is designed to be modular, extensible, and production-ready.

## Architecture Principles

### Design Philosophy

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Modularity**: Components are loosely coupled and highly cohesive
3. **Extensibility**: Easy to add new features without modifying existing code
4. **Testability**: All components are designed to be easily testable
5. **Type Safety**: Comprehensive type hints throughout the codebase

### Key Design Patterns

- **Builder Pattern**: Settings configuration with validation
- **Registry Pattern**: Tool management system
- **State Pattern**: Conversation state management
- **Strategy Pattern**: Flexible tool execution

## Module Breakdown

### 1. Configuration Module (`config/`)

**Purpose**: Manages application settings and environment variables

**Key Components**:
- `Settings`: Pydantic model for configuration with validation
  - Environment variable loading
  - Default values
  - Validation logic

**Responsibilities**:
- Load configuration from environment
- Validate required settings
- Provide configuration to other modules

**Design Decisions**:
- Uses Pydantic for validation and type safety
- Environment variables prefixed with `_` to avoid conflicts
- Immutable settings after initialization

### 2. Core AI Mirror (`src/ai_mirror/`)

#### 2.1 Client Module (`client.py`)

**Purpose**: Main interface for interacting with the AI system

**Key Components**:
- `AIMirrorClient`: Primary client class

**Responsibilities**:
- Manage connection to Anthropic API
- Handle chat requests and responses
- Coordinate conversation state
- Integrate tool system
- Provide streaming support

**API Design**:
```python
class AIMirrorClient:
    - verify_connection() -> tuple[bool, Optional[str]]
    - chat(message, system_prompt) -> str
    - chat_async(message, system_prompt) -> str
    - chat_stream(message, system_prompt) -> AsyncIterator[str]
    - set_system_prompt(prompt) -> None
    - clear_conversation() -> None
    - get_conversation_history() -> Dict[str, Any]
```

**Design Decisions**:
- Single responsibility: API communication and orchestration
- Composition over inheritance: Uses Conversation and ToolRegistry
- Error handling at the boundary
- Synchronous by default, async support where needed

#### 2.2 Conversation Module (`conversation.py`)

**Purpose**: Manage conversation state and message history

**Key Components**:
- `Message`: Individual message model
- `Conversation`: Conversation state container

**Responsibilities**:
- Store message history
- Format messages for API
- Manage system messages
- Provide conversation utilities

**Data Model**:
```python
Message:
    - role: Literal["user", "assistant", "system"]
    - content: str
    - timestamp: datetime
    - metadata: Optional[Dict[str, Any]]

Conversation:
    - messages: List[Message]
    - conversation_id: Optional[str]
    - metadata: Optional[Dict[str, Any]]
```

**Design Decisions**:
- Immutable messages after creation
- Automatic timestamp generation
- Flexible metadata support
- Separate system messages from conversation flow

#### 2.3 Tools Module (`tools.py`)

**Purpose**: Extensible tool/function calling system

**Key Components**:
- `Tool`: Individual tool definition
- `ToolRegistry`: Tool management
- `create_example_tools()`: Factory for demo tools

**Responsibilities**:
- Define tool schemas
- Register and manage tools
- Execute tool handlers
- Convert to Anthropic format

**Tool Structure**:
```python
Tool:
    - name: str
    - description: str
    - input_schema: Dict[str, Any]
    - handler: Optional[Callable]
```

**Design Decisions**:
- Declarative tool definitions
- Separate schema from implementation
- Async-first handler design
- Registry pattern for extensibility

### 3. Scripts (`scripts/`)

**Purpose**: Utility scripts for verification, validation, and demonstration

**Components**:
- `verify_llm.py`: LLM connection verification
- `validate_python.py`: Python syntax validation
- `demo_basic_chat.py`: Basic chat demonstration
- `demo_with_tools.py`: Tool system demonstration

**Design Decisions**:
- Each script is self-contained
- Clear, informative output
- Proper exit codes for automation
- Example-driven documentation

### 4. Tests (`tests/`)

**Purpose**: Comprehensive test suite ensuring system reliability

**Test Structure**:
```
tests/
├── conftest.py           # Shared fixtures
├── test_settings.py      # Configuration tests
├── test_conversation.py  # Conversation management tests
├── test_tools.py         # Tool system tests
└── test_client.py        # Client integration tests
```

**Test Categories**:
1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Multi-component interaction
3. **Validation Tests**: Configuration and settings
4. **Error Handling Tests**: Edge cases and failures

**Coverage Areas**:
- ✅ Settings validation and loading
- ✅ Message creation and management
- ✅ Conversation state management
- ✅ Tool registration and execution
- ✅ Client initialization and configuration
- ✅ API connection verification
- ✅ Chat functionality
- ✅ Error handling

## Data Flow

### Chat Request Flow

```
User Input
    ↓
AIMirrorClient.chat()
    ↓
Add to Conversation
    ↓
Format for API
    ↓
Anthropic API Request
    ↓
Response Processing
    ↓
Tool Execution (if needed)
    ↓
Add Assistant Response to Conversation
    ↓
Return to User
```

### Tool Execution Flow

```
AI Response with tool_use
    ↓
Extract Tool Call
    ↓
ToolRegistry.get(tool_name)
    ↓
Tool.handler(**inputs)
    ↓
Format Result
    ↓
Return to Client
```

## Extension Points

### Adding New Tools

1. Create tool definition with schema
2. Implement async handler function
3. Register with ToolRegistry
4. Add tests for new tool

Example:
```python
custom_tool = Tool(
    name="custom_function",
    description="Description",
    input_schema={...}
)
custom_tool.handler = async_handler_function
registry.register(custom_tool)
```

### Extending the Client

1. Subclass `AIMirrorClient`
2. Override specific methods
3. Add new capabilities
4. Maintain interface compatibility

### Custom Message Types

1. Extend `Message` with new metadata
2. Add processing logic in `Conversation`
3. Update API formatting if needed

## Error Handling Strategy

### Levels of Error Handling

1. **Configuration Level**: Validation errors at startup
2. **Connection Level**: API connectivity errors
3. **Request Level**: Individual request failures
4. **Tool Level**: Tool execution errors

### Error Propagation

- Errors caught at appropriate levels
- User-friendly error messages
- Detailed logging for debugging
- Graceful degradation where possible

## Performance Considerations

### Optimizations

1. **Lazy Initialization**: Components initialized only when needed
2. **Efficient Message Storage**: Minimal overhead per message
3. **Stream Support**: For long responses
4. **Connection Reuse**: Single client instance reused

### Scalability

- Stateless client design (except conversation)
- Can support multiple conversations
- Tool registry shared across instances
- Async support for concurrent operations

## Security Considerations

### API Key Management

- Environment variable storage
- Never logged or exposed
- Validated at startup

### Input Validation

- Pydantic models for all inputs
- Type checking throughout
- Safe error messages (no sensitive data)

### Tool Safety

- Explicit tool registration required
- Handler validation
- Error isolation

## Testing Strategy

### Test Pyramid

```
           /\
          /  \
         / E2E\
        /------\
       / Integ. \
      /----------\
     /   Unit     \
    /--------------\
```

### Test Coverage Goals

- Unit Tests: >90% coverage
- Integration Tests: Key workflows
- Error Cases: All error paths
- Edge Cases: Boundary conditions

### Test Fixtures

Shared fixtures in `conftest.py`:
- `settings`: Configured Settings instance
- `client`: Initialized AIMirrorClient
- `client_with_tools`: Client with example tools
- `tool_registry`: Pre-configured ToolRegistry

## Future Enhancements

### Potential Improvements

1. **Streaming Implementation**: Full async streaming support
2. **Context Window Management**: Automatic message truncation
3. **Conversation Persistence**: Save/load conversations
4. **Multi-Model Support**: Easy model switching
5. **Rate Limiting**: Built-in rate limit handling
6. **Caching**: Response caching for repeated queries
7. **Logging**: Structured logging with levels
8. **Metrics**: Performance and usage metrics
9. **Web Interface**: Optional web UI
10. **CLI Tool**: Rich command-line interface

### Extension Patterns

- Plugin system for tools
- Event-driven architecture for hooks
- Middleware for request/response processing
- Custom formatters for different output types

## Dependencies

### Core Dependencies

- `anthropic>=0.39.0`: Anthropic API client
- `pydantic>=2.0.0`: Data validation and settings
- `requests>=2.31.0`: HTTP client utilities

### Development Dependencies

- `pytest>=8.0.0`: Testing framework
- `pytest-asyncio>=0.23.0`: Async test support

### Optional Dependencies

None currently, but can be extended for:
- Logging: `structlog`
- Web UI: `fastapi`, `streamlit`
- CLI: `click`, `rich`
- Persistence: `sqlalchemy`, `redis`

## Best Practices

### Code Standards

1. **Type Hints**: All functions have type hints
2. **Docstrings**: Public APIs documented
3. **Testing**: All features tested
4. **Error Handling**: Comprehensive error cases
5. **Naming**: Clear, descriptive names

### Development Workflow

1. Write tests first (TDD)
2. Implement feature
3. Validate with scripts
4. Update documentation
5. Review and refactor

### Git Workflow

1. Feature branches for new work
2. Descriptive commit messages
3. Tests must pass before merge
4. Code review for all changes

## Deployment

### Production Checklist

- ✅ All tests passing
- ✅ Python scripts validated
- ✅ Environment variables configured
- ✅ Dependencies installed
- ✅ API connection verified
- ✅ Error handling tested
- ✅ Logging configured
- ✅ Monitoring in place

### Environment Setup

1. Set environment variables
2. Create virtual environment
3. Install dependencies
4. Run verification script
5. Test with demo scripts

## Maintenance

### Regular Tasks

- Dependency updates
- Security patches
- Test coverage maintenance
- Documentation updates
- Performance monitoring

### Monitoring Points

- API response times
- Error rates
- Token usage
- Tool execution success rates
- Conversation lengths

## Conclusion

The AI Mirror System demonstrates production-ready software engineering practices:

- Clean architecture with clear separation of concerns
- Comprehensive testing at all levels
- Type safety and validation throughout
- Extensible design for future growth
- Well-documented and maintainable code

The system is ready for both development and production use, with clear patterns for extension and customization.
