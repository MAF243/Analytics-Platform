<script setup lang="ts">
import { InboxIcon } from 'lucide-vue-next';

defineProps<{
  title?: string;
  message?: string;
}>();
</script>

<template>
  <div class="flex flex-col items-center justify-center h-full min-h-[200px] w-full text-muted-foreground p-6">
    <div class="bg-surface/50 p-4 rounded-full mb-4 border border-dashed border-border">
      <InboxIcon class="w-8 h-8 opacity-50" />
    </div>
    <h3 class="font-medium text-text mb-1">{{ title || 'No Data Available' }}</h3>
    <p class="text-sm text-center max-w-sm">
      {{ message || 'There is no data to display for this visualization at the moment.' }}
    </p>
  </div>
</template>
