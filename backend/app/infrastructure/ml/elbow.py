import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import MiniBatchKMeans

from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.ml_services import (
    IElbowDetectionService,
    IElbowStrategy,
)
from backend.app.domain.value_objects.pipeline_state import PipelineState


class KneeLocatorStrategy(IElbowStrategy):
    def detect(self, context: AnalyticsContext) -> AnalyticsContext:
        if not context.scaled_features:
            raise ValueError()
        df: pd.DataFrame = context.scaled_features.get_raw_object()

        inertias = []
        k_range = range(2, min(15, len(df)))

        seed = context.processing_metadata.get("random_seed", 42)
        for k in k_range:
            kmeans = MiniBatchKMeans(
                n_clusters=k, random_state=seed, batch_size=256, n_init="auto"
            )
            kmeans.fit(df)
            inertias.append(kmeans.inertia_)

        kl = KneeLocator(
            list(k_range), inertias, curve="convex", direction="decreasing"
        )
        optimal_k = kl.elbow

        if optimal_k is None:
            # Fallback heuristic: choose k where inertia drops significantly
            diffs = [inertias[i] - inertias[i + 1] for i in range(len(inertias) - 1)]
            optimal_k = k_range[diffs.index(max(diffs)) + 1] if diffs else 2

        context.optimal_k = optimal_k
        context.processing_metadata["optimal_k"] = int(optimal_k)
        # We store elbow coordinates for the frontend plot
        context.processing_metadata["elbow_curve"] = {
            "k": list(k_range),
            "inertia": inertias,
        }
        return context


class ElbowDetectionService(IElbowDetectionService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        if context.scaled_features is None:
            raise ValueError("Scaled features missing.")

        strategy = KneeLocatorStrategy()
        context = strategy.detect(context)

        context.state = PipelineState.ELBOW_COMPLETED
        return context
