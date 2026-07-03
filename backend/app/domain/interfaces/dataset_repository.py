from abc import ABC, abstractmethod
from typing import Optional

from backend.app.domain.entities.dataset import Dataset
from backend.app.domain.value_objects.dataset_id import DatasetId


class DatasetRepository(ABC):
    """Abstract interface for managing Dataset domain entities."""

    @abstractmethod
    def save(self, dataset: Dataset) -> None:
        """Saves a dataset entity."""
        pass

    @abstractmethod
    def get_by_id(self, dataset_id: DatasetId) -> Optional[Dataset]:
        """Retrieves a dataset entity by its ID."""
        pass
