"""
FastAPI application main module.
Heart Disease Prediction API with advanced ML capabilities.
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger

from .core.config import app_settings
from .core.logging import configure_logging
from .api.endpoints import prediction, health
from .services.ml_service import ml_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    
    # Startup
    logger.info("Starting Heart Disease Prediction API...")
    
    try:
        # Initialize ML service
        await ml_service.initialize_service()
        if ml_service.is_model_loaded:
            logger.info("ML service initialized successfully")
        else:
            logger.warning("API started with an unavailable model; predictions return 503")
        
    except Exception as error:
        logger.error(f"Failed to initialize ML service: {error}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Heart Disease Prediction API...")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Configure logging
    configure_logging()
    
    # Create FastAPI application
    app = FastAPI(
        title=app_settings.api_title,
        description=app_settings.api_description,
        version=app_settings.api_version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Add trusted host middleware for security
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure appropriately for production
    )
    
    # Include API routers
    app.include_router(
        health.router,
        tags=["Health Checks"],
        prefix="/api/v1"
    )
    
    app.include_router(
        prediction.router,
        tags=["Heart Disease Prediction"],
        prefix="/api/v1"
    )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global exception handler caught: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "timestamp": str(asyncio.get_event_loop().time())
            }
        )
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "Heart Disease Prediction API",
            "version": app_settings.api_version,
            "description": "Advanced ML-powered heart disease risk assessment",
            "docs_url": "/docs",
            "health_check": "/api/v1/health"
        }
    
    logger.info("FastAPI application created successfully")
    return app


# Create the application
app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=app_settings.api_host,
        port=app_settings.api_port,
        reload=True,
        log_level=app_settings.log_level.lower()
    )
