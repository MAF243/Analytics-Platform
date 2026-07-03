from abc import ABC, abstractmethod
from typing import Any, Dict

from backend.app.domain.value_objects.dataset_id import DatasetId


class MetadataRepository(ABC):
    """Abstract interface for dataset metadata storage."""

    @abstractmethod
    def save_metadata(self, dataset_id: DatasetId, metadata: Dict[str, Any]) -> None:
        """Saves metadata associated with the dataset."""
        pass

    @abstractmethod
    def get_metadata(self, dataset_id: DatasetId) -> Dict[str, Any]:
        """Retrieves metadata associated with the dataset."""
        pass

    @abstractmethod
    def save_artifact(
        self, dataset_id: DatasetId, name: str, data: Dict[str, Any]
    ) -> None:
        """Saves a JSON artifact to the metadata directory."""
        pass

    @abstractmethod
    def get_artifact(self, dataset_id: DatasetId, name: str) -> Dict[str, Any]:
        """Retrieves a JSON artifact from the metadata directory."""
        pass
