# Architecture Documentation

## Overview

The AI Assistant Replica is designed as a modular, extensible system that mirrors the capabilities of the cto.new AI assistant. This document describes the system architecture, component interactions, and design decisions.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                  (Python API / CLI / Script)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Assistant Class                          │
│  ┌────────────────┬──────────────┬────────────────────────┐ │
│  │ Task Processor │  LLM Client  │  Memory Manager        │ │
│  └────────────────┴──────────────┴────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Tool Framework                          │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐ │
│  │ ReadFile │WriteFile │ EditFile │Terminal  │  Search   │ │
│  │   Tool   │   Tool   │   Tool   │   Tool   │   Tools   │ │
│  └──────────┴──────────┴──────────┴──────────┴───────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Systems                          │
│  ┌──────────────┬──────────────────┬─────────────────────┐ │
│  │ File System  │  Shell/Terminal  │  LLM API Service    │ │
│  └──────────────┴──────────────────┴─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Assistant Class

**Purpose**: Main orchestrator that coordinates all operations

**Responsibilities**:
- Initialize and manage tools
- Interface with LLM service
- Manage memory persistence
- Process tasks and coordinate tool execution
- Handle errors and maintain state

**Key Methods**:
- `__init__()`: Initialize assistant with configuration
- `use_tool()`: Execute a specific tool
- `execute_simple_task()`: Process simple LLM tasks
- `process_task()`: Handle complex multi-step tasks
- `update_memory()` / `get_memory()`: Memory management

**Design Decisions**:
- Singleton pattern for tool registry
- Lazy loading of resources
- Fail-safe error handling
- Stateless between tasks (except memory)

### 2. Tool Framework

**Purpose**: Provide modular, reusable capabilities

**Base Tool Class**:
```python
@dataclass
class Tool:
    name: str
    description: str
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError
```

**Tool Design Principles**:
- Single responsibility per tool
- Consistent return format (success/error dict)
- Parameter validation
- Timeout protection
- Error isolation

**Available Tools**:

#### ReadFileTool
- Reads file contents with optional pagination
- Handles encoding errors gracefully
- Supports large files via offset/limit

#### WriteFileTool
- Creates or overwrites files
- Auto-creates parent directories
- Handles line endings consistently
- Atomic write operations

#### EditFileTool
- Precise text replacement
- Ensures uniqueness (prevents multiple matches)
- Preserves file integrity
- Context-aware editing

#### TerminalTool
- Executes shell commands safely
- Timeout protection (30s default)
- Captures stdout/stderr
- Working directory management

#### LsToolTool
- Lists directory contents
- Pagination support
- Sorting and filtering
- Error handling for permissions

#### GlobToolTool
- Pattern-based file search
- Recursive directory traversal
- Sort by modification time
- Efficient for large codebases

#### GrepToolTool
- Regex content search
- File type filtering
- Line number reporting
- Performance optimized

### 3. LLM Integration

**Purpose**: Provide intelligent reasoning and decision-making

**Architecture**:
```
Assistant
    │
    ├─> Anthropic Client (via anthropic-sdk-python)
    │       │
    │       ├─> API Key Authentication
    │       ├─> Base URL Configuration
    │       └─> Model Selection
    │
    └─> Response Processing
            │
            ├─> Text Extraction
            ├─> Thinking Block Handling
            └─> Error Recovery
```

**Key Features**:
- Configurable model selection
- Custom base URL support (for proxies/alternatives)
- Automatic retry logic
- Response streaming support (future)
- Token usage tracking

**Response Handling**:
```python
def _extract_text_from_response(self, message):
    text = ""
    for block in message.content:
        if hasattr(block, 'text'):
            text += block.text
    return text
```

### 4. Memory System

**Purpose**: Persist learning and preferences across sessions

**Storage Format**: JSON
```json
{
  "codebase_info": {
    "language": "python",
    "framework": "django",
    "test_command": "pytest"
  },
  "preferences": {
    "indent_style": "spaces",
    "indent_size": 4,
    "quote_style": "double"
  },
  "important_commands": [
    "python manage.py migrate",
    "npm run build"
  ]
}
```

**Memory Operations**:
- `_load_memory()`: Read from file on initialization
- `_save_memory()`: Write to file on updates
- `update_memory()`: Update specific keys
- `get_memory()`: Retrieve values

**Design Considerations**:
- File-based for simplicity and portability
- JSON for human readability
- Atomic writes to prevent corruption
- Graceful degradation if memory file missing

## Data Flow

### Simple Task Execution

```
User Request
     │
     ▼
Assistant.execute_simple_task()
     │
     ├─> Build message
     ├─> Call LLM API
     ├─> Extract response
     └─> Return result
```

### Complex Task Execution

```
User Request
     │
     ▼
Assistant.process_task()
     │
     ├─> Initialize conversation
     │
     ├─> Iteration Loop (max N times)
     │    │
     │    ├─> Call LLM
     │    ├─> Parse response
     │    ├─> Extract tool calls
     │    ├─> Execute tools
     │    ├─> Collect results
     │    └─> Add to conversation
     │
     └─> Return results
```

### Tool Execution

```
Tool Request
     │
     ▼
Assistant.use_tool()
     │
     ├─> Validate tool exists
     ├─> Get tool instance
     ├─> Execute with parameters
     │    │
     │    ├─> Try operation
     │    ├─> Handle errors
     │    └─> Format result
     │
     └─> Return result dict
```

## Error Handling Strategy

### Levels of Error Handling

1. **Tool Level**: Individual tools catch and return errors
2. **Assistant Level**: Catches tool errors and decides next action
3. **API Level**: Handles LLM API errors with retries
4. **System Level**: Top-level exception handling

### Error Response Format

```python
{
    "success": False,
    "error": "Error description",
    "error_type": "IOError",
    "context": {...}
}
```

### Recovery Strategies

- **Retry**: For transient API errors
- **Fallback**: Use alternative approach
- **Graceful Degradation**: Continue with reduced functionality
- **Fail Fast**: For unrecoverable errors

## Security Architecture

### Principle: Defense in Depth

**Layer 1: Input Validation**
- Validate all file paths
- Sanitize command inputs
- Check parameter types

**Layer 2: Operation Sandboxing**
- Restrict to project directory
- Command timeouts
- Resource limits

**Layer 3: Error Isolation**
- Catch all exceptions
- Prevent information leakage
- Log securely

**Layer 4: Audit Trail**
- Log all operations
- Track tool usage
- Record decisions

### Path Security

```python
def validate_path(path: str, base: str) -> bool:
    """Ensure path is within base directory."""
    abs_path = Path(path).resolve()
    abs_base = Path(base).resolve()
    return abs_path.is_relative_to(abs_base)
```

## Performance Considerations

### File Operations
- Use streaming for large files
- Implement pagination (offset/limit)
- Cache frequently accessed files (future)

### LLM Calls
- Batch when possible
- Use appropriate context windows
- Implement caching (future)
- Stream responses for better UX (future)

### Memory Management
- Lazy load memory
- Write only on changes
- Keep memory size bounded

## Scalability

### Current Limitations
- Single-threaded execution
- Synchronous tool execution
- In-process memory

### Future Enhancements
- Async tool execution
- Parallel file operations
- Distributed memory (Redis/DB)
- Tool result caching
- LLM response streaming

## Testing Architecture

### Test Pyramid

```
        ┌─────────────┐
       ╱  Integration  ╲     (test_behavior_comparison.py)
      ╱─────────────────╲
     ╱   Component Tests  ╲   (test_assistant.py)
    ╱─────────────────────╲
   ╱      Unit Tests        ╲  (test_assistant.py - TestTools)
  ╱─────────────────────────╲
```

### Test Categories

1. **Unit Tests**: Individual tool functionality
2. **Component Tests**: Assistant class methods
3. **Integration Tests**: End-to-end workflows
4. **Behavior Tests**: Compare to expected behavior

### Test Environment
- Temporary directories for isolation
- Mock LLM responses (when API unavailable)
- Cleanup after each test
- Deterministic test data

## Extension Points

### Adding New Tools

1. Create tool class inheriting from `Tool`
2. Implement `execute()` method
3. Register in `Assistant.__init__()`
4. Add tests
5. Update documentation

Example:
```python
@dataclass
class MyNewTool(Tool):
    def __init__(self):
        super().__init__(
            name="MyNewTool",
            description="Does something useful"
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            # Implementation
            return {"success": True, "result": ...}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### Adding New Capabilities

1. Extend `Assistant` class
2. Add helper methods
3. Update system message
4. Add tests
5. Document

## Deployment Considerations

### Environment Variables
```bash
_ANTHROPIC_API_KEY=<key>
_ANTHROPIC_BASE_URL=<url>
_MODEL_NAME=<model>
```

### Dependencies
- Python 3.8+
- anthropic SDK
- Standard library only for tools

### File Structure
```
/home/engine/project/
├── assistant_replica.py    # Main code
├── test_*.py               # Tests
├── requirements.txt        # Dependencies
├── docs/                   # Documentation
└── examples/              # Usage examples
```

## Design Patterns Used

1. **Strategy Pattern**: Tool selection and execution
2. **Factory Pattern**: Tool instantiation
3. **Template Method**: Common tool structure
4. **Singleton**: Tool registry
5. **Observer**: Memory updates (future)
6. **Command**: Tool execution encapsulation

## Future Roadmap

### Phase 1: Core Enhancement
- [ ] Async tool execution
- [ ] Response streaming
- [ ] Enhanced memory system
- [ ] Tool result caching

### Phase 2: Advanced Features
- [ ] Multi-file atomic edits
- [ ] Git integration
- [ ] Code analysis tools
- [ ] Test execution tools

### Phase 3: Production Features
- [ ] Distributed deployment
- [ ] Web API interface
- [ ] Real-time collaboration
- [ ] Advanced security features

---

This architecture is designed to be simple, maintainable, and extensible while providing all the capabilities of the original cto.new assistant system.
