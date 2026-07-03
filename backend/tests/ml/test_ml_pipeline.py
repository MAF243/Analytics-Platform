import io
from pathlib import Path
from typing import Generator

import pandas as pd
import pytest

from backend.app.application.use_cases.run_analytics import RunAnalyticsUseCase
from backend.app.core.config import settings
from backend.app.domain.entities.dataset import Dataset
from backend.app.domain.value_objects.dataset_id import DatasetId
from backend.app.infrastructure.ml.cleaning import PandasCleaningService
from backend.app.infrastructure.ml.clustering import MiniBatchKMeansClusteringService
from backend.app.infrastructure.ml.dashboard_builder import RepositoryDashboardBuilder
from backend.app.infrastructure.ml.elbow import ElbowDetectionService
from backend.app.infrastructure.ml.feature_selection import (
    PandasFeatureSelectionService,
)
from backend.app.infrastructure.ml.pca import ScikitLearnPCAService
from backend.app.infrastructure.ml.profiling import PandasProfilingService
from backend.app.infrastructure.ml.scaling import PandasScalingService
from backend.app.infrastructure.ml.summaries import (
    PandasCategorySummaryService,
    PandasSummaryService,
)
from backend.app.infrastructure.storage.local_storage import LocalStorageRepositoryImpl


@pytest.fixture
def storage_repo(tmp_path: Path) -> Generator[LocalStorageRepositoryImpl, None, None]:
    original_path = settings.storage_base_path
    settings.storage_base_path = str(tmp_path / "data")
    repo = LocalStorageRepositoryImpl()
    yield repo
    settings.storage_base_path = original_path


def test_full_ml_pipeline_deterministic(
    storage_repo: LocalStorageRepositoryImpl,
) -> None:
    # 1. Setup Mock Dataset
    dataset_id_str = "123e4567-e89b-12d3-a456-426614174000"
    ds_id = DatasetId(dataset_id_str)

    # Create Synthetic Data
    data = {
        "id": range(100),
        "feature_1": [i * 2.5 + (i % 3) for i in range(100)],
        "feature_2": [100 - i for i in range(100)],
        "category": ["A", "B", "A", "C"] * 25,
        "date": pd.date_range(start="2024-01-01", periods=100),
    }
    df = pd.DataFrame(data)

    # Add some nulls to test cleaning
    df.loc[10, "feature_1"] = None
    df.loc[20, "category"] = None

    # Write to simulated storage
    storage_repo.prepare_storage_layout(ds_id)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    storage_repo.save_raw_dataset(ds_id, buffer)

    # Create Dataset entity metadata
    ds = Dataset(id=ds_id, filename="test.csv", size_bytes=1000)
    storage_repo.save(ds)

    # 2. Setup Use Case
    use_case = RunAnalyticsUseCase(
        dataset_repo=storage_repo,
        storage_repo=storage_repo,
        metadata_repo=storage_repo,
        profiling_service=PandasProfilingService(),
        cleaning_service=PandasCleaningService(),
        feature_selection_service=PandasFeatureSelectionService(),
        scaling_service=PandasScalingService(),
        pca_service=ScikitLearnPCAService(),
        elbow_service=ElbowDetectionService(),
        clustering_service=MiniBatchKMeansClusteringService(),
        summary_service=PandasSummaryService(),
        category_summary_service=PandasCategorySummaryService(),
        dashboard_builder=RepositoryDashboardBuilder(storage_repo),
    )

    # 3. Execute Pipeline
    dashboard = use_case.execute(dataset_id_str)

    # 4. Assertions
    assert dashboard["dataset_id"] == dataset_id_str

    # Check Profiling
    assert dashboard["profiling"]["row_count"] == 100
    assert dashboard["profiling"]["column_count"] == 5

    # Check Cleaning
    assert dashboard["cleaning"]["missing_values_imputed"] == 2

    # Check Feature Selection (drops id, date, category)
    assert "feature_1" in dashboard["features_selected"]
    assert "feature_2" in dashboard["features_selected"]
    assert "id" not in dashboard["features_selected"]

    # Check Elbow/Clustering
    optimal_k = dashboard["processing_metadata"]["optimal_k"]
    assert optimal_k > 0
    assert "clusters" in dashboard["summary"]

    # Check PCA structure
    assert "pca_points" in dashboard["pca"]
    pca_pts = dashboard["pca"]["pca_points"]
    assert len(pca_pts) == 100
    assert "x" in pca_pts[0]
    assert "y" in pca_pts[0]
    assert "cluster" in pca_pts[0]

    # Check consistency
    cluster_sizes = sum(c["size"] for c in dashboard["summary"]["clusters"].values())
    assert dashboard["profiling"]["row_count"] == len(pca_pts) == cluster_sizes == 100

    # Check saved artifacts
    assert (
        Path(settings.storage_base_path) / dataset_id_str / "metadata" / "manifest.json"
    ).exists()
    assert (
        Path(settings.storage_base_path) / dataset_id_str / "results" / "cleaned.csv"
    ).exists()
    assert (
        Path(settings.storage_base_path) / dataset_id_str / "results" / "clustered.csv"
    ).exists()
