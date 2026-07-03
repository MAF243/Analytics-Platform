import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './assets/main.css';
import App from './app/App.vue';
import router from './router';
import { container } from './di/container';
import { SentryTelemetryProvider } from './observability/SentryTelemetryProvider';
import { setTelemetryProvider, reportError } from './observability';

const app = createApp(App);

const sentryDsn = import.meta.env.VITE_SENTRY_DSN;
if (sentryDsn) {
  const sentryProvider = new SentryTelemetryProvider(app, router, sentryDsn);
  setTelemetryProvider(sentryProvider);
}

// Centralized Vue Error Handler
app.config.errorHandler = (err: any, instance, info) => {
  const errorObj = err instanceof Error ? err : new Error(String(err));
  container.logger.error(errorObj, {
    source: 'Vue:errorHandler',
    info,
    component: instance?.$options?.name || 'AnonymousComponent'
  });
  reportError(errorObj, { source: 'Vue:errorHandler', info });
};

// Global Window Error Handler
window.onerror = (message, source, lineno, colno, error) => {
  const errorObj = error || new Error(String(message));
  container.logger.error(errorObj, {
    source: 'window:onerror',
    file: source,
    line: lineno,
    col: colno
  });
  reportError(errorObj, { source: 'window:onerror' });
  return true; // Prevent default browser logging
};

// Global Unhandled Promise Rejection
window.onunhandledrejection = (event) => {
  const errorObj = event.reason instanceof Error ? event.reason : new Error(String(event.reason));
  container.logger.error(errorObj, {
    source: 'window:onunhandledrejection'
  });
  reportError(errorObj, { source: 'window:onunhandledrejection' });
};

app.use(createPinia());
app.use(router);

app.mount('#app');
