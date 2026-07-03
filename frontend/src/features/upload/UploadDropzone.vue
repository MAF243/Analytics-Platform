<script setup lang="ts">
/* global File, HTMLInputElement, FileReader, DragEvent, Event */
import { ref } from 'vue';
import { UploadCloudIcon, FileTextIcon } from 'lucide-vue-next';
import { cn } from '../../utils/cn';
import { APP_CONFIG } from '../../config/app.config';
import Papa from 'papaparse';
import { container } from '../../di/container';

const emit = defineEmits<{
  (e: 'fileSelected', file: File): void;
  (e: 'error', message: string): void;
}>();

const isDragging = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

const readFirst64KB = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const chunk = file.slice(0, 64 * 1024);
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target?.result as string);
    reader.onerror = () => reject(new Error('Failed to read file chunk'));
    reader.readAsText(chunk, 'utf-8');
  });
};

const validateCSVContent = async (file: File): Promise<boolean> => {
  try {
    const content = await readFirst64KB(file);
    if (!content.trim()) {
      emit('error', 'The file appears to be empty.');
      return false;
    }

    return new Promise((resolve) => {
      Papa.parse(content, {
        preview: 20, // Only parse first 20 rows
        skipEmptyLines: true,
        complete: (results) => {
          if (results.errors.length > 0 && results.errors[0].code !== 'UndetectableDelimiter') {
            container.logger.warn('CSV Parse Error', { errors: results.errors });
            // Note: we don't strictly fail on Unquoted/Delimiter errors in partial chunks unless critical.
          }

          const data = results.data as string[][];
          if (data.length < 2) {
            emit('error', 'The CSV must contain at least a header and one data row.');
            resolve(false);
            return;
          }

          const headerCols = data[0].length;
          // Verify columns consistency
          for (let i = 1; i < data.length; i++) {
            if (data[i].length !== headerCols) {
              // Note: the last row in a 64KB chunk might be cut in half, so we ignore the very last parsed row
              if (i === data.length - 1) continue; 

              emit('error', `Column count mismatch at row ${i + 1}. Expected ${headerCols}, found ${data[i].length}.`);
              resolve(false);
              return;
            }
          }
          resolve(true);
        },
        error: (err: any) => {
          container.logger.error(err as Error, { source: 'PapaParse' });
          emit('error', 'Malformed CSV file.');
          resolve(false);
        }
      });
    });
  } catch {
    emit('error', 'Failed to read file.');
    return false;
  }
};

const validateFileMetadata = (file: File): boolean => {
  if (!file) {
    emit('error', 'No file selected.');
    return false;
  }
  if (!(APP_CONFIG.supportedUploadMimeTypes as readonly string[]).includes(file.type) && !file.name.endsWith('.csv')) {
    emit('error', 'Unsupported file type. Please upload a CSV.');
    return false;
  }
  if (file.size > APP_CONFIG.maxUploadSizeBytes) {
    emit('error', `File size exceeds ${APP_CONFIG.maxUploadSizeBytes / (1024 * 1024)}MB limit.`);
    return false;
  }
  return true;
};

const handleFile = async (file: File) => {
  if (validateFileMetadata(file)) {
    const isContentValid = await validateCSVContent(file);
    if (isContentValid) {
      emit('fileSelected', file);
    }
  }
};

const onDrop = (e: DragEvent) => {
  isDragging.value = false;
  if (e.dataTransfer?.files.length) {
    handleFile(e.dataTransfer.files[0]);
  }
};

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files?.length) {
    handleFile(target.files[0]);
    if (fileInput.value) fileInput.value.value = '';
  }
};

const openFileDialog = () => {
  fileInput.value?.click();
};
</script>

<template>
  <div
    class="relative group cursor-pointer outline-none"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="onDrop"
    @click="openFileDialog"
    @keydown.enter.prevent="openFileDialog"
    tabindex="0"
    role="button"
    aria-label="File Upload Dropzone"
  >
    <input
      type="file"
      ref="fileInput"
      class="hidden"
      accept=".csv,text/csv,application/vnd.ms-excel"
      @change="onFileChange"
    />

    <div
      :class="cn(
        'flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-12 transition-all duration-200 ease-in-out focus-visible:ring-2 focus-visible:ring-primary',
        isDragging ? 'border-primary bg-primary/5' : 'border-border bg-surface hover:border-primary/50 hover:bg-surface-variant'
      )"
    >
      <div class="mb-4 rounded-full bg-surface-variant p-4 text-primary group-hover:scale-110 transition-transform">
        <UploadCloudIcon class="h-8 w-8" />
      </div>
      <p class="mb-1 text-lg font-semibold text-text">Click or drag file to this area</p>
      <p class="mb-4 text-sm text-muted-foreground">Support for a single or bulk CSV upload.</p>

      <div class="flex items-center gap-2 text-xs text-muted-foreground">
        <FileTextIcon class="h-4 w-4" />
        <span>Max file size: 50MB</span>
      </div>
    </div>
  </div>
</template>
