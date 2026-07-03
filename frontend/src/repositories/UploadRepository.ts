import { BaseRepository } from './BaseRepository';
import { API_ROUTES } from '../constants/api';
import type { UploadResponseDTO } from '../types';
import type { AxiosRequestConfig } from 'axios';

export class UploadRepository extends BaseRepository {
  async uploadFile(file: File, config?: AxiosRequestConfig): Promise<UploadResponseDTO> {
    const formData = new FormData();
    formData.append('file', file);

    // Pass custom config containing onUploadProgress and cancel token logic
    return this.post<UploadResponseDTO>(API_ROUTES.UPLOAD, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      ...config
    });
  }
}
