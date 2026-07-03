import io
import shutil
from pathlib import Path
from typing import Generator

import pytest

from backend.app.core.config import settings
from backend.app.domain.entities.dataset import Dataset
from backend.app.domain.value_objects.dataset_id import DatasetId
from backend.app.infrastructure.storage.local_storage import LocalStorageRepositoryImpl


@pytest.fixture
def storage_repo(tmp_path: Path) -> Generator[LocalStorageRepositoryImpl, None, None]:
    original_path = settings.storage_base_path
    settings.storage_base_path = str(tmp_path / "data")
    repo = LocalStorageRepositoryImpl()
    yield repo
    settings.storage_base_path = original_path
    shutil.rmtree(settings.storage_base_path, ignore_errors=True)


def test_storage_lifecycle(storage_repo: LocalStorageRepositoryImpl) -> None:
    ds_id = DatasetId("123e4567-e89b-12d3-a456-426614174000")

    # Prepare layout
    storage_repo.prepare_storage_layout(ds_id)

    # Save raw
    content = b"test content"
    storage_repo.save_raw_dataset(ds_id, io.BytesIO(content))

    # Get raw
    stream = storage_repo.get_raw_dataset(ds_id)
    assert stream.read() == content
    stream.close()

    # Save/Get Entity
    ds = Dataset(id=ds_id, filename="test.csv", size_bytes=12)
    storage_repo.save(ds)

    loaded_ds = storage_repo.get_by_id(ds_id)
    assert loaded_ds is not None
    assert loaded_ds.id.value == ds.id.value
    assert loaded_ds.filename == "test.csv"
    assert loaded_ds.size_bytes == 12
