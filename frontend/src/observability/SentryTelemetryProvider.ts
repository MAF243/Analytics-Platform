import * as Sentry from '@sentry/vue';
import type { ITelemetryProvider } from './ITelemetryProvider';
import type { App } from 'vue';

export class SentryTelemetryProvider implements ITelemetryProvider {
  constructor(app: App, router: any, dsn: string) {
    if (dsn) {
      Sentry.init({
        app,
        dsn,
        integrations: [
          Sentry.browserTracingIntegration({ router }),
          Sentry.replayIntegration(),
        ],
        tracesSampleRate: 1.0,
        replaysSessionSampleRate: 0.1,
        replaysOnErrorSampleRate: 1.0,
      });
      console.log('[Telemetry] Sentry initialized.');
    }
  }

  trackEvent(eventName: string, properties?: Record<string, any>): void {
    Sentry.addBreadcrumb({
      category: 'event',
      message: eventName,
      data: properties,
      level: 'info',
    });
  }

  trackError(error: Error | unknown, context?: Record<string, any>): void {
    Sentry.captureException(error, { extra: context });
  }

  trackMetric(metricName: string, value: number, properties?: Record<string, any>): void {
    // Sentry metrics API (optional, can also use breadcrumbs or transactions)
    // Here we use a generic breadcrumb as fallback, or custom measurements.
    Sentry.metrics?.distribution(metricName, value, properties);
  }
}
