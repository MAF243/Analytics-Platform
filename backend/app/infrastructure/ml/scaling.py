import pandas as pd
from sklearn.preprocessing import RobustScaler, StandardScaler

from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.ml_services import IScalingService, IScalingStrategy
from backend.app.domain.value_objects.pipeline_state import PipelineState
from backend.app.infrastructure.ml.dataset_frame import PandasDatasetFrame


class StandardScalerStrategy(IScalingStrategy):
    def scale(self, context: AnalyticsContext) -> AnalyticsContext:
        if not context.cleaned_dataset:
            raise ValueError()
        df: pd.DataFrame = context.cleaned_dataset.get_raw_object()
        features = df[context.selected_features]

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(features)

        scaled_df = pd.DataFrame(
            scaled_data, columns=context.selected_features, index=df.index
        )
        context.scaled_features = PandasDatasetFrame(scaled_df)
        context.processing_metadata["scaler"] = "StandardScaler"
        return context


class RobustScalerStrategy(IScalingStrategy):
    def scale(self, context: AnalyticsContext) -> AnalyticsContext:
        if not context.cleaned_dataset:
            raise ValueError()
        df: pd.DataFrame = context.cleaned_dataset.get_raw_object()
        features = df[context.selected_features]

        scaler = RobustScaler()
        scaled_data = scaler.fit_transform(features)

        scaled_df = pd.DataFrame(
            scaled_data, columns=context.selected_features, index=df.index
        )
        context.scaled_features = PandasDatasetFrame(scaled_df)
        context.processing_metadata["scaler"] = "RobustScaler"
        return context


class PandasScalingService(IScalingService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        if not context.selected_features or context.cleaned_dataset is None:
            raise ValueError("No features selected for scaling.")

        df: pd.DataFrame = context.cleaned_dataset.get_raw_object()
        features = df[context.selected_features]

        # Simple Outlier Detection using IQR heuristic to choose scaler
        Q1 = features.quantile(0.25)
        Q3 = features.quantile(0.75)
        IQR = Q3 - Q1
        outlier_condition = (
            ((features < (Q1 - 1.5 * IQR)) | (features > (Q3 + 1.5 * IQR))).sum().sum()
        )

        # If outliers are more than 5% of data points, use RobustScaler
        total_data_points = features.shape[0] * features.shape[1]

        strategy: IScalingStrategy
        if outlier_condition > (0.05 * total_data_points):
            strategy = RobustScalerStrategy()
        else:
            strategy = StandardScalerStrategy()

        context = strategy.scale(context)
        context.state = PipelineState.SCALED
        return context
