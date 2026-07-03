export interface LogMetadata {
  source?: string;
  correlationId?: string;
  component?: string;
  action?: string;
  stack?: string;
  [key: string]: any;
}

export interface ILogger {
  info(message: string, meta?: LogMetadata): void;
  warn(message: string, meta?: LogMetadata): void;
  error(error: Error, meta?: LogMetadata): void;
  debug(message: string, meta?: LogMetadata): void;
}

export class ConsoleLogger implements ILogger {
  private formatOutput(level: string, message: string, meta?: LogMetadata, err?: Error): string {
    const payload = {
      timestamp: new Date().toISOString(),
      level,
      message,
      metadata: meta || {},
      errorName: err?.name,
      errorMessage: err?.message,
      stack: err?.stack || meta?.stack
    };
    return JSON.stringify(payload);
  }

  info(message: string, meta?: LogMetadata): void {
    console.info(this.formatOutput('INFO', message, meta));
  }

  warn(message: string, meta?: LogMetadata): void {
    console.warn(this.formatOutput('WARN', message, meta));
  }

  error(error: Error, meta?: LogMetadata): void {
    console.error(this.formatOutput('ERROR', error.message, meta, error));
  }

  debug(message: string, meta?: LogMetadata): void {
    console.debug(this.formatOutput('DEBUG', message, meta));
  }
}
