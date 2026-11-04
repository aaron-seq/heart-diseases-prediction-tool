"""Unavailable models must not turn HTTP startup into a training job."""

import asyncio

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "failure",
    [
        FileNotFoundError("synthetic missing model"),
        ValueError("synthetic invalid model"),
        ModuleNotFoundError("synthetic missing ML dependency"),
    ],
)
def test_model_load_failure_keeps_api_available(
    application_modules, service, patient_data, monkeypatch, failure
):
    def fail_load():
        raise failure

    predictor = service.predictor
    monkeypatch.setattr(predictor, "load_model", fail_load)
    with TestClient(application_modules["main"].create_application()) as client:
        health = client.get("/api/v1/health")
        assert health.status_code == 200
        assert health.json()["status"] == "degraded"
        assert health.json()["model_status"]["is_model_healthy"] is False
        assert health.json()["model_status"]["model_version"] == "unknown"
        ready = client.get("/api/v1/ready")
        assert ready.status_code == 503
        assert ready.json()["ready"] is False
        prediction = client.post("/api/v1/predict", json={"patient_data": patient_data})
        assert prediction.status_code == 503
        assert predictor.prediction_inputs == []
        assert predictor.training_calls == 0


def test_failed_reload_revokes_readiness(service, monkeypatch):
    asyncio.run(service.initialize_service())
    assert service.is_model_loaded is True
    predictor = service.predictor

    def fail_load():
        raise ValueError("synthetic invalid replacement")

    monkeypatch.setattr(predictor, "load_model", fail_load)
    asyncio.run(service.initialize_service())
    assert service.is_model_loaded is False
    assert predictor.training_calls == 0


def test_readiness_has_unavailable_status(client, service):
    service.is_model_loaded = False
    response = client.get("/api/v1/ready")
    assert response.status_code == 503
    assert response.json()["ready"] is False


def test_missing_optional_dependencies_leave_real_service_unready(
    application_modules, service, monkeypatch
):
    service.predictor = None
    calls = []

    def missing_dependency():
        calls.append("create")
        raise ModuleNotFoundError("synthetic missing ML dependency")

    monkeypatch.setattr(service, "_create_predictor", missing_dependency)
    with TestClient(application_modules["main"].create_application()) as client:
        assert client.get("/api/v1/live").status_code == 200
        assert client.get("/api/v1/health").json()["status"] == "degraded"
        assert client.get("/api/v1/model-status").json()["model_version"] == "unknown"
        assert client.get("/api/v1/ready").status_code == 503
    assert calls == ["create"]
