import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AnalysisFacade } from '../src/facades/AnalysisFacade';
import { container } from '../src/di/container';

describe('AnalysisPollingStrategy', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('stops polling when status is completed', async () => {
    // Mock repositories
    container.analysisRepository.startAnalysis = vi.fn().mockResolvedValue(undefined);
    container.analysisRepository.getStatus = vi.fn()
      .mockResolvedValueOnce({ status: 'processing', progress: 50 })
      .mockResolvedValueOnce({ status: 'completed', progress: 100 });

    const onStatusChange = vi.fn();
    const onComplete = vi.fn();
    const onError = vi.fn();

    const poller = AnalysisFacade.createPoller('123', {
      onStatusChange, onComplete, onError
    });

    // Start kicks off startAnalysis and first poll
    await poller.start();

    // First poll resolves to 'processing'
    await vi.runOnlyPendingTimersAsync();
    expect(onStatusChange).toHaveBeenCalledWith({ status: 'processing', progress: 50 });

    // Second poll resolves to 'completed'
    await vi.runOnlyPendingTimersAsync();
    expect(onStatusChange).toHaveBeenCalledWith({ status: 'completed', progress: 100 });
    expect(onComplete).toHaveBeenCalled();
    expect(onError).not.toHaveBeenCalled();

    poller.stop();
  });
});
