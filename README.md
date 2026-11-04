# Heart Disease Prediction Tool

A research prototype with a FastAPI prediction backend, a model-development
notebook, and a React screen for checking API health. The current screen does not
submit patient predictions. No trained-model accuracy or clinical suitability
has been established by the engineering checks described here.

## Frontend quickstart

Use Node.js 22 or 24 and npm. From the repository root:

```sh
cd frontend
npm ci
npm run dev
```

Open [the local frontend](http://localhost:5173) and select **Ping API**. During
development, `/api` is proxied to `http://localhost:8000`. For a separately hosted
backend, set `VITE_API_BASE_URL` to its origin before building, for example
`https://api.example.com`; see [the example configuration](frontend/.env.example).
This value is public and compiled into the browser bundle. The backend must
allow the frontend's origin through CORS. A static deployment needs either that
API-base setting or its own `/api` reverse proxy.

```sh
npm run lint
npm run type-check
npm run build
npx playwright install chromium
npm test
npm audit --audit-level=high
```

Browser tests exercise production bundles against synthetic local API responses,
including same-origin and configured-API modes. They do not validate backend
availability or model predictions. See [validation and limitations](docs/engineering-evidence.md).

## Backend and notebook

The backend accepts a `patient_data` object and prediction options, as defined in
[its request schema](backend/app/models/schemas.py). It exposes health, readiness,
model-status and prediction operations. With a configured backend running,
[Swagger UI](http://localhost:8000/docs) describes its contract.

Use Python 3.11 or 3.13 for API-only diagnostics:

```sh
cd backend
python -m venv .venv-api
# Activate: Windows .venv-api\Scripts\Activate.ps1; Linux: . .venv-api/bin/activate
python -m pip install --require-hashes -r requirements-api.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

This starts the real API without the ML stack or saved model. Observed behavior:
`/api/v1/health` returns 200 with `status: "degraded"`; `/api/v1/ready` returns 503
with `ready: false`; valid prediction requests return 503. Startup never trains
or downloads a dataset. A failed model reload revokes readiness.

[`examples/prediction-request.json`](backend/examples/prediction-request.json)
is a synthetic schema example, not a patient record or evaluated prediction.
Use `MODEL_PATH` for trusted model artifacts and `ALLOWED_ORIGINS` as a JSON array
of frontend origins. Full neural-model dependencies, artifact loading/inference
and Docker startup remain unverified; see [#4](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/4),
[#7](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/7) and
[#9](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/9).

The [notebook](Enhanced2025_Heart_Disease_Prediction.ipynb) contains exploratory
training/evaluation code, without saved execution results. Held-out evaluation
and preprocessing remain part of [issue #6](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/6).
The Compose file is in `backend/`; it does not provide a frontend service.

## Development and tracking

- [Contribution checks](CONTRIBUTING.md)
- [Product scope and roadmap](docs/product/PRODUCT.md)
- [Current checkpoint](docs/product/PROJECT-STATUS.md)
- [Threat model, test map and evidence](docs/engineering-evidence.md)
- [Milestone 1](https://github.com/aaron-seq/heart-diseases-prediction-tool/milestone/1)
- [Draft PR #24 and current checks](https://github.com/aaron-seq/heart-diseases-prediction-tool/pull/24)
- [Engineering Project](https://github.com/users/aaron-seq/projects/13) (maintainer access)
- [Repository issues](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues)

The earlier README declared MIT, but no authoritative license file is tracked.
[Issue #22](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/22)
records the owner decision and redistribution evidence needed. This change does
not choose a license or alter existing grants.
