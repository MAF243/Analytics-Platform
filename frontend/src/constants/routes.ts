export const APP_ROUTES = {
  UPLOAD: '/upload',
  ANALYSIS: '/analysis/:dataset_id',
  DASHBOARD: '/dashboard/:dataset_id',
  LOGIN: '/login',
  NOT_FOUND: '/:pathMatch(.*)*',
} as const;
