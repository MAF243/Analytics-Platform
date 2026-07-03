export interface ProfilingDTO {
  row_count: number;
  column_count: number;
  columns: Record<string, string>; // specific type mapped to pandas dtypes
}

export interface ClusterSummaryDTO {
  size: number;
  percentage: number;
  features: Record<string, number>;
}

export interface CategorySummaryDTO {
  frequency: Record<string, number>;
  unique_values: number;
  mode: string;
}

export interface SummaryDTO {
  clusters: Record<string, ClusterSummaryDTO>;
  categories: Record<string, CategorySummaryDTO>;
}

export interface PcaPointDTO {
  x: number;
  y: number;
  cluster: string;
}

export interface PcaDTO {
  pca_points: PcaPointDTO[];
}

export interface ProcessingMetadataDTO {
  total_rows: number;
  duplicate_rows_removed: number;
  started_at: string;
  finished_at: string;
}

export interface DashboardDTO {
  dataset_id: string;
  profiling: ProfilingDTO;
  features_selected: string[];
  pca: PcaDTO;
  summary: SummaryDTO;
  processing_metadata: ProcessingMetadataDTO;
}

export interface UploadResponseDTO {
  dataset_id: string;
}
