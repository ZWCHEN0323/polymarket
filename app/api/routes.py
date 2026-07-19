"""FastAPI HTTP route handlers."""

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.core.constants import (
    APP_NAME,
    APP_VERSION,
    ComponentStatus,
    HealthStatus,
)

router = APIRouter()


def _build_database_check(settings: Settings) -> dict[str, str]:
    """Build database health check payload based on current configuration."""
    if not settings.is_database_configured:
        return {
            "status": ComponentStatus.NOT_CONFIGURED.value,
            "message": "Database credentials are not configured",
        }
    return {
        "status": ComponentStatus.NOT_CONFIGURED.value,
        "message": "Database connectivity check will be enabled in Milestone 4",
    }


@router.get("/")
async def root(settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    """Return basic system information."""
    return {
        "name": settings.app_name or APP_NAME,
        "version": settings.app_version or APP_VERSION,
        "environment": settings.environment.value,
        "status": "running",
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    """Return system and component health status."""
    database_check = _build_database_check(settings)
    api_status = ComponentStatus.OK.value

    overall_status = HealthStatus.HEALTHY.value
    if database_check["status"] == ComponentStatus.ERROR.value:
        overall_status = HealthStatus.UNHEALTHY.value
    elif database_check["status"] == ComponentStatus.NOT_CONFIGURED.value:
        overall_status = HealthStatus.DEGRADED.value

    return {
        "status": overall_status,
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "checks": {
            "api": {
                "status": api_status,
                "message": "FastAPI application is responsive",
            },
            "database": database_check,
        },
    }
