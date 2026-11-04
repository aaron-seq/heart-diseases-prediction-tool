# Product scope and roadmap

Status: engineering scope derived from repository evidence; no stakeholder or
clinical approval inferred. [Project](https://github.com/users/aaron-seq/projects/13)
tracks execution; [checkpoint](PROJECT-STATUS.md) records verified delivery state.

## Current objective

Give contributors a reproducible frontend build and an honest API-health screen.
The existing screen is a health probe; backend predictions and notebook research
are separate capabilities. Source: [App](../../frontend/src/App.tsx),
[backend schema](../../backend/app/models/schemas.py).

| Requirement | Acceptance | Tracking |
| --- | --- | --- |
| FR-001 | Health probe uses configured API origin or same-origin `/api`; shows pending, success, failure and recovery without overlapping requests | [#5](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/5) |
| NFR-001 | Clean lockfile install, lint, types, build and production-bundle browser tests pass on the supported frontend matrix | [#5](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/5) |
| NFR-002 | Documentation distinguishes tested frontend behavior from unverified model quality, runtime and deployment claims | [#5](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/5), [evidence](../engineering-evidence.md) |

Assumed users are contributors and prototype evaluators. Actual user demand,
clinical utility, calibrated prediction quality, performance targets and adoption
baselines are unknown. Engineering success here means a fresh contributor can
reproduce the selected checks; passing checks do not establish medical outcomes.

## Roadmap

| Sequence | Outcome and dependencies |
| --- | --- |
| Now | [Milestone 1](https://github.com/aaron-seq/heart-diseases-prediction-tool/milestone/1): frontend health/build verification; requires review, exact-head frontend CI and documentation. No prediction UI or deployment. |
| Next | Reconcile [runtime dependencies #4](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/4), [model startup #12](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/12), [API tests #7](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/7) and [container execution #9](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/9). Requires supported Python dependencies and trusted model artifacts. |
| Next | Verify training/held-out preprocessing in [#6](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/6) before publishing accuracy claims. Resolve [license/provenance #22](https://github.com/aaron-seq/heart-diseases-prediction-tool/issues/22) before redistribution. |
| Later | Consider a prediction UI only after a tested API/model contract and an explicit product decision. No delivery date or user benefit is assumed. |

Risks: legacy backend CI and dependency setup remain blockers to whole-repository
validation; model provenance/evaluation and licensing remain evidence gaps.
Confidential work uses restricted records. No owner, date, risk acceptance, release
or deployment commitment is inferred.

Decision: reuse the existing API client and health screen, remove source-unused
dependencies, and test compiled bundles with synthetic responses. A new product UI
or broad rewrite would add scope without evidence for this milestone. Rollback is
a revert of the frontend patch; retain dependency fixes or reassess their advisories.
