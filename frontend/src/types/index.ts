/**
 * TypeScript type definitions for the Heart Disease Prediction app.
 */

export interface PatientHealthData {
  age: number;
  is_male: boolean;
  chest_pain_type: ChestPainType;
  resting_blood_pressure: number;
  serum_cholesterol: number;
  maximum_heart_rate_achieved: number;
  fasting_blood_sugar_over_120: boolean;
  resting_ecg_results: RestingECGType;
  exercise_induced_angina: boolean;
  st_depression_exercise: number;
  st_slope_peak_exercise: SlopeType;
  major_vessels_colored: number;
  thalassemia_type: ThalassemiaType;
}

export type ChestPainType = 
  | 'typical_angina' 
  | 'atypical_angina' 
  | 'non_anginal_pain' 
  | 'asymptomatic';

export type RestingECGType = 
  | 'normal' 
  | 'st_t_abnormality' 
  | 'left_ventricular_hypertrophy';

export type SlopeType = 
  | 'upsloping' 
  | 'flat' 
  | 'downsloping';

export type ThalassemiaType = 
  | 'normal' 
  | 'fixed_defect' 
  | 'reversible_defect';

export interface HeartDiseaseRiskPrediction {
  has_heart_disease_risk: boolean;
  risk_probability: number;
  risk_level: string;
  confidence_score: number;
  primary_risk_factors: string[];
  protective_factors: string[];
  lifestyle_recommendations: string[];
  medical_recommendations: string[];
}

export interface PredictionRequest {
  patient_data: PatientHealthData;
  explain_prediction: boolean;
}

export interface ModelHealthStatus {
  is_model_healthy: boolean;
  model_version: string;
  last_training_date: string;
  model_accuracy: number;
  total_predictions_made: number;
  average_response_time_ms: number;
}

export interface APIHealthResponse {
  status: string;
  timestamp: string;
  version: string;
  model_status: ModelHealthStatus;
}

// Form-specific types
export type PatientFormData = PatientHealthData;

export interface RiskVisualizationData {
  name: string;
  value: number;
  color: string;
}

// UI Component Props
export interface PredictionResultProps {
  prediction: HeartDiseaseRiskPrediction;
  patientData: PatientHealthData;
}

export interface HealthFormProps {
  onSubmit: (data: PatientHealthData) => void;
  isLoading: boolean;
}

export interface RiskFactorCardProps {
  title: string;
  factors: string[];
  type: 'risk' | 'protective';
}

export interface RecommendationCardProps {
  title: string;
  recommendations: string[];
  type: 'lifestyle' | 'medical';
}
