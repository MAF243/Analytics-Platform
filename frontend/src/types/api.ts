export interface ApiErrorDTO {
  code: string;
  details?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T | null;
  error: ApiErrorDTO | null;
  timestamp: string;
  request_id: string;
  processing_time: number;
  version: string;
  status: number;
}
