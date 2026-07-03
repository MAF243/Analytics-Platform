import type { ApiErrorDTO } from '../types';

export class FrontendException extends Error {
  public message: string;
  public code: string;
  public details?: string;
  public statusCode: number;

  constructor(
    message: string,
    code: string = 'UNKNOWN_ERROR',
    details?: string,
    statusCode: number = 500
  ) {
    super(message);
    this.message = message;
    this.code = code;
    this.details = details;
    this.statusCode = statusCode;
    this.name = 'FrontendException';
  }
}

export const mapApiError = (error: any): FrontendException => {
  if (error.response) {
    const data = error.response.data;
    if (data && data.error) {
      const apiErr = data.error as ApiErrorDTO;
      return new FrontendException(
        data.message || 'API Error',
        apiErr.code,
        apiErr.details,
        error.response.status
      );
    }
    return new FrontendException('Server Error', 'SERVER_ERROR', undefined, error.response.status);
  }
  if (error.request) {
    return new FrontendException(
      'Network Error. Please check your connection.',
      'NETWORK_ERROR',
      undefined,
      0
    );
  }
  return new FrontendException(error.message, 'CLIENT_ERROR');
};
