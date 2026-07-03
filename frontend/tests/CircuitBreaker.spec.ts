import { describe, it, expect, vi, beforeEach } from 'vitest';
import { CircuitBreaker } from '../src/infrastructure/CircuitBreaker';

describe('CircuitBreaker', () => {
  beforeEach(() => { vi.useFakeTimers(); });

  it('transitions to OPEN after threshold failures', async () => {
    const cb = new CircuitBreaker('test', { failureThreshold: 3, cooldownMs: 10000 });
    const failAction = vi.fn().mockRejectedValue(new Error('fail'));

    await expect(cb.execute(failAction)).rejects.toThrow('fail');
    await expect(cb.execute(failAction)).rejects.toThrow('fail');
    await expect(cb.execute(failAction)).rejects.toThrow('fail');

    expect(cb.getState()).toBe('OPEN');

    // Fast-fail
    await expect(cb.execute(failAction)).rejects.toThrow('CircuitBreaker [test] is OPEN');
    expect(failAction).toHaveBeenCalledTimes(3);
  });

  it('transitions to HALF_OPEN after cooldown and recovers if success', async () => {
    const cb = new CircuitBreaker('test', { failureThreshold: 1, cooldownMs: 10000 });
    let shouldFail = true;
    const action = vi.fn().mockImplementation(async () => {
      if (shouldFail) throw new Error('fail');
      return 'success';
    });

    await expect(cb.execute(action)).rejects.toThrow();
    expect(cb.getState()).toBe('OPEN');

    vi.advanceTimersByTime(11000);
    shouldFail = false;

    const res = await cb.execute(action);
    expect(res).toBe('success');
    expect(cb.getState()).toBe('CLOSED');
  });

  it('ignores 409 errors (does not trip breaker)', async () => {
    const cb = new CircuitBreaker('test', { failureThreshold: 1, cooldownMs: 10000 });
    const action = vi.fn().mockRejectedValue({ statusCode: 409 });

    await expect(cb.execute(action)).rejects.toEqual({ statusCode: 409 });
    expect(cb.getState()).toBe('CLOSED');
  });
});
