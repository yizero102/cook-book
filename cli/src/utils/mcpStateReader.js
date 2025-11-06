import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import chalk from 'chalk';

export function getMcpStatePath() {
  const stateDir = join(homedir(), '.claude', 'state');
  return join(stateDir, 'mcp.json');
}

export function readMcpState() {
  try {
    const statePath = getMcpStatePath();
    if (!existsSync(statePath)) {
      throw new Error('MCP state file not found');
    }
    const content = readFileSync(statePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error(chalk.red('Error: MCP state not available'));
    console.error('The mcp command is only available within a Claude Code session');
    process.exit(1);
  }
}
