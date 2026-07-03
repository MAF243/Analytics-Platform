import { ConsoleTelemetryProvider } from './ConsoleTelemetryProvider';
import type { ITelemetryProvider } from './ITelemetryProvider';

// Injectable instance (can be swapped in Phase 6 with SentryTelemetryProvider)
export let telemetry: ITelemetryProvider = new ConsoleTelemetryProvider();

export const setTelemetryProvider = (provider: ITelemetryProvider) => {
  telemetry = provider;
};

export const reportTelemetry = (eventName: string, properties?: Record<string, any>) => {
  telemetry.trackEvent(eventName, properties);
};

export const reportError = (error: Error | unknown, context?: Record<string, any>) => {
  telemetry.trackError(error, context);
};

export const reportMetric = (metricName: string, value: number, properties?: Record<string, any>) => {
  telemetry.trackMetric(metricName, value, properties);
};
