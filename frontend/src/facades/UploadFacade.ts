import { container } from '../di/container';
import { reportMetric } from '../observability';
import type { UploadResponseDTO } from '../types';
import type { AxiosRequestConfig } from 'axios';

export class UploadFacade {
  static async upload(file: File, onProgress?: (percent: number) => void, signal?: AbortSignal): Promise<UploadResponseDTO> {
    const config: AxiosRequestConfig = {
      signal,
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percent);
        }
      }
    };
    const start = performance.now();
    try {
      const response = await container.uploadRepository.uploadFile(file, config);
      reportMetric('upload_duration_ms', performance.now() - start, { filename: file.name, size: file.size });
      return response;
    } catch (error) {
      reportMetric('upload_duration_ms_failed', performance.now() - start, { filename: file.name, size: file.size });
      throw error;
    }
  }
}
