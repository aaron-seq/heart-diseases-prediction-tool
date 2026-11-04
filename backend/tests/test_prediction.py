def test_prediction_validation_error(client):
    resp = client.post("/api/v1/predict", json={"age": 50})
    assert resp.status_code == 422


def test_prediction_happy_path(client, service, patient_data):
    resp = client.post("/api/v1/predict", json={"patient_data": patient_data})
    assert resp.status_code == 200
    body = resp.json()
    assert body["risk_probability"] == 0.25
    assert body["has_heart_disease_risk"] is False
    assert body["risk_level"] == "Low Risk"
    assert body["confidence_score"] == 0.75
    assert body["primary_risk_factors"] == []
    assert body["protective_factors"] == []
    assert body["lifestyle_recommendations"]
    assert body["medical_recommendations"]
    assert service.predictor.prediction_inputs == [
        {
            "age": 55,
            "sex": 1,
            "cp": 1,
            "trestbps": 130,
            "chol": 245,
            "fbs": 0,
            "restecg": 0,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 1.0,
            "slope": 1,
            "ca": 0,
            "thal": 3,
        }
    ]
    assert service.total_predictions == 1
    assert service.predictor.load_calls == 1
    assert service.predictor.training_calls == 0


def test_flat_payload_is_rejected(client, service, patient_data):
    resp = client.post("/api/v1/predict", json=patient_data)
    assert resp.status_code == 422
    assert service.predictor.prediction_inputs == []


def test_prediction_when_model_unavailable(client, service, patient_data):
    service.is_model_loaded = False
    resp = client.post("/api/v1/predict", json={"patient_data": patient_data})
    assert resp.status_code == 503
    assert service.predictor.prediction_inputs == []
