"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.core.constants import APP_NAME, APP_VERSION
from app.core.logging import get_logger, setup_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize application resources on startup and clean up on shutdown."""
    settings = get_settings()
    setup_logging(settings.log_level)
    logger = get_logger(__name__)
    logger.info(
        "Application startup complete",
        extra={
            "environment": settings.environment.value,
            "debug": settings.debug,
        },
    )
    yield
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name or APP_NAME,
        version=settings.app_version or APP_VERSION,
        debug=settings.debug,
        lifespan=lifespan,
    )
    application.include_router(router)
    return application


app = create_app()
