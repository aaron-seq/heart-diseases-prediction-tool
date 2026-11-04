"""HTTP contract tests with a controlled predictor, never real training.

These tests exercise the real application, lifespan, schemas, and ML service.
They do not validate TensorFlow, model artifacts, or prediction accuracy.
"""

import importlib
import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


class ControlledPredictor:
    def __init__(self):
        self.model_metadata = {"model_version": "controlled-test-model"}
        self.load_calls = 0
        self.training_calls = 0
        self.prediction_inputs = []

    def load_model(self):
        self.load_calls += 1

    def train_model(self):
        self.training_calls += 1
        raise AssertionError("HTTP contract tests must never train a model")

    def predict_heart_disease_risk(self, patient_data):
        self.prediction_inputs.append(patient_data)
        return {
            "has_heart_disease_risk": False,
            "risk_probability": 0.25,
            "risk_level": "Low Risk",
            "confidence_score": 0.75,
        }


@pytest.fixture(scope="session")
def application_modules(tmp_path_factory):
    existing_modules = set(sys.modules)
    with pytest.MonkeyPatch.context() as patch:
        # Settings and file logging must never read/write the checkout's files.
        patch.chdir(tmp_path_factory.mktemp("api-contract"))
        try:
            modules = {
                "main": importlib.import_module("app.main"),
                "service": importlib.import_module("app.services.ml_service"),
                "prediction": importlib.import_module("app.api.endpoints.prediction"),
                "health": importlib.import_module("app.api.endpoints.health"),
            }
            yield modules
        finally:
            # Do not leave app settings or services from this session for later tests.
            for name in set(sys.modules) - existing_modules:
                if name == "app" or name.startswith("app."):
                    sys.modules.pop(name, None)


@pytest.fixture
def service(application_modules, monkeypatch):
    service = application_modules["service"].HeartDiseaseMLService(
        ControlledPredictor()
    )
    for name in ("main", "prediction", "health"):
        monkeypatch.setattr(application_modules[name], "ml_service", service)
    return service


@pytest.fixture
def client(application_modules, service):
    with TestClient(application_modules["main"].create_application()) as client:
        yield client


@pytest.fixture
def patient_data():
    example = Path(__file__).resolve().parents[1] / "examples/prediction-request.json"
    return json.loads(example.read_text(encoding="utf-8"))["patient_data"]
