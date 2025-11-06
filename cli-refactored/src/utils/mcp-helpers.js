export function parseToolIdentifier(toolId) {
  const parts = toolId.split('/');
  
  if (parts.length !== 2 || !parts[0] || !parts[1]) {
    console.error(`Error: Invalid tool identifier '${toolId}'`);
    console.error('Expected format: <server>/<tool>');
    process.exit(1);
  }
  
  return { server: parts[0], tool: parts[1] };
}

export function getMCPStateFromFd(readFdFunc, getFdFunc) {
  try {
    const fd = getFdFunc();
    const content = readFdFunc(fd, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error('Error: MCP state not available');
    console.error('The mcp command is only available within a Claude Code session');
    process.exit(1);
  }
}
