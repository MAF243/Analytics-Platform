import pandas as pd

from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.ml_services import IFeatureSelectionService
from backend.app.domain.value_objects.pipeline_state import PipelineState


class PandasFeatureSelectionService(IFeatureSelectionService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        if context.cleaned_dataset is None:
            raise ValueError("Cleaned dataset is missing.")

        df: pd.DataFrame = context.cleaned_dataset.get_raw_object()

        # Only consider numeric columns
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

        selected = []
        for col in numeric_cols:
            # Ignore ID-like columns (high cardinality heuristic or name heuristic)
            if "id" in str(col).lower() and df[col].nunique() == len(df):
                continue

            # Ignore constant columns (zero variance)
            if df[col].nunique() <= 1:
                continue

            selected.append(col)

        if not selected:
            raise ValueError("No valid numeric features found for clustering.")

        context.selected_features = selected
        context.state = PipelineState.FEATURE_SELECTED
        return context
