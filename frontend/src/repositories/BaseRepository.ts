import { apiClient } from '../services/apiClient';
import { NetworkException, TimeoutException, ValidationException, NotFoundException, ApiException, UnauthorizedException, ForbiddenException, ConflictException } from '../exceptions';
import type { AxiosRequestConfig } from 'axios';
import type { ApiResponse } from '../types';

export class BaseRepository {
  protected async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await apiClient.get<ApiResponse<T>>(url, config);
      return response.data.data as T;
    } catch (e: any) {
      this.handleAxiosError(e);
      throw e;
    }
  }

  protected async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await apiClient.post<ApiResponse<T>>(url, data, config);
      return response.data.data as T;
    } catch (e: any) {
      this.handleAxiosError(e);
      throw e;
    }
  }

  private handleAxiosError(error: any) {
    if (error.code === 'ECONNABORTED') throw new TimeoutException();
    if (!error.response) throw new NetworkException();

    const status = error.response.status;
    const msg = error.response.data?.message || 'API Error';

    if (status === 401) throw new UnauthorizedException(msg);
    if (status === 403) throw new ForbiddenException(msg);
    if (status === 404) throw new NotFoundException(msg);
    if (status === 409) throw new ConflictException(msg);
    if (status === 422) throw new ValidationException(msg);

    throw new ApiException(msg, status);
  }
}
