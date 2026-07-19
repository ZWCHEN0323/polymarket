"""Application-wide constant definitions."""

from enum import StrEnum


class AppEnvironment(StrEnum):
    """Supported runtime environments."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class HealthStatus(StrEnum):
    """Health check status values."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class ComponentStatus(StrEnum):
    """Individual component check status values."""

    OK = "ok"
    ERROR = "error"
    NOT_CONFIGURED = "not_configured"


APP_NAME: str = "Polymarket Trading Bot"
APP_VERSION: str = "0.1.0"
DEFAULT_LOG_LEVEL: str = "INFO"
API_V1_PREFIX: str = "/api/v1"
HTTP_DEFAULT_TIMEOUT_SECONDS: float = 30.0
HTTP_MAX_RETRIES: int = 3
MASKED_SECRET_VISIBLE_CHARS: int = 4
