# Engineering evidence and test strategy

Verified 2026-11-04 (Asia/Kolkata). Baseline `3583203526f414cdeab50b81bdf1851bc6d32d3a`;
frontend implementation `8007ce0` (same frontend content as agent `0254508`).
Delivery state and continuation: [checkpoint](product/PROJECT-STATUS.md).
This is a bounded engineering assessment, not clinical validation or a complete
security audit. No deployed/shared service was tested.

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
ancestors of baseline `3583203`: zero candidate files for those patterns. No live
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
