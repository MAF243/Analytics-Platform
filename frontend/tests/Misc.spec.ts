import { describe, it, expect, vi } from 'vitest';
import { ApiException } from '../src/exceptions';
import { ConsoleLogger } from '../src/observability/logger';
import { container } from '../src/di/container';

describe('Exceptions', () => {
  it('creates ApiException correctly', () => {
    const ex = new ApiException('error', 400);
    expect(ex.statusCode).toBe(400);
  });
});

describe('Logger', () => {
  it('logs structured JSON to console', () => {
    const logger = new ConsoleLogger();
    const spyInfo = vi.spyOn(console, 'info').mockImplementation(() => {});
    const spyWarn = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const spyError = vi.spyOn(console, 'error').mockImplementation(() => {});
    const spyDebug = vi.spyOn(console, 'debug').mockImplementation(() => {});

    logger.info('test', { src: 'a' });
    expect(spyInfo).toHaveBeenCalled();
    logger.warn('warn', { src: 'a' });
    expect(spyWarn).toHaveBeenCalled();
    logger.error(new Error('err'), { src: 'a' });
    expect(spyError).toHaveBeenCalled();
    logger.debug('dbg', { src: 'a' });
    expect(spyDebug).toHaveBeenCalled();
  });
});

describe('DI Container Edge Cases', () => {
  it('throws error for missing service', () => {
    expect(() => container.resolve('Unknown')).toThrow();
  });
  it('logs warning when overwriting', () => {
    const spyWarn = vi.spyOn(console, 'warn').mockImplementation(() => {});
    container.register('ILogger', new ConsoleLogger()); // Overwrite existing
    expect(spyWarn).toHaveBeenCalled();
  });
});
