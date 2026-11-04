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

The existing setup targets Python 3.11 and
[backend/requirements.txt](backend/requirements.txt). Full dependency installation,
trained-model loading, inference and Docker startup remain unverified in this
delivery; follow [issues #4](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/4),
[#7](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/7),
[#9](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/9) and
[#12](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/12).
Startup can download training data and train if model loading fails; it is not
an offline inference-only quickstart.

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
- [Engineering Project](https://github.com/users/aaron-seq/projects/13) (maintainer access)
- [Repository issues](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues)

The earlier README declared MIT, but no authoritative license file is tracked.
[Issue #22](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/22)
records the owner decision and redistribution evidence needed. This change does
not choose a license or alter existing grants.
