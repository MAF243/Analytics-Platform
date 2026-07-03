import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import UploadDropzone from '../src/features/upload/UploadDropzone.vue';
import { APP_CONFIG } from '../src/config/app.config';

describe('UploadDropzone Validation', () => {
  it('emits fileSelected when a valid CSV is selected', async () => {
    const wrapper = mount(UploadDropzone);
    const validFile = new File(['a,b\n1,2'], 'data.csv', { type: 'text/csv' });

    // @ts-expect-error bypass private vm typing
    await wrapper.vm.handleFile(validFile);

    expect(wrapper.emitted('fileSelected')).toBeTruthy();
    expect(wrapper.emitted('fileSelected')![0]).toEqual([validFile]);
  });

  it('emits error and rejects file if oversized', async () => {
    const wrapper = mount(UploadDropzone);

    // Mock file larger than APP_CONFIG max (50MB by default)
    const largeFile = new File([''], 'huge.csv', { type: 'text/csv' });
    Object.defineProperty(largeFile, 'size', { value: APP_CONFIG.maxUploadSizeBytes + 1024 });

    // @ts-expect-error bypass private vm typing
    await wrapper.vm.handleFile(largeFile);

    expect(wrapper.emitted('fileSelected')).toBeFalsy();
    expect(wrapper.emitted('error')).toBeTruthy();
    expect(wrapper.emitted('error')![0][0]).toContain('exceeds');
  });

  it('emits error if file is unsupported mime type', async () => {
    const wrapper = mount(UploadDropzone);
    const exeFile = new File([''], 'malicious.exe', { type: 'application/x-msdownload' });

    // @ts-expect-error bypass private vm typing
    await wrapper.vm.handleFile(exeFile);

    expect(wrapper.emitted('fileSelected')).toBeFalsy();
    expect(wrapper.emitted('error')).toBeTruthy();
    expect(wrapper.emitted('error')![0][0]).toContain('Unsupported file type');
  });
});
