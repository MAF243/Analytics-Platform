export const API_ROUTES = {
  UPLOAD: '/upload',
  ANALYSIS: (id: string) => `/analysis/${id}`,
  ANALYSIS_STATUS: (id: string) => `/analysis/${id}/status`,
  DASHBOARD: (id: string) => `/dashboard/${id}`,
} as const;
