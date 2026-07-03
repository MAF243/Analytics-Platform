from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.ml_services import (
    ICategorySummaryService,
    ISummaryService,
)
from backend.app.domain.value_objects.pipeline_state import PipelineState


class PandasSummaryService(ISummaryService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        if context.cleaned_dataset is None or not context.cluster_labels:
            raise ValueError("Cleaned dataset or cluster labels missing.")

        df = context.cleaned_dataset.get_raw_object().copy()
        df["Cluster"] = context.cluster_labels

        cluster_sizes = df["Cluster"].value_counts().to_dict()
        cluster_percentages = (
            df["Cluster"].value_counts(normalize=True) * 100
        ).to_dict()

        # Numeric averages per cluster
        numeric_cols = (
            df.select_dtypes(include=["number"])
            .columns.drop("Cluster", errors="ignore")
            .tolist()
        )

        cluster_stats = {}
        for cluster_id in sorted(df["Cluster"].unique()):
            cluster_df = df[df["Cluster"] == cluster_id]
            stats = {
                "size": int(cluster_sizes[cluster_id]),
                "percentage": float(cluster_percentages[cluster_id]),
            }
            if numeric_cols:
                stats["averages"] = cluster_df[numeric_cols].mean().to_dict()
                stats["medians"] = cluster_df[numeric_cols].median().to_dict()
            cluster_stats[f"Cluster {cluster_id}"] = stats

        largest = max(cluster_sizes, key=cluster_sizes.get)
        smallest = min(cluster_sizes, key=cluster_sizes.get)

        context.summary = {
            "overall": {
                "total_clusters": context.optimal_k,
                "largest_cluster": f"Cluster {largest}",
                "smallest_cluster": f"Cluster {smallest}",
            },
            "clusters": cluster_stats,
        }

        context.state = PipelineState.SUMMARY_GENERATED
        return context


class PandasCategorySummaryService(ICategorySummaryService):
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        if context.cleaned_dataset is None:
            raise ValueError("Cleaned dataset missing.")

        df = context.cleaned_dataset.get_raw_object()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns

        cat_summary = {}
        for col in cat_cols:
            if df[col].nunique() <= 20:
                cat_summary[col] = df[col].value_counts().to_dict()

        context.category_summary = cat_summary
        return context
