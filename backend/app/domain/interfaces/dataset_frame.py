from typing import Any, List, Protocol


class DatasetFrame(Protocol):
    """
    Protocol abstracting a DataFrame for the Domain layer.
    Ensures Clean Architecture by decoupling from Pandas.
    """

    @property
    def row_count(self) -> int: ...

    @property
    def column_count(self) -> int: ...

    @property
    def columns(self) -> List[str]: ...

    def get_raw_object(self) -> Any:
        """Returns the underlying framework-specific object (e.g., pd.DataFrame)"""
        ...
