import chalk from 'chalk';
import { readMcpState } from '../utils/mcpStateReader.js';
import { trackEvent } from '../utils/telemetry.js';

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
    state.clients.forEach((client) => {
      const statusColor = client.type === 'connected' 
        ? chalk.green('connected')
        : client.type === 'failed' 
        ? chalk.red('failed')
        : chalk.yellow(client.type);
      
      let capabilities = '';
      if (client.type === 'connected') {
        const caps = [];
        if (client.capabilities?.tools) caps.push('tools');
        if (client.capabilities?.resources) caps.push('resources');
        if (client.capabilities?.prompts) caps.push('prompts');
        if (caps.length > 0) {
          capabilities = ` (${caps.join(', ')})`;
        }
      }
      
      console.log(`${client.name} - ${statusColor}${capabilities}`);
    });
  }
  
  await trackEvent('tengu_mcp_cli_command_executed', {
    command: 'servers',
    server_count: state.clients.length
  });
}
