export async function trackEvent(eventName, properties = {}) {
  try {
    const telemetryModule = await import('../core/telemetryCore.js');
    if (telemetryModule && telemetryModule.track) {
      await telemetryModule.track(eventName, properties);
    }
  } catch (error) {
    }
}
