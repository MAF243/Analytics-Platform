import pandas as pd
from sklearn.cluster import MiniBatchKMeans

from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.ml_services import IClusteringService
from backend.app.domain.value_objects.pipeline_state import PipelineState


class MiniBatchKMeansClusteringService(IClusteringService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        if context.scaled_features is None or not context.optimal_k:
            raise ValueError("Scaled features or optimal K missing.")

        df: pd.DataFrame = context.scaled_features.get_raw_object()
        k = context.optimal_k
        seed = context.processing_metadata.get("random_seed", 42)

        kmeans = MiniBatchKMeans(
            n_clusters=k, random_state=seed, batch_size=256, n_init="auto"
        )
        labels = kmeans.fit_predict(df)

        context.cluster_labels = labels.tolist()

        # Save cluster centroids mapping (inverse scaled back to original scale would
        # be better, but for simplicity we keep scaled or just save the raw centroids)
        # Actually, business insights want raw feature averages, handled in Summary.
        context.centroids = {
            f"Cluster {i}": centroid.tolist()
            for i, centroid in enumerate(kmeans.cluster_centers_)
        }

        context.state = PipelineState.CLUSTERED
        return context
