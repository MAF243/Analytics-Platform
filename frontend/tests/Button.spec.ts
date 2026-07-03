import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Button from '../src/components/ui/Button.vue';

describe('Button Primitive', () => {
  it('renders default slot content', () => {
    const wrapper = mount(Button, {
      slots: { default: 'Click Me' }
    });
    expect(wrapper.text()).toContain('Click Me');
  });

  it('applies variant classes via CVA', () => {
    const wrapper = mount(Button, {
      props: { variant: 'destructive' }
    });
    expect(wrapper.classes()).toContain('bg-destructive');
  });

  it('disables button when loading', () => {
    const wrapper = mount(Button, {
      props: { loading: true }
    });
    expect(wrapper.attributes('disabled')).toBeDefined();
    expect(wrapper.find('span.animate-spin').exists()).toBe(true);
  });
});
