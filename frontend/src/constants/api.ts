export const API_ROUTES = {
  UPLOAD: '/upload',
  ANALYSIS: (id: string) => `/analysis/${id}`,
  DASHBOARD: (id: string) => `/dashboard/${id}`,
} as const;
