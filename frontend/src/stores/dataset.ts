import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { DashboardDTO } from '../types';

interface CacheEntry {
  data: DashboardDTO;
  timestamp: number;
}

const TTL_MS = 5 * 60 * 1000; // 5 minutes

export const useDatasetStore = defineStore('dataset', () => {
  const dashboardCache = ref<Map<string, CacheEntry>>(new Map());

  const getDashboard = (id: string): DashboardDTO | null => {
    const entry = dashboardCache.value.get(id);
    if (!entry) return null;

    if (Date.now() - entry.timestamp > TTL_MS) {
      dashboardCache.value.delete(id);
      return null;
    }
    return entry.data;
  };

  const setDashboard = (id: string, data: DashboardDTO) => {
    dashboardCache.value.set(id, { data, timestamp: Date.now() });
  };

  const clearCache = () => dashboardCache.value.clear();

  const invalidateDataset = (id: string) => {
    dashboardCache.value.delete(id);
  };

  return { getDashboard, setDashboard, clearCache, invalidateDataset };
});
