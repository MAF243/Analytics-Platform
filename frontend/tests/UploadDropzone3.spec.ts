import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import UploadDropzone from '../src/features/upload/UploadDropzone.vue';

vi.mock('papaparse', () => ({
  default: {
    parse: vi.fn((content, config) => {
      // Simulate complete callback for success
      if (content === 'success') {
        config.complete({ errors: [], data: [['col1', 'col2'], ['1', '2']] });
      } else if (content === 'empty') {
        config.complete({ errors: [], data: [] });
      } else if (content === 'error') {
        config.error(new Error('Parse error'));
      }
    })
  }
}));

describe('UploadDropzone PapaParse Mocked', () => {

  it('handles PapaParse empty fields', async () => {
    const wrapper = mount(UploadDropzone);
    const file = new File(['empty'], 'empty.csv', { type: 'text/csv' });
    const input = wrapper.find('input[type="file"]');
    Object.defineProperty(input.element, 'files', { value: [file] });

    await input.trigger('change');
    await new Promise(r => setTimeout(r, 0));

    expect(wrapper.emitted('fileSelected')).toBeFalsy();
  });

  it('handles PapaParse error', async () => {
    const wrapper = mount(UploadDropzone);
    const file = new File(['error'], 'error.csv', { type: 'text/csv' });
    const input = wrapper.find('input[type="file"]');
    Object.defineProperty(input.element, 'files', { value: [file] });

    await input.trigger('change');
    await new Promise(r => setTimeout(r, 0));

    expect(wrapper.emitted('fileSelected')).toBeFalsy();
  });
});
