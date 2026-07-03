<script setup lang="ts">
/* global File, AbortController */
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { UploadFacade } from '../../facades/UploadFacade';
import { useToast } from '../../composables/useToast';
import { ApiException } from '../../exceptions';
import Container from '../../components/layout/Container.vue';
import Card from '../../components/ui/Card.vue';
import Button from '../../components/ui/Button.vue';
import UploadDropzone from './UploadDropzone.vue';
import UploadProgress from './UploadProgress.vue';

const router = useRouter();
const toast = useToast();

const currentFile = ref<File | null>(null);
const uploadStatus = ref<'idle' | 'uploading' | 'processing' | 'completed' | 'error'>('idle');
const progress = ref(0);
let abortController: AbortController | null = null;

const onFileSelected = async (file: File) => {
  currentFile.value = file;
  await startUpload();
};

const startUpload = async () => {
  if (!currentFile.value) return;

  uploadStatus.value = 'uploading';
  progress.value = 0;
  abortController = new AbortController();

  try {
    const response = await UploadFacade.upload(
      currentFile.value,
      (pct) => { 
        progress.value = pct;
        if (pct === 100) uploadStatus.value = 'processing';
      },
      abortController.signal
    );

    uploadStatus.value = 'completed';
    toast.success('Upload Successful', `Dataset ${response.dataset_id} created.`);

    // Redirect to analysis
    setTimeout(() => {
      router.push(`/analysis/${response.dataset_id}`);
    }, 1000);

  } catch (err: any) {
    if (err.name === 'CanceledError' || err.message === 'canceled') {
      toast.info('Upload Canceled');
      uploadStatus.value = 'idle';
      currentFile.value = null;
    } else {
      uploadStatus.value = 'error';
      const msg = err instanceof ApiException ? err.message : 'An unknown error occurred.';
      toast.error('Upload Failed', msg);
    }
  }
};

const cancelUpload = () => {
  if (abortController) {
    abortController.abort();
    abortController = null;
  }
};

const resetUpload = () => {
  uploadStatus.value = 'idle';
  progress.value = 0;
  currentFile.value = null;
};
</script>

<template>
  <Container class="flex min-h-[calc(100vh-4rem)] items-center justify-center py-12">
    <Card class="w-full max-w-2xl p-8 shadow-elevation-2">
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold tracking-tight text-text">Dataset Upload</h1>
        <p class="mt-2 text-muted-foreground">Upload your raw CSV dataset to begin the cleaning and profiling process.</p>
      </div>

      <div v-if="uploadStatus === 'idle'">
        <UploadDropzone @file-selected="onFileSelected" @error="(msg) => toast.error('Validation Error', msg)" />
      </div>

      <div v-else class="space-y-6">
        <div class="flex items-center gap-4 rounded-lg border bg-surface-variant/50 p-4">
          <div class="flex-1 min-w-0">
            <p class="truncate font-medium text-text">{{ currentFile?.name }}</p>
            <p class="text-sm text-muted-foreground">{{ currentFile ? (currentFile.size / (1024*1024)).toFixed(2) : 0 }} MB</p>
          </div>
        </div>

        <UploadProgress :progress="progress" :status="uploadStatus" />

        <div class="flex justify-end gap-3 pt-4">
          <Button v-if="uploadStatus === 'error'" variant="outline" @click="resetUpload">Try Again</Button>
          <Button v-if="uploadStatus === 'uploading' || uploadStatus === 'processing'" variant="destructive" @click="cancelUpload">Cancel</Button>
        </div>
      </div>
    </Card>
  </Container>
</template>
