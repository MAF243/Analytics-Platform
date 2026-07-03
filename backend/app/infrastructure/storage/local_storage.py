import json
import shutil
import typing
from datetime import datetime
from pathlib import Path
from typing import Any, BinaryIO, Dict, Optional

import numpy as np
import pandas as pd

from backend.app.core.config import settings
from backend.app.core.constants import (
    METADATA_DIR_NAME,
    METADATA_FILE_NAME,
    RAW_DIR_NAME,
    RAW_FILE_NAME,
    RESULTS_DIR_NAME,
)
from backend.app.core.exceptions import StorageException
from backend.app.domain.entities.dataset import Dataset
from backend.app.domain.interfaces.dataset_repository import DatasetRepository
from backend.app.domain.interfaces.metadata_repository import MetadataRepository
from backend.app.domain.interfaces.storage_repository import StorageRepository
from backend.app.domain.value_objects.dataset_id import DatasetId


class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for numpy data types"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        if pd.isna(obj):
            return None
        return super().default(obj)


class LocalStorageRepositoryImpl(
    StorageRepository, MetadataRepository, DatasetRepository
):
    """
    Implements local file system storage for datasets, metadata, and raw files.
    """

    def __init__(self) -> None:
        self.base_path = Path(settings.storage_base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_dataset_dir(self, dataset_id: DatasetId) -> Path:
        return self.base_path / str(dataset_id)

    # --- StorageRepository ---

    def prepare_storage_layout(self, dataset_id: DatasetId) -> None:
        dataset_dir = self._get_dataset_dir(dataset_id)
        try:
            (dataset_dir / RAW_DIR_NAME).mkdir(parents=True, exist_ok=True)
            (dataset_dir / METADATA_DIR_NAME).mkdir(parents=True, exist_ok=True)
            (dataset_dir / RESULTS_DIR_NAME).mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise StorageException(f"Failed to prepare storage layout: {str(e)}")

    def save_raw_dataset(self, dataset_id: DatasetId, file_stream: BinaryIO) -> None:
        raw_path = self._get_dataset_dir(dataset_id) / RAW_DIR_NAME / RAW_FILE_NAME
        try:
            with open(raw_path, "wb") as f:
                shutil.copyfileobj(file_stream, f)
        except Exception as e:
            raise StorageException(f"Failed to save raw dataset: {str(e)}")

    def get_raw_dataset(self, dataset_id: DatasetId) -> BinaryIO:
        raw_path = self._get_dataset_dir(dataset_id) / RAW_DIR_NAME / RAW_FILE_NAME
        if not raw_path.exists():
            raise StorageException("Raw dataset file not found.")
        return open(raw_path, "rb")

    def get_raw_dataset_path(self, dataset_id: DatasetId) -> str:
        raw_path = self._get_dataset_dir(dataset_id) / RAW_DIR_NAME / RAW_FILE_NAME
        if not raw_path.exists():
            raise StorageException("Raw dataset file not found.")
        return str(raw_path.absolute())

    def save_result_csv(
        self, dataset_id: DatasetId, name: str, stream: BinaryIO
    ) -> None:
        result_path = self._get_dataset_dir(dataset_id) / RESULTS_DIR_NAME / name
        try:
            with open(result_path, "wb") as f:
                shutil.copyfileobj(stream, f)
        except Exception as e:
            raise StorageException(f"Failed to save result CSV: {str(e)}")

    # --- MetadataRepository ---

    def save_metadata(self, dataset_id: DatasetId, metadata: Dict[str, Any]) -> None:
        meta_path = (
            self._get_dataset_dir(dataset_id) / METADATA_DIR_NAME / METADATA_FILE_NAME
        )
        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4, cls=NumpyEncoder)
        except Exception as e:
            raise StorageException(f"Failed to save metadata: {str(e)}")

    def get_metadata(self, dataset_id: DatasetId) -> Dict[str, Any]:
        meta_path = (
            self._get_dataset_dir(dataset_id) / METADATA_DIR_NAME / METADATA_FILE_NAME
        )
        if not meta_path.exists():
            return {}
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return typing.cast(Dict[str, Any], data)

    def save_artifact(
        self, dataset_id: DatasetId, name: str, data: Dict[str, Any]
    ) -> None:
        meta_path = self._get_dataset_dir(dataset_id) / METADATA_DIR_NAME / name
        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, cls=NumpyEncoder)
        except Exception as e:
            raise StorageException(f"Failed to save artifact {name}: {str(e)}")

    def get_artifact(self, dataset_id: DatasetId, name: str) -> Dict[str, Any]:
        meta_path = self._get_dataset_dir(dataset_id) / METADATA_DIR_NAME / name
        if not meta_path.exists():
            return {}
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return typing.cast(Dict[str, Any], data)

    # --- DatasetRepository ---

    def save(self, dataset: Dataset) -> None:
        """Saves dataset entity state to metadata json."""
        meta = self.get_metadata(dataset.id)
        meta.update(
            {
                "id": str(dataset.id),
                "filename": dataset.filename,
                "size_bytes": dataset.size_bytes,
                "created_at": dataset.created_at.isoformat(),
            }
        )
        self.save_metadata(dataset.id, meta)

    def get_by_id(self, dataset_id: DatasetId) -> Optional[Dataset]:
        meta = self.get_metadata(dataset_id)
        if not meta or "id" not in meta:
            return None
        return Dataset(
            id=DatasetId(meta["id"]),
            filename=meta["filename"],
            size_bytes=meta["size_bytes"],
            created_at=datetime.fromisoformat(meta["created_at"]),
        )
