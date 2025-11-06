# Claude Code CLI - Refactored Structure

This directory contains a refactored version of the Claude Code CLI with improved readability, maintainability, and structure.

## Directory Structure

```
cli-refactored/
├── src/
│   ├── commands/          # CLI command implementations
│   │   └── mcp-commands.js    # MCP (Model Context Protocol) commands
│   ├── utils/             # Utility functions
│   │   ├── colorize.js        # Terminal color utilities
│   │   └── mcp-helpers.js     # MCP-specific helper functions
│   ├── config/            # Configuration management
│   │   └── settings.js        # Settings loading and processing
│   └── core/              # Core application logic
│       ├── entry.js           # Main entry point and routing
│       └── main.js            # Main CLI initialization and setup
└── README.md
```

## Module Descriptions

### Commands (`src/commands/`)

#### `mcp-commands.js`
Implements all MCP (Model Context Protocol) related commands:
- `servers` - List connected MCP servers
- `tools` - List available MCP tools
- `info` - Get detailed information about a tool
- `call` - Invoke an MCP tool
- `grep` - Search tools using regex patterns
- `resources` - List MCP resources

### Utils (`src/utils/`)

#### `colorize.js`
Provides terminal color utilities for output formatting:
- `red()`, `green()`, `yellow()` - Color text
- `bold()`, `dim()` - Text styling

#### `mcp-helpers.js`
Helper functions for MCP operations:
- `parseToolIdentifier()` - Parse server/tool identifiers
- `getMCPStateFromFd()` - Read MCP state from file descriptor

### Config (`src/config/`)

#### `settings.js`
Handles configuration and settings management:
- `eagerLoadSettings()` - Load settings from command-line flags
- `processSettingsFlag()` - Process --settings flag
- `processSettingSourcesFlag()` - Process --setting-sources flag
- `loadManagedSettings()` - Load managed policy settings

### Core (`src/core/`)

#### `entry.js`
Main entry point with routing logic:
- `cliEntry()` - Route to appropriate CLI mode (MCP, ripgrep, or main)
- `detectClientType()` - Detect how CLI is being run
- `setEntrypoint()` - Set the appropriate entrypoint
- `shouldRunInQuietMode()` - Determine if quiet mode should be used
- `isDebugMode()` - Check if debug/inspect mode is active

#### `main.js`
Main CLI initialization and execution:
- `main()` - Initialize and run the main CLI application
- `setupProcessHandlers()` - Setup process event handlers

## Key Improvements

1. **Separation of Concerns**: Each module has a clear, single responsibility
2. **Improved Readability**: Descriptive function and variable names
3. **Better Organization**: Logical grouping of related functionality
4. **Maintainability**: Easier to locate and modify specific features
5. **Testability**: Modular structure enables easier unit testing
6. **Documentation**: Clear inline comments and module descriptions

## Integration with Original CLI

The original CLI (`cli/cli.js`) is a bundled, minified file containing all dependencies. This refactored version extracts the core logic into maintainable modules while preserving the same functionality.

To integrate:
1. The refactored modules can be imported and composed together
2. Dependencies from the bundled file can be passed as parameters
3. The original bundled file serves as a reference for the complete implementation

## Usage Patterns

### MCP Commands
```javascript
import { createMCPCommands, runMCPCLI } from './src/commands/mcp-commands.js';

const mcpProgram = createMCPCommands(dependencies);
await runMCPCLI(args, mcpProgram, flushOutput);
```

### Entry Point
```javascript
import { cliEntry } from './src/core/entry.js';

await cliEntry(dependencies);
```

### Settings Management
```javascript
import { eagerLoadSettings, loadManagedSettings } from './src/config/settings.js';

eagerLoadSettings();
loadManagedSettings(dependencies);
```

## Notes

- This refactored code extracts the logical structure from the bundled CLI
- The original `cli/cli.js` contains the full implementation with all dependencies
- This structure demonstrates best practices for CLI application organization
- All modules use ES6 imports/exports for modern JavaScript standards
