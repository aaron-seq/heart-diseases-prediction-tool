"""
Pydantic schemas for request/response models.
"""

from typing import List
from pydantic import BaseModel, Field, validator
from enum import Enum


class ChestPainType(str, Enum):
    """Chest pain type enumeration."""
    TYPICAL_ANGINA = "typical_angina"
    ATYPICAL_ANGINA = "atypical_angina" 
    NON_ANGINAL_PAIN = "non_anginal_pain"
    ASYMPTOMATIC = "asymptomatic"


class RestingECGType(str, Enum):
    """Resting ECG type enumeration."""
    NORMAL = "normal"
    ST_T_ABNORMALITY = "st_t_abnormality" 
    LEFT_VENTRICULAR_HYPERTROPHY = "left_ventricular_hypertrophy"


class SlopeType(str, Enum):
    """ST slope type enumeration."""
    UPSLOPING = "upsloping"
    FLAT = "flat"
    DOWNSLOPING = "downsloping"


class ThalassemiaType(str, Enum):
    """Thalassemia type enumeration."""
    NORMAL = "normal"
    FIXED_DEFECT = "fixed_defect"
    REVERSIBLE_DEFECT = "reversible_defect"


class PatientHealthData(BaseModel):
    """Patient health data for heart disease prediction."""
    
    # Demographic Information
    age: int = Field(..., ge=1, le=120, description="Patient age in years")
    is_male: bool = Field(..., description="True if patient is male, False if female")
    
    # Chest Pain Information
    chest_pain_type: ChestPainType = Field(..., description="Type of chest pain experienced")
    
    # Vital Signs
    resting_blood_pressure: int = Field(..., ge=80, le=250, description="Resting blood pressure in mmHg")
    serum_cholesterol: int = Field(..., ge=100, le=600, description="Serum cholesterol in mg/dl")
    maximum_heart_rate_achieved: int = Field(..., ge=60, le=220, description="Maximum heart rate achieved during exercise")
    
    # Medical Test Results
    fasting_blood_sugar_over_120: bool = Field(..., description="True if fasting blood sugar > 120 mg/dl")
    resting_ecg_results: RestingECGType = Field(..., description="Resting electrocardiographic results")
    exercise_induced_angina: bool = Field(..., description="True if exercise induced angina")
    st_depression_exercise: float = Field(..., ge=0, le=10, description="ST depression induced by exercise relative to rest")
    st_slope_peak_exercise: SlopeType = Field(..., description="Slope of peak exercise ST segment")
    major_vessels_colored: int = Field(..., ge=0, le=4, description="Number of major vessels colored by fluoroscopy")
    thalassemia_type: ThalassemiaType = Field(..., description="Thalassemia test result")
    
    @validator('age')
    def validate_age_range(cls, age_value):
        """Validate age is in reasonable range."""
        if not 18 <= age_value <= 100:
            raise ValueError("Age should be between 18 and 100 years")
        return age_value
    
    @validator('resting_blood_pressure')
    def validate_blood_pressure(cls, bp_value):
        """Validate blood pressure is in reasonable range."""
        if not 90 <= bp_value <= 200:
            raise ValueError("Resting blood pressure should be between 90 and 200 mmHg")
        return bp_value


class HeartDiseaseRiskPrediction(BaseModel):
    """Heart disease risk prediction response."""
    
    has_heart_disease_risk: bool = Field(..., description="Predicted heart disease risk (True if at risk)")
    risk_probability: float = Field(..., ge=0, le=1, description="Probability of heart disease (0-1)")
    risk_level: str = Field(..., description="Risk level categorization")
    confidence_score: float = Field(..., ge=0, le=1, description="Model confidence in prediction")
    
    # Risk Factors Analysis
    primary_risk_factors: List[str] = Field(default=[], description="Primary contributing risk factors")
    protective_factors: List[str] = Field(default=[], description="Factors reducing risk")
    
    # Recommendations
    lifestyle_recommendations: List[str] = Field(default=[], description="Lifestyle improvement suggestions")
    medical_recommendations: List[str] = Field(default=[], description="Medical consultation recommendations")


class PredictionRequest(BaseModel):
    """Request model for heart disease prediction."""
    
    patient_data: PatientHealthData
    explain_prediction: bool = Field(default=True, description="Include SHAP explanations")


class ModelHealthStatus(BaseModel):
    """Model health and performance metrics."""
    
    is_model_healthy: bool = Field(..., description="Overall model health status")
    model_version: str = Field(..., description="Current model version")
    last_training_date: str = Field(..., description="Last model training date")
    model_accuracy: float = Field(
        ..., strict=True, ge=0, le=1, allow_inf_nan=False,
        description="Model accuracy fraction on test set (0-1)",
    )
    total_predictions_made: int = Field(..., description="Total predictions made")
    average_response_time_ms: float = Field(..., description="Average response time in milliseconds")


class APIHealthResponse(BaseModel):
    """API health check response."""
    
    status: str = Field(..., description="API status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    model_status: ModelHealthStatus
