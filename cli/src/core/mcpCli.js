import { Command } from 'commander';
import chalk from 'chalk';
import {
  handleServersCommand,
  handleToolsCommand,
  handleInfoCommand,
  handleCallCommand,
  handleGrepCommand,
  handleResourcesCommand
} from '../commands/index.js';

export function createMcpCli(dependencies = {}) {
  const program = new Command();
  
  program
    .name('mcp-cli')
    .description('Interact with MCP servers and tools')
    .version('1.0.0');
  
  program
    .command('servers')
    .description('List all connected MCP servers')
    .option('--json', 'Output in JSON format')
    .action(async (options) => {
      await handleServersCommand(options);
    });
  
  program
    .command('tools')
    .description('List all available tools')
    .argument('[server]', 'Filter by server name')
    .option('--json', 'Output in JSON format')
    .action(async (server, options) => {
      await handleToolsCommand(server, options);
    });
  
  program
    .command('info')
    .description('Get detailed information about a tool')
    .argument('<tool>', 'Tool identifier in format <server>/<tool>')
    .option('--json', 'Output in JSON format')
    .action(async (tool, options) => {
      await handleInfoCommand(tool, options);
    });
  
  program
    .command('call')
    .description('Invoke an MCP tool')
    .argument('<tool>', 'Tool identifier in format <server>/<tool>')
    .argument('<args>', 'Tool arguments as JSON string or "-" for stdin')
    .option('--json', 'Output in JSON format')
    .option('--timeout <ms>', 'Timeout in milliseconds', '30000')
    .option('--debug', 'Show debug output')
    .action(async (tool, args, options) => {
      await handleCallCommand(tool, args, options, dependencies);
    });
  
  program
    .command('grep')
    .description('Search tool names and descriptions using regex patterns')
    .argument('<pattern>', 'Regex pattern to search for')
    .option('--json', 'Output in JSON format')
    .option('-i, --ignore-case', 'Case insensitive search (default: true)', true)
    .action(async (pattern, options) => {
      await handleGrepCommand(pattern, options);
    });
  
  program
    .command('resources')
    .description('List MCP resources')
    .argument('[server]', 'Filter by server name')
    .option('--json', 'Output in JSON format')
    .action(async (server, options) => {
      await handleResourcesCommand(server, options);
    });
  
  return program;
}

export async function runMcpCli(args, dependencies = {}) {
  try {
    const program = createMcpCli(dependencies);
    
    if (dependencies.initTelemetry) {
      dependencies.initTelemetry();
    }
    
    if (dependencies.initLogger) {
      dependencies.initLogger();
    }
    
    await program.parseAsync(args, { from: 'user' });
    
    if (dependencies.flushLogger) {
      await dependencies.flushLogger()?.flush();
    }
    
    return 0;
  } catch (error) {
    console.error(chalk.red('Error:'), error);
    
    if (dependencies.flushLogger) {
      await dependencies.flushLogger()?.flush();
    }
    
    return 1;
  }
}
