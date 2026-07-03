import { container } from '../di/container';

export type CacheState = 'fresh' | 'stale' | 'expired' | 'loading';

export interface CacheEntry<T> {
  data: T | null;
  timestamp: number;
  expiresAt: number;
  state: CacheState;
  fetchPromise: Promise<T> | null;
}

export class QueryCache<T> {
  private cache = new Map<string, CacheEntry<T>>();
  private ttlMs: number;
  private staleMs: number;

  constructor(ttlMs = 300000, staleMs = 60000) {
    this.ttlMs = ttlMs;
    this.staleMs = staleMs;
  }

  async fetchWithSWR(
    key: string,
    fetcher: () => Promise<T>,
    forceRefresh = false
  ): Promise<T> {
    const entry = this.cache.get(key);
    const now = Date.now();

    if (entry?.fetchPromise && !forceRefresh) {
      container.logger.info(`[Cache] Coalescing request for key: ${key}`);
      return entry.fetchPromise;
    }

    if (entry && entry.data && !forceRefresh) {
      if (now < entry.timestamp + this.staleMs) {
        entry.state = 'fresh';
        return entry.data;
      }
      if (now < entry.expiresAt) {
        entry.state = 'stale';
        container.logger.info(`[Cache] Stale-While-Revalidate triggered for key: ${key}`);
        this.executeFetch(key, fetcher);
        return entry.data;
      }
    }

    return this.executeFetch(key, fetcher);
  }

  private async executeFetch(key: string, fetcher: () => Promise<T>): Promise<T> {
    let entry = this.cache.get(key);

    if (!entry) {
      entry = { data: null, timestamp: 0, expiresAt: 0, state: 'loading', fetchPromise: null };
      this.cache.set(key, entry);
    } else {
      entry.state = 'loading';
    }

    const promise = fetcher().then((data) => {
      const finishTime = Date.now();
      entry!.data = data;
      entry!.timestamp = finishTime;
      entry!.expiresAt = finishTime + this.ttlMs;
      entry!.state = 'fresh';
      entry!.fetchPromise = null;
      return data;
    }).catch((err) => {
      entry!.state = 'expired';
      entry!.fetchPromise = null;
      throw err;
    });

    entry.fetchPromise = promise;
    return promise;
  }

  get(key: string): T | null {
    return this.cache.get(key)?.data || null;
  }

  getState(key: string): CacheState | null {
    return this.cache.get(key)?.state || null;
  }

  invalidate(key: string) {
    this.cache.delete(key);
  }
}
