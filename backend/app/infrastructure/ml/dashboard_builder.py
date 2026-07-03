from backend.app.domain.entities.analysis_result import AnalyticsContext
from backend.app.domain.interfaces.metadata_repository import MetadataRepository
from backend.app.domain.interfaces.ml_services import IDashboardBuilder
from backend.app.domain.value_objects.pipeline_state import PipelineState


class RepositoryDashboardBuilder(IDashboardBuilder):
    def __init__(self, metadata_repo: MetadataRepository):
        self.metadata_repo = metadata_repo

    def build(self, context: AnalyticsContext) -> AnalyticsContext:
        pca_points = []
        if context.pca_result and "coordinates" in context.pca_result:
            coords = context.pca_result["coordinates"]
            clusters = (
                context.cluster_labels
                if context.cluster_labels
                else ["Unknown"] * len(coords)
            )

            for i, coord in enumerate(coords):
                cluster_label = clusters[i] if i < len(clusters) else "Unknown"
                if len(coord) >= 2:
                    pca_points.append(
                        {"x": coord[0], "y": coord[1], "cluster": cluster_label}
                    )

        # Replace simple coordinates with mapped points
        pca_output = dict(context.pca_result) if context.pca_result else {}
        pca_output["pca_points"] = pca_points
        if "coordinates" in pca_output:
            del pca_output["coordinates"]

        dashboard = {
            "dataset_id": str(context.dataset_id),
            "profiling": context.profiling_result,
            "cleaning": context.cleaning_report,
            "features_selected": context.selected_features,
            "pca": pca_output,
            "elbow": context.processing_metadata.get("elbow_curve", {}),
            "summary": context.summary,
            "category_summary": context.category_summary,
            "processing_metadata": context.processing_metadata,
        }

        context.dashboard_dto = dashboard
        context.state = PipelineState.DASHBOARD_READY

        # Save final dashboard artifact
        self.metadata_repo.save_artifact(
            context.dataset_id, "dashboard.json", dashboard
        )
        context.manifest.append("dashboard.json")

        # Save manifest
        self.metadata_repo.save_artifact(
            context.dataset_id, "manifest.json", {"artifacts": context.manifest}
        )

        return context
