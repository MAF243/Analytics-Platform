import type { ITelemetryProvider } from './ITelemetryProvider';

export class ConsoleTelemetryProvider implements ITelemetryProvider {
  trackEvent(eventName: string, properties?: Record<string, any>): void {
    if (import.meta.env.DEV) {
      console.debug(`[Telemetry:Event] ${eventName}`, properties || '');
    }
  }

  trackError(error: Error | unknown, context?: Record<string, any>): void {
    console.error(`[Telemetry:Error]`, error, context || '');
  }

  trackMetric(metricName: string, value: number, properties?: Record<string, any>): void {
    if (import.meta.env.DEV) {
      console.debug(`[Telemetry:Metric] ${metricName}: ${value}`, properties || '');
    }
  }
}
