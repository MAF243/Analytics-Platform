import { defineComponent, h, ref, watch, onMounted } from 'vue';
import VChart from 'vue-echarts';
import { useThemeStore } from '../../stores/theme';
import { reportTelemetry, reportError, reportMetric } from '../../observability';

export const EChartsRenderer = defineComponent({
  props: { option: { type: Object, required: true } },
  setup(props) {
    const themeStore = useThemeStore();
    const chartRef = ref<any>(null);

    onMounted(() => {
      const startTime = performance.now();
      reportTelemetry('chart_mounted', { title: props.option.title?.text });
      // Record rendering duration approximation
      setTimeout(() => {
        reportMetric('chart_render_duration_ms', performance.now() - startTime, { title: props.option.title?.text });
      }, 0);
    });

    // When theme changes, we want to force ECharts to repaint because
    // it doesn't automatically detect CSS variable changes inside the Canvas.
    // By calling setOption with the same option, it redraws without losing state.
    watch(() => themeStore.isDark, () => {
      if (chartRef.value) {
        chartRef.value.setOption(props.option, { notMerge: false, replaceMerge: [] });
        reportTelemetry('theme_switched');
      }
    });

    return () => h(VChart, {
      ref: chartRef,
      option: props.option,
      autoresize: true,
      class: 'w-full h-full',
      onError: (err: Error) => reportError(err, { component: 'ChartRenderer', title: props.option.title?.text })
    });
  }
});
