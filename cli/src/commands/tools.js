import { readMcpState } from '../utils/mcpStateReader.js';
import { formatToolName } from '../utils/toolIdentifier.js';
import { trackEvent } from '../utils/telemetry.js';

export async function handleToolsCommand(serverFilter, options) {
  const state = readMcpState();
  let tools = state.tools;
  
  if (serverFilter) {
    const prefix = `mcp__${serverFilter}__`;
    tools = tools.filter((tool) => tool.name.startsWith(prefix));
  }
  
  if (options.json) {
    const output = tools.map((tool) => {
      const { server, name } = formatToolName(tool.name);
      return {
        server,
        name,
        description: typeof tool.description === 'function' ? '' : tool.description
      };
    });
    console.log(JSON.stringify(output));
  } else if (serverFilter) {
    tools.forEach((tool) => {
      const match = tool.name.match(/^mcp__[^_]+__(.+)$/);
      const name = match?.[1] || tool.name;
      console.log(name);
    });
  } else {
    tools.forEach((tool) => {
      const { server, name } = formatToolName(tool.name);
      console.log(`${server}/${name}`);
    });
  }
  
  await trackEvent('tengu_mcp_cli_command_executed', {
    command: 'tools',
    tool_count: tools.length,
    filtered: !!serverFilter
  });
}
