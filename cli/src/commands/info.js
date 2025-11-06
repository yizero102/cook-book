import chalk from 'chalk';
import { readMcpState } from '../utils/mcpStateReader.js';
import { parseToolIdentifier, buildToolName } from '../utils/toolIdentifier.js';
import { trackEvent } from '../utils/telemetry.js';

export async function handleInfoCommand(toolIdentifier, options) {
  const state = readMcpState();
  const { server, tool } = parseToolIdentifier(toolIdentifier);
  
  const fullToolName = buildToolName(server, tool);
  const toolInfo = state.tools.find((t) => t.name === fullToolName);
  
  if (!toolInfo) {
    console.error(chalk.red(`Error: Tool '${toolIdentifier}' not found`));
    await trackEvent('tengu_mcp_cli_command_executed', {
      command: 'info',
      tool_found: false
    });
    process.exit(1);
  }
  
  const description = typeof toolInfo.description === 'string' 
    ? toolInfo.description 
    : '';
  
  if (options.json) {
    const output = {
      server,
      name: tool,
      description,
      inputSchema: toolInfo.inputJSONSchema || {}
    };
    console.log(JSON.stringify(output));
  } else {
    console.log(chalk.bold(`Tool: ${toolIdentifier}`));
    console.log(chalk.dim(`Server: ${server}`));
    if (description) {
      console.log(chalk.dim(`Description: ${description}`));
    }
    console.log();
    console.log(chalk.bold('Input Schema:'));
    console.log(JSON.stringify(toolInfo.inputJSONSchema || {}, null, 2));
  }
  
  await trackEvent('tengu_mcp_cli_command_executed', {
    command: 'info',
    tool_found: true
  });
}
