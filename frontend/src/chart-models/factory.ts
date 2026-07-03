import { PieChartModel, ScatterChartModel, BarChartModel, StackedBarChartModel, GaugeChartModel } from './models';
import { BaseChartOptionFactory } from './baseFactory';
import type { EChartsOption } from 'echarts';

export class EChartsOptionFactory {
  static createDonut(model: PieChartModel): EChartsOption {
    const base = BaseChartOptionFactory.createBaseOption(model.title);
    return {
      ...base,
      series: [
        {
          name: model.title,
          type: 'pie',
          radius: ['45%', '75%'],
          itemStyle: { borderRadius: 8, borderColor: 'var(--surface)', borderWidth: 2 },
          label: { show: true, color: 'var(--text)' },
          data: model.series
        }
      ]
    };
  }

  static createScatter(model: ScatterChartModel): EChartsOption {
    const base = BaseChartOptionFactory.createBaseOption(model.title);
    const clusters = [...new Set(model.points.map(p => p.cluster))];
    const series = clusters.map(c => ({
      name: `Cluster ${c}`,
      type: 'scatter',
      data: model.points.filter(p => p.cluster === c).map(p => [p.x, p.y]),
      symbolSize: 8
    }));

    return {
      ...base,
      legend: { bottom: 0, textStyle: { color: 'var(--text)' } },
      xAxis: { type: 'value', splitLine: { lineStyle: { color: 'var(--border)' } } },
      yAxis: { type: 'value', splitLine: { lineStyle: { color: 'var(--border)' } } },
      series: series as any
    };
  }

  static createBar(model: BarChartModel): EChartsOption {
    const base = BaseChartOptionFactory.createBaseOption(model.title);
    return {
      ...base,
      tooltip: { ...base.tooltip, trigger: 'axis' },
      xAxis: { type: 'category', data: model.categories, axisLabel: { color: 'var(--text)', rotate: 45 } },
      yAxis: { type: 'value', splitLine: { lineStyle: { color: 'var(--border)' } } },
      series: [
        {
          type: 'bar',
          data: model.values,
          itemStyle: { borderRadius: [4, 4, 0, 0] }
        }
      ]
    };
  }

  static createStackedBar(model: StackedBarChartModel): EChartsOption {
    const base = BaseChartOptionFactory.createBaseOption(model.title);
    return {
      ...base,
      tooltip: { ...base.tooltip, trigger: 'axis' },
      legend: { bottom: 0, textStyle: { color: 'var(--text)' } },
      xAxis: { type: 'category', data: model.categories, axisLabel: { color: 'var(--text)', rotate: 45 } },
      yAxis: { type: 'value', splitLine: { lineStyle: { color: 'var(--border)' } } },
      series: model.series.map(s => ({
        name: s.name,
        type: 'bar',
        stack: 'total',
        data: s.data
      })) as any
    };
  }

  static createGauge(model: GaugeChartModel): EChartsOption {
    const base = BaseChartOptionFactory.createBaseOption(model.title);
    return {
      ...base,
      series: [
        {
          type: 'gauge',
          startAngle: 180,
          endAngle: 0,
          min: 0,
          max: 100,
          pointer: { show: true },
          progress: { show: true, overlap: false, roundCap: true, clip: false },
          axisLine: { lineStyle: { width: 14 } },
          detail: { valueAnimation: true, formatter: '{value}%', color: 'var(--text)', fontSize: 24 },
          data: [{ value: model.score, name: 'Score' }]
        }
      ]
    };
  }
}
