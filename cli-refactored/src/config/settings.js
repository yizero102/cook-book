import { existsSync, readFileSync, writeFileSync } from 'fs';
import { resolve } from 'path';

export function eagerLoadSettings() {
  const settingsIndex = process.argv.findIndex((arg) => arg === '--settings');
  
  if (settingsIndex !== -1 && settingsIndex + 1 < process.argv.length) {
    const settingsValue = process.argv[settingsIndex + 1];
    if (settingsValue) {
      processSettingsFlag(settingsValue);
    }
  }

  const settingSourcesIndex = process.argv.findIndex((arg) => arg === '--setting-sources');
  
  if (settingSourcesIndex !== -1 && settingSourcesIndex + 1 < process.argv.length) {
    const sourcesValue = process.argv[settingSourcesIndex + 1];
    if (sourcesValue !== undefined) {
      processSettingSourcesFlag(sourcesValue);
    }
  }
}

export function processSettingsFlag(settingsInput, dependencies = {}) {
  const { colorize, applySettings, reloadConfig } = dependencies;

  try {
    const trimmed = settingsInput.trim();
    const isJSON = trimmed.startsWith('{') && trimmed.endsWith('}');
    let settingsFile;

    if (isJSON) {
      if (!isValidJSON(trimmed)) {
        console.error(colorize?.red('Error: Invalid JSON provided to --settings') || 'Error: Invalid JSON');
        process.exit(1);
      }
      
      settingsFile = createTempFile('claude-settings', '.json');
      writeFileSync(settingsFile, trimmed, 'utf8');
    } else {
      const resolvedPath = resolvePath(process.cwd(), settingsInput);
      
      if (!existsSync(resolvedPath)) {
        console.error(
          colorize?.red(`Error: Settings file not found: ${resolvedPath}`) || 
          `Error: Settings file not found: ${resolvedPath}`
        );
        process.exit(1);
      }
      
      settingsFile = resolvedPath;
    }

    applySettings?.(settingsFile);
    reloadConfig?.();
  } catch (error) {
    console.error(
      colorize?.red(`Error processing settings: ${error.message}`) || 
      `Error processing settings: ${error.message}`
    );
    process.exit(1);
  }
}

export function processSettingSourcesFlag(sourcesInput, dependencies = {}) {
  const { colorize, applySettingSources, reloadConfig } = dependencies;

  try {
    const sources = parseSettingSources(sourcesInput);
    applySettingSources?.(sources);
    reloadConfig?.();
  } catch (error) {
    console.error(
      colorize?.red(`Error processing --setting-sources: ${error.message}`) ||
      `Error processing --setting-sources: ${error.message}`
    );
    process.exit(1);
  }
}

export function loadManagedSettings(dependencies = {}) {
  const { readPolicySetting, trackEvent } = dependencies;

  try {
    const policySetting = readPolicySetting?.('policySettings');
    
    if (policySetting) {
      const keys = Object.keys(policySetting);
      trackEvent?.('tengu_managed_settings_loaded', {
        keyCount: keys.length,
        keys: keys.join(','),
      });
    }
  } catch (error) {
    }
}

function isValidJSON(str) {
  try {
    JSON.parse(str);
    return true;
  } catch {
    return false;
  }
}

function resolvePath(baseDir, path) {
  return resolve(baseDir, path);
}

function parseSettingSources(sourcesInput) {
  return sourcesInput.split(',').map((s) => s.trim()).filter(Boolean);
}

function createTempFile(prefix, extension) {
  const tmpDir = process.env.TMPDIR || '/tmp';
  const randomId = Math.random().toString(36).substring(7);
  return `${tmpDir}/${prefix}-${randomId}${extension}`;
}
