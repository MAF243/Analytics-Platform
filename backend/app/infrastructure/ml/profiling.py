import pandas as pd

from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.ml_services import IProfilingService
from backend.app.domain.value_objects.pipeline_state import PipelineState


class PandasProfilingService(IProfilingService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        df: pd.DataFrame = context.raw_dataset.get_raw_object()

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        datetime_cols = df.select_dtypes(include=["datetime"]).columns.tolist()

        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100

        profiling = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "datetime_columns": datetime_cols,
            "missing_values": missing.to_dict(),
            "missing_percentage": missing_pct.to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_bytes": int(df.memory_usage(deep=True).sum()),
        }

        # Safe descriptive stats for numeric only
        if numeric_cols:
            profiling["descriptive_statistics"] = df[numeric_cols].describe().to_dict()
        else:
            profiling["descriptive_statistics"] = {}

        context.profiling_result = profiling
        context.processing_metadata["total_rows"] = len(df)
        context.processing_metadata["total_columns"] = len(df.columns)
        context.processing_metadata["numeric_columns"] = len(numeric_cols)
        context.processing_metadata["categorical_columns"] = len(categorical_cols)

        context.state = PipelineState.PROFILED
        return context
