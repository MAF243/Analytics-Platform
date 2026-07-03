import io
from datetime import datetime
from typing import Any, Dict, cast

import pandas as pd

from backend.app.core.exceptions import ApplicationException
from backend.app.core.serialization import JsonSerializer
from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.dataset_repository import DatasetRepository
from backend.app.domain.interfaces.metadata_repository import MetadataRepository
from backend.app.domain.interfaces.ml_services import (
    ICategorySummaryService,
    ICleaningService,
    IClusteringService,
    IDashboardBuilder,
    IElbowDetectionService,
    IFeatureSelectionService,
    IPCAService,
    IProfilingService,
    IScalingService,
    ISummaryService,
)
from backend.app.domain.interfaces.storage_repository import StorageRepository
from backend.app.domain.value_objects.dataset_id import DatasetId
from backend.app.infrastructure.ml.dataset_frame import PandasDatasetFrame


class RunAnalyticsUseCase:
    def __init__(
        self,
        dataset_repo: DatasetRepository,
        storage_repo: StorageRepository,
        metadata_repo: MetadataRepository,
        profiling_service: IProfilingService,
        cleaning_service: ICleaningService,
        feature_selection_service: IFeatureSelectionService,
        scaling_service: IScalingService,
        pca_service: IPCAService,
        elbow_service: IElbowDetectionService,
        clustering_service: IClusteringService,
        summary_service: ISummaryService,
        category_summary_service: ICategorySummaryService,
        dashboard_builder: IDashboardBuilder,
    ):
        self.dataset_repo = dataset_repo
        self.storage_repo = storage_repo
        self.metadata_repo = metadata_repo

        self.profiling_service = profiling_service
        self.cleaning_service = cleaning_service
        self.feature_selection_service = feature_selection_service
        self.scaling_service = scaling_service
        self.pca_service = pca_service
        self.elbow_service = elbow_service
        self.clustering_service = clustering_service
        self.summary_service = summary_service
        self.category_summary_service = category_summary_service
        self.dashboard_builder = dashboard_builder

    def execute(self, dataset_id_str: str) -> Dict[str, Any]:
        dataset_id = DatasetId(dataset_id_str)
        dataset = self.dataset_repo.get_by_id(dataset_id)
        if not dataset:
            raise ApplicationException("Dataset not found.")

        # Load Data
        raw_path = self.storage_repo.get_raw_dataset_path(dataset_id)
        try:
            df = pd.read_csv(raw_path)
        except Exception as e:
            raise ApplicationException(f"Failed to load dataset: {str(e)}")

        context = AnalyticsContext(dataset_id, PandasDatasetFrame(df))
        context.processing_metadata["started_at"] = datetime.utcnow().isoformat()

        # Pipeline Execution
        try:
            context = self.profiling_service.process(context)
            self._save_artifact(context, "profiling.json", context.profiling_result)

            context = self.cleaning_service.process(context)
            self._save_artifact(context, "cleaning.json", context.cleaning_report)

            # Save cleaned CSV
            if context.cleaned_dataset:
                buffer = io.StringIO()
                context.cleaned_dataset.get_raw_object().to_csv(buffer, index=False)
                buffer.seek(0)
                bytes_buffer = io.BytesIO(buffer.getvalue().encode("utf-8"))
                self.storage_repo.save_result_csv(
                    dataset_id, "cleaned.csv", bytes_buffer
                )

            context = self.feature_selection_service.process(context)
            self._save_artifact(
                context,
                "feature_selection.json",
                {"features": context.selected_features},
            )

            context = self.scaling_service.process(context)
            self._save_artifact(
                context,
                "scaling.json",
                {"scaler": context.processing_metadata.get("scaler")},
            )

            context = self.pca_service.process(context)
            self._save_artifact(context, "pca.json", context.pca_result)

            context = self.elbow_service.process(context)
            self._save_artifact(
                context,
                "elbow.json",
                {
                    "optimal_k": context.optimal_k,
                    "curve": context.processing_metadata.get("elbow_curve"),
                },
            )

            context = self.clustering_service.process(context)
            self._save_artifact(
                context, "clustering.json", {"centroids": context.centroids}
            )

            context = self.summary_service.process(context)
            self._save_artifact(context, "summary.json", context.summary)

            context = self.category_summary_service.process(context)
            self._save_artifact(
                context, "category_summary.json", context.category_summary
            )

            # Save clustered CSV
            if context.cleaned_dataset and context.cluster_labels:
                clustered_df = context.cleaned_dataset.get_raw_object().copy()
                clustered_df["Cluster"] = context.cluster_labels
                buffer = io.StringIO()
                clustered_df.to_csv(buffer, index=False)
                buffer.seek(0)
                bytes_buffer = io.BytesIO(buffer.getvalue().encode("utf-8"))
                self.storage_repo.save_result_csv(
                    dataset_id, "clustered.csv", bytes_buffer
                )

            context.processing_metadata["finished_at"] = datetime.utcnow().isoformat()

            # Build Dashboard DTO and save processing metadata/manifest
            self._save_artifact(
                context, "processing_metadata.json", context.processing_metadata
            )
            context = self.dashboard_builder.build(context)

        except Exception as e:
            # We would normally transition state to FAILED and save it,
            # but we can just raise for now
            raise ApplicationException(f"Analytics Pipeline Failed: {str(e)}")

        return cast(Dict[str, Any], JsonSerializer.to_native(context.dashboard_dto))

    def _save_artifact(
        self, context: AnalyticsContext, name: str, data: Dict[str, Any]
    ) -> None:
        self.metadata_repo.save_artifact(context.dataset_id, name, data)
        context.manifest.append(name)
