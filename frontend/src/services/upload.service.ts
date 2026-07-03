import { apiClient } from './apiClient';
import { API_ROUTES } from '../constants/api';
import type { ApiResponse, UploadResponseDTO } from '../types';
import type { AxiosRequestConfig } from 'axios';

export const uploadService = {
  uploadFile: async (
    file: File,
    config?: AxiosRequestConfig
  ): Promise<ApiResponse<UploadResponseDTO>> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<ApiResponse<UploadResponseDTO>>(
      API_ROUTES.UPLOAD,
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
        ...config,
      }
    );
    return response.data;
  },
};
