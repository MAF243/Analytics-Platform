import { BaseRepository } from './BaseRepository';
import { API_ROUTES } from '../constants/api';
import type { DashboardDTO } from '../types';

export class DashboardRepository extends BaseRepository {
  async fetchDashboard(datasetId: string, signal?: AbortSignal): Promise<DashboardDTO> {
    return this.get<DashboardDTO>(API_ROUTES.DASHBOARD(datasetId), { signal });
  }
}

export const dashboardRepository = new DashboardRepository();
