import chalk from 'chalk';
import { readMcpState } from '../utils/mcpStateReader.js';
import { formatToolName } from '../utils/toolIdentifier.js';
import { trackEvent } from '../utils/telemetry.js';

export async function handleGrepCommand(pattern, options) {
  const state = readMcpState();
  
  let regex;
  try {
    regex = new RegExp(pattern, options.ignoreCase ? 'i' : '');
  } catch (error) {
    console.error(chalk.red('Error: Invalid regex pattern'));
    console.error(String(error));
    process.exit(1);
  }
  
  const matchedTools = state.tools.filter((tool) => {
    const description = typeof tool.description === 'string' ? tool.description : '';
    const { server, name } = formatToolName(tool.name);
    const fullName = `${server}/${name}`;
    
    return regex.test(fullName) || regex.test(description);
  });
  
  if (options.json) {
    const output = matchedTools.map((tool) => {
      const { server, name } = formatToolName(tool.name);
      return {
        server,
        name,
        description: typeof tool.description === 'string' ? tool.description : ''
      };
    });
    console.log(JSON.stringify(output));
  } else {
    if (matchedTools.length === 0) {
      console.log(chalk.yellow('No tools found matching pattern'));
      process.exit(0);
    }
    
    matchedTools.forEach((tool) => {
      const { server, name } = formatToolName(tool.name);
      const description = typeof tool.description === 'string' ? tool.description : '';
      
      console.log(chalk.bold(`${server}/${name}`));
      
      if (description) {
        const truncated = description.length > 100 
          ? description.slice(0, 100) + '...' 
          : description;
        console.log(chalk.dim(`  ${truncated}`));
      }
      
      console.log();
    });
  }
  
  await trackEvent('tengu_mcp_cli_command_executed', {
    command: 'grep',
    match_count: matchedTools.length
  });
}
