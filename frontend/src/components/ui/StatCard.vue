<script setup lang="ts">
import Card from './Card.vue';

defineProps<{
  title: string;
  value: string | number;
  icon?: any; // lucide icon
  trend?: string;
  trendUp?: boolean;
}>();
</script>

<template>
  <Card class="p-6">
    <div class="flex items-center justify-between pb-2">
      <h3 class="text-sm font-medium text-muted-foreground">{{ title }}</h3>
      <component :is="icon" v-if="icon" class="h-4 w-4 text-muted-foreground" />
    </div>
    <div class="text-2xl font-bold text-text">{{ value }}</div>
    <p v-if="trend" class="text-xs mt-1" :class="trendUp ? 'text-success' : 'text-error'">
      {{ trend }}
    </p>
  </Card>
</template>
