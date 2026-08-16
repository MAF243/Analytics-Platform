export interface AnalysisStatusDTO {
  job_id: string;
  dataset_id: string;
  status: 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  current_step?: string;
  steps_completed: number;
  total_steps: number;
  started_at?: string;
  updated_at?: string;
  finished_at?: string;
  estimated_remaining_seconds?: number;
  error_message?: string;
  is_cancelled: boolean;
  message?: string;
}
