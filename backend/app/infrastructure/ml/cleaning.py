import pandas as pd

from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.ml_services import ICleaningService
from backend.app.domain.value_objects.pipeline_state import PipelineState
from backend.app.infrastructure.ml.dataset_frame import PandasDatasetFrame


class PandasCleaningService(ICleaningService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        df: pd.DataFrame = context.raw_dataset.get_raw_object().copy()

        initial_rows = len(df)
        initial_missing = df.isnull().sum().sum()

        # 1. Deduplicate
        df.drop_duplicates(inplace=True)
        duplicates_removed = initial_rows - len(df)

        # 2. Trim whitespace for string columns
        str_cols = df.select_dtypes(include=["object"]).columns
        for col in str_cols:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

        # 3. Handle Missing Values
        numeric_cols = df.select_dtypes(include=["number"]).columns
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns
        datetime_cols = df.select_dtypes(include=["datetime"]).columns

        for col in numeric_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())

        for col in categorical_cols:
            if df[col].isnull().any():
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val[0])
                else:
                    df[col] = df[col].fillna("Unknown")

        for col in datetime_cols:
            if df[col].isnull().any():
                df[col] = df[col].ffill().bfill()

        final_missing = df.isnull().sum().sum()
        missing_imputed = initial_missing - final_missing

        context.cleaned_dataset = PandasDatasetFrame(df)
        context.cleaning_report = {
            "duplicates_removed": int(duplicates_removed),
            "missing_values_imputed": int(missing_imputed),
        }

        context.processing_metadata["duplicate_rows_removed"] = int(duplicates_removed)
        context.processing_metadata["missing_values_imputed"] = int(missing_imputed)
        context.state = PipelineState.CLEANED
        return context
