"""
Machine Learning service for heart disease prediction.
Handles model operations and prediction logic.
"""

from typing import Dict, Any, List, Optional, TYPE_CHECKING
import asyncio
from datetime import datetime
from loguru import logger

from ..models.schemas import PatientHealthData, HeartDiseaseRiskPrediction, ModelHealthStatus

if TYPE_CHECKING:
    from ..models.heart_disease_predictor import EnhancedHeartDiseasePredictor


class HeartDiseaseMLService:
    """Service class for heart disease ML operations."""
    
    def __init__(self, predictor: Optional["EnhancedHeartDiseasePredictor"] = None):
        """Initialize the ML service."""
        self.predictor = predictor
        self.total_predictions = 0
        self.average_response_time = 0.0
        self.is_model_loaded = False
        
        logger.info("Heart Disease ML Service initialized")
    
    async def initialize_service(self) -> None:
        """Load operator-supplied artifacts; remain unavailable if loading fails."""
        self.is_model_loaded = False
        try:
            logger.info("Loading heart disease prediction model...")
            if self.predictor is None:
                self.predictor = self._create_predictor()
            self.predictor.load_model()
            self._build_model_health_status(self.predictor.model_metadata, True)
        except Exception as error:
            # Model availability must not prevent liveness/diagnostics or start training.
            logger.warning(
                "Model unavailable ({}). Check ML dependencies and MODEL_PATH; "
                "predictions remain disabled. Startup does not train a model.",
                type(error).__name__,
            )
            return
        self.is_model_loaded = True
        logger.info("Pre-trained model loaded successfully")

    @staticmethod
    def _create_predictor():
        # Schema and health imports must work without the optional ML stack.
        from ..models.heart_disease_predictor import EnhancedHeartDiseasePredictor

        return EnhancedHeartDiseasePredictor()
    
    async def _train_new_model(self) -> None:
        """Train a new model asynchronously."""

        if self.predictor is None:
            self.predictor = self._create_predictor()
        
        # Run training in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        def train_model():
            return self.predictor.train_model()
        
        training_result = await loop.run_in_executor(None, train_model)
        self.is_model_loaded = True
        
        logger.info("New model trained successfully")
        return training_result
    
    async def predict_heart_disease(
        self, 
        patient_data: PatientHealthData
    ) -> HeartDiseaseRiskPrediction:
        """
        Predict heart disease risk for a patient.
        
        Args:
            patient_data: Patient health information
            
        Returns:
            Heart disease risk prediction
        """
        
        if not self.is_model_loaded:
            raise ValueError("ML model not loaded. Service not properly initialized.")
        
        start_time = datetime.now()
        
        try:
            # Convert Pydantic model to dictionary for processing
            patient_dict = self._convert_patient_data_to_dict(patient_data)
            
            # Make prediction
            prediction_result = self.predictor.predict_heart_disease_risk(patient_dict)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(patient_data, prediction_result)
            
            # Create response
            response = HeartDiseaseRiskPrediction(
                has_heart_disease_risk=prediction_result['has_heart_disease_risk'],
                risk_probability=prediction_result['risk_probability'],
                risk_level=prediction_result['risk_level'],
                confidence_score=prediction_result['confidence_score'],
                primary_risk_factors=prediction_result.get('primary_risk_factors', []),
                protective_factors=prediction_result.get('protective_factors', []),
                lifestyle_recommendations=recommendations['lifestyle'],
                medical_recommendations=recommendations['medical']
            )
            
            # Update service metrics
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            self._update_metrics(response_time)
            
            logger.info(f"Prediction completed in {response_time:.2f}ms")
            
            return response
            
        except Exception as error:
            logger.error(f"Prediction failed: {error}")
            raise
    
    def _convert_patient_data_to_dict(self, patient_data: PatientHealthData) -> Dict[str, Any]:
        """Convert Pydantic model to dictionary format expected by the predictor."""
        
        # Map Pydantic field names to original dataset column names
        field_mapping = {
            'age': patient_data.age,
            'sex': 1 if patient_data.is_male else 0,
            'cp': self._map_chest_pain_type(patient_data.chest_pain_type),
            'trestbps': patient_data.resting_blood_pressure,
            'chol': patient_data.serum_cholesterol,
            'fbs': 1 if patient_data.fasting_blood_sugar_over_120 else 0,
            'restecg': self._map_resting_ecg_type(patient_data.resting_ecg_results),
            'thalach': patient_data.maximum_heart_rate_achieved,
            'exang': 1 if patient_data.exercise_induced_angina else 0,
            'oldpeak': patient_data.st_depression_exercise,
            'slope': self._map_slope_type(patient_data.st_slope_peak_exercise),
            'ca': patient_data.major_vessels_colored,
            'thal': self._map_thalassemia_type(patient_data.thalassemia_type)
        }
        
        return field_mapping
    
    def _map_chest_pain_type(self, chest_pain_type: str) -> int:
        """Map chest pain type to numeric value."""
        mapping = {
            'typical_angina': 1,
            'atypical_angina': 2,
            'non_anginal_pain': 3,
            'asymptomatic': 4
        }
        return mapping.get(chest_pain_type, 1)
    
    def _map_resting_ecg_type(self, ecg_type: str) -> int:
        """Map resting ECG type to numeric value."""
        mapping = {
            'normal': 0,
            'st_t_abnormality': 1,
            'left_ventricular_hypertrophy': 2
        }
        return mapping.get(ecg_type, 0)
    
    def _map_slope_type(self, slope_type: str) -> int:
        """Map ST slope type to numeric value."""
        mapping = {
            'upsloping': 1,
            'flat': 2,
            'downsloping': 3
        }
        return mapping.get(slope_type, 1)
    
    def _map_thalassemia_type(self, thal_type: str) -> int:
        """Map thalassemia type to numeric value."""
        mapping = {
            'normal': 3,
            'fixed_defect': 6,
            'reversible_defect': 7
        }
        return mapping.get(thal_type, 3)
    
    def _generate_recommendations(
        self, 
        patient_data: PatientHealthData, 
        prediction_result: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate personalized recommendations based on patient data and prediction."""
        
        lifestyle_recommendations = []
        medical_recommendations = []
        
        risk_probability = prediction_result['risk_probability']
        
        # General recommendations based on risk level
        if risk_probability > 0.7:
            medical_recommendations.extend([
                "Schedule immediate consultation with a cardiologist",
                "Consider comprehensive cardiac stress testing",
                "Discuss medication options for heart disease prevention"
            ])
        elif risk_probability > 0.4:
            medical_recommendations.extend([
                "Schedule routine cardiology consultation",
                "Monitor blood pressure and cholesterol regularly",
                "Consider cardiac screening tests"
            ])
        
        # Specific recommendations based on patient factors
        if patient_data.resting_blood_pressure > 140:
            lifestyle_recommendations.append("Focus on blood pressure management through diet and exercise")
            medical_recommendations.append("Discuss blood pressure medication with your doctor")
        
        if patient_data.serum_cholesterol > 240:
            lifestyle_recommendations.append("Adopt heart-healthy diet low in saturated fats")
            medical_recommendations.append("Consider cholesterol-lowering medication")
        
        if patient_data.age > 55:
            lifestyle_recommendations.append("Increase focus on regular cardiovascular exercise")
            medical_recommendations.append("Consider more frequent cardiac health screenings")
        
        if not patient_data.exercise_induced_angina and patient_data.maximum_heart_rate_achieved > 150:
            lifestyle_recommendations.append("Continue current exercise routine - great cardiovascular fitness!")
        
        # Default healthy lifestyle recommendations
        lifestyle_recommendations.extend([
            "Maintain regular physical activity (150 minutes moderate exercise per week)",
            "Follow Mediterranean or DASH diet pattern",
            "Manage stress through relaxation techniques",
            "Maintain healthy weight",
            "Avoid smoking and limit alcohol consumption"
        ])
        
        return {
            'lifestyle': lifestyle_recommendations,
            'medical': medical_recommendations
        }
    
    def _update_metrics(self, response_time_ms: float) -> None:
        """Update service performance metrics."""
        
        self.total_predictions += 1
        
        # Calculate rolling average response time
        if self.total_predictions == 1:
            self.average_response_time = response_time_ms
        else:
            alpha = 0.1  # Smoothing factor
            self.average_response_time = (
                alpha * response_time_ms + 
                (1 - alpha) * self.average_response_time
            )
    
    def get_model_health_status(self) -> ModelHealthStatus:
        """Get current model health and performance metrics."""
        
        model_metadata = self.predictor.model_metadata if self.is_model_loaded else {}
        return self._build_model_health_status(model_metadata, self.is_model_loaded)

    def _build_model_health_status(self, model_metadata, is_model_healthy) -> ModelHealthStatus:
        if not isinstance(model_metadata, dict):
            raise ValueError("Model metadata must be a JSON object")
        
        return ModelHealthStatus(
            is_model_healthy=is_model_healthy,
            model_version=model_metadata.get('model_version', 'unknown'),
            last_training_date=model_metadata.get('training_date', 'unknown'),
            model_accuracy=model_metadata.get('test_accuracy', 0.0),
            total_predictions_made=self.total_predictions,
            average_response_time_ms=self.average_response_time
        )


# Global service instance
ml_service = HeartDiseaseMLService()
