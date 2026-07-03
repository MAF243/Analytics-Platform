import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AnalysisFacade, AnalysisPollingStrategy } from '../src/facades/AnalysisFacade';
import { container } from '../src/di/container';

describe('AnalysisFacade Polling', () => {
  beforeEach(() => { vi.useFakeTimers(); });

  it('creates poller', () => {
    const cb = { onStatusChange: vi.fn(), onComplete: vi.fn(), onError: vi.fn() };
    const poller = AnalysisFacade.createPoller('123', cb);
    expect(poller).toBeInstanceOf(AnalysisPollingStrategy);
    poller.stop();
  });

  it('handles startAnalysis success and starts polling', async () => {
    const cb = { onStatusChange: vi.fn(), onComplete: vi.fn(), onError: vi.fn() };
    const poller = AnalysisFacade.createPoller('123', cb);

    vi.spyOn(container.analysisRepository, 'startAnalysis').mockResolvedValue();
    vi.spyOn(container.analysisRepository, 'getStatus').mockResolvedValue({ status: 'queued' } as any);

    await poller.start();
    expect(cb.onStatusChange).toHaveBeenCalled();
    poller.stop();
  });

  it('handles offline pausing', async () => {
    const cb = { onStatusChange: vi.fn(), onComplete: vi.fn(), onError: vi.fn() };
    const poller = AnalysisFacade.createPoller('123', cb);

    Object.defineProperty(navigator, 'onLine', { value: false, configurable: true });
    vi.spyOn(container.analysisRepository, 'startAnalysis').mockResolvedValue();
    await poller.start();
    expect(cb.onStatusChange).not.toHaveBeenCalled(); 

    Object.defineProperty(navigator, 'onLine', { value: true, configurable: true });
    vi.spyOn(container.analysisRepository, 'getStatus').mockResolvedValue({ status: 'completed' } as any);
    window.dispatchEvent(new Event('online'));

    await vi.runAllTimersAsync();
    poller.stop();
  });

  it('handles polling completion', async () => {
    const cb = { onStatusChange: vi.fn(), onComplete: vi.fn(), onError: vi.fn() };
    const poller = AnalysisFacade.createPoller('123', cb);

    vi.spyOn(container.analysisRepository, 'startAnalysis').mockResolvedValue();
    vi.spyOn(container.analysisRepository, 'getStatus').mockResolvedValue({ status: 'completed' } as any);

    await poller.start();
    expect(cb.onComplete).toHaveBeenCalled();
    poller.stop();
  });

  it('handles polling failure', async () => {
    const cb = { onStatusChange: vi.fn(), onComplete: vi.fn(), onError: vi.fn() };
    const poller = AnalysisFacade.createPoller('123', cb);

    vi.spyOn(container.analysisRepository, 'startAnalysis').mockResolvedValue();
    vi.spyOn(container.analysisRepository, 'getStatus').mockResolvedValue({ status: 'failed', message: 'err' } as any);

    await poller.start();
    expect(cb.onError).toHaveBeenCalled();
    poller.stop();
  });

  it('handles polling errors and retries (code coverage)', async () => {
    const cb = { onStatusChange: vi.fn(), onComplete: vi.fn(), onError: vi.fn() };
    const poller = AnalysisFacade.createPoller('123', cb);

    vi.spyOn(container.analysisRepository, 'startAnalysis').mockResolvedValue();
    vi.spyOn(container.analysisRepository, 'getStatus').mockRejectedValue(new Error('timeout'));

    await poller.start();
    expect(cb.onError).not.toHaveBeenCalled();
    poller.stop();
  });
});
