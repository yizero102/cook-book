export async function cliEntry(dependencies) {
  const { 
    isClaudeCodeSession,
    runMCPCLI,
    runRipgrep,
    mainCLI,
    instrumentTimings 
  } = dependencies;

  instrumentTimings('cli_entry');
  instrumentTimings('cli_imports_loaded');

  if (isClaudeCodeSession() && process.argv[2] === '--mcp-cli') {
    const mcpArgs = process.argv.slice(3);
    process.exit(await runMCPCLI(mcpArgs));
  }

  if (process.argv[2] === '--ripgrep') {
    instrumentTimings('cli_ripgrep_path');
    const ripgrepArgs = process.argv.slice(3);
    process.exitCode = runRipgrep(ripgrepArgs);
    return;
  }

  instrumentTimings('cli_before_main_import');
  await mainCLI();
  instrumentTimings('cli_after_main_complete');
}

export function detectClientType() {
  if (process.env.GITHUB_ACTIONS === 'true') {
    return 'github-action';
  }
  if (process.env.CLAUDE_CODE_ENTRYPOINT === 'sdk-ts') {
    return 'sdk-typescript';
  }
  if (process.env.CLAUDE_CODE_ENTRYPOINT === 'sdk-py') {
    return 'sdk-python';
  }
  if (process.env.CLAUDE_CODE_ENTRYPOINT === 'sdk-cli') {
    return 'sdk-cli';
  }
  if (process.env.CLAUDE_CODE_ENTRYPOINT === 'claude-vscode') {
    return 'claude-vscode';
  }
  if (
    process.env.CLAUDE_CODE_SESSION_ACCESS_TOKEN ||
    process.env.CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR
  ) {
    return 'remote';
  }
  return 'cli';
}

export function setEntrypoint(isSDKMode) {
  if (process.env.CLAUDE_CODE_ENTRYPOINT) {
    return;
  }

  const args = process.argv.slice(2);
  const mcpIndex = args.indexOf('mcp');
  
  if (mcpIndex !== -1 && args[mcpIndex + 1] === 'serve') {
    process.env.CLAUDE_CODE_ENTRYPOINT = 'mcp';
    return;
  }

  if (process.env.CLAUDE_CODE_ACTION) {
    process.env.CLAUDE_CODE_ENTRYPOINT = 'claude-code-github-action';
    return;
  }

  process.env.CLAUDE_CODE_ENTRYPOINT = isSDKMode ? 'sdk-cli' : 'cli';
}

export function shouldRunInQuietMode() {
  const args = process.argv.slice(2);
  const hasPrintFlag = args.includes('-p') || args.includes('--print');
  const hasSDKUrl = args.some((arg) => arg.startsWith('--sdk-url'));
  return hasPrintFlag || hasSDKUrl || !process.stdout.isTTY;
}

export function isDebugMode() {
  const args = process.argv;
  
  const hasInspectFlag = process.execArgv.some((arg) => {
    return /--inspect(-brk)?|--debug(-brk)?/.test(arg);
  });
  
  const hasNodeOptions =
    process.env.NODE_OPTIONS &&
    /--inspect(-brk)?|--debug(-brk)?/.test(process.env.NODE_OPTIONS);

  try {
    const inspector = global.require('inspector');
    return !!inspector.url() || hasInspectFlag || hasNodeOptions;
  } catch {
    return hasInspectFlag || hasNodeOptions;
  }
}
