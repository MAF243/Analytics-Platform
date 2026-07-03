import type { DashboardDTO } from '../types';

export class QualityService {
  /**
   * Calculates the overall dataset quality score (0-100).
   * Extensible for future metrics like outlier percentage, missing values, etc.
   */
  static calculateQualityScore(dashboardDto: DashboardDTO): number {
    const meta = dashboardDto.processing_metadata;
    if (!meta || meta.total_rows === 0) return 100; // Default if no data

    // Example calculation based on duplicates removed
    const originalRows = meta.total_rows;
    const duplicates = meta.duplicate_rows_removed;
    
    const validRows = originalRows - duplicates;
    const score = (validRows / originalRows) * 100;
    
    // Future metrics can deduct points here:
    // score -= missingValuePenalty;
    // score -= outlierPenalty;
    
    return Math.max(0, Math.min(100, Math.round(score * 100) / 100));
  }
}
