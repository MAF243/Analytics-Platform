import { createRouter, createWebHistory } from 'vue-router';
import { APP_ROUTES } from '../constants/routes';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: APP_ROUTES.UPLOAD
    },
    {
      path: APP_ROUTES.UPLOAD,
      name: 'upload',
      component: () => import('../features/upload/UploadPage.vue')
    },
    {
      path: APP_ROUTES.ANALYSIS,
      name: 'analysis',
      component: () => import('../features/analysis/AnalysisPage.vue')
    },
    {
      path: APP_ROUTES.DASHBOARD,
      name: 'dashboard',
      component: () => import('../features/dashboard/DashboardPage.vue')
    },
    {
      path: APP_ROUTES.NOT_FOUND,
      name: 'not-found',
      component: () => import('../features/shared/NotFoundPage.vue')
    }
  ]
});

export default router;
