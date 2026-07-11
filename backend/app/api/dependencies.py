from fastapi import Request

from backend.app.application.orchestration.analysis_executor import AnalysisExecutor
from backend.app.application.ports.analysis_job_repository import (
    AnalysisJobRepository,
)
from backend.app.application.use_cases.get_dashboard import (
    GetAnalyticsArtifactUseCase,
    GetDashboardUseCase,
)
from backend.app.application.use_cases.run_analytics import RunAnalyticsUseCase
from backend.app.application.use_cases.upload_dataset import UploadDatasetUseCase
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
from backend.app.infrastructure.persistence.in_memory_analysis_job_repository import (
    InMemoryAnalysisJobRepository,
)
from backend.app.infrastructure.storage.local_storage import LocalStorageRepositoryImpl
from backend.app.infrastructure.validation.validators import CSVValidationService

# Singleton instances for MVP
storage_repo = LocalStorageRepositoryImpl()
validation_service = CSVValidationService()
analysis_job_repo = InMemoryAnalysisJobRepository()

# Singleton ML Services
profiling_service = PandasProfilingService()
cleaning_service = PandasCleaningService()
feature_selection_service = PandasFeatureSelectionService()
scaling_service = PandasScalingService()
pca_service = ScikitLearnPCAService()
elbow_service = ElbowDetectionService()
clustering_service = MiniBatchKMeansClusteringService()
summary_service = PandasSummaryService()
category_summary_service = PandasCategorySummaryService()
dashboard_builder = RepositoryDashboardBuilder(storage_repo)


def get_upload_use_case() -> UploadDatasetUseCase:
    """Dependency provider for UploadDatasetUseCase."""
    return UploadDatasetUseCase(
        validation_service=validation_service,
        storage_repository=storage_repo,
        dataset_repository=storage_repo,
        metadata_repository=storage_repo,
    )


def get_run_analytics_use_case() -> RunAnalyticsUseCase:
    return RunAnalyticsUseCase(
        dataset_repo=storage_repo,
        storage_repo=storage_repo,
        metadata_repo=storage_repo,
        profiling_service=profiling_service,
        cleaning_service=cleaning_service,
        feature_selection_service=feature_selection_service,
        scaling_service=scaling_service,
        pca_service=pca_service,
        elbow_service=elbow_service,
        clustering_service=clustering_service,
        summary_service=summary_service,
        category_summary_service=category_summary_service,
        dashboard_builder=dashboard_builder,
    )


def get_dashboard_use_case() -> GetDashboardUseCase:
    return GetDashboardUseCase(dataset_repo=storage_repo, metadata_repo=storage_repo)


def get_analysis_job_repository() -> AnalysisJobRepository:
    return analysis_job_repo


def get_analysis_executor() -> AnalysisExecutor:
    return AnalysisExecutor(
        use_case=get_run_analytics_use_case(),
        status_repository=analysis_job_repo,
    )


def get_analytics_artifact_use_case() -> GetAnalyticsArtifactUseCase:
    return GetAnalyticsArtifactUseCase(
        dataset_repo=storage_repo, metadata_repo=storage_repo
    )


def get_request_id(request: Request) -> str:
    """Dependency to retrieve the request ID injected by middleware."""
    return getattr(request.state, "request_id", "unknown")


def get_processing_time(request: Request) -> float:
    """Dependency to retrieve processing time injected by middleware."""
    return getattr(request.state, "processing_time", 0.0)
