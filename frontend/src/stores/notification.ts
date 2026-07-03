import { defineStore } from 'pinia';
import { ref } from 'vue';

export type ToastType = 'info' | 'success' | 'warning' | 'error';

export interface ToastMessage {
  id: string;
  title: string;
  description?: string;
  type: ToastType;
  duration?: number;
}

export const useNotificationStore = defineStore('notification', () => {
  const toasts = ref<ToastMessage[]>([]);

  const addToast = (toast: Omit<ToastMessage, 'id'>) => {
    const id = Math.random().toString(36).substring(2, 9);
    toasts.value.push({ ...toast, id });
    if (toast.duration !== 0) {
      setTimeout(() => removeToast(id), toast.duration || 4000);
    }
  };

  const removeToast = (id: string) => {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  };

  return { toasts, addToast, removeToast };
});
