<script setup lang="ts">
import Card from '../ui/Card.vue';
import ErrorBoundary from '../ui/ErrorBoundary.vue';
import Skeleton from '../ui/Skeleton.vue';
import EmptyState from './EmptyState.vue';

defineProps<{
  isEmpty?: boolean;
}>();
</script>

<template>
  <Card class="flex flex-col relative w-full h-full min-h-[350px] p-4 bg-surface border-border shadow-sm">
    <ErrorBoundary>
      <div v-if="isEmpty" class="flex-1 flex items-center justify-center">
        <EmptyState />
      </div>
      <Suspense v-else>
        <template #default>
          <div class="flex-1 w-full h-full relative">
            <slot />
          </div>
        </template>
        <template #fallback>
          <div class="flex-1 w-full h-full p-2">
            <Skeleton class="w-full h-full rounded-md" />
          </div>
        </template>
      </Suspense>
    </ErrorBoundary>
  </Card>
</template>
