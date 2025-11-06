# Testing Guide

## Verification Strategy

This document outlines how to verify that the refactored code maintains the same functionality as the original bundled CLI.

## Prerequisites

- Node.js >= 18.0.0
- Original CLI at `../cli/cli.js`
- Refactored code in `./src/`

## Testing Approach

### 1. Unit Testing

Each module can be tested independently:

```javascript
// Example: Testing parseToolIdentifier
import { parseToolIdentifier } from './src/utils/mcp-helpers.js';

// Test valid input
const result = parseToolIdentifier('server/tool');
assert.equal(result.server, 'server');
assert.equal(result.tool, 'tool');

// Test invalid input (should exit)
try {
  parseToolIdentifier('invalid');
  assert.fail('Should have exited');
} catch (error) {
  // Expected
}
```

### 2. Integration Testing

Test command execution flow:

```javascript
import { createMCPCommands } from './src/commands/mcp-commands.js';

const mockDependencies = {
  getMCPState: () => ({ clients: [], tools: [], resources: {} }),
  parseToolIdentifier: (id) => ({ server: 's', tool: 't' }),
  colorize: {
    red: (t) => t,
    green: (t) => t,
    yellow: (t) => t,
    bold: (t) => t,
    dim: (t) => t,
  },
  trackEvent: async () => {},
  // ... other dependencies
};

const program = createMCPCommands(mockDependencies);
// Test commands
```

### 3. Functional Testing

Compare output of original vs refactored:

#### Test 1: Version Check
```bash
# Original
node ../cli/cli.js --version
# Expected: 2.0.34 (Claude Code)

# Refactored (when integrated)
node integrated-cli.js --version
# Expected: Same output
```

#### Test 2: Help Output
```bash
# Original
node ../cli/cli.js --help | head -20

# Refactored (when integrated)
node integrated-cli.js --help | head -20

# Compare outputs
diff <(node ../cli/cli.js --help) <(node integrated-cli.js --help)
```

#### Test 3: MCP Commands (if MCP session available)
```bash
# Original
node ../cli/cli.js --mcp-cli servers --json

# Refactored
node integrated-cli.js --mcp-cli servers --json

# Compare JSON output
```

### 4. Manual Testing Checklist

- [ ] CLI starts without errors
- [ ] Help text displays correctly
- [ ] Version command works
- [ ] MCP commands execute (in Claude Code session)
  - [ ] `servers` command
  - [ ] `tools` command
  - [ ] `info` command
  - [ ] `call` command
  - [ ] `grep` command
  - [ ] `resources` command
- [ ] Settings loading works
  - [ ] `--settings` flag
  - [ ] `--setting-sources` flag
- [ ] Entry point routing works
  - [ ] MCP CLI mode
  - [ ] Ripgrep mode
  - [ ] Main CLI mode
- [ ] Process handlers work
  - [ ] SIGINT (Ctrl+C)
  - [ ] Exit cleanup

### 5. Regression Testing

Key functionality to verify:

1. **Command Parsing**: Arguments and options parsed correctly
2. **Error Handling**: Errors reported appropriately
3. **Output Format**: Text and JSON output match original
4. **Exit Codes**: Process exits with correct codes
5. **State Management**: MCP state read correctly
6. **Event Tracking**: Analytics events fired

### 6. Performance Testing

Compare execution times:

```bash
# Original
time node ../cli/cli.js --version

# Refactored
time node integrated-cli.js --version

# Should be similar (within 10%)
```

## Test Environment Setup

### Mock MCP State

Create a test MCP state file for testing:

```json
{
  "clients": [
    {
      "name": "test-server",
      "type": "connected",
      "capabilities": {
        "tools": true,
        "resources": true,
        "prompts": false
      }
    }
  ],
  "tools": [
    {
      "name": "mcp__test-server__test-tool",
      "description": "A test tool",
      "inputJSONSchema": {
        "type": "object",
        "properties": {
          "input": { "type": "string" }
        }
      }
    }
  ],
  "resources": {
    "test-server": [
      {
        "server": "test-server",
        "name": "test-resource",
        "uri": "test://resource"
      }
    ]
  },
  "configs": {
    "test-server": {
      "type": "stdio",
      "command": "test",
      "args": []
    }
  }
}
```

### Mock Dependencies

```javascript
export const mockDependencies = {
  getMCPState: () => require('./mock-mcp-state.json'),
  parseToolIdentifier: (id) => {
    const [server, tool] = id.split('/');
    return { server, tool };
  },
  colorize: {
    red: (text) => `\x1b[31m${text}\x1b[0m`,
    green: (text) => `\x1b[32m${text}\x1b[0m`,
    yellow: (text) => `\x1b[33m${text}\x1b[0m`,
    bold: (text) => `\x1b[1m${text}\x1b[0m`,
    dim: (text) => `\x1b[2m${text}\x1b[0m`,
  },
  trackEvent: async (event, data) => {
    console.log(`Event: ${event}`, data);
  },
  connectToMCPServer: async () => {
    throw new Error('Mock: Not implemented');
  },
  readFd: () => '{}',
  fdExists: () => true,
};
```

## Automated Test Script

```bash
#!/bin/bash

# test-comparison.sh

echo "=== Testing Original CLI ==="
node ../cli/cli.js --version

echo ""
echo "=== Testing Help Output ==="
node ../cli/cli.js --help | head -10

echo ""
echo "=== Checking File Sizes ==="
ls -lh ../cli/cli.js
du -sh ../cli-refactored/src/

echo ""
echo "=== Line Count Comparison ==="
echo "Original: $(wc -l < ../cli/cli.js) lines"
echo "Refactored: $(find src/ -name '*.js' -exec wc -l {} + | tail -1 | awk '{print $1}') lines"

echo ""
echo "All tests completed!"
```

## Expected Results

### Success Criteria

1. ✅ All unit tests pass
2. ✅ Integration tests execute without errors
3. ✅ Functional tests produce identical output
4. ✅ No regression in functionality
5. ✅ Performance within acceptable range
6. ✅ Code is more readable and maintainable

### Known Differences

- The refactored code does not include bundled dependencies
- Variable names are different (more descriptive)
- Structure is modular vs. monolithic
- File size is dramatically smaller (core logic only)

## Continuous Verification

To ensure ongoing compatibility:

1. Run tests before committing changes
2. Compare output with original CLI
3. Monitor for any behavioral differences
4. Update tests as features evolve

## Troubleshooting

### If Tests Fail

1. Check Node.js version (>= 18.0.0)
2. Verify all dependencies are mocked correctly
3. Ensure file paths are correct
4. Check for environment variable requirements
5. Compare error messages with original

### Common Issues

- **Import Errors**: Check module paths
- **Missing Dependencies**: Ensure all mocks are provided
- **Exit Code Mismatches**: Verify error handling
- **Output Differences**: Check formatting and colorization

## Conclusion

The refactored code should maintain 100% functional compatibility with the original while providing improved structure and readability. Regular testing ensures this compatibility is maintained over time.
