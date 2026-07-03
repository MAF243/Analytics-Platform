from decimal import Decimal
from pathlib import Path
from uuid import UUID

import numpy as np
import pandas as pd

from backend.app.core.serialization import JsonSerializer


def test_json_serializer_native_types() -> None:
    obj = {
        "int": np.int64(42),
        "float": np.float64(3.1415),
        "nan": pd.NA,
        "np_nan": np.nan,
        "pd_timestamp": pd.Timestamp("2024-01-01T12:00:00Z"),
        "list": [np.int64(1), np.float64(2.0)],
        "array": np.array([1, 2, 3]),
        "decimal": Decimal("10.5"),
        "uuid": UUID("123e4567-e89b-12d3-a456-426614174000"),
        "path": Path("/data/file.csv"),
    }

    cleaned = JsonSerializer.to_native(obj)

    assert isinstance(cleaned["int"], int)
    assert cleaned["int"] == 42
    assert isinstance(cleaned["float"], float)
    assert cleaned["nan"] is None
    assert cleaned["np_nan"] is None
    assert isinstance(cleaned["pd_timestamp"], str)
    assert isinstance(cleaned["list"][0], int)
    assert isinstance(cleaned["list"][1], float)
    assert isinstance(cleaned["array"], list)
    assert cleaned["array"] == [1, 2, 3]
    assert isinstance(cleaned["decimal"], str)
    assert cleaned["decimal"] == "10.5"
    assert isinstance(cleaned["uuid"], str)
    assert isinstance(cleaned["path"], str)
