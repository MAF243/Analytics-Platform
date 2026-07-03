import { describe, it, expect, vi, beforeEach } from 'vitest';
import { DashboardQuery } from '../src/queries/DashboardQuery';
import { container } from '../src/di/container';
import type { DashboardDTO } from '../src/types';

const mockDashboardData: DashboardDTO = {
  dataset_id: 'test',
  profiling: { row_count: 100, column_count: 10, columns: {} },
  features_selected: [],
  pca: { pca_points: [] },
  summary: { clusters: {}, categories: {} },
  processing_metadata: { total_rows: 100, duplicate_rows_removed: 0, started_at: '', finished_at: '' }
};

describe('DashboardQuery Cache Isolation', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    container.dashboardRepository.fetchDashboard = vi.fn().mockResolvedValue(mockDashboardData);
  });

  it('fetches from API on first call and caches on second call', async () => {
    const query = new DashboardQuery();

    const result1 = await query.fetch('data-1');
    expect(result1).toEqual(mockDashboardData);
    expect(container.dashboardRepository.fetchDashboard).toHaveBeenCalledTimes(1);

    const result2 = await query.fetch('data-1');
    expect(result2).toEqual(mockDashboardData);
    expect(container.dashboardRepository.fetchDashboard).toHaveBeenCalledTimes(1); // Still 1
  });

  it('bypasses cache when forceRefresh is true', async () => {
    const query = new DashboardQuery();

    await query.fetch('data-2');
    expect(container.dashboardRepository.fetchDashboard).toHaveBeenCalledTimes(1);

    await query.fetch('data-2', true);
    expect(container.dashboardRepository.fetchDashboard).toHaveBeenCalledTimes(2);
  });
});
