<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { AnalysisFacade, type AnalysisPollingStrategy } from '../../facades/AnalysisFacade';
import { useToast } from '../../composables/useToast';
import Container from '../../components/layout/Container.vue';
import Card from '../../components/ui/Card.vue';
import Button from '../../components/ui/Button.vue';
import AnalysisProgress from './AnalysisProgress.vue';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const datasetId = route.params.dataset_id as string;

const statusMessage = ref('Initializing analysis pipeline...');
const progress = ref(0);
const hasError = ref(false);

let poller: AnalysisPollingStrategy | null = null;

onMounted(() => {
  if (!datasetId) {
    toast.error('Invalid Route', 'Dataset ID is missing.');
    router.push('/');
    return;
  }

  poller = AnalysisFacade.createPoller(datasetId, {
    onStatusChange: (status) => {
      progress.value = status.progress || progress.value;

      switch(status.status) {
        case 'queued':
          statusMessage.value = 'Dataset queued for processing...';
          break;
        case 'processing':
          statusMessage.value = status.message || 'Cleaning and profiling data...';
          break;
        case 'completed':
          statusMessage.value = 'Analysis complete!';
          progress.value = 100;
          break;
      }
    },
    onComplete: () => {
      toast.success('Analysis Completed', 'Navigating to Dashboard...');
      setTimeout(() => {
        router.push(`/dashboard/${datasetId}`);
      }, 1000);
    },
    onError: (err) => {
      hasError.value = true;
      statusMessage.value = err.message;
      toast.error('Analysis Failed', err.message);
    }
  });

  poller.start();
});

onUnmounted(() => {
  if (poller) {
    poller.stop();
  }
});

const handleCancel = () => {
  if (poller) poller.stop();
  router.push('/');
};

const handleRetry = () => {
  hasError.value = false;
  statusMessage.value = 'Retrying analysis...';
  progress.value = 0;
  if (poller) poller.start();
};
</script>

<template>
  <Container class="flex min-h-[calc(100vh-4rem)] items-center justify-center py-12">
    <Card class="w-full max-w-xl p-8 shadow-elevation-2">
      <div class="mb-8 text-center space-y-2">
        <h1 class="text-2xl font-bold tracking-tight text-text">Dataset Analysis</h1>
        <p class="text-sm text-muted-foreground">ID: {{ datasetId }}</p>
      </div>

      <div class="space-y-8">
        <AnalysisProgress :progress="progress" :message="statusMessage" :is-error="hasError" />

        <div class="flex justify-end gap-3 pt-4 border-t border-border">
          <Button v-if="hasError" variant="default" @click="handleRetry">Retry</Button>
          <Button variant="outline" @click="handleCancel">Cancel</Button>
        </div>
      </div>
    </Card>
  </Container>
</template>
