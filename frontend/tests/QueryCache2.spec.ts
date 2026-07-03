import { describe, it, expect, vi } from 'vitest';
import { QueryCache } from '../src/queries/QueryCache';

describe('QueryCache Advanced', () => {
  it('handles fetch promise rejection', async () => {
    const cache = new QueryCache<string>(1000, 500);
    const fetcher = vi.fn().mockRejectedValue(new Error('fail'));

    await expect(cache.fetchWithSWR('key2', fetcher)).rejects.toThrow('fail');
    expect(cache.getState('key2')).toBe('expired');
  });

  it('getState and invalidate', async () => {
    const cache = new QueryCache<string>(1000, 500);
    const fetcher = vi.fn().mockResolvedValue('ok');

    await cache.fetchWithSWR('key3', fetcher);
    expect(cache.get('key3')).toBe('ok');
    expect(cache.getState('key3')).toBe('fresh');

    cache.invalidate('key3');
    expect(cache.get('key3')).toBeNull();
  });
});
