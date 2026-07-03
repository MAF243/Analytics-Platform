import pandas as pd
from sklearn.decomposition import PCA

from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.ml_services import IPCAService
from backend.app.domain.value_objects.pipeline_state import PipelineState


class ScikitLearnPCAService(IPCAService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        if context.scaled_features is None:
            raise ValueError("Scaled features missing.")

        df: pd.DataFrame = context.scaled_features.get_raw_object()

        if len(df.columns) < 2:
            # Cannot do 2D PCA if there is only 1 feature
            context.pca_result = {
                "components": 0,
                "explained_variance_ratio": [],
                "coordinates": [],
            }
            context.state = PipelineState.PCA_COMPLETED
            return context

        pca = PCA(
            n_components=2,
            random_state=context.processing_metadata.get("random_seed", 42),
        )
        pca_coords = pca.fit_transform(df)

        context.pca_result = {
            "components": 2,
            "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
            "coordinates": pca_coords.tolist(),
        }

        context.state = PipelineState.PCA_COMPLETED
        return context
