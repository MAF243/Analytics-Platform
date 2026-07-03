<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { reportMetric } from '../../observability';
import { dashboardQuery } from '../../queries/DashboardQuery';
import { useApiState } from '../../composables/useApiState';
import { useToast } from '../../composables/useToast';
import type { DashboardDTO } from '../../types';

import DashboardOverview from './DashboardOverview.vue';
import DashboardCharts from './DashboardCharts.vue';
import DashboardSidebar from './DashboardSidebar.vue';

import Button from '../../components/ui/Button.vue';
import Skeleton from '../../components/ui/Skeleton.vue';

const setupStart = window.performance.now();

const route = useRoute();
const datasetId = route.params.dataset_id as string;
const toast = useToast();

const { state, error, start, success, fail } = useApiState();
const dashboardData = ref<DashboardDTO | null>(null);

const fetchDashboard = async (forceRefresh = false) => {
  start();
  try {
    const data = await dashboardQuery.fetch(datasetId, forceRefresh);
    dashboardData.value = data;
    success();
  } catch (err: any) {
    fail(err);
    toast.error('Dashboard Error', err.message);
  }
};

onMounted(() => {
  reportMetric('dashboard_render_duration_ms', window.performance.now() - setupStart);
  fetchDashboard();
});
</script>

<template>
  <div class="flex h-screen bg-background overflow-hidden">
    <DashboardSidebar />

    <main class="flex-1 overflow-y-auto p-8">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold tracking-tight text-text">Analytics Dashboard</h1>
          <p class="text-sm text-muted-foreground">ID: {{ datasetId }}</p>
        </div>
        <Button variant="outline" @click="fetchDashboard(true)" :loading="state === 'loading'">Refresh Cache</Button>
      </div>

      <!-- Loading State -->
      <div v-if="state === 'loading' && !dashboardData" class="space-y-4">
        <div class="grid grid-cols-4 gap-4"><Skeleton class="h-24 w-full" v-for="i in 4" :key="i"/></div>
        <div class="grid grid-cols-2 gap-4"><Skeleton class="h-[400px] w-full" v-for="i in 2" :key="i"/></div>
      </div>

      <!-- Error State -->
      <div v-else-if="state === 'error'" class="flex flex-col items-center justify-center h-64 border border-dashed rounded-lg bg-surface">
        <p class="text-destructive font-medium mb-2">Failed to load dashboard</p>
        <p class="text-sm text-muted-foreground mb-4">{{ error?.message }}</p>
        <Button @click="fetchDashboard()">Retry</Button>
      </div>

      <!-- Success State -->
      <div v-else-if="dashboardData">
        <DashboardOverview :data="dashboardData" />
        <DashboardCharts :data="dashboardData" />
      </div>
    </main>
  </div>
</template>
