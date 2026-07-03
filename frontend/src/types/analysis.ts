export interface AnalysisStatusDTO {
  status: 'queued' | 'processing' | 'completed' | 'failed';
  message?: string;
  progress?: number;
}
