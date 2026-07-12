from typing import Any, Dict

from fastapi import APIRouter

from backend.app.core.build_info import get_build_info

router = APIRouter(tags=["Version"])

@router.get("/version")
async def get_version() -> Dict[str, Any]:
    """Returns deployment and build metadata."""
    build_info = get_build_info()
    return build_info.model_dump()
