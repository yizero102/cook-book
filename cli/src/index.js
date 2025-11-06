#!/usr/bin/env node

import { runMcpCli } from './core/mcpCli.js';

const COREPACK_ENV = 'COREPACK_ENABLE_AUTO_PIN';
process.env[COREPACK_ENV] = '0';

function trackPerformance(marker) {
}

function isPlatformSupported() {
  return true;
}

async function main() {
  trackPerformance('cli_entry');
  trackPerformance('cli_imports_loaded');
  
  if (isPlatformSupported() && process.argv[2] === '--mcp-cli') {
    const mcpArgs = process.argv.slice(3);
    process.exit(await runMcpCli(mcpArgs));
  }
  
  if (process.argv[2] === '--ripgrep') {
    trackPerformance('cli_ripgrep_path');
    const ripgrepArgs = process.argv.slice(3);
    
    try {
      const { ripgrepMain } = await import('./ripgrep/index.js');
      process.exitCode = ripgrepMain(ripgrepArgs);
      return;
    } catch (error) {
      console.error('Error loading ripgrep:', error);
      process.exit(1);
    }
  }
  
  trackPerformance('cli_before_main_import');
  
  try {
    const { main: mainFunction } = await import('./main/index.js');
    trackPerformance('cli_after_main_import');
    await mainFunction();
    trackPerformance('cli_after_main_complete');
  } catch (error) {
    console.error('Error in main:', error);
    process.exit(1);
  }
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
