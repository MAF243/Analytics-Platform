<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue';
import { AlertTriangleIcon } from 'lucide-vue-next';
import Button from './Button.vue';
import { container } from '../../di/container';

const error = ref<Error | null>(null);

onErrorCaptured((err) => {
  container.logger.error(err as Error, { source: 'ErrorBoundary' });
  error.value = err as Error;
  return false; // Stop propagation
});

const retry = () => {
  error.value = null;
};
</script>

<template>
  <div v-if="error" class="flex flex-col items-center justify-center p-6 border border-destructive/20 bg-destructive/5 rounded-lg w-full h-full min-h-[200px]">
    <AlertTriangleIcon class="h-8 w-8 text-destructive mb-3" />
    <h3 class="text-sm font-semibold text-destructive mb-1">Widget Failed to Load</h3>
    <p class="text-xs text-muted-foreground mb-4 text-center max-w-[250px]">{{ error.message }}</p>
    <Button variant="outline" size="sm" @click="retry">Retry Widget</Button>
  </div>
  <slot v-else></slot>
</template>
