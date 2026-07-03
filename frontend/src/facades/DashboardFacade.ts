import { dashboardRepository } from '../repositories/DashboardRepository';
import { useDatasetStore } from '../stores/dataset';
import { useToast } from '../composables/useToast';
import type { DashboardDTO } from '../types';

export class DashboardFacade {
  static async loadDashboard(datasetId: string, signal?: AbortSignal): Promise<DashboardDTO | null> {
    const store = useDatasetStore();
    const toast = useToast();

    // Check TTL Cache
    const cached = store.getDashboard(datasetId);
    if (cached) return cached;

    try {
      const data = await dashboardRepository.fetchDashboard(datasetId, signal);
      store.setDashboard(datasetId, data);
      return data;
    } catch (e: any) {
      toast.error('Dashboard Error', e.message);
      return null;
    }
  }
}
