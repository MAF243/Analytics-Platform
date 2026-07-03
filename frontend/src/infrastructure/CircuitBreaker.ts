export const CircuitBreakerState = {
  CLOSED: 'CLOSED' as const,
  OPEN: 'OPEN' as const,
  HALF_OPEN: 'HALF_OPEN' as const
};
export type CircuitState = typeof CircuitBreakerState[keyof typeof CircuitBreakerState];

export interface CircuitBreakerConfig {
  failureThreshold: number;
  cooldownMs: number;
}

export class CircuitBreaker {
  private state: CircuitState = 'CLOSED';
  private failureCount = 0;
  private lastFailureTime = 0;

  private name: string;
  private config: CircuitBreakerConfig;

  constructor(
    name: string,
    config: CircuitBreakerConfig = { failureThreshold: 5, cooldownMs: 15000 }
  ) {
    this.name = name;
    this.config = config;
  }

  async execute<T>(action: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      const now = Date.now();
      if (now - this.lastFailureTime > this.config.cooldownMs) {
        this.transitionTo('HALF_OPEN');
      } else {
        throw new Error(`CircuitBreaker [${this.name}] is OPEN. Fast-failing request.`);
      }
    }

    try {
      const result = await action();
      if (this.state === 'HALF_OPEN') {
        this.transitionTo('CLOSED');
      }
      this.failureCount = 0;
      return result;
    } catch (error: any) {
      this.failureCount++;
      this.lastFailureTime = Date.now();

      const isExpectedError = error.statusCode === 409 || error.name === 'CanceledError';

      if (!isExpectedError && this.failureCount >= this.config.failureThreshold) {
        this.transitionTo('OPEN');
      } else if (this.state === 'HALF_OPEN' && !isExpectedError) {
        this.transitionTo('OPEN');
      }

      throw error;
    }
  }

  private transitionTo(newState: CircuitState) {
    console.warn(`CircuitBreaker [${this.name}] transitioned: ${this.state} -> ${newState}`);
    this.state = newState;
  }

  getState(): CircuitState { return this.state; }
}
