from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.config.database import engine
from src.config.settings import get_settings
from src.core.log_handlers import setup_logging
from src.core.middleware import LoggingMiddleware
from src.infrastructure.database.models import Base


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    settings = get_settings()
    logger = setup_logging()
    app = FastAPI(
        title="Image Processing API",
        description="API for processing and retrieving image frames",
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)
    app.include_router(router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup():
        # Create database tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown():
        # Properly close the engine on shutdown
        await engine.dispose()
        # Loop through all handlers and close them
        for handler in logger.handlers:
            logger.removeHandler(handler)
            handler.close()

    return app


app = create_app()
