import { readMcpState } from '../utils/mcpStateReader.js';
import { trackEvent } from '../utils/telemetry.js';

export async function handleResourcesCommand(serverFilter, options) {
  const state = readMcpState();
  let resources = [];
  
  if (serverFilter) {
    resources = state.resources[serverFilter] || [];
  } else {
    resources = Object.values(state.resources).flat();
  }
  
  if (options.json) {
    console.log(JSON.stringify(resources));
  } else {
    resources.forEach((resource) => {
      console.log(`${resource.server}/${resource.name || resource.uri}`);
    });
  }
  
  await trackEvent('tengu_mcp_cli_command_executed', {
    command: 'resources',
    resource_count: resources.length,
    filtered: !!serverFilter
  });
}
