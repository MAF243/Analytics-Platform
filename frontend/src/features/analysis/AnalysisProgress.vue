<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  progress?: number;
  message?: string;
  isError?: boolean;
}>();

const pct = computed(() => props.progress || 0);
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center text-sm font-medium">
      <span :class="{'text-destructive': isError}">{{ message || (isError ? 'Analysis Failed' : 'Analyzing dataset...') }}</span>
      <span v-if="!isError">{{ pct }}%</span>
    </div>
    <div class="h-2 w-full overflow-hidden rounded-full bg-surface-variant">
      <div
        class="h-full transition-all duration-500 ease-in-out"
        :class="isError ? 'bg-destructive' : 'bg-primary'"
        :style="{ width: `${pct}%` }"
      ></div>
    </div>
  </div>
</template>
