# Engineering evidence and test strategy

Verified 2026-11-04 (Asia/Kolkata). Baseline `3583203526f414cdeab50b81bdf1851bc6d32d3a`;
frontend implementation `8007ce0` (same frontend content as agent `0254508`).
Delivery state and continuation: [checkpoint](product/PROJECT-STATUS.md).
This is a bounded engineering assessment, not clinical validation or a complete
security audit. No deployed/shared service was tested.

The frontend records below describe the first milestone. The subsequent
[API startup milestone](#api-startup-milestone) records the new backend behavior.

## Baseline and scope

The initial working tree was clean. No checkpoint, lockfile, license file or
security policy was tracked. All 21 original issues/PRs (open and closed) were
inventoried; no open PR required integration. Existing issues were reused.

The discovery agent mapped FastAPI → service → local model/preprocessor and
training dataset/artifact boundaries, plus the React health screen. The baseline
agent ran checks with a restricted environment and disposable CWD. The parent
verified material source claims, live GitHub state and retained final checks.

| Baseline check | Actual result / provenance |
| --- | --- |
| `python -m pytest backend/tests -v -p no:cacheprovider` | Agent-run, exit 4 before collection: TensorFlow unavailable. No assertions passed. Parent reviewed import chain. |
| `npm ci --ignore-scripts --dry-run --no-audit --no-fund` | Agent-run, exit 1: missing lockfile. |
| `npm run type-check`, `npm run build` | Agent-run, exit 1: dependencies/`tsc` unavailable. |
| Main CI at `3583203` | Parent inspected [published run](https://github.com/aaron-seq/heart-diseases-prediction-tool/actions/runs/20487450254): frontend/backend failures, Docker skipped. Quality/scanner job success does not establish passing checks because failures were masked. |

Backend request/lifespan, dependency, container and held-out-preprocessing gaps
are recorded in [#7](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/7),
[#4](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/4),
[#9](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/9),
[#12](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/12) and
[#6](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/6).
No full ML installation, training, evaluation, notebook execution or Docker run
was performed. Python 3.11.9 is available but its ML environment is not configured.

## Frontend validation

Parent personally ran these on the integrated frontend, Windows x64,
Node 22.18.0, npm 11.6.2, Vite 6.4.5, Playwright 1.64.1 and Chromium 156.0.8078.4:

| Command, from `frontend/` | Result |
| --- | --- |
| `npm ci --no-audit --no-fund` | Exit 0, 277 packages installed from lockfile; reviewed install-hook inventory (esbuild, optional macOS fsevents). |
| `npm run lint` | Exit 0; enforced ESLint assertions. |
| `npm run type-check` | Exit 0. |
| `npm run build` | Exit 0; production bundle built. |
| `npm test` | Exit 0; 6 Chromium tests, no retries. |
| `npm audit --audit-level=high --json --fetch-retries=0 --fetch-timeout=15000` | Exit 0; 15 moderate development paths, zero high/critical. |
| `npm audit --omit=dev --json --fetch-retries=0 --fetch-timeout=15000` | Exit 0; zero runtime dependency alerts detected. |

Runtime checks used a Windows environment allowlist, temporary home/npm config,
and no credential variables. The production test server disables `.env` loading
and strips host environment variables before importing Vite. This is process
hygiene, not OS-level sandbox isolation. The initial parent launcher failed before
lint because npm rejected one file being used for both user/global config; using
separate empty files fixed the harness. It was not a product-test failure.

The implementer observed Red: the original rendered button remained enabled
during a pending request. After the fix, all six tests passed. The fresh verifier
reran the browser suite, lint and types; independently built using the real Vite
environment value; forced ten pending clicks; and checked path-prefix/trailing-
slash normalization, HTTP 500 recovery and stale-response clearing. Parent
reviewed the source and test assertions. These agents are delegated perspectives
from the same system, not independent human review.

| Requirement / invariant | Test and oracle | Boundary / limitation |
| --- | --- | --- |
| FR-001: correct destination | `tests/health.spec.ts`, both projects: exact expected URL, unexpected requests rejected | Same-origin and configured local origin with trailing slash; requests intercepted, no real backend/CORS validation |
| FR-001: one pending request | Same test: count remains one, loading status and disabled button, ready again after completion | Fresh reviewer additionally forced DOM-enabled clicks |
| FR-001: failure/recovery | HTTP 503 and network failure, visible error, subsequent success; exact two calls | Timeout path and deployed proxy failures untested |
| NFR-001 | Lock install, lint/types/build and browser commands above; CI matrix Node 22/24 | Local execution only Node 22/Windows; hosted results must match current PR head |
| NFR-002 | Parent source review and relative-link/JSON/YAML checks | No model accuracy, clinical utility or production-readiness result |

Browser tests build production bundles for both configurations and intercept
only synthetic local fixtures. They do not demonstrate an actual frontend →
backend → trained model journey. Accessibility coverage is limited to named
controls/live status and disabled state; keyboard/screen-reader, mobile, other
browsers, scale, latency, deployment and recovery remain untested.

## Threat model and security coverage

| Asset / boundary | Control and selected verification | Coverage |
| --- | --- | --- |
| Browser → API destination and failure state | Reuse typed client, public build-time origin, one in-flight request and error recovery | Browser contract verified with fixtures; deployed TLS/CORS not tested |
| Patient input → model and logs | Existing Pydantic validation; API/runtime issues above | Source reviewed; private follow-up retains sensitive detail; no real data used |
| Operator model artifacts / training data | Existing filesystem/network trust assumptions | Code review only; artifact provenance, deserialization trust, fallback training and evaluation unresolved |
| CI / dependency authors → build | Reviewed scripts, committed lock, official action SHAs, frontend job `contents: read`, no privileged trigger added | Frontend workflow reviewed; legacy backend/scanner jobs and repository rules remain separate |
| Credentials → source/history | `.env`/models/logs ignored; redacted checks below | Limited patterns only; no specialist secret scanner available |

Selected reference: [ASVS 5.0.0 frontend controls](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x12-V3-Web-Frontend-Security.md)
3.4.2 for trusted CORS origins; [error handling](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md)
16.5.2–16.5.3 for dependency failure behavior. Actual deployed CORS verification
under [WSTG v4.2 CLIENT-07](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/11-Client-side_Testing/07-Testing_Cross_Origin_Resource_Sharing/)
is not completed. No conformance or full-domain pass is claimed. Account/tenant,
payment, database and webhook tests are not applicable to implemented workflows;
there is no corresponding product subsystem.

Parent personally reran Bandit 1.9.4 on backend source: one B104 bind-address
alert, medium scanner severity; it is not a demonstrated vulnerability. Parent
reran pip-audit 2.10.1 with `--no-deps --disable-pip -r
backend/requirements-runtime.txt --format json`: exit 1, 21 raw rows across four
direct packages with duplicates. Exact dependency applicability/severity and
transitives remain unresolved; restricted artifacts retain details. These scans
were also run by the baseline agent. No clean-backend claim follows.

Parent checked common provider-token/private-key patterns in HEAD and all 97
revisions reachable from baseline `3583203` (including that revision): zero candidate files for those patterns. No live
credential validation was attempted. This deliberately limited search does not
replace Gitleaks/TruffleHog or prove no secrets exist. Specialist secret, container,
Actions and dynamic scanners were unavailable/not run. Dependabot alerts and
secret scanning were disabled; code-scanning alert inventory was empty. No
settings were enabled or permissions broadened.

Frontend residual advisory triage is [issue #23](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/23).
Fifteen paths are not fifteen independently confirmed vulnerabilities. The
[upstream moderate advisory](https://github.com/isaacs/minimatch/security/advisories/GHSA-g3hv-75wg-m249)
names 10.2.6/optimization level 2, while npm applies a broader range to our 3.x/9.x
development copies; reachable conditions remain unresolved. No suppression was
added. The narrow 9.0.7 override addresses separate published high alerts using
[upstream patched-version guidance](https://github.com/isaacs/minimatch/security/advisories/GHSA-7r86-cg39-jmmj).

New tooling provenance: Vite/plugin-react (vitejs, MIT), Playwright
(microsoft/playwright, Apache-2.0), minimatch (isaacs/minimatch, ISC). Package
metadata/source and upstream migration/advisory guidance were reviewed. No new
runtime framework or assets were introduced. This does not establish project,
dataset or model redistribution rights; [#22](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/22)
records that gap.

## Delivery and tracking controls

[Project 13](https://github.com/users/aaron-seq/projects/13) is private, owned by
`aaron-seq`, linked to this repository. Linked issues remain public. Status is
manual: Todo=captured, Ready=selected, In Progress=implementation/validation,
In review / Retest=reviewable with acceptance/integration pending, Done=acceptance
and integration verified. P0/P1/P2/P3 mean critical/high/normal/low priority.
No dates, assignments, automations or outcome forecasts were invented.

Saved Overview/Execution/Roadmap-and-backlog/Review-and-retest views and filters
were read back through GitHub GraphQL. The API exposes no grouping input here;
board grouping/UI behavior remains unverified. No Insights chart is claimed.
No branch-protection/required-check setting was changed or verified. Current-head
CI and review state belong in the PR and Project, not inferred from workflow YAML.

## API startup milestone

Primary [issue #12](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/12),
[milestone 2](https://github.com/aaron-seq/heart-diseases-prediction-tool/milestone/2).
Base `8ab0e12` / reviewed frontend PR #24; implementation `6341b68` followed by
workflow/documentation review. No main-branch merge or deployment is implied.
Metadata validation is fixed in `6a5bb3f`; subsequent delivery changes are
workflow/docs only. The fresh verifier reran all 29 tests and the real Uvicorn
smoke, reproduced the original null-metadata case as degraded, and verified
null-to-valid recovery through health/readiness/prediction with zero training.
No concrete regression remained within that tested scope.

Problem: schema imports eagerly imported the scientific model module, and a load
failure triggered training before the lifespan could yield. Parent reproduced
five failures with a training spy that raises instead of doing work: three load
errors aborted startup, a failed reload attempted training, and readiness returned
200 while unavailable. Eight normal contract tests passed in that Red run.
Fresh same-system review then reproduced a metadata edge case: a successful load
with JSON-null metadata broke health/status while readiness remained true. Parent
observed ten further Red metadata cases and validated metadata before declaring
ready. Non-object/wrong-typed metadata and non-finite/out-of-range accuracy are
rejected; numeric accuracy boundaries 0/1 remain valid. This is an artifact
contract check, not a validation of model quality.

Decision: defer model construction; initialize readiness false, load supplied
artifacts, and retain degraded availability on any load error. Never train from
startup. Readiness now returns HTTP 503 when unavailable, preserving its JSON
shape; health/liveness remain available, and prediction already rejects with 503.
Successful controlled loading still runs through the actual app/lifespan/service.
The service accepts an injected predictor for contract tests; production still
constructs the original model. No fake predictor is shipped as runtime behavior.

Retaining automatic training would preserve network/computation side effects and
hide artifact failures. Bundling or replacing a model would require provenance,
evaluation and licensing evidence that is absent. This slice adds no model/data
asset or clinical/performance claim. Reverting restores the earlier startup
failure/training behavior and must be reassessed before any deployment.

| Requirement / oracle | Retained check | Coverage / limit |
| --- | --- | --- |
| FR-002: import API without ML | `tests/test_import_boundary.py` blocks scientific imports in a fresh process | Real schema/app imports; startup loading tested separately |
| FR-002: unavailable model never trains | `tests/test_startup.py`: missing file, invalid model and missing-dependency load errors; factory error; failed reload and invalid metadata | Controlled predictor spies; real handlers/status/503, no real corrupt Keras artifact parsed |
| FR-002: valid controlled path preserved | `tests/test_prediction.py`, `tests/test_health.py` | Exact request/mapping/response and lifespan load count; no real neural inference |
| NFR-003: actual server without ML | `python tests/smoke_api.py` | Real Uvicorn, TCP/HTTP, JSON-origin config, health/liveness, readiness and valid prediction 503; ML packages/artifacts absent |
| NFR-003: reproducible dependencies | API/test `.in` files and hash locks, clean install, `pip check`, dedicated CI | API-only profiles; full ML requirements remain unresolved under #4 |

Parent personally ran on Windows x64/Python 3.11.9 in a new isolated environment:

```sh
python -m pip install --require-hashes -r requirements-api.txt
python -m pip install --require-hashes -r requirements-api-test.txt
python -m pip check
python -m pytest tests -q -p no:cacheprovider
python tests/smoke_api.py
```

Installs/check exit 0; **29 tests pass**, with 13 library/config deprecation
warnings retained. Actual Uvicorn smoke exits 0 after graceful shutdown and temp
cleanup. Missing NumPy/pandas/TensorFlow/scikit-learn/SHAP/MLflow is asserted by
the smoke checker. A first subprocess-based smoke passed HTTP assertions but
failed Windows log-file cleanup; the retained checker uses a gracefully stopped
Uvicorn thread and explicitly closes logging. No cleanup error is suppressed.
No orphaned test server remained when checked.

Parent also ran `python -m ruff check` with `--select E9,F` on affected app files
and tests, and `python -m black --check backend/tests`: both pass. JSON/YAML and
Render's `ALLOWED_ORIGINS` JSON value were parsed. No frontend source changed, so
its previously verified checks were not rerun solely for backend work.

Dependency decision: reuse the locally proven FastAPI 0.141.1, Pydantic 2.11.3,
settings 2.3.0, Uvicorn 0.34.0 and Loguru 0.7.3 API versions. Pin Starlette 1.3.1
for the tested HTTPX 0.28 adapter; its deprecation warning is visible. Compile
complete pinned/hash-checked API and test graphs, retaining Windows-only markers.
Direct package names/source links/licenses were checked against PyPI and upstream
repositories. This profile deliberately excludes inference/training libraries;
the contradictory full-runtime pins are not silently replaced or declared fixed.

The initially considered pytest 8.3.4 test pin triggered
[GHSA-6w46-j5rx-g56g](https://github.com/advisories/GHSA-6w46-j5rx-g56g).
The [upstream 9.0.3 release](https://github.com/pytest-dev/pytest/releases/tag/9.0.3)
and advisory identify the patched version. The test lock uses 9.0.3; the full
suite was rerun. No extra pytest plugins are needed by this profile. Parent
pip-audit 2.10.1 scans of both final flattened locks returned **zero known alerts**
(exit 0); the initial duplicated pytest rows represented one advisory. Scope is
lock entries, excluding bootstrap tools and the separate full ML environment.
No exploit or global security conclusion follows from these scan results.

Lock maintenance uses pip-tools 7.5.2 in a separate tooling environment, Python
3.11, following [official hash/layered-requirements guidance](https://pip-tools.pypa.io/en/stable/):

```sh
python -m piptools compile --generate-hashes --strip-extras --no-header --no-emit-index-url --no-emit-trusted-host --pip-args=--only-binary=:all: --output-file requirements-api.txt requirements-api.in
python -m piptools compile --generate-hashes --strip-extras --no-header --no-emit-index-url --no-emit-trusted-host --pip-args=--only-binary=:all: --output-file requirements-api-test.txt requirements-api-test.in
```

The dedicated API workflow uses ordinary `pull_request`/main-push events,
`contents: read`, official SHA-pinned actions and Python 3.11/3.13. It does not
relax the existing ML/backend workflow or claim branch protection. Inspect the
current PR head for hosted results. [FastAPI lifespan testing guidance](https://fastapi.tiangolo.com/advanced/testing-events/)
supports the explicit TestClient context used here. Remaining: real trained-model
loading/inference and calibration, full ML locks/advisories, Docker (local daemon
unavailable), deployed behavior, scale and recovery. Licensing remains unresolved
by the owner's explicit decision in #22.
