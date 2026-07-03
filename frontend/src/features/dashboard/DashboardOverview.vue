<script setup lang="ts">
import { computed } from 'vue';
import { DatabaseIcon, HashIcon, ClockIcon, ActivityIcon, FolderTreeIcon } from 'lucide-vue-next';
import type { DashboardDTO } from '../../types';
import StatCard from '../../components/ui/StatCard.vue';
import { QualityService } from '../../services/QualityService';

const props = defineProps<{ data: DashboardDTO }>();

const rowCount = computed(() => props.data.profiling.row_count);
const colCount = computed(() => props.data.profiling.column_count);
const clusterCount = computed(() => Object.keys(props.data.summary.clusters).length);
const qualityScore = computed(() => QualityService.calculateQualityScore(props.data));
const totalTime = computed(() => {
  const start = new Date(props.data.processing_metadata.started_at);
  const end = new Date(props.data.processing_metadata.finished_at);
  return ((end.getTime() - start.getTime()) / 1000).toFixed(2) + 's';
});
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
    <StatCard title="Quality Score" :value="`${qualityScore}%`" :icon="ActivityIcon" />
    <StatCard title="Total Rows" :value="rowCount" :icon="DatabaseIcon" />
    <StatCard title="Clusters Found" :value="clusterCount" :icon="FolderTreeIcon" />
    <StatCard title="Total Columns" :value="colCount" :icon="HashIcon" />
    <StatCard title="Processing Time" :value="totalTime" :icon="ClockIcon" />
  </div>
</template>
