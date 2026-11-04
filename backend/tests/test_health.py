def test_health_ok(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert body["model_status"]["model_version"] == "controlled-test-model"


def test_health_options_cors(client):
    resp = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp.status_code == 200
    assert resp.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_model_status_after_lifespan_initialization(client, service):
    resp = client.get("/api/v1/model-status")
    assert resp.status_code == 200
    assert resp.json()["is_model_healthy"] is True
    assert service.predictor.load_calls == 1
    assert service.predictor.training_calls == 0


def test_readiness_tracks_model_availability(client, service):
    assert client.get("/api/v1/ready").status_code == 200
    assert client.get("/api/v1/ready").json()["ready"] is True
    service.is_model_loaded = False
    assert client.get("/api/v1/ready").json()["ready"] is False
