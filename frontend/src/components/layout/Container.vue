<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '../../utils/cn';
const props = defineProps<{ class?: any }>();
const classes = computed(() => cn('mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8', props.class));
</script>
<template>
  <div :class="classes"><slot /></div>
</template>
