import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.api.v1.routers import api_v1_router
from app.dependencies import get_logger
from app.infrastructure.config import get_settings
from app.infrastructure.database.connector import db_connector


def create_app() -> FastAPI:
    """Create the FastAPI application."""
    settings = get_settings()
    logger = get_logger()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        await init_db()
        yield

    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_v1_router, prefix="/api/v1")

    @app.get("/welcome")
    async def welcome(logger: Annotated[logging.Logger, Depends(get_logger)]):
        logger.debug("Welcome endpoint accessed")
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "log_level": settings.LOG_LEVEL,
            "environment": settings.ENVIRONMENT,
            "database": settings.DATABASE,
            "status": "OK",
        }

    @app.get("/ping")
    async def ping(logger: Annotated[logging.Logger, Depends(get_logger)]):
        logger.debug("Ping endpoint accessed")
        return {"message": "pong"}

    logger.debug("Application initialized")
    return app


async def init_db():
    """Initialize database tables and schema."""
    await db_connector.create_database()
