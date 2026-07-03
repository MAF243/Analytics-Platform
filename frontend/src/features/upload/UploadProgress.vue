<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  progress: number;
  status: 'uploading' | 'processing' | 'completed' | 'error';
}>();

const label = computed(() => {
  switch(props.status) {
    case 'uploading': return 'Uploading file...';
    case 'processing': return 'Processing dataset...';
    case 'completed': return 'Upload complete!';
    case 'error': return 'Upload failed';
    default: return '';
  }
});

const progressColor = computed(() => {
  if (props.status === 'error') return 'bg-destructive';
  if (props.status === 'completed') return 'bg-success';
  return 'bg-primary';
});
</script>

<template>
  <div class="w-full space-y-2" role="status" aria-live="polite">
    <div class="flex justify-between text-sm font-medium">
      <span :class="{'text-destructive': status === 'error'}">{{ label }}</span>
      <span v-if="status === 'uploading' || status === 'processing'">{{ progress }}%</span>
    </div>
    <div class="h-2 w-full overflow-hidden rounded-full bg-surface-variant">
      <div
        class="h-full transition-all duration-300 ease-out"
        :class="progressColor"
        :style="{ width: `${progress}%` }"
        :aria-valuenow="progress"
        aria-valuemin="0"
        aria-valuemax="100"
      ></div>
    </div>
  </div>
</template>
