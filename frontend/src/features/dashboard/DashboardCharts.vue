<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue';
import type { DashboardDTO } from '../../types';
import { DashboardMapper } from '../../mappers/DashboardMapper';
import { EChartsOptionFactory } from '../../chart-models/factory';
import ChartCard from '../../components/dashboard/ChartCard.vue';

// Async Component with strict timeout/fallback
const ChartRenderer = defineAsyncComponent({
  loader: () => import('../../components/charts/ChartRenderer').then((m) => m.EChartsRenderer),
  timeout: 10000,
});

const props = defineProps<{ data: DashboardDTO }>();

const gaugeOption = computed(() => {
  const model = DashboardMapper.toDataQualityGaugeModel(props.data);
  return EChartsOptionFactory.createGauge(model);
});

const donutOption = computed(() => {
  const model = DashboardMapper.toClusterDonutModel(props.data);
  return EChartsOptionFactory.createDonut(model);
});

const barOption = computed(() => {
  const model = DashboardMapper.toCategoryBarModel(props.data);
  return EChartsOptionFactory.createBar(model);
});

const scatterOption = computed(() => {
  const model = DashboardMapper.toPcaScatterModel(props.data);
  return EChartsOptionFactory.createScatter(model);
});

const stackedBarOption = computed(() => {
  const model = DashboardMapper.toFeatureMeansModel(props.data);
  return EChartsOptionFactory.createStackedBar(model);
});

// Calculate empty states
const hasCategories = computed(() => Object.keys(props.data.summary.categories).length > 0);
const hasClusters = computed(() => Object.keys(props.data.summary.clusters).length > 0);
const hasPca = computed(() => props.data.pca && props.data.pca.pca_points.length > 0);
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
    <!-- Row 1: KPI & Distribution -->
    <ChartCard :isEmpty="false" class="xl:col-span-1">
      <ChartRenderer :option="gaugeOption" />
    </ChartCard>

    <ChartCard :isEmpty="!hasClusters" class="xl:col-span-1">
      <ChartRenderer :option="donutOption" />
    </ChartCard>

    <ChartCard :isEmpty="!hasCategories" class="xl:col-span-2">
      <ChartRenderer :option="barOption" />
    </ChartCard>

    <!-- Row 2: Deep Analysis -->
    <ChartCard :isEmpty="!hasPca" class="xl:col-span-2 min-h-[400px]">
      <ChartRenderer :option="scatterOption" />
    </ChartCard>

    <ChartCard :isEmpty="!hasClusters" class="xl:col-span-2 min-h-[400px]">
      <ChartRenderer :option="stackedBarOption" />
    </ChartCard>
  </div>
</template>
