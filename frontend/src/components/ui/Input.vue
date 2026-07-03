<script setup lang="ts">
import { useId } from 'vue';
interface Props {
  modelValue: string;
  label?: string;
  error?: string;
  id?: string;
  type?: string;
  placeholder?: string;
}
const props = withDefaults(defineProps<Props>(), {
  type: 'text',
});
const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>();
const inputId = props.id || useId();
</script>

<template>
  <div class="space-y-1 w-full">
    <label
      v-if="label"
      :for="inputId"
      class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
    >
      {{ label }}
    </label>
    <input
      :id="inputId"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      class="flex h-10 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
      :class="{ 'border-error': error }"
      :aria-invalid="!!error"
    />
    <p v-if="error" class="text-[0.8rem] font-medium text-error" role="alert">{{ error }}</p>
  </div>
</template>
