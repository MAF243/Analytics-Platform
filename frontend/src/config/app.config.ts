export const APP_CONFIG = {
  apiBaseUrl: import.meta.env.VITE_API_URL || '/api/v1',
  apiTimeoutMs: 30000,
  maxUploadSizeBytes: 50 * 1024 * 1024, // 50MB
  supportedUploadMimeTypes: ['text/csv', 'application/vnd.ms-excel'],
  supportedUploadExtensions: ['.csv'],
} as const;
