from typing import Any, List, cast

import pandas as pd

from backend.app.domain.interfaces.dataset_frame import DatasetFrame


class PandasDatasetFrame(DatasetFrame):
    """Pandas implementation of the DatasetFrame protocol."""

    def __init__(self, df: pd.DataFrame):
        self._df = df

    @property
    def row_count(self) -> int:
        return len(self._df)

    @property
    def column_count(self) -> int:
        return len(self._df.columns)

    @property
    def columns(self) -> List[str]:
        return cast(List[str], self._df.columns.tolist())

    def get_raw_object(self) -> Any:
        return self._df
