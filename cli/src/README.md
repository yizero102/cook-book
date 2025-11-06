# CLI Source Code Structure

This directory contains the refactored, well-structured source code for the Claude CLI application.

## Directory Structure

```
src/
├── commands/           # CLI command implementations
│   ├── servers.js     # MCP servers list command
│   ├── tools.js       # MCP tools list command
│   ├── info.js        # Tool information command
│   ├── call.js        # MCP tool invocation command
│   ├── grep.js        # Tool search command
│   ├── resources.js   # MCP resources list command
│   └── index.js       # Command exports
│
├── core/              # Core functionality
│   ├── mcpCli.js      # MCP CLI program definition
│   └── telemetryCore.js # Telemetry functionality
│
├── utils/             # Utility functions
│   ├── mcpStateReader.js   # MCP state file reading
│   ├── toolIdentifier.js   # Tool name parsing and formatting
│   └── telemetry.js        # Telemetry helper
│
├── main/              # Main CLI functionality
│   └── index.js       # Main entry point (placeholder)
│
├── ripgrep/           # Ripgrep integration
│   └── index.js       # Ripgrep functionality (placeholder)
│
└── index.js           # CLI entry point

## Architecture

### Commands

Each command is isolated in its own module with a clear, single responsibility:

- **servers**: Lists all connected MCP servers with their capabilities
- **tools**: Lists available tools, optionally filtered by server
- **info**: Displays detailed information about a specific tool
- **call**: Invokes an MCP tool with given arguments
- **grep**: Searches tools by name or description using regex
- **resources**: Lists MCP resources, optionally filtered by server

### Utils

Utility modules provide shared functionality:

- **mcpStateReader**: Reads and parses the MCP state file
- **toolIdentifier**: Parses and formats MCP tool identifiers
- **telemetry**: Tracks usage events for analytics

### Core

Core modules handle the main application logic:

- **mcpCli**: Defines the MCP CLI program structure using Commander.js
- **telemetryCore**: Core telemetry functionality

## Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Injection**: Commands receive dependencies as parameters
3. **Error Handling**: Consistent error handling with proper exit codes
4. **Separation of Concerns**: Commands, utilities, and core logic are separate
5. **Testability**: Pure functions with clear inputs and outputs

## Usage

The refactored code is designed to be:
- **Readable**: Clear naming and structure
- **Maintainable**: Easy to modify and extend
- **Understandable**: Well-organized with clear responsibilities

## Integration with Bundle

The main `cli.js` file is a bundled application that includes all dependencies.
The source code in this directory represents the logical structure that could
be used to rebuild or modify the CLI functionality.

To use the refactored structure:
1. Install dependencies: `npm install commander chalk`
2. Run the CLI: `node src/index.js --mcp-cli [command]`

## Dependencies

- **commander**: CLI framework
- **chalk**: Terminal string styling
- **fs**: File system operations (Node.js built-in)
- **path**: Path utilities (Node.js built-in)
- **os**: Operating system utilities (Node.js built-in)
