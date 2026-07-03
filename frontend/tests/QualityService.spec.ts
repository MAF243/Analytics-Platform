import { describe, it, expect } from 'vitest';
import { QualityService } from '../src/services/QualityService';
import type { DashboardDTO } from '../src/types';

describe('QualityService', () => {
  it('calculates 100% quality when no duplicates are removed', () => {
    const dto = {
      processing_metadata: {
        total_rows: 1000,
        duplicate_rows_removed: 0
      }
    } as DashboardDTO;
    expect(QualityService.calculateQualityScore(dto)).toBe(100);
  });

  it('calculates correct quality when duplicates exist', () => {
    const dto = {
      processing_metadata: {
        total_rows: 1000,
        duplicate_rows_removed: 100
      }
    } as DashboardDTO;
    expect(QualityService.calculateQualityScore(dto)).toBe(90); // 900 / 1000
  });

  it('handles zero total_rows to avoid division by zero', () => {
    const dto = {
      processing_metadata: {
        total_rows: 0,
        duplicate_rows_removed: 0
      }
    } as DashboardDTO;
    expect(QualityService.calculateQualityScore(dto)).toBe(100);
  });
});
