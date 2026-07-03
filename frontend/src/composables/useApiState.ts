import { ref } from 'vue';

export type UiState = 'idle' | 'loading' | 'success' | 'error' | 'empty';

export const useApiState = () => {
  const state = ref<UiState>('idle');
  const error = ref<Error | null>(null);

  const start = () => {
    state.value = 'loading';
    error.value = null;
  };
  const success = () => {
    state.value = 'success';
  };
  const fail = (err: Error) => {
    state.value = 'error';
    error.value = err;
  };
  const empty = () => {
    state.value = 'empty';
  };

  return { state, error, start, success, fail, empty };
};
