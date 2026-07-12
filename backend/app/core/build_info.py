import json
import os
from pathlib import Path
from pydantic import BaseModel, computed_field


class BuildInfo(BaseModel):
    git_commit: str = "unknown"
    git_branch: str = "unknown"
    build_time: str = "unknown"
    github_run_id: str = "unknown"
    github_run_number: str = "unknown"
    github_repository: str = "unknown"
    docker_image: str = "unknown"
    application_version: str = "unknown"

    @computed_field
    @property
    def build_id(self) -> str:
        short_sha = (
            self.git_commit[:7]
            if self.git_commit and self.git_commit != "unknown" and self.git_commit != "dev"
            else self.git_commit
        )
        return f"{self.github_run_number}-{short_sha}"


_build_info_cache = None


def get_build_info() -> BuildInfo:
    """
    Loads build information with priority:
    1. Environment variables
    2. build_info.json
    3. Development defaults
    """
    global _build_info_cache
    if _build_info_cache is not None:
        return _build_info_cache

    # 3. Development defaults
    data = {
        "git_commit": "dev",
        "git_branch": "dev",
        "build_time": "dev",
        "github_run_id": "0",
        "github_run_number": "0",
        "github_repository": "local",
        "docker_image": "local",
        "application_version": "0.0.0",
    }

    # 2. build_info.json
    try:
        json_path = Path(__file__).parent.parent / "build_info.json"
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                data.update(json_data)
    except Exception:
        pass  # Silently fallback to defaults

    # 1. Environment variables
    env_mapping = {
        "BUILD_GIT_COMMIT": "git_commit",
        "BUILD_GIT_BRANCH": "git_branch",
        "BUILD_TIME": "build_time",
        "BUILD_RUN_ID": "github_run_id",
        "BUILD_RUN_NUMBER": "github_run_number",
        "BUILD_REPOSITORY": "github_repository",
        "BUILD_DOCKER_IMAGE": "docker_image",
        "APPLICATION_VERSION": "application_version",
    }
    for env_var, field_name in env_mapping.items():
        val = os.environ.get(env_var)
        if val:
            data[field_name] = val

    _build_info_cache = BuildInfo(**data)
    return _build_info_cache
