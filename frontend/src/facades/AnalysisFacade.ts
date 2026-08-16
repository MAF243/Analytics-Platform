import { container } from '../di/container';
import type { AnalysisStatusDTO } from '../types/analysis';

export interface AnalysisCallbacks {
  onStatusChange: (status: AnalysisStatusDTO) => void;
  onComplete: () => void;
  onError: (error: Error) => void;
}

export class AnalysisPollingStrategy {
  private timer: ReturnType<typeof setTimeout> | null = null;
  private isCancelled = false;
  private retryCount = 0;
  private currentIntervalMs: number;
  private abortController: AbortController | null = null;

  private datasetId: string;
  private callbacks: AnalysisCallbacks;
  private baseIntervalMs: number;
  private maxIntervalMs: number;
  private maxRetries: number;

  constructor(
    datasetId: string,
    callbacks: AnalysisCallbacks,
    baseIntervalMs = 2000,
    maxIntervalMs = 30000,
    maxRetries = 10
  ) {
    this.datasetId = datasetId;
    this.callbacks = callbacks;
    this.baseIntervalMs = baseIntervalMs;
    this.maxIntervalMs = maxIntervalMs;
    this.maxRetries = maxRetries;
    this.currentIntervalMs = baseIntervalMs;
    window.addEventListener('online', this.handleOnline);
  }

  private handleOnline = () => {
    if (!this.isCancelled && !this.timer) {
      container.logger.info('Network restored. Resuming analysis polling.');
      this.poll();
    }
  };

  async start() {
    this.isCancelled = false;
    this.retryCount = 0;
    this.currentIntervalMs = this.baseIntervalMs;
    this.abortController = new AbortController();

    this.callbacks.onStatusChange({
      job_id: 'unknown',
      dataset_id: this.datasetId,
      status: 'queued',
      progress: 0,
      steps_completed: 0,
      total_steps: 0,
      is_cancelled: false,
      message: 'Starting analysis pipeline...'
    });

    try {
      await container.analysisRepository.startAnalysis(this.datasetId, { signal: this.abortController.signal });
      if (!this.isCancelled) {
        this.poll();
      }
    } catch (e: any) {
      if (e.statusCode === 409) {
        if (!this.isCancelled) this.poll();
      } else if (!this.isCancelled && e.name !== 'CanceledError' && e.message !== 'canceled') {
        this.callbacks.onError(e);
      }
    }
  }

  private async poll() {
    if (this.isCancelled) return;

    if (!navigator.onLine) {
      container.logger.warn('Browser is offline. Pausing polling until network returns.');
      return;
    }

    try {
      this.abortController = new AbortController();
      const status = await container.analysisRepository.getStatus(this.datasetId, { signal: this.abortController.signal });

      this.retryCount = 0;
      this.currentIntervalMs = this.baseIntervalMs;

      if (!this.isCancelled) {
        this.callbacks.onStatusChange(status);

        if (status.status === 'completed') {
          this.callbacks.onComplete();
          return;
        }
        
        if (status.status === 'failed') {
          this.callbacks.onError(new Error(status.error_message || status.message || 'Analysis failed internally.'));
          this.stop();
          return;
        }

        if (status.status === 'cancelled') {
          this.callbacks.onError(new Error('Analysis was cancelled on the server.'));
          this.stop();
          return;
        }

        this.scheduleNextPoll();
      }
    } catch (e: any) {
      if (e.name === 'CanceledError' || e.message === 'canceled') return;

      this.retryCount++;
      container.logger.warn(`Polling failed (attempt ${this.retryCount}/${this.maxRetries})`, e);

      if (this.retryCount >= this.maxRetries) {
        if (!this.isCancelled) {
          this.callbacks.onError(new Error('Analysis polling failed. Please check your network connection and try again.'));
          this.stop();
        }
        return;
      }

      this.currentIntervalMs = Math.min(this.currentIntervalMs * 2, this.maxIntervalMs);
      this.scheduleNextPoll();
    }
  }

  private scheduleNextPoll() {
    if (this.isCancelled) return;
    this.timer = setTimeout(() => this.poll(), this.currentIntervalMs);
  }

  stop() {
    this.isCancelled = true;
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
    window.removeEventListener('online', this.handleOnline);
  }
}

export class AnalysisFacade {
  static startAnalysis(datasetId: string, callbacks: AnalysisCallbacks): AnalysisPollingStrategy {
    return new AnalysisPollingStrategy(datasetId, callbacks);
  }
}
