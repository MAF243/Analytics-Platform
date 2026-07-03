import type { SummaryDTO } from '../types';

export class ClusterMapper {
  static toDistributionPieChart(summary: SummaryDTO) {
    const data = Object.entries(summary.clusters).map(([key, val]) => ({
      name: `Cluster ${key}`,
      value: val.size
    }));
    return {
      tooltip: { trigger: 'item' },
      series: [
        {
          type: 'pie',
          radius: ['40%', '70%'],
          itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
          data
        }
      ]
    };
  }
}
