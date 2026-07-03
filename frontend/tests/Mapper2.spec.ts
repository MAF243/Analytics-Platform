import { describe, it, expect } from 'vitest';
import { mapApiError } from '../src/services/mapper';
import { apiClient } from '../src/services/apiClient';

describe('mapApiError', () => {
  it('handles empty axios err', () => {
    const ex = mapApiError({ response: null });
    expect(ex.statusCode).toBe(500);
  });
  it('handles axios err', () => {
    const ex = mapApiError({ response: { status: 400, data: { error: { code: 'ERR' }, message: 'err' } } });
    expect(ex.statusCode).toBe(400);
    expect(ex.message).toBe('err');
  });
  it('handles request network error', () => {
    const ex = mapApiError({ request: {} });
    expect(ex.code).toBe('NETWORK_ERROR');
  });
});

describe('apiClient setup coverage', () => {
  it('exists', () => {
    expect(apiClient).toBeDefined();
  });
});
