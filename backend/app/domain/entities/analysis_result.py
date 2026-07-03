from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from backend.app.domain.interfaces.dataset_frame import DatasetFrame
from backend.app.domain.value_objects.dataset_id import DatasetId
from backend.app.domain.value_objects.pipeline_state import PipelineState


class AnalyticsContext:
    """State object passed sequentially through the analytics pipeline."""

    def __init__(self, dataset_id: DatasetId, raw_dataset: DatasetFrame):
        self.dataset_id: DatasetId = dataset_id
        self.raw_dataset: DatasetFrame = raw_dataset

        self.state: PipelineState = PipelineState.VALIDATED

        self.cleaned_dataset: Optional[DatasetFrame] = None
        self.selected_features: List[str] = []
        self.scaled_features: Optional[DatasetFrame] = None
        self.pca_result: Dict[str, Any] = {}
        self.optimal_k: int = 0
        self.cluster_labels: List[int] = []
        self.centroids: Dict[str, Any] = {}

        self.profiling_result: Dict[str, Any] = {}
        self.cleaning_report: Dict[str, Any] = {}
        self.summary: Dict[str, Any] = {}
        self.category_summary: Dict[str, Any] = {}

        self.dashboard_dto: Dict[str, Any] = {}
        self.processing_metadata: Dict[str, Any] = {
            "dataset_id": str(dataset_id),
            "started_at": None,
            "finished_at": None,
            "duration": None,
            "algorithm": "MiniBatchKMeans",
            "scaler": None,
            "optimal_k": None,
            "random_seed": 42,
            "total_rows": 0,
            "total_columns": 0,
            "numeric_columns": 0,
            "categorical_columns": 0,
            "duplicate_rows_removed": 0,
            "missing_values_imputed": 0,
            "application_version": "1.0.0",
        }
        self.manifest: List[str] = []


class AnalysisResult(BaseModel):
    """Canonical Domain Entity representing the final analytics output."""

    dataset_id: str
    status: PipelineState
    profiling: Dict[str, Any] = Field(default_factory=dict)
    cleaning_summary: Dict[str, Any] = Field(default_factory=dict)
    clustering_summary: Dict[str, Any] = Field(default_factory=dict)
    category_summary: Dict[str, Any] = Field(default_factory=dict)
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)
    dashboard: Dict[str, Any] = Field(default_factory=dict)
