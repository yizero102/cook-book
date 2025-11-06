import chalk from 'chalk';

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

export function formatToolName(toolName) {
  const match = toolName.match(/^mcp__([^_]+)__(.+)$/);
  if (!match) {
    return {
      server: 'unknown',
      name: toolName
    };
  }
  
  return {
    server: match[1],
    name: match[2]
  };
}

export function buildToolName(server, tool) {
  return `mcp__${server}__${tool}`;
}
