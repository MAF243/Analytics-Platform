<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '../../utils/cn';

const props = defineProps<{ class?: any; gap?: 1 | 2 | 4 | 8 | 16 }>();
const gapMap = { 1: 'gap-1', 2: 'gap-2', 4: 'gap-4', 8: 'gap-8', 16: 'gap-16' };
const classes = computed(() => cn('flex flex-col', props.gap ? gapMap[props.gap] : 'gap-4', props.class));
</script>
<template>
  <div :class="classes"><slot /></div>
</template>
