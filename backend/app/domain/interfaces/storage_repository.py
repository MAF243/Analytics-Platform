from abc import ABC, abstractmethod
from typing import BinaryIO

from backend.app.domain.value_objects.dataset_id import DatasetId


class StorageRepository(ABC):
    """Abstract interface for raw dataset file storage."""

    @abstractmethod
    def save_raw_dataset(self, dataset_id: DatasetId, file_stream: BinaryIO) -> None:
        """Saves a binary stream to the raw storage."""
        pass

    @abstractmethod
    def get_raw_dataset(self, dataset_id: DatasetId) -> BinaryIO:
        """Retrieves the raw binary stream of the dataset."""
        pass

    @abstractmethod
    def prepare_storage_layout(self, dataset_id: DatasetId) -> None:
        """Prepares the directory structures (raw, metadata, results)."""
        pass

    @abstractmethod
    def save_result_csv(
        self, dataset_id: DatasetId, name: str, stream: BinaryIO
    ) -> None:
        """Saves a processed CSV to the results directory."""
        pass

    @abstractmethod
    def get_raw_dataset_path(self, dataset_id: DatasetId) -> str:
        """Gets the absolute file path for the raw dataset."""
        pass
