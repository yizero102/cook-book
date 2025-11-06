# Claude CLI - Refactored Structure

This directory contains the Claude CLI application with a refactored, well-structured codebase.

## Files

- **cli.js** - Main bundled CLI application (production-ready, minified)
- **cli.js.backup** - Backup of the original CLI file
- **sdk-tools.d.ts** - TypeScript definitions for tool inputs
- **package.json** - Package configuration
- **src/** - Refactored source code (for reference and maintenance)

## Source Code Structure

The `src/` directory contains a clean, well-organized version of the CLI code:

```
src/
├── commands/              # Individual command handlers
│   ├── servers.js        # List MCP servers
│   ├── tools.js          # List MCP tools
│   ├── info.js           # Show tool information
│   ├── call.js           # Invoke MCP tools
│   ├── grep.js           # Search tools
│   ├── resources.js      # List MCP resources
│   └── index.js          # Command exports
├── core/                 # Core functionality
│   ├── mcpCli.js         # MCP CLI program
│   └── telemetryCore.js  # Telemetry
├── utils/                # Shared utilities
│   ├── mcpStateReader.js # Read MCP state
│   ├── toolIdentifier.js # Parse tool IDs
│   └── telemetry.js      # Telemetry helper
├── main/                 # Main CLI logic
├── ripgrep/              # Ripgrep integration
└── index.js              # Entry point
```

## Architecture Improvements

### 1. Separation of Concerns
- Commands are isolated in individual modules
- Utilities are reusable across commands
- Core logic is centralized

### 2. Single Responsibility Principle
- Each module has one clear purpose
- Functions are focused and testable
- Easy to understand and modify

### 3. Improved Readability
- Clear naming conventions
- Consistent code structure
- Comprehensive comments
- Logical organization

### 4. Better Maintainability
- Easy to add new commands
- Simple to modify existing functionality
- Clear dependencies between modules
- Testable components

### 5. Error Handling
- Consistent error messages
- Proper exit codes
- User-friendly output
- Graceful degradation

## Main CLI (`cli.js`)

The main `cli.js` file is a bundled application containing:

1. **React and dependencies** - UI framework and libraries
2. **MCP CLI** - Command-line interface for MCP
3. **Ripgrep integration** - Fast search functionality
4. **Main application** - Interactive Claude Code session

### Entry Points

The CLI supports multiple modes:

```bash
# MCP CLI mode
node cli.js --mcp-cli servers
node cli.js --mcp-cli tools
node cli.js --mcp-cli call server/tool '{"arg": "value"}'

# Ripgrep mode
node cli.js --ripgrep [args]

# Main interactive mode (default)
node cli.js [options]
```

## MCP CLI Commands

### servers
Lists all connected MCP servers with their capabilities.

```bash
claude --mcp-cli servers
claude --mcp-cli servers --json
```

### tools
Lists available MCP tools, optionally filtered by server.

```bash
claude --mcp-cli tools
claude --mcp-cli tools server-name
claude --mcp-cli tools --json
```

### info
Shows detailed information about a specific tool.

```bash
claude --mcp-cli info server/tool
claude --mcp-cli info server/tool --json
```

### call
Invokes an MCP tool with given arguments.

```bash
claude --mcp-cli call server/tool '{"arg": "value"}'
claude --mcp-cli call server/tool - < args.json
claude --mcp-cli call server/tool '{}' --debug --timeout 60000
```

### grep
Searches tools by name or description using regex.

```bash
claude --mcp-cli grep pattern
claude --mcp-cli grep pattern --json
claude --mcp-cli grep pattern -i
```

### resources
Lists MCP resources, optionally filtered by server.

```bash
claude --mcp-cli resources
claude --mcp-cli resources server-name
claude --mcp-cli resources --json
```

## Development

### Understanding the Code

The refactored source code in `src/` demonstrates the logical structure:

1. **commands/** - Each command is a pure function that:
   - Receives options and arguments
   - Validates input
   - Performs the operation
   - Outputs results
   - Tracks telemetry

2. **utils/** - Shared functionality:
   - `mcpStateReader.js` - Reads MCP configuration
   - `toolIdentifier.js` - Parses tool identifiers
   - `telemetry.js` - Tracks usage events

3. **core/** - Application logic:
   - `mcpCli.js` - Defines the CLI program
   - `telemetryCore.js` - Core telemetry

### Code Quality Improvements

**Before (original):**
- Single 10MB+ minified file
- Unclear structure
- Hard to maintain
- Difficult to test
- Poor readability

**After (refactored):**
- Modular structure
- Clear responsibilities
- Easy to maintain
- Testable components
- Excellent readability
- Comprehensive comments

### Design Patterns

1. **Command Pattern** - Each command is encapsulated
2. **Dependency Injection** - Dependencies passed as parameters
3. **Pure Functions** - Predictable inputs and outputs
4. **Error First** - Consistent error handling
5. **Single Source of Truth** - Centralized state reading

## Testing

The modular structure makes testing straightforward:

```javascript
import { handleServersCommand } from './src/commands/servers.js';

// Mock dependencies
const mockState = {
  clients: [
    { name: 'test', type: 'connected', capabilities: { tools: true } }
  ]
};

// Test command
await handleServersCommand({ json: true });
```

## Future Improvements

1. **TypeScript Migration** - Add type safety
2. **Unit Tests** - Test each module independently
3. **Integration Tests** - Test command workflows
4. **Documentation** - Add JSDoc comments
5. **Error Handling** - More specific error types
6. **Logging** - Structured logging system
7. **Configuration** - Externalize configuration
8. **Plugin System** - Allow command extensions

## Contributing

When modifying the CLI:

1. Update the source code in `src/`
2. Follow the established patterns
3. Maintain separation of concerns
4. Add comments for complex logic
5. Test changes thoroughly
6. Update this documentation

## License

SEE LICENSE IN README.md

## Support

For issues and questions:
- GitHub: https://github.com/anthropics/claude-code
- Email: support@anthropic.com
