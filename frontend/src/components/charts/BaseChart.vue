<script setup lang="ts">
import { computed } from 'vue';
import { useThemeStore } from '../../stores/theme';
import VChart from 'vue-echarts';

// We rely on dynamic importing and manual chunks for echarts
// to prevent massive initial bundle sizes.

defineProps<{ 
  option: any;
  loading?: boolean;
  isEmpty?: boolean;
  error?: Error | null;
}>();

const themeStore = useThemeStore();
const theme = computed(() => (themeStore.isDark ? 'dark' : 'light'));
</script>

<template>
  <div class="relative w-full h-full min-h-[300px]">
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-surface/50 z-10">
      <slot name="loading">
        <span class="animate-spin" aria-hidden="true">↻</span>
      </slot>
    </div>
    <div v-else-if="error" class="absolute inset-0 flex items-center justify-center text-error z-10">
      <slot name="error">
        <span>{{ error.message || 'Error loading chart' }}</span>
      </slot>
    </div>
    <div v-else-if="isEmpty" class="absolute inset-0 flex items-center justify-center text-muted-foreground z-10">
      <slot name="empty">
        <span>No data available</span>
      </slot>
    </div>

    <VChart 
      v-show="!loading && !error && !isEmpty" 
      :option="option" 
      :theme="theme" 
      autoresize 
      class="w-full h-full" 
    />
  </div>
</template>
