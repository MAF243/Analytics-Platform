import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import UploadDropzone from '../src/features/upload/UploadDropzone.vue';

describe('UploadDropzone Advanced', () => {
  it('validates CSV with papaparse correctly', async () => {
    const wrapper = mount(UploadDropzone);

    const file = new File(['col1,col2\n1,2'], 'test.csv', { type: 'text/csv' });
    const input = wrapper.find('input[type="file"]');
    Object.defineProperty(input.element, 'files', { value: [file] });

    await input.trigger('change');

    // Wait for Papa.parse (async via readAsText / chunking)
    await new Promise(r => setTimeout(r, 100));

    // The component emits 'fileSelected' on success
    expect(wrapper.emitted('fileSelected')).toBeTruthy();
    expect(wrapper.emitted('fileSelected')![0][0]).toBe(file);
  });

  it('rejects invalid file type', async () => {
    const wrapper = mount(UploadDropzone);

    const file = new File(['txt'], 'test.txt', { type: 'text/plain' });
    const input = wrapper.find('input[type="file"]');
    Object.defineProperty(input.element, 'files', { value: [file] });

    await input.trigger('change');

    expect(wrapper.emitted('fileSelected')).toBeFalsy();
  });
});
