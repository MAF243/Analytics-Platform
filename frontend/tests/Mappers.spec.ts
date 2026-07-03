import { describe, it, expect } from 'vitest';
import { DashboardMapper } from '../src/mappers/DashboardMapper';
import { DashboardDTO } from '../src/types';

describe('Mappers', () => {
  it('DashboardMapper maps to donut model', () => {
    const dto = {
      summary: {
        clusters: {
          '0': { size: 100, percentage: 0.6, features: {} },
          '1': { size: 50, percentage: 0.4, features: {} }
        }
      }
    } as unknown as DashboardDTO;

    const donut = DashboardMapper.toClusterDonutModel(dto);
    expect(donut.series).toHaveLength(2);
    expect(donut.series[0].name).toBe('Cluster 0');
  });

  it('DashboardMapper maps to scatter model', () => {
    const dto = {
      pca: {
        pca_points: [
          { cluster_id: 0, pca_1: 1, pca_2: 2 }
        ]
      }
    } as unknown as DashboardDTO;

    const scatter = DashboardMapper.toPcaScatterModel(dto);
    expect(scatter.points).toHaveLength(1);
  });
});
