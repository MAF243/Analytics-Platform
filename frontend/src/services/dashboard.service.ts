import { apiClient } from './apiClient';
import { API_ROUTES } from '../constants/api';
import type { ApiResponse, DashboardDTO } from '../types';

export const dashboardService = {
  getDashboard: async (
    datasetId: string,
    signal?: AbortSignal
  ): Promise<ApiResponse<DashboardDTO>> => {
    const response = await apiClient.get<ApiResponse<DashboardDTO>>(
      API_ROUTES.DASHBOARD(datasetId),
      {
        signal,
      }
    );
    return response.data;
  },
};
