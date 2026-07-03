import { describe, it, expect, vi } from 'vitest';
import { apiClient } from '../src/services/apiClient';
import { BaseRepository } from '../src/repositories/BaseRepository';
import { UploadRepository } from '../src/repositories/UploadRepository';
import { AnalysisRepository } from '../src/repositories/AnalysisRepository';
import { DashboardRepository } from '../src/repositories/DashboardRepository';

describe('API Client & Exceptions', () => {
  it('handles GET requests', async () => {
    const mockGet = vi.fn().mockResolvedValue({ data: { data: 'ok' } });
    apiClient.get = mockGet;

    class TestRepo extends BaseRepository {
      async test() { return this.get<string>('/test'); }
    }
    const repo = new TestRepo();
    expect(await repo.test()).toBe('ok');
  });

  it('handles POST requests', async () => {
    const mockPost = vi.fn().mockResolvedValue({ data: { data: 'ok' } });
    apiClient.post = mockPost;

    class TestRepo extends BaseRepository {
      async test() { return this.post<string>('/test', {a:1}); }
    }
    const repo = new TestRepo();
    expect(await repo.test()).toBe('ok');
  });

  it('handles multipart form data in UploadRepository', async () => {
    const mockPost = vi.fn().mockResolvedValue({ data: { data: { datasetId: '123' } } });
    apiClient.post = mockPost;

    const repo = new UploadRepository();
    const res = await repo.uploadFile(new File([''], 'a.csv'), {});
    expect(res.datasetId).toBe('123');
  });
});

describe('AnalysisRepository Circuit Breaker', () => {
  it('executes startAnalysis through breaker', async () => {
    const mockPost = vi.fn().mockResolvedValue({ data: { data: null } });
    apiClient.post = mockPost;
    const repo = new AnalysisRepository();
    await repo.startAnalysis('123');
    expect(mockPost).toHaveBeenCalled();
  });

  it('executes getStatus through breaker', async () => {
    const mockGet = vi.fn().mockResolvedValue({ data: { data: { status: 'queued' } } });
    apiClient.get = mockGet;
    const repo = new AnalysisRepository();
    const res = await repo.getStatus('123');
    expect(res.status).toBe('queued');
  });
});

describe('DashboardRepository', () => {
  it('executes fetchDashboard', async () => {
    const mockGet = vi.fn().mockResolvedValue({ data: { data: { metadata: {} } } });
    apiClient.get = mockGet;
    const repo = new DashboardRepository();
    const res = await repo.fetchDashboard('123');
    expect(res.metadata).toBeDefined();
  });
});
