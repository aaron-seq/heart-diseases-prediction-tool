# Project status and continuation

Last verified: 2026-11-04, Asia/Kolkata.
[Repository](https://github.com/aaron-seq/heart-diseases-prediction-tool) ·
[Project 13](https://github.com/users/aaron-seq/projects/13) ·
[scope/roadmap](PRODUCT.md) · [evidence](../engineering-evidence.md).

## Current state

- Active [issue #12](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/12),
  [milestone 2](https://github.com/aaron-seq/heart-diseases-prediction-tool/milestone/2):
  offline API startup with explicit model readiness. Branch
  `codex/12-offline-api-startup`, based on `8ab0e12` / unmerged
  [PR #24](https://github.com/aaron-seq/heart-diseases-prediction-tool/pull/24).
  Implementation `6341b68`, metadata fix `6a5bb3f`; delivery docs follow those
  commits. [Draft PR #25](https://github.com/aaron-seq/heart-diseases-prediction-tool/pull/25)
  is stacked on #24; its [current-head checks](https://github.com/aaron-seq/heart-diseases-prediction-tool/pull/25/checks)
  and the Project record final hosted state.
- API starts without ML dependencies/artifacts, serves degraded health, and
  returns 503 for readiness/predictions. Startup never trains. Invalid model
  metadata cannot report ready. API-only hash locks and actual Uvicorn smoke are
  retained; they do not replace the neural model or provide evaluated predictions.
- Frontend milestone 1 remains in review: PR #24 / `8ab0e12` passed local checks
  and Linux Node 22/24 CI. Its inherited backend workflow failed. New API checks
  are a separate profile; the legacy ML workflow is not removed or weakened.
- No default-branch merge, release or deployment. Confidential work retains its
  restricted records and private integration/retest state; keep details there.
- [#22](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/22): owner
  explicitly chose to keep licensing unresolved pending evidence. No grant or
  consent is inferred. [#23](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/23)
  retains the separate development-tool advisory work.

## Validation and review

- Parent observed five startup/readiness Red failures, then ten metadata Red
  failures after fresh review found the edge case. Final clean Python 3.11.9 API
  environment: hash installs, `pip check`, **29 contract tests**, real loopback
  Uvicorn smoke, affected-file Ruff E9/F and test Black checks pass.
- Serving/test locks were compiled with pip-tools 7.5.2. Both final flattened
  graphs returned zero known pip-audit 2.10.1 alerts. Initial pytest advisory was
  fixed with 9.0.3, then tests rerun; no suppression. This excludes bootstrap
  tools and the separate full ML dependencies, whose issues remain open.
- Fresh same-system verifier reran 29 tests/Uvicorn and original-null/recovery
  probes; parent checked the report/source. Earlier discovery/baseline and two
  implementers belong to milestone 1/restricted work. No human approval implied.
- Controlled predictor tests execute actual app/lifespan/service/handlers. The
  smoke uses real Uvicorn/HTTP with no ML packages/artifacts. No real trained
  model, clinical quality, scale, deployed CORS or container result is claimed.
- Hosted Python 3.11/3.13 results belong to the current stacked PR head and
  Project. Inspect them before acceptance. Docker CLI is present but its local
  daemon is unavailable. Dependency/config deprecation warnings remain visible.
  Both API jobs passed at `171531d` in [published CI](https://github.com/aaron-seq/heart-diseases-prediction-tool/actions/runs/41780315242);
  later documentation edits require their own current-head check inspection.

## Resume here

1. Check `git status --short --branch`, `git log -3 --oneline`, `git worktree list`
   and open PRs. Confirm #12's PR base is the frontend branch and inspect its
   current-head API checks. Review #24 separately; never infer it was merged.
2. In a fresh Python 3.11/3.13 API-only environment, from `backend/`:
   `python -m pip install --require-hashes -r requirements-api-test.txt`,
   `python -m pip check`, `python -m pytest tests -q`,
   `python tests/smoke_api.py`. Smoke requires ML packages to be absent.
3. Follow [the API evidence/test map](../engineering-evidence.md#api-startup-milestone).
   Recheck private visibility/state before operating on restricted work.
4. Next: [#4](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/4)
   coherent full inference dependencies and trusted artifacts;
   [#7](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/7) real
   model integration; [#9](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/9)
   actual container execution; [#6](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/6)
   held-out evaluation before accuracy claims. No dates/owner commitments invented.

Raw logs, caches and isolated API/tool environments remain in the access-restricted
session evidence directory outside this checkout; losing the machine loses those
transient artifacts. Versioned tests/locks, PRs/issues and the restricted checkpoint
retain the reproducible conclusions. Agent dependency/build outputs stay ignored
in their separate worktree. Do not commit model files, health data or local secrets.
