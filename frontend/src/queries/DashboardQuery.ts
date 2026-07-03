import { QueryCache } from './QueryCache';
import { container } from '../di/container';
import type { DashboardDTO } from '../types';

export class DashboardQuery {
  private cache = new QueryCache<DashboardDTO>();

  async fetch(datasetId: string, forceRefresh = false, signal?: AbortSignal): Promise<DashboardDTO> {
    return this.cache.fetchWithSWR(
      datasetId,
      () => container.dashboardRepository.fetchDashboard(datasetId, signal),
      forceRefresh
    );
  }

  invalidate(datasetId: string) { this.cache.invalidate(datasetId); }
}
export const dashboardQuery = new DashboardQuery();
