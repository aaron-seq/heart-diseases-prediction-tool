"""Real loopback Uvicorn smoke in an API-only environment, with no ML artifacts."""

import importlib.util
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request


def main():
    backend = Path(__file__).resolve().parents[1]
    for package in ("tensorflow", "numpy", "pandas", "sklearn", "shap", "mlflow"):
        if importlib.util.find_spec(package) is not None:
            raise RuntimeError("Run this smoke check in the API-only environment")

    original_cwd = Path.cwd()
    allowed = {"systemroot", "windir", "path", "pathext", "comspec", "systemdrive"}
    with tempfile.TemporaryDirectory(prefix="heart-api-smoke-") as scratch:
        env = {k: v for k, v in os.environ.items() if k.casefold() in allowed}
        env.update(
            {
                "TEMP": scratch,
                "TMP": scratch,
                "USERPROFILE": scratch,
                "MODEL_PATH": str(Path(scratch) / "missing-model"),
                "ALLOWED_ORIGINS": json.dumps(["http://localhost:5173"]),
            }
        )
        os.environ.clear()
        os.environ.update(env)
        os.chdir(scratch)
        sys.path.insert(0, str(backend))
        from loguru import logger
        import uvicorn

        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            base = f"http://127.0.0.1:{listener.getsockname()[1]}"

            def request(path, expected, payload=None):
                data = json.dumps(payload).encode() if payload is not None else None
                req = urllib.request.Request(
                    base + path, data=data, headers={"Content-Type": "application/json"}
                )
                try:
                    response = opener.open(req, timeout=3)
                except urllib.error.HTTPError as error:
                    response = error
                with response:
                    assert response.code == expected, (path, response.code)
                    return json.load(response)

            server = uvicorn.Server(
                uvicorn.Config(
                    "app.main:app",
                    loop="asyncio",
                    http="h11",
                    lifespan="on",
                    log_level="warning",
                    access_log=False,
                    timeout_graceful_shutdown=5,
                )
            )
            worker = threading.Thread(
                target=server.run, kwargs={"sockets": [listener]}, daemon=True
            )
            worker.start()
            try:
                deadline = time.monotonic() + 20
                while True:
                    if not worker.is_alive():
                        raise RuntimeError("Uvicorn exited before serving liveness")
                    try:
                        assert request("/api/v1/live", 200)["alive"] == "true"
                        break
                    except urllib.error.URLError:
                        if time.monotonic() >= deadline:
                            raise RuntimeError(
                                "Uvicorn did not start within 20 seconds"
                            )
                        time.sleep(0.1)
                health = request("/api/v1/health", 200)
                assert health["status"] == "degraded"
                assert health["model_status"]["is_model_healthy"] is False
                assert request("/api/v1/ready", 503)["ready"] is False
                payload = json.loads(
                    (backend / "examples/prediction-request.json").read_text()
                )
                assert (
                    "ML model not available"
                    in request("/api/v1/predict", 503, payload)["detail"]
                )
                assert not (Path(scratch) / "missing-model").exists()
            finally:
                server.should_exit = True
                worker.join(timeout=10)
                logger.remove()
                os.chdir(original_cwd)
                if worker.is_alive():
                    raise RuntimeError("Uvicorn did not shut down cleanly")
    print(
        "PASS: real Uvicorn liveness/health, readiness 503 and prediction 503 without ML"
    )


if __name__ == "__main__":
    main()
