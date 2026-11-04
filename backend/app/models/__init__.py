"""Data models and schemas."""

from .schemas import (
    PatientHealthData,
    HeartDiseaseRiskPrediction,
    ModelHealthStatus,
    PredictionRequest,
)


def __getattr__(name):
    if name == "EnhancedHeartDiseasePredictor":
        from .heart_disease_predictor import EnhancedHeartDiseasePredictor

        return EnhancedHeartDiseasePredictor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "PatientHealthData",
    "HeartDiseaseRiskPrediction",
    "ModelHealthStatus",
    "PredictionRequest",
    "EnhancedHeartDiseasePredictor",
]
