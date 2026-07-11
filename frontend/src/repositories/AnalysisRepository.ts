import { BaseRepository } from './BaseRepository';
import { API_ROUTES } from '../constants/api';
import type { AnalysisStatusDTO } from '../types/analysis';
import { CircuitBreaker } from '../infrastructure/CircuitBreaker';

export class AnalysisRepository extends BaseRepository {
  private circuitBreaker = new CircuitBreaker('AnalysisAPI', { failureThreshold: 5, cooldownMs: 15000 });

  async startAnalysis(datasetId: string, options?: { signal?: AbortSignal }): Promise<void> {
    return this.circuitBreaker.execute(() => 
      this.post<void>(API_ROUTES.ANALYSIS(datasetId), undefined, options)
    );
  }
}
