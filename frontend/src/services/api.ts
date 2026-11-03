/**
 * API service for Heart Disease Prediction backend communication.
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  PatientHealthData,
  HeartDiseaseRiskPrediction,
  PredictionRequest,
  APIHealthResponse,
  ModelHealthStatus
} from '../types';

class HeartDiseaseAPIService {
  private api: AxiosInstance;
  private readonly baseURL: string;

  constructor() {
    this.baseURL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');
    
    this.api = axios.create({
      baseURL: `${this.baseURL}/api/v1`,
      timeout: 30000, // 30 seconds timeout
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for logging
    this.api.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error('API Response Error:', error.response?.data || error.message);
        
        // Handle different error types
        if (error.response?.status === 503) {
          throw new Error('Service temporarily unavailable. Model is initializing.');
        } else if (error.response?.status === 500) {
          throw new Error('Internal server error. Please try again later.');
        } else if (error.code === 'ECONNABORTED') {
          throw new Error('Request timeout. Please check your connection.');
        }
        
        throw error;
      }
    );
  }

  /**
   * Predict heart disease risk for a patient
   */
  async predictHeartDiseaseRisk(
    patientData: PatientHealthData,
    explainPrediction: boolean = true
  ): Promise<HeartDiseaseRiskPrediction> {
    try {
      const requestPayload: PredictionRequest = {
        patient_data: patientData,
        explain_prediction: explainPrediction
      };

      const response: AxiosResponse<HeartDiseaseRiskPrediction> = await this.api.post(
        '/predict',
        requestPayload
      );

      return response.data;
    } catch (error) {
      console.error('Failed to get heart disease prediction:', error);
      throw this.handleAPIError(error);
    }
  }

  /**
   * Get API health status
   */
  async getHealthStatus(): Promise<APIHealthResponse> {
    try {
      const response: AxiosResponse<APIHealthResponse> = await this.api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Failed to get health status:', error);
      throw this.handleAPIError(error);
    }
  }

  /**
   * Get model health status
   */
  async getModelStatus(): Promise<ModelHealthStatus> {
    try {
      const response: AxiosResponse<ModelHealthStatus> = await this.api.get('/model-status');
      return response.data;
    } catch (error) {
      console.error('Failed to get model status:', error);
      throw this.handleAPIError(error);
    }
  }

  /**
   * Check if API is ready
   */
  async checkReadiness(): Promise<boolean> {
    try {
      const response = await this.api.get('/ready');
      return response.data.ready === true;
    } catch (error) {
      console.error('Readiness check failed:', error);
      return false;
    }
  }

  /**
   * Trigger model retraining (admin function)
   */
  async retrainModel(): Promise<{ status: string; message: string }> {
    try {
      const response = await this.api.post('/retrain-model');
      return response.data;
    } catch (error) {
      console.error('Failed to trigger model retraining:', error);
      throw this.handleAPIError(error);
    }
  }

  /**
   * Handle API errors consistently
   */
  private handleAPIError(error: unknown): Error {
    if (axios.isAxiosError(error) && error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || error.response.data?.message || 'Unknown server error';
      return new Error(`Server Error (${error.response.status}): ${message}`);
    } else if (axios.isAxiosError(error) && error.request) {
      // Network error
      return new Error('Network Error: Unable to connect to the server. Please check your internet connection.');
    } else {
      // Other error
      return new Error(`Request Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Get base URL for the API
   */
  getBaseURL(): string {
    return this.baseURL;
  }
}

// Export singleton instance
export const heartDiseaseAPI = new HeartDiseaseAPIService();
export default heartDiseaseAPI;
