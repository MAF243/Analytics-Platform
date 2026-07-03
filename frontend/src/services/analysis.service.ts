import { apiClient } from './apiClient';
import { API_ROUTES } from '../constants/api';
import type { ApiResponse } from '../types';

export const analysisService = {
  runAnalysis: async (datasetId: string, signal?: AbortSignal): Promise<ApiResponse<any>> => {
    const response = await apiClient.post<ApiResponse<any>>(
      API_ROUTES.ANALYSIS(datasetId),
      {},
      {
        signal,
      }
    );
    return response.data;
  },
};
