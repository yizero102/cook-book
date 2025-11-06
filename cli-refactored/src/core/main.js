export async function main(dependencies) {
  const {
    instrumentTimings,
    detectClientType,
    setEntrypoint,
    shouldRunInQuietMode,
    initializeWarningHandlers,
    loadManagedSettings,
    eagerLoadSettings,
    initializeApp,
    runApp,
    setQuietMode,
    setClientType,
  } = dependencies;

  instrumentTimings('main_function_start');

  process.env.NoDefaultCurrentDirectoryInExePath = '1';
  
  setupProcessHandlers(dependencies);
  instrumentTimings('main_warning_handler_initialized');

  const isQuietMode = shouldRunInQuietMode();
  setQuietMode(isQuietMode);
  setEntrypoint(isQuietMode);
  
  if (!isQuietMode) {
    console.log('Starting Claude Code CLI...');
  }

  const clientType = detectClientType();
  setClientType(clientType);
  instrumentTimings('main_client_type_determined');

  eagerLoadSettings();
  instrumentTimings('main_before_init');

  loadManagedSettings();

  const initResult = await initializeApp();
  if (initResult instanceof Promise) {
    await initResult;
  }

  instrumentTimings('main_after_init');
  process.title = 'claude';

  await runApp();
  instrumentTimings('main_after_run');
}

function setupProcessHandlers(dependencies) {
  const { exitHandler, cleanupTimings } = dependencies;

  process.on('exit', () => {
    cleanupTimings();
  });

  process.on('SIGINT', () => {
    process.exit(0);
  });

  if (exitHandler) {
    process.on('exit', exitHandler);
  }
}
