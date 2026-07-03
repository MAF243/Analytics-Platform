from typing import Any, Dict, cast

from backend.app.core.exceptions import ApplicationException
from backend.app.core.serialization import JsonSerializer
from backend.app.domain.interfaces.dataset_repository import DatasetRepository
from backend.app.domain.interfaces.metadata_repository import MetadataRepository
from backend.app.domain.value_objects.dataset_id import DatasetId


class GetDashboardUseCase:
    def __init__(
        self, dataset_repo: DatasetRepository, metadata_repo: MetadataRepository
    ):
        self.dataset_repo = dataset_repo
        self.metadata_repo = metadata_repo

    def execute(self, dataset_id_str: str) -> Dict[str, Any]:
        dataset_id = DatasetId(dataset_id_str)
        dataset = self.dataset_repo.get_by_id(dataset_id)
        if not dataset:
            raise ApplicationException("Dataset not found.")

        dashboard_dto = self.metadata_repo.get_artifact(dataset_id, "dashboard.json")
        if not dashboard_dto:
            raise ApplicationException(
                "Dashboard data not ready yet. Please run analytics first."
            )

        return cast(Dict[str, Any], JsonSerializer.to_native(dashboard_dto))


class GetAnalyticsArtifactUseCase:
    def __init__(
        self, dataset_repo: DatasetRepository, metadata_repo: MetadataRepository
    ):
        self.dataset_repo = dataset_repo
        self.metadata_repo = metadata_repo

    def execute(self, dataset_id_str: str, artifact_name: str) -> Dict[str, Any]:
        dataset_id = DatasetId(dataset_id_str)
        dataset = self.dataset_repo.get_by_id(dataset_id)
        if not dataset:
            raise ApplicationException("Dataset not found.")

        artifact = self.metadata_repo.get_artifact(dataset_id, artifact_name)
        if not artifact:
            raise ApplicationException(f"Artifact {artifact_name} not found.")

        return cast(Dict[str, Any], JsonSerializer.to_native(artifact))
