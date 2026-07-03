import type { EChartsOption } from 'echarts';

export class BaseChartOptionFactory {
  /**
   * Generates the universal base configuration for all charts.
   * Ensures consistent typography, tooltips, responsive grid, ARIA, and export options.
   */
  static createBaseOption(title: string): EChartsOption {
    return {
      title: {
        text: title,
        left: 'center',
        textStyle: { color: 'var(--text)', fontSize: 16, fontWeight: 600, fontFamily: 'Inter, sans-serif' }
      },
      tooltip: {
        trigger: 'item',
        backgroundColor: 'var(--surface)',
        borderColor: 'var(--border)',
        textStyle: { color: 'var(--text)' },
        padding: [8, 12],
        borderRadius: 6
      },
      toolbox: {
        show: true,
        feature: {
          saveAsImage: {
            title: 'Save Image',
            type: 'png',
            pixelRatio: 2,
            backgroundColor: 'transparent'
          }
        },
        iconStyle: { borderColor: 'var(--muted-foreground)' }
      },
      grid: {
        top: 60,
        bottom: 40,
        left: 50,
        right: 40,
        containLabel: true
      },
      aria: {
        enabled: true,
        decal: { show: true }
      },
      animationDuration: 500,
      animationEasing: 'cubicOut'
    };
  }
}
