import { describe, it, expect } from 'vitest';
import { cn } from '../src/utils/cn';

describe('cn utility', () => {
  it('merges tailwind classes properly', () => {
    const result = cn('px-2 py-1 bg-red-500', 'p-4 bg-blue-500');
    // tailwind-merge resolves p-4 overriding px-2 py-1, and bg-blue overriding bg-red
    expect(result).toBe('p-4 bg-blue-500');
  });

  it('supports conditional classes via clsx', () => {
    const isActive = true;
    const result = cn('text-sm', { 'text-primary': isActive, 'text-muted': !isActive });
    expect(result).toBe('text-sm text-primary');
  });
});
