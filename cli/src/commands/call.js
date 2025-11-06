import { readFileSync, existsSync } from 'fs';
import chalk from 'chalk';
import { parseToolIdentifier, buildToolName } from '../utils/toolIdentifier.js';
import { getMcpStatePath } from '../utils/mcpStateReader.js';
import { trackEvent } from '../utils/telemetry.js';

async function readStdinAsJson() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf-8').trim();
}

async function connectToMcpServer(server, config, mcpModule) {
  return await mcpModule.connectClient(server, config);
}

export async function handleCallCommand(toolIdentifier, argsInput, options, dependencies) {
  const { server, tool } = parseToolIdentifier(toolIdentifier);
  
  let argsString = argsInput;
  if (argsInput === '-') {
    argsString = await readStdinAsJson();
  }
  
  let parsedArgs;
  try {
    parsedArgs = JSON.parse(argsString);
  } catch (error) {
    console.error(chalk.red('Error: Invalid JSON arguments'));
    console.error(String(error));
    process.exit(1);
  }
  
  const statePath = getMcpStatePath();
  if (!existsSync(statePath)) {
    console.error(chalk.red('Error: MCP state file not found. Is Claude Code running?'));
    process.exit(1);
  }
  
  let state;
  try {
    state = JSON.parse(readFileSync(statePath, 'utf-8'));
  } catch (error) {
    console.error(chalk.red('Error reading MCP state:'), String(error));
    process.exit(1);
  }
  
  const serverConfig = state.configs?.[server];
  if (!serverConfig) {
    console.error(chalk.red(`Error: Server '${server}' not found in state`));
    process.exit(1);
  }
  
  if (options.debug) {
    console.error(`Connecting to ${server} (${serverConfig.type})...`);
  }
  
  const startTime = Date.now();
  const fullToolName = buildToolName(server, tool);
  
  try {
    const connection = await connectToMcpServer(server, serverConfig, dependencies.mcpModule);
    
    if (connection.client.type !== 'connected') {
      console.error(chalk.red(`Error: Failed to connect to server '${server}'`));
      const duration = Date.now() - startTime;
      
      await trackEvent('tengu_tool_use_error', {
        toolName: fullToolName,
        isMcp: true,
        error: 'connection_failed',
        durationMs: duration
      });
      
      await trackEvent('tengu_mcp_cli_command_executed', {
        command: 'call',
        tool_name: fullToolName,
        success: false,
        error_type: 'connection_failed',
        duration_ms: duration
      });
      
      process.exit(1);
    }
    
    if (options.debug) {
      console.error(`Calling tool ${tool}...`);
    }
    
    const timeout = parseInt(options.timeout, 10);
    const result = await connection.client.client.callTool({
      name: tool,
      arguments: parsedArgs
    }, dependencies.mcpOptions, {
      signal: AbortSignal.timeout(timeout)
    });
    
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
      durationMs: duration
    });
    
    await trackEvent('tengu_mcp_cli_command_executed', {
      command: 'call',
      tool_name: fullToolName,
      success: true,
      duration_ms: duration
    });
    
    process.exit(0);
  } catch (error) {
    console.error(chalk.red('Error calling tool:'), String(error));
    
    const duration = Date.now() - startTime;
    const errorMessage = String(error).slice(0, 2000);
    
    await trackEvent('tengu_tool_use_error', {
      toolName: fullToolName,
      isMcp: true,
      error: errorMessage,
      durationMs: duration
    });
    
    await trackEvent('tengu_mcp_cli_command_executed', {
      command: 'call',
      tool_name: fullToolName,
      success: false,
      error_type: 'tool_execution_failed',
      duration_ms: duration
    });
    
    process.exit(1);
  }
}
