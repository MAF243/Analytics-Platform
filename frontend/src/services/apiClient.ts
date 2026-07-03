import axios from 'axios';
import { APP_CONFIG } from '../config/app.config';
import { mapApiError } from './mapper';

const apiClient = axios.create({
  baseURL: APP_CONFIG.apiBaseUrl,
  timeout: APP_CONFIG.apiTimeoutMs,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(mapApiError(error));
  }
);

export { apiClient };
