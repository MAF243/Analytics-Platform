import { describe, it, expect, vi } from 'vitest';
import { BaseRepository } from '../src/repositories/BaseRepository';
import { apiClient } from '../src/services/apiClient';
import { AnalysisFacade } from '../src/facades/AnalysisFacade';
import { DashboardQuery } from '../src/queries/DashboardQuery';
import { container } from '../src/di/container';

describe('BaseRepository Catch Blocks', () => {
  it('handles get rejection', async () => {
    class TestRepo extends BaseRepository {
      async test() { return this.get('/test'); }
    }
    vi.spyOn(apiClient, 'get').mockRejectedValue({ response: { status: 500, data: { message: 'err' } } });
    await expect(new TestRepo().test()).rejects.toThrow('err');
  });

  it('handles post rejection', async () => {
    class TestRepo extends BaseRepository {
      async test() { return this.post('/test'); }
    }
    vi.spyOn(apiClient, 'post').mockRejectedValue({ response: { status: 500, data: { message: 'err' } } });
    await expect(new TestRepo().test()).rejects.toThrow('err');
  });
});

describe('AnalysisFacade Edge Cases', () => {
  it('retries on 409', async () => {
    const cb = { onStatusChange: vi.fn(), onComplete: vi.fn(), onError: vi.fn() };
    const poller = AnalysisFacade.createPoller('123', cb);

    vi.spyOn(container.analysisRepository, 'startAnalysis').mockRejectedValue({ statusCode: 409 });
    vi.spyOn(container.analysisRepository, 'getStatus').mockResolvedValue({ status: 'completed' } as any);

    await poller.start();
    expect(cb.onComplete).toHaveBeenCalled();
    poller.stop();
  });

  it('ignores CanceledError', async () => {
    const cb = { onStatusChange: vi.fn(), onComplete: vi.fn(), onError: vi.fn() };
    const poller = AnalysisFacade.createPoller('123', cb);

    vi.spyOn(container.analysisRepository, 'startAnalysis').mockResolvedValue();
    vi.spyOn(container.analysisRepository, 'getStatus').mockRejectedValue({ name: 'CanceledError' });

    await poller.start();
    // It should just return, no retries logged and no error called
    expect(cb.onError).not.toHaveBeenCalled();
    poller.stop();
  });
});

describe('DashboardQuery error', () => {
  it('catches and throws', async () => {
    vi.spyOn(container.dashboardRepository, 'fetchDashboard').mockRejectedValue(new Error('dash err'));
    const query = new DashboardQuery('123');
    await expect(query.fetch()).rejects.toThrow('dash err');
  });
});
