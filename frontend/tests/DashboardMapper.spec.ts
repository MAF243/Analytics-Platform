import { describe, it, expect } from 'vitest';
import { DashboardMapper } from '../src/mappers/DashboardMapper';
import type { DashboardDTO } from '../src/types';

describe('DashboardMapper additional coverage', () => {
  const dummyDTO: DashboardDTO = {
    dataset_id: '123',
    profiling: { row_count: 100, column_count: 5, columns: {} },
    features_selected: ['A', 'B'],
    pca: { pca_points: [] },
    summary: {
      clusters: {
        '0': { size: 60, percentage: 0.6, features: { 'A': 1, 'B': 2 } },
        '1': { size: 40, percentage: 0.4, features: { 'A': 3, 'B': 4 } }
      },
      categories: {
        'Category1': { frequency: { 'X': 10, 'Y': 5 }, unique_values: 2, mode: 'X' }
      }
    },
    processing_metadata: { total_rows: 100, duplicate_rows_removed: 0, started_at: '', finished_at: '' }
  };

  it('toDataQualityGaugeModel', () => {
    const result = DashboardMapper.toDataQualityGaugeModel(dummyDTO);
    expect(result.score).toBe(100);
  });

  it('toCategoryBarModel', () => {
    const result = DashboardMapper.toCategoryBarModel(dummyDTO);
    expect(result.categories.length).toBeGreaterThan(0);
    expect(result.values).toHaveLength(result.categories.length);
  });

  it('toFeatureMeansModel', () => {
    const result = DashboardMapper.toFeatureMeansModel(dummyDTO);
    expect(result.categories).toEqual(['A', 'B']); // features
    expect(result.series).toHaveLength(2); // clusters 0 and 1
  });
});
