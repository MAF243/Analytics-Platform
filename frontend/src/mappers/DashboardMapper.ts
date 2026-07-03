import { PieChartModel, ScatterChartModel, BarChartModel, StackedBarChartModel, GaugeChartModel } from '../chart-models/models';
import type { DashboardDTO } from '../types';
import { QualityService } from '../services/QualityService';

export class DashboardMapper {
  static toClusterDonutModel(dto: DashboardDTO): PieChartModel {
    const series = Object.entries(dto.summary.clusters).map(([key, val]) => ({
      name: `Cluster ${key}`,
      value: val.size
    }));
    return new PieChartModel('Cluster Distribution', series);
  }

  static toPcaScatterModel(dto: DashboardDTO): ScatterChartModel {
    return new ScatterChartModel('PCA Visualization', dto.pca.pca_points);
  }

  static toCategoryBarModel(dto: DashboardDTO): BarChartModel {
    // Pick the first categorical feature for the demo bar chart, or aggregate them
    const catKeys = Object.keys(dto.summary.categories);
    if (catKeys.length === 0) {
      return new BarChartModel('Top Categories', [], []);
    }
    
    // Sort by number of unique values descending and pick the top one
    const topCatKey = catKeys.sort((a, b) => dto.summary.categories[b].unique_values - dto.summary.categories[a].unique_values)[0];
    const topCat = dto.summary.categories[topCatKey];
    
    // Get top 10 frequencies
    const freqEntries = Object.entries(topCat.frequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);
      
    const categories = freqEntries.map(e => e[0]);
    const values = freqEntries.map(e => e[1]);
    
    return new BarChartModel(`Frequencies: ${topCatKey}`, categories, values);
  }

  static toFeatureMeansModel(dto: DashboardDTO): StackedBarChartModel {
    const clusterKeys = Object.keys(dto.summary.clusters);
    if (clusterKeys.length === 0) return new StackedBarChartModel('Feature Means by Cluster', [], []);

    // Get all unique features across all clusters
    const allFeatures = new Set<string>();
    for (const key of clusterKeys) {
      Object.keys(dto.summary.clusters[key].features).forEach(f => allFeatures.add(f));
    }
    const features = Array.from(allFeatures).slice(0, 10); // Limit to top 10 features for readability

    const series = clusterKeys.map(cKey => {
      const clusterFeatures = dto.summary.clusters[cKey].features;
      const data = features.map(f => clusterFeatures[f] || 0);
      return { name: `Cluster ${cKey}`, data };
    });

    return new StackedBarChartModel('Top 10 Feature Means', features, series);
  }

  static toDataQualityGaugeModel(dto: DashboardDTO): GaugeChartModel {
    const score = QualityService.calculateQualityScore(dto);
    return new GaugeChartModel('Data Quality Score', score);
  }
}
