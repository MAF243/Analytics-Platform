import { useNotificationStore } from '../stores/notification';

export const useToast = () => {
  const store = useNotificationStore();
  return {
    toast: store.addToast,
    success: (title: string, desc?: string) =>
      store.addToast({ type: 'success', title, description: desc }),
    error: (title: string, desc?: string) =>
      store.addToast({ type: 'error', title, description: desc }),
    info: (title: string, desc?: string) =>
      store.addToast({ type: 'info', title, description: desc }),
    warning: (title: string, desc?: string) =>
      store.addToast({ type: 'warning', title, description: desc }),
  };
};
