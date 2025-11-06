# CLI Refactoring Guide

This document explains how the original CLI code has been refactored into a well-structured, maintainable codebase.

## Overview

The original `cli.js` is a 10MB+ bundled file containing:
- Minified React and dependencies
- MCP CLI commands
- Ripgrep integration  
- Main application logic

The refactored version (`src/`) extracts the application logic into clean, modular components while preserving functionality.

## Refactoring Approach

### Original Code Structure

```javascript
// Original: All in one file, minified variable names
function l$A(){try{let A=DQ1(),B=no2(A,"utf-8");return JSON.parse(B)}catch{
console.error(nA.red("Error: MCP state not available")),console.error(
"The mcp command is only available within a Claude Code session"),
process.exit(1)}}function ao2(A){let B=A.split("/");if(B.length!==2||!B[0]
||!B[1])console.error(nA.red(`Error: Invalid tool identifier '${A}'`)),
console.error("Expected format: <server>/<tool>"),process.exit(1);
return{server:B[0],tool:B[1]}}var Jt=new eNA().name("mcp-cli")...
```

### Refactored Code Structure

```javascript
// Refactored: Modular, clear naming, documented

// utils/mcpStateReader.js
/**
 * Reads and parses the MCP state file
 * @returns {Object} Parsed MCP state
 * @throws {Error} If state file is not available
 */
export function readMcpState() {
  try {
    const statePath = getMcpStatePath();
    if (!existsSync(statePath)) {
      throw new Error('MCP state file not found');
    }
    const content = readFileSync(statePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error(chalk.red('Error: MCP state not available'));
    console.error('The mcp command is only available within a Claude Code session');
    process.exit(1);
  }
}
```

## Key Improvements

### 1. Module Organization

**Before:**
```javascript
// Everything in one file
var Jt=new eNA().name("mcp-cli").description("Interact with MCP servers and tools")
.version("1.0.0");Jt.command("servers").description("List all connected MCP 
servers").option("--json","Output in JSON format").action(async(A)=>{let B=l$A();
if(A.json)console.log(JSON.stringify(B.clients.map((Q)=>({name:Q.name,type:Q.type,
hasTools:Q.type==="connected"&&!!Q.capabilities?.tools,hasResources:Q.type===
"connected"&&!!Q.capabilities?.resources}))));...});
```

**After:**
```javascript
// commands/servers.js
export async function handleServersCommand(options) {
  const state = readMcpState();
  
  if (options.json) {
    const output = state.clients.map((client) => ({
      name: client.name,
      type: client.type,
      hasTools: client.type === 'connected' && !!client.capabilities?.tools,
      hasResources: client.type === 'connected' && !!client.capabilities?.resources
    }));
    console.log(JSON.stringify(output));
  } else {
    // ... formatted output
  }
  
  await trackEvent('tengu_mcp_cli_command_executed', {
    command: 'servers',
    server_count: state.clients.length
  });
}

// core/mcpCli.js
program
  .command('servers')
  .description('List all connected MCP servers')
  .option('--json', 'Output in JSON format')
  .action(async (options) => {
    await handleServersCommand(options);
  });
```

### 2. Clear Naming

**Before:**
- `l$A()` - Unclear purpose
- `ao2()` - No indication of function
- `Jt` - Meaningless variable name
- `nA` - Hidden dependency

**After:**
- `readMcpState()` - Clear purpose
- `parseToolIdentifier()` - Descriptive name
- `program` - Standard convention
- `chalk` - Explicit dependency

### 3. Separation of Concerns

**Before:**
```javascript
// Command logic, state reading, validation, and error handling all mixed
Jt.command("call").action(async(A,B,Q)=>{let{server:I,tool:G}=ao2(A);if(B==="-"){
let C=[];for await(let V of process.stdin)C.push(V);B=Buffer.concat(C).toString
("utf-8").trim()}let Z;try{Z=JSON.parse(B)}catch(C){console.error(nA.red
("Error: Invalid JSON arguments")),console.error(String(C)),process.exit(1)}...});
```

**After:**
```javascript
// commands/call.js - Pure business logic
export async function handleCallCommand(toolIdentifier, argsInput, options, dependencies) {
  const { server, tool } = parseToolIdentifier(toolIdentifier);
  const argsString = argsInput === '-' 
    ? await readStdinAsJson() 
    : argsInput;
  
  const parsedArgs = parseJsonArgs(argsString);
  const state = validateMcpState();
  const result = await invokeToolWithRetry(server, tool, parsedArgs, options);
  
  outputResult(result, options);
  await trackSuccess(toolIdentifier, result);
}

// Each function has a single responsibility
async function readStdinAsJson() { /* ... */ }
function parseJsonArgs(input) { /* ... */ }
function validateMcpState() { /* ... */ }
```

### 4. Error Handling

**Before:**
```javascript
// Inconsistent error handling
if(B.length!==2||!B[0]||!B[1])console.error(nA.red(`Error: Invalid tool 
identifier '${A}'`)),console.error("Expected format: <server>/<tool>"),
process.exit(1);
```

**After:**
```javascript
// Consistent, well-structured error handling
export function parseToolIdentifier(toolString) {
  const parts = toolString.split('/');
  
  if (parts.length !== 2 || !parts[0] || !parts[1]) {
    console.error(chalk.red(`Error: Invalid tool identifier '${toolString}'`));
    console.error('Expected format: <server>/<tool>');
    process.exit(1);
  }
  
  return {
    server: parts[0],
    tool: parts[1]
  };
}
```

### 5. Documentation

**Before:**
```javascript
// No documentation
function l$A(){try{let A=DQ1(),B=no2(A,"utf-8");return JSON.parse(B)}catch{...}}
```

**After:**
```javascript
/**
 * Reads and parses the MCP state file
 * 
 * The MCP state file contains information about connected servers,
 * available tools, and resources. It's located in the user's home
 * directory under .claude/state/mcp.json
 * 
 * @returns {Object} Parsed MCP state containing clients, tools, and resources
 * @throws {Error} If the state file doesn't exist or is invalid
 * 
 * @example
 * const state = readMcpState();
 * console.log(state.clients.length); // Number of connected servers
 */
export function readMcpState() {
  // Implementation
}
```

## Module-by-Module Refactoring

### MCP State Reader

**Purpose:** Read and parse MCP configuration

**Before:** `l$A()` - Unclear, embedded in main file

**After:** `utils/mcpStateReader.js`
- `getMcpStatePath()` - Get state file location
- `readMcpState()` - Read and parse state
- Clear error messages
- Proper exports

### Tool Identifier Parser

**Purpose:** Parse and format tool identifiers

**Before:** `ao2()` - Unclear purpose

**After:** `utils/toolIdentifier.js`
- `parseToolIdentifier()` - Parse server/tool format
- `formatToolName()` - Format MCP tool names
- `buildToolName()` - Build full tool name
- Validation logic

### Commands

**Purpose:** Handle individual CLI commands

**Before:** Inline action handlers

**After:** Separate command modules
- `commands/servers.js` - List servers
- `commands/tools.js` - List tools
- `commands/info.js` - Show tool info
- `commands/call.js` - Invoke tools
- `commands/grep.js` - Search tools
- `commands/resources.js` - List resources

Each command module:
- Exports a single handler function
- Handles one command
- Uses utilities for common tasks
- Tracks telemetry
- Returns proper exit codes

### Core

**Purpose:** Core application logic

**After:** `core/mcpCli.js`
- `createMcpCli()` - Build CLI program
- `runMcpCli()` - Execute CLI with error handling
- Dependency injection support
- Telemetry integration

## Testing Strategy

The refactored code is easily testable:

```javascript
// commands/servers.test.js
import { jest } from '@jest/globals';
import { handleServersCommand } from './servers.js';

jest.mock('../utils/mcpStateReader.js', () => ({
  readMcpState: jest.fn(() => ({
    clients: [
      {
        name: 'test-server',
        type: 'connected',
        capabilities: { tools: true, resources: false }
      }
    ]
  }))
}));

test('handleServersCommand outputs JSON correctly', async () => {
  const consoleSpy = jest.spyOn(console, 'log');
  
  await handleServersCommand({ json: true });
  
  expect(consoleSpy).toHaveBeenCalled();
  const output = JSON.parse(consoleSpy.mock.calls[0][0]);
  expect(output).toHaveLength(1);
  expect(output[0].name).toBe('test-server');
  expect(output[0].hasTools).toBe(true);
});
```

## Benefits

### For Developers

1. **Easy to Understand** - Clear module boundaries
2. **Quick to Modify** - Change one thing at a time
3. **Simple to Test** - Mock dependencies easily
4. **Fast to Debug** - Isolated components
5. **Safe to Refactor** - Well-defined interfaces

### For the Codebase

1. **Maintainable** - Easy to update and extend
2. **Scalable** - Simple to add new commands
3. **Reliable** - Testable components
4. **Documented** - Clear purpose and usage
5. **Consistent** - Standard patterns throughout

## Migration Path

To fully migrate to the refactored structure:

1. **Extract remaining functionality** from the bundle
2. **Add TypeScript types** for better safety
3. **Implement unit tests** for each module
4. **Setup build process** to bundle for distribution
5. **Add integration tests** for command workflows
6. **Document all public APIs** with JSDoc
7. **Create developer guide** for contributors

## Conclusion

The refactored code demonstrates best practices:
- **Modular design**
- **Clear naming**
- **Separation of concerns**
- **Proper error handling**
- **Comprehensive documentation**
- **Testable components**

This makes the codebase maintainable, understandable, and ready for future enhancements.
