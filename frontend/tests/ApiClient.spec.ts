import { describe, it, expect } from 'vitest';
import { apiClient } from '../src/services/apiClient';

describe('apiClient interceptors', () => {
  it('handles response interceptor success', () => {
    const handler = (apiClient.interceptors.response as any).handlers[0].fulfilled;
    const response = { data: 'ok' };
    expect(handler(response)).toBe(response);
  });

  it('handles response interceptor error', async () => {
    const handler = (apiClient.interceptors.response as any).handlers[0].rejected;
    const error = { response: { status: 500, data: { message: 'err' } } };
    await expect(handler(error)).rejects.toThrow();
  });
});
