"""
Health check endpoints for the API.
"""

from fastapi import APIRouter, Response
from datetime import datetime
from typing import Dict, Any

from ...models.schemas import APIHealthResponse
from ...services.ml_service import ml_service
from ...core.config import app_settings

router = APIRouter()


@router.get(
    "/health",
    response_model=APIHealthResponse,
    summary="API Health Check",
    description="Check overall API health and model availability."
)
async def health_check() -> APIHealthResponse:
    """
    Comprehensive health check for the API and ML model.
    
    Returns:
        Detailed health status including API and model information
    """
    
    # Get model status
    model_status = ml_service.get_model_health_status()
    
    # Determine overall API status
    api_status = "healthy" if model_status.is_model_healthy else "degraded"
    
    return APIHealthResponse(
        status=api_status,
        timestamp=datetime.now().isoformat(),
        version=app_settings.api_version,
        model_status=model_status
    )


@router.get(
    "/ready",
    summary="Readiness Check",
    description="Check if the API is ready to serve requests.",
    responses={503: {"description": "Prediction model unavailable"}},
)
async def readiness_check(response: Response) -> Dict[str, Any]:
    """
    Readiness probe for container orchestration.
    
    Returns:
        Simple readiness status
    """
    
    is_ready = ml_service.is_model_loaded
    response.status_code = 200 if is_ready else 503
    
    return {
        "ready": is_ready,
        "timestamp": datetime.now().isoformat(),
        "service": "heart-disease-prediction-api"
    }


@router.get(
    "/live",
    summary="Liveness Check", 
    description="Check if the API is alive and responding."
)
async def liveness_check() -> Dict[str, str]:
    """
    Liveness probe for container orchestration.
    
    Returns:
        Simple liveness confirmation
    """
    
    return {
        "alive": "true",
        "timestamp": datetime.now().isoformat(),
        "service": "heart-disease-prediction-api"
    }
