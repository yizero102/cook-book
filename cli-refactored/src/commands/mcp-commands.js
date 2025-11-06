import { Command } from 'commander';

export function createMCPCommands(dependencies) {
  const { 
    getMCPState, 
    parseToolIdentifier, 
    colorize, 
    trackEvent,
    connectToMCPServer,
    readFd,
    fdExists 
  } = dependencies;

  const mcpProgram = new Command()
    .name('mcp-cli')
    .description('Interact with MCP servers and tools')
    .version('1.0.0');

  mcpProgram
    .command('servers')
    .description('List all connected MCP servers')
    .option('--json', 'Output in JSON format')
    .action(async (options) => {
      const state = getMCPState();
      
      if (options.json) {
        console.log(
          JSON.stringify(
            state.clients.map((client) => ({
              name: client.name,
              type: client.type,
              hasTools: client.type === 'connected' && !!client.capabilities?.tools,
              hasResources: client.type === 'connected' && !!client.capabilities?.resources,
            })),
          ),
        );
      } else {
        state.clients.forEach((client) => {
          const statusColor =
            client.type === 'connected'
              ? colorize.green('connected')
              : client.type === 'failed'
                ? colorize.red('failed')
                : colorize.yellow(client.type);
          
          let capabilities = '';
          if (client.type === 'connected') {
            const caps = [];
            if (client.capabilities?.tools) caps.push('tools');
            if (client.capabilities?.resources) caps.push('resources');
            if (client.capabilities?.prompts) caps.push('prompts');
            if (caps.length > 0) capabilities = ` (${caps.join(', ')})`;
          }
          console.log(`${client.name} - ${statusColor}${capabilities}`);
        });
      }
      
      await trackEvent('tengu_mcp_cli_command_executed', {
        command: 'servers',
        server_count: state.clients.length,
      });
    });

  mcpProgram
    .command('tools')
    .description('List all available tools')
    .argument('[server]', 'Filter by server name')
    .option('--json', 'Output in JSON format')
    .action(async (serverFilter, options) => {
      let tools = getMCPState().tools;
      
      if (serverFilter) {
        const prefix = `mcp__${serverFilter}__`;
        tools = tools.filter((tool) => tool.name.startsWith(prefix));
      }
      
      if (options.json) {
        const toolsList = tools.map((tool) => {
          const match = tool.name.match(/^mcp__([^_]+)__(.+)$/);
          return {
            server: match?.[1] || 'unknown',
            name: match?.[2] || tool.name,
            description: typeof tool.description === 'function' ? '' : tool.description,
          };
        });
        console.log(JSON.stringify(toolsList));
      } else if (serverFilter) {
        tools.forEach((tool) => {
          const toolName = tool.name.match(/^mcp__[^_]+__(.+)$/)?.[1] || tool.name;
          console.log(`${toolName}`);
        });
      } else {
        tools.forEach((tool) => {
          const match = tool.name.match(/^mcp__([^_]+)__(.+)$/);
          const server = match?.[1] || 'unknown';
          const name = match?.[2] || tool.name;
          console.log(`${server}/${name}`);
        });
      }
      
      await trackEvent('tengu_mcp_cli_command_executed', {
        command: 'tools',
        tool_count: tools.length,
        filtered: !!serverFilter,
      });
    });

  mcpProgram
    .command('info')
    .description('Get detailed information about a tool')
    .argument('<tool>', 'Tool identifier in format <server>/<tool>')
    .option('--json', 'Output in JSON format')
    .action(async (toolId, options) => {
      const state = getMCPState();
      const { server, tool } = parseToolIdentifier(toolId);
      const toolName = `mcp__${server}__${tool}`;
      const toolInfo = state.tools.find((t) => t.name === toolName);
      
      if (!toolInfo) {
        console.error(colorize.red(`Error: Tool '${toolId}' not found`));
        await trackEvent('tengu_mcp_cli_command_executed', {
          command: 'info',
          tool_found: false,
        });
        process.exit(1);
      }
      
      const description = typeof toolInfo.description === 'string' ? toolInfo.description : '';
      
      if (options.json) {
        console.log(
          JSON.stringify({
            server,
            name: tool,
            description,
            inputSchema: toolInfo.inputJSONSchema || {},
          }),
        );
      } else {
        console.log(colorize.bold(`Tool: ${toolId}`));
        console.log(colorize.dim(`Server: ${server}`));
        if (description) {
          console.log(colorize.dim(`Description: ${description}`));
        }
        console.log();
        console.log(colorize.bold('Input Schema:'));
        console.log(JSON.stringify(toolInfo.inputJSONSchema || {}, null, 2));
      }
      
      await trackEvent('tengu_mcp_cli_command_executed', {
        command: 'info',
        tool_found: true,
      });
    });

  mcpProgram
    .command('call')
    .description('Invoke an MCP tool')
    .argument('<tool>', 'Tool identifier in format <server>/<tool>')
    .argument('<args>', 'Tool arguments as JSON string or "-" for stdin')
    .option('--json', 'Output in JSON format')
    .option('--timeout <ms>', 'Timeout in milliseconds', '30000')
    .option('--debug', 'Show debug output')
    .action(async (toolId, argsInput, options) => {
      const { server, tool } = parseToolIdentifier(toolId);
      
      let argsString = argsInput;
      if (argsInput === '-') {
        const chunks = [];
        for await (const chunk of process.stdin) {
          chunks.push(chunk);
        }
        argsString = Buffer.concat(chunks).toString('utf-8').trim();
      }
      
      let args;
      try {
        args = JSON.parse(argsString);
      } catch (error) {
        console.error(colorize.red('Error: Invalid JSON arguments'));
        console.error(String(error));
        process.exit(1);
      }
      
      const stateFd = getMCPState.fd();
      if (!fdExists(stateFd)) {
        console.error(
          colorize.red('Error: MCP state file not found. Is Claude Code running?'),
        );
        process.exit(1);
      }
      
      let state;
      try {
        state = JSON.parse(readFd(stateFd, 'utf-8'));
      } catch (error) {
        console.error(colorize.red('Error reading MCP state:'), String(error));
        process.exit(1);
      }
      
      const serverConfig = state.configs?.[server];
      if (!serverConfig) {
        console.error(colorize.red(`Error: Server '${server}' not found in state`));
        process.exit(1);
      }
      
      if (options.debug) {
        console.error(`Connecting to ${server} (${serverConfig.type})...`);
      }
      
      const startTime = Date.now();
      const fullToolName = `mcp__${server}__${tool}`;
      
      try {
        const connection = await connectToMCPServer(server, serverConfig);
        
        if (connection.client.type !== 'connected') {
          console.error(colorize.red(`Error: Failed to connect to server '${server}'`));
          const duration = Date.now() - startTime;
          await trackEvent('tengu_tool_use_error', {
            toolName: fullToolName,
            isMcp: true,
            error: 'connection_failed',
            durationMs: duration,
          });
          await trackEvent('tengu_mcp_cli_command_executed', {
            command: 'call',
            tool_name: fullToolName,
            success: false,
            error_type: 'connection_failed',
            duration_ms: duration,
          });
          process.exit(1);
        }
        
        if (options.debug) {
          console.error(`Calling tool ${tool}...`);
        }
        
        const result = await connection.client.client.callTool(
          { name: tool, arguments: args },
          undefined,
          { signal: AbortSignal.timeout(parseInt(options.timeout, 10)) }
        );
        
        connection.client.client.close();
        
        if (options.json) {
          console.log(JSON.stringify(result));
        } else if (typeof result === 'string') {
          console.log(result);
        } else {
          console.log(JSON.stringify(result, null, 2));
        }
        
        const duration = Date.now() - startTime;
        await trackEvent('tengu_tool_use_success', {
          toolName: fullToolName,
          isMcp: true,
          durationMs: duration,
        });
        await trackEvent('tengu_mcp_cli_command_executed', {
          command: 'call',
          tool_name: fullToolName,
          success: true,
          duration_ms: duration,
        });
        process.exit(0);
      } catch (error) {
        console.error(colorize.red('Error calling tool:'), String(error));
        const duration = Date.now() - startTime;
        const errorMessage = String(error).slice(0, 2000);
        await trackEvent('tengu_tool_use_error', {
          toolName: fullToolName,
          isMcp: true,
          error: errorMessage,
          durationMs: duration,
        });
        await trackEvent('tengu_mcp_cli_command_executed', {
          command: 'call',
          tool_name: fullToolName,
          success: false,
          error_type: 'tool_execution_failed',
          duration_ms: duration,
        });
        process.exit(1);
      }
    });

  mcpProgram
    .command('grep')
    .description('Search tool names and descriptions using regex patterns')
    .argument('<pattern>', 'Regex pattern to search for')
    .option('--json', 'Output in JSON format')
    .option('-i, --ignore-case', 'Case insensitive search (default: true)', true)
    .action(async (pattern, options) => {
      const state = getMCPState();
      let regex;
      
      try {
        regex = new RegExp(pattern, options.ignoreCase ? 'i' : '');
      } catch (error) {
        console.error(colorize.red('Error: Invalid regex pattern'));
        console.error(String(error));
        process.exit(1);
      }
      
      const matchingTools = state.tools.filter((tool) => {
        const description = typeof tool.description === 'string' ? tool.description : '';
        const match = tool.name.match(/^mcp__([^_]+)__(.+)$/);
        const fullName = match ? `${match[1]}/${match[2]}` : tool.name;
        return regex.test(fullName) || regex.test(description);
      });
      
      if (options.json) {
        const results = matchingTools.map((tool) => {
          const match = tool.name.match(/^mcp__([^_]+)__(.+)$/);
          return {
            server: match?.[1] || 'unknown',
            name: match?.[2] || tool.name,
            description: typeof tool.description === 'string' ? tool.description : '',
          };
        });
        console.log(JSON.stringify(results));
      } else {
        if (matchingTools.length === 0) {
          console.log(colorize.yellow('No tools found matching pattern'));
          process.exit(0);
        }
        
        matchingTools.forEach((tool) => {
          const match = tool.name.match(/^mcp__([^_]+)__(.+)$/);
          const server = match?.[1] || 'unknown';
          const name = match?.[2] || tool.name;
          const description = typeof tool.description === 'string' ? tool.description : '';
          
          console.log(colorize.bold(`${server}/${name}`));
          if (description) {
            const truncated = description.length > 100 ? description.slice(0, 100) + '...' : description;
            console.log(colorize.dim(`  ${truncated}`));
          }
          console.log();
        });
      }
      
      await trackEvent('tengu_mcp_cli_command_executed', {
        command: 'grep',
        match_count: matchingTools.length,
      });
    });

  mcpProgram
    .command('resources')
    .description('List MCP resources')
    .argument('[server]', 'Filter by server name')
    .option('--json', 'Output in JSON format')
    .action(async (serverFilter, options) => {
      const state = getMCPState();
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
        filtered: !!serverFilter,
      });
    });

  return mcpProgram;
}

export async function runMCPCLI(args, mcpProgram, flushOutput) {
  try {
    await mcpProgram.parseAsync(args, { from: 'user' });
    await flushOutput?.();
    return 0;
  } catch (error) {
    console.error(colorize.red('Error:'), error);
    await flushOutput?.();
    return 1;
  }
}
