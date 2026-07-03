import { describe, it, expect, vi, beforeEach } from 'vitest';
import { QueryCache } from '../src/queries/QueryCache';

describe('QueryCache - Production Hardening', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  it('coalesces identical concurrent requests into a single promise', async () => {
    const cache = new QueryCache<string>(1000, 500);
    const fetcher = vi.fn().mockImplementation(() => new Promise(res => setTimeout(() => res('data'), 100)));

    // Fire 3 simultaneous requests
    const p1 = cache.fetchWithSWR('key', fetcher);
    const p2 = cache.fetchWithSWR('key', fetcher);
    const p3 = cache.fetchWithSWR('key', fetcher);

    vi.runAllTimers();
    const results = await Promise.all([p1, p2, p3]);

    expect(results).toEqual(['data', 'data', 'data']);
    expect(fetcher).toHaveBeenCalledTimes(1); // Crucial: only one network hit
  });

  it('triggers background SWR fetch when data is stale but not expired', async () => {
    const cache = new QueryCache<string>(10000, 1000); // ttl=10s, stale=1s
    const fetcher = vi.fn().mockResolvedValue('fresh data');

    // Inject mock stale state
    // @ts-expect-error private field access for testing
    cache.cache.set('stale_key', {
      data: 'old data',
      timestamp: Date.now() - 2000, // 2s old (stale, but not expired)
      expiresAt: Date.now() + 8000,
      state: 'stale',
      fetchPromise: null
    });

    const result = await cache.fetchWithSWR('stale_key', fetcher);
    expect(result).toBe('old data'); // Returned immediately
    expect(fetcher).toHaveBeenCalledTimes(1); // Background fetch kicked off
  });
});
