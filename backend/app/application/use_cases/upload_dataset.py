import uuid
from typing import BinaryIO

from loguru import logger

from backend.app.application.dtos.upload_response import UploadResponse
from backend.app.domain.entities.dataset import Dataset
from backend.app.domain.interfaces.dataset_repository import DatasetRepository
from backend.app.domain.interfaces.metadata_repository import MetadataRepository
from backend.app.domain.interfaces.storage_repository import StorageRepository
from backend.app.domain.interfaces.validation_service import ValidationService
from backend.app.domain.value_objects.dataset_id import DatasetId


class UploadDatasetUseCase:
    """Use case for handling file uploads."""

    def __init__(
        self,
        validation_service: ValidationService,
        storage_repository: StorageRepository,
        dataset_repository: DatasetRepository,
        metadata_repository: MetadataRepository,
    ):
        self.validation_service = validation_service
        self.storage_repository = storage_repository
        self.dataset_repository = dataset_repository
        self.metadata_repository = metadata_repository

    def execute(
        self, file_stream: BinaryIO, filename: str, content_type: str, size_bytes: int
    ) -> UploadResponse:
        logger.info(f"Executing UploadDatasetUseCase for file: {filename}")

        # 1. Validation
        self.validation_service.validate_upload(file_stream, filename, content_type)
        file_stream.seek(0)  # Reset stream pointer after validation

        # 2. Domain Entity Creation
        dataset_id = DatasetId(str(uuid.uuid4()))
        dataset = Dataset(id=dataset_id, filename=filename, size_bytes=size_bytes)

        # 3. Storage
        self.storage_repository.prepare_storage_layout(dataset_id)
        self.storage_repository.save_raw_dataset(dataset_id, file_stream)

        # 4. Save Metadata
        self.metadata_repository.save_metadata(
            dataset_id,
            {
                "original_filename": filename,
                "size_bytes": size_bytes,
                "content_type": content_type,
                "created_at": dataset.created_at.isoformat(),
            },
        )

        # 5. Save Entity
        self.dataset_repository.save(dataset)

        logger.info(f"Dataset successfully uploaded and stored with ID: {dataset_id}")

        return UploadResponse(
            dataset_id=str(dataset.id),
            filename=dataset.filename,
            size_bytes=dataset.size_bytes,
            created_at=dataset.created_at,
        )
