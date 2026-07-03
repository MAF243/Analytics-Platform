export interface ITelemetryProvider {
  trackEvent(eventName: string, properties?: Record<string, any>): void;
  trackError(error: Error | unknown, context?: Record<string, any>): void;
  trackMetric(metricName: string, value: number, properties?: Record<string, any>): void;
}
