import { container } from '../di/container';
import type { AnalysisStatusDTO } from '../types/analysis';

export interface AnalysisCallbacks {
  onStatusChange: (status: AnalysisStatusDTO) => void;
  onComplete: () => void;
  onError: (error: Error) => void;
}

export class AnalysisExecutionStrategy {
  private abortController: AbortController | null = null;
  private isCancelled = false;
  private datasetId: string;
  private callbacks: AnalysisCallbacks;

  constructor(datasetId: string, callbacks: AnalysisCallbacks) {
    this.datasetId = datasetId;
    this.callbacks = callbacks;
  }

  async start() {
    this.isCancelled = false;
    this.abortController = new AbortController();
    
    this.callbacks.onStatusChange({ 
      status: 'processing', 
      progress: 50, 
      message: 'Running synchronous analysis...' 
    });

    try {
      await container.analysisRepository.startAnalysis(this.datasetId, { signal: this.abortController.signal });
      
      if (!this.isCancelled) {
        this.callbacks.onComplete();
      }
    } catch (e: any) {
      if (!this.isCancelled && e.name !== 'CanceledError' && e.message !== 'canceled') {
        this.callbacks.onError(e);
      }
    }
  }

  stop() {
    this.isCancelled = true;
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
  }
}

export class AnalysisFacade {
  static startAnalysis(datasetId: string, callbacks: AnalysisCallbacks): AnalysisExecutionStrategy {
    return new AnalysisExecutionStrategy(datasetId, callbacks);
  }
}
